from typing import Optional, Dict, Any
import math
import copy
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

    def get_move_with_data(self, state: GameState) -> Dict[str, Any]:
        """
        Chọn nước đi tốt nhất và trả về dữ liệu đầy đủ cho dataset.
        
        Returns:
            Dict chứa:
            - board: trạng thái bàn cờ (copy của state.board)
            - all_legal_moves: tất cả các nước đi hợp lệ
            - best_move: nước đi được chọn
            - best_score: điểm số minimax của nước đi được chọn
            - current_player: người chơi hiện tại
            - is_maximizing: True nếu là lượt người chơi có AI, False ngược lại
        """
        maximizing = (state.current_player == self.player)

        best_score = -math.inf if maximizing else math.inf
        best_move = None
        all_moves = state.get_all_legal_moves()

        # Nếu không có nước đi hợp lệ
        if not all_moves:
            return {
                'board': copy.deepcopy(state.board),
                'all_legal_moves': all_moves,
                'best_move': None,
                'best_score': None,
                'current_player': state.current_player,
                'is_maximizing': maximizing,
                'has_legal_moves': False
            }

        for move in all_moves:
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

        return {
            'board': copy.deepcopy(state.board),
            'all_legal_moves': all_moves,
            'best_move': best_move,
            'best_score': best_score,
            'current_player': state.current_player,
            'is_maximizing': maximizing,
            'has_legal_moves': True
        }

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
