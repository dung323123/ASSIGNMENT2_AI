import argparse
import os
import random
from typing import Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split


# =============== 1. Decode board ==================

def decode_board(hex_str: str) -> np.ndarray:
    """Decode board hex string to np.array float32 shape (90,)."""
    if pd.isna(hex_str):
        return np.zeros((90,), dtype=np.float32)

    b = bytes.fromhex(hex_str)
    arr = np.frombuffer(b, dtype=np.int64)

    if arr.size != 90:
        tmp = np.zeros((90,), dtype=np.int64)
        n = min(arr.size, 90)
        tmp[:n] = arr[:n]
        arr = tmp

    return arr.astype(np.float32)


# =============== 2. Dataset ==================

class XiangqiValueDataset(Dataset):
    def __init__(self, csv_path: str, max_rows: int = None):
        df = pd.read_csv(csv_path)

        if max_rows is not None:
            df = df.sample(n=min(max_rows, len(df)), random_state=42).reset_index(drop=True)

        if not all(c in df.columns for c in ["board", "current_player", "value"]):
            raise ValueError("CSV must contain board, current_player, value")

        self.boards_hex = df["board"].values
        self.players = df["current_player"].astype(np.float32).values

        # ===== NEW: Normalize value label to [-1, 1] =====
        vals = df["value"].astype(np.float32).values
        max_abs = max(abs(vals.min()), abs(vals.max()), 1)
        self.targets = (vals / max_abs).astype(np.float32)

        print(f"[INFO] Value normalization factor = {max_abs:.4f}")

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        board = decode_board(self.boards_hex[idx])
        player = np.array([self.players[idx]], dtype=np.float32)
        x = np.concatenate([board, player], axis=0)
        y = np.array([self.targets[idx]], dtype=np.float32)
        return torch.from_numpy(x), torch.from_numpy(y)


# =============== 3. Model (Residual MLP) ==================

class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.act = nn.ReLU()
        self.fc2 = nn.Linear(dim, dim)
        self.bn = nn.BatchNorm1d(dim)

    def forward(self, x):
        out = self.fc1(x)
        out = self.act(out)
        out = self.fc2(out)
        out = self.bn(out)
        return self.act(out + x)


class ValueNet(nn.Module):
    def __init__(self, input_dim=91):
        super().__init__()
        hidden = 512

        self.input = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.BatchNorm1d(hidden)
        )

        # 3 strong residual blocks
        self.res1 = ResidualBlock(hidden)
        self.res2 = ResidualBlock(hidden)
        self.res3 = ResidualBlock(hidden)

        self.output = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(hidden, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        x = self.input(x)
        x = self.res1(x)
        x = self.res2(x)
        x = self.res3(x)
        return self.output(x)


# =============== 4. Train & Validate ==================

def train_epoch(model, loader, optimizer, loss_fn, device):
    model.train()
    total = 0

    for xb, yb in loader:
        xb, yb = xb.to(device).float(), yb.to(device).float()

        optimizer.zero_grad()
        pred = model(xb)
        loss = loss_fn(pred, yb)
        loss.backward()

        # ===== NEW: gradient clipping (helps stability) =====
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()
        total += loss.item() * xb.size(0)

    return total / len(loader.dataset)


def validate_epoch(model, loader, loss_fn, device):
    model.eval()
    total = 0
    with torch.no_grad():
        for xb, yb in loader:
            xb, yb = xb.to(device).float(), yb.to(device).float()
            total += loss_fn(model(xb), yb).item() * xb.size(0)
    return total / len(loader.dataset)


# =============== 5. Main ==================

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", type=str, default="dataset.csv")
    p.add_argument("--epochs", type=int, default=40)
    p.add_argument("--batch", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--model-path", type=str, default="value_net.pt")
    p.add_argument("--val-split", type=float, default=0.1)
    p.add_argument("--max-rows", type=int, default=None)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    ds = XiangqiValueDataset(args.csv, max_rows=args.max_rows)

    n = len(ds)
    val_count = int(n * args.val_split)
    train_count = n - val_count

    train_ds, val_ds = random_split(ds, [train_count, val_count])

    train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch)

    model = ValueNet(91).to(device)

    # ===== NEW: SmoothL1Loss (Huber) - better for noisy data =====
    loss_fn = nn.SmoothL1Loss()
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)

    best_val = float("inf")
    patience = 8
    bad_epochs = 0

    for epoch in range(1, args.epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, loss_fn, device)
        val_loss = validate_epoch(model, val_loader, loss_fn, device)

        print(f"Epoch {epoch:02d} | Train {train_loss:.6f} | Val {val_loss:.6f}")

        # Early stopping
        if val_loss < best_val:
            best_val = val_loss
            bad_epochs = 0
            torch.save(model.state_dict(), args.model_path)
            print(f" → Saved best model ({best_val:.6f})")
        else:
            bad_epochs += 1
            if bad_epochs >= patience:
                print("Early stopping triggered.")
                break

    print("Training finished.")


if __name__ == "__main__":
    main()
