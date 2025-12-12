from typing import Optional, List
import numpy as np
import torch
import torch.nn as nn
from src.game.board import GameState, Move, Player, RED, BLACK
from src.train_ml import ValueNet

class MLAgent:

    def __init__(
        self, 
        player_symbol: Player, 
        model_path: str = "value_net.pt", 
        device: Optional[str] = None,
        exploration_rate: float = 0.05  # 5% khám phá ngẫu nhiên
    ):
        self.player = player_symbol
        self.exploration_rate = exploration_rate
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        
        # Load ML model
        self.model = ValueNet(input_dim=91).to(self.device)
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        print(f"[MLAgent] 🤖 Loaded Value Network (NO search)")
        print(f"[MLAgent] 🎲 Exploration rate: {exploration_rate:.1%}")
        
        # Chống lặp đơn giản
        self.position_history = []
        self.max_history = 20
        
        # Stats
        self.moves_evaluated = 0
    
    # ============================================================
    # ENCODING
    # ============================================================
    def encode_state(self, state: GameState) -> np.ndarray:
        """Encode state thành 91 features"""
        board_flat = state.board.flatten().astype(np.float32)
        cur_player = np.array([float(state.current_player)], np.float32)
        return np.concatenate([board_flat, cur_player], axis=0)
    
    # ============================================================
    # EVALUATION: Pure ML (No Heuristic)
    # ============================================================
    def evaluate_state(self, state: GameState) -> float:
        """
        Đánh giá state bằng Value Network
        Trả về điểm từ góc nhìn self.player
        """
        # Game over
        if state.is_game_over():
            if state.current_player == self.player:
                return -1000.0  # Mình thua
            else:
                return 1000.0   # Địch thua
        
        # ML prediction
        features = self.encode_state(state)
        x = torch.tensor(features, dtype=torch.float32, device=self.device).unsqueeze(0)
        
        with torch.no_grad():
            value = self.model(x).view(-1).item()
        
        # value ∈ [-1, 1], chuyển về góc nhìn self.player
        if state.current_player == self.player:
            return value
        else:
            return -value
    
    # ============================================================
    # REPETITION CHECK
    # ============================================================
    def is_repetition(self, state: GameState) -> bool:
        """Kiểm tra lặp vị trí"""
        key = tuple(state.board.flatten())
        return self.position_history.count(key) >= 2
    
    # ============================================================
    # GET MOVE: Greedy 1-ply (No Search)
    # ============================================================
    def get_move(self, state: GameState) -> Optional[Move]:
        """
        Chọn nước đi tốt nhất (greedy):
        1. Đánh giá tất cả nước đi hợp lệ
        2. Chọn nước có eval cao nhất
        3. Tránh lặp
        """
        moves = state.get_all_legal_moves()
        if not moves:
            return None
        
        self.moves_evaluated = len(moves)
        
        # Exploration: 5% khám phá ngẫu nhiên (giúp tránh local minima)
        if np.random.random() < self.exploration_rate:
            move = moves[np.random.randint(len(moves))]
            print(f"[MLAgent] 🎲 Random exploration")
            self._update_history(state)
            return move
        
        # Đánh giá từng nước đi
        best_score = -1e9
        best_move = None
        
        for move in moves:
            next_state = state.make_move(move)
            
            # Phạt lặp (nhẹ hơn so với search-based agent)
            if self.is_repetition(next_state):
                score = -10.0  # Phạt nhẹ
            else:
                # ML evaluation
                score = self.evaluate_state(next_state)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        print(f"[MLAgent] ✓ Evaluated {len(moves)} moves, best score: {best_score:.3f}")
        
        # Cập nhật history
        self._update_history(state)
        
        return best_move
    
    def _update_history(self, state: GameState):
        """Cập nhật lịch sử vị trí"""
        key = tuple(state.board.flatten())
        self.position_history.append(key)
        if len(self.position_history) > self.max_history:
            self.position_history.pop(0)
    
    # ============================================================
    # UTILITIES
    # ============================================================
    def reset_history(self):
        """Reset lịch sử"""
        self.position_history.clear()
        print("[MLAgent] 🔄 History reset")
    
    def get_stats(self) -> dict:
        """Thống kê"""
        return {
            "moves_evaluated": self.moves_evaluated,
            "history_length": len(self.position_history),
            "exploration_rate": self.exploration_rate
        }
