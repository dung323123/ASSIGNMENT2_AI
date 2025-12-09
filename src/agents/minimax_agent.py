from typing import Optional
import math
from src.game.board import GameState, Move, Player

class MinimaxAgent:
    def __init__(self, player_symbol: Player, max_depth: int = 2):
        """
        player_symbol: RED (1) hoặc BLACK (-1)
        """
        self.player = player_symbol
        self.max_depth = max_depth

    def get_move(self, state: GameState) -> Optional[Move]:
        """
        Chọn nước đi tốt nhất từ trạng thái hiện tại
        """
        maximizing = (state.current_player == self.player)

        best_score = -math.inf if maximizing else math.inf
        best_move = None
        all_move = state.get_all_legal_moves()

        for move in state.get_all_legal_moves():
            next_state = state.make_move(move)

            score = self._minimax(
                next_state,
                depth=self.max_depth - 1,
                alpha=-math.inf,
                beta=math.inf,
                maximizing=(next_state.current_player == self.player)
            )

            if maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        print(state.board)
        print("Lượt đi của :", state.board[best_move[0][0], best_move[0][1]] )
        print("Các move hợp lệ :", all_move )
        print("Best move :", best_move )
        print("--------------------------------------------------" )
        return best_move

    def _minimax(self, state: GameState, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """
        Minimax với Alpha-Beta
        """
        # Node lá
        if depth == 0 or state.is_game_over():
            return state.evaluate_heuristic(self.player)

        moves = state.get_all_legal_moves()

        # Không có nước đi → thua
        if not moves:
            # Nếu đến lượt AI mà không có nước → thua nặng
            if state.current_player == self.player:
                return -math.inf
            else:
                return math.inf

        if maximizing:
            max_eval = -math.inf
            for move in moves:
                eval = self._minimax(
                    state.make_move(move),
                    depth - 1,
                    alpha,
                    beta,
                    maximizing=False
                )
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            for move in moves:
                eval = self._minimax(
                    state.make_move(move),
                    depth - 1,
                    alpha,
                    beta,
                    maximizing=True
                )
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
