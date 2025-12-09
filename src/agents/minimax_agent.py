from typing import Optional
import math
from src.game.board import GameState, Move, Player

class MinimaxAgent:
    def __init__(self, player: Player, max_depth: int = 5):
        """
        player: RED (1) hoặc BLACK (-1)
        max_depth: độ sâu Minimax
        """
        self.player = player
        self.max_depth = max_depth

    def choose_move(self, state: GameState) -> Optional[Move]:
        """
        Chọn nước đi tốt nhất từ trạng thái hiện tại
        """
        best_score = -math.inf
        best_move = None

        for move in state.get_all_legal_moves():
            next_state = state.make_move(move)
            score = self._minimax(next_state, depth=self.max_depth - 1, alpha=-math.inf, beta=math.inf, maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, state: GameState, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """
        Hàm Minimax với alpha-beta pruning
        """
        if depth == 0 or state.is_game_over():
            return state.evaluate_heuristic(self.player)

        if maximizing:
            max_eval = -math.inf
            for move in state.get_all_legal_moves():
                next_state = state.make_move(move)
                eval = self._minimax(next_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # prune
            return max_eval
        else:
            min_eval = math.inf
            for move in state.get_all_legal_moves():
                next_state = state.make_move(move)
                eval = self._minimax(next_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # prune
            return min_eval
