import csv
import json
import os
from typing import List, Dict, Any, Tuple
import numpy as np

from src.game.board import GameState, RED, BLACK
from src.agents.minimax_agent import MinimaxAgent
from src.agents.random_agent import RandomAgent

Move = Tuple[Tuple[int, int], Tuple[int, int]]

class DatasetGenerator92:
    def __init__(
        self,
        num_games: int = 100,
        max_depth: int = 2,
        output_file: str = "dataset.csv",
        board_dtype=np.int64,
        save_all_games: bool = True,
        save_only_red: bool = False,
        overwrite: bool = False  # <--- ALWAYS append if False
    ):
        self.num_games = num_games
        self.max_depth = max_depth
        self.output_file = output_file
        self.board_dtype = board_dtype
        self.save_all_games = save_all_games
        self.save_only_red = save_only_red
        self.overwrite = overwrite

        # Agents
        self.red_agent = MinimaxAgent(RED, max_depth)
        self.black_agent = RandomAgent(BLACK)

        self.dataset: List[Dict[str, Any]] = []


    # -------------------------
    # Encoding helpers
    # -------------------------
    def board_to_string(self, board: np.ndarray) -> str:
        b = board.astype(self.board_dtype, copy=False)
        return b.flatten().tobytes().hex()

    def move_to_string(self, move: Move) -> str:
        if move is None:
            return "None"
        (r1, c1), (r2, c2) = move
        return f"{r1},{c1}->{r2},{c2}"


    # -------------------------
    # Play one game
    # -------------------------
    def play_one_game(self) -> Tuple[List[Dict[str, Any]], int]:
        state = GameState()
        samples: List[Dict[str, Any]] = []
        turn = 0
        max_turns = 150

        while not state.is_game_over() and turn < max_turns:
            turn += 1
            player = state.current_player

            legal_moves = state.get_all_legal_moves()
            if not legal_moves:
                break

            if player == RED:
                mdata = self.red_agent.get_move_with_data(state)
                if not mdata.get("has_legal_moves", True):
                    break
                selected_move = mdata["best_move"]
                board_arr = state.board.copy()
            else:
                selected_move = self.black_agent.get_move(state)
                board_arr = state.board.copy()

            # Save sample (RED only or both players)
            if (not self.save_only_red) or (self.save_only_red and player == RED):
                try:
                    value = float(state.evaluate_heuristic(player))
                except Exception:
                    value = 0.0

                sample = {
                    "board": self.board_to_string(board_arr),
                    "board_element_bytes": int(np.dtype(self.board_dtype).itemsize),
                    "current_player": int(player),
                    "legal_moves": str(legal_moves),
                    "selected_move": self.move_to_string(selected_move),
                    "value": float(value),
                    "is_terminal": int(state.is_game_over()),
                    "outcome": 0  # fill later
                }
                samples.append(sample)

            # Apply move
            state = state.make_move(selected_move)

        # Determine winner
        if state.is_game_over():
            winner = -state.current_player
        else:
            winner = 0  # draw

        # Fill outcomes
        for s in samples:
            if winner == 0:
                s["outcome"] = 0
            else:
                s["outcome"] = 1 if s["current_player"] == winner else -1

        return samples, winner


    # -------------------------
    # Generate many games
    # -------------------------
    def generate_dataset(self):
        print(f"=== GENERATING DATASET ({self.num_games} games) ===")
        saved_games = 0
        total_records = 0

        for i in range(self.num_games):
            game_samples, winner = self.play_one_game()

            should_save = self.save_all_games or (winner == RED)
            if should_save and game_samples:
                self.dataset.extend(game_samples)
                saved_games += 1
                total_records += len(game_samples)

            print(f"[Game {i+1}] Winner={winner}, Produced={len(game_samples)}, Saved={should_save and len(game_samples)}>")

        print("==== DONE ====")
        print(f"Saved games: {saved_games}/{self.num_games}")
        print(f"Total records: {total_records}")


    # -------------------------
    # SAVE CSV — ALWAYS APPEND
    # -------------------------
    def save_csv(self):
        if not self.dataset:
            print("No data to save.")
            return

        path = os.path.join(os.path.dirname(__file__), self.output_file)
        file_exists = os.path.exists(path)

        mode = "a" if file_exists else "w"

        fields = [
            "board",
            "board_element_bytes",
            "current_player",
            "legal_moves",
            "selected_move",
            "value",
            "is_terminal",
            "outcome",
        ]

        with open(path, mode, newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.dataset)

        print(f"APPENDED CSV to {path} (rows added: {len(self.dataset)}; mode={mode})")


    # -------------------------
    # SAVE JSON — ALWAYS APPEND
    # -------------------------
    def save_json(self):
        path = self.output_file.replace(".csv", ".json")
        path = os.path.join(os.path.dirname(__file__), path)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                old_data = json.load(f)
        else:
            old_data = []

        old_data.extend(self.dataset)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(old_data, f, indent=2)

        print(f"APPENDED JSON to {path} (total items now: {len(old_data)})")


def main():
    gen = DatasetGenerator92(
        num_games=500,
        max_depth=2,
        output_file="dataset.csv",
        board_dtype=np.int64,
        save_all_games=True,
        save_only_red=False,
        overwrite=False   # <--- ALWAYS append mode
    )
    gen.generate_dataset()
    gen.save_csv()
    gen.save_json()


if __name__ == "__main__":
    main()
