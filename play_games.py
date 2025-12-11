"""
Script để chạy nhiều ván chơi và thống kê kết quả (không sinh dataset)
RED (Minimax) vs BLACK (Random)
"""

from src.game.board import GameState, RED, BLACK
from src.agents.minimax_agent import MinimaxAgent
from src.agents.random_agent import RandomAgent


class GameTester:
    def __init__(self, num_games: int = 10, max_depth: int = 2):
        """
        num_games: số ván chơi cần chạy
        max_depth: độ sâu của minimax
        """
        self.num_games = num_games
        self.max_depth = max_depth
        self.red_agent = MinimaxAgent(RED, max_depth=max_depth)
        self.black_agent = RandomAgent(player_symbol=BLACK)
        
        self.red_wins = 0
        self.black_wins = 0
        self.draws = 0
        self.total_moves = 0

    def play_one_game(self, game_num: int, verbose: bool = False) -> dict:
        """
        Chơi 1 ván đầy đủ
        verbose: True để in chi tiết, False để chỉ in kết quả
        """
        state = GameState()
        turn = 0
        max_turns = 200

        while not state.is_game_over() and turn < max_turns:
            turn += 1
            current_player = state.current_player
            
            if current_player == RED:
                move_data = self.red_agent.get_move_with_data(state)
                if not move_data['has_legal_moves']:
                    break
                best_move = move_data['best_move']
            else:
                legal_moves = state.get_all_legal_moves()
                if not legal_moves:
                    break
                best_move = self.black_agent.get_move(state)

            if verbose:
                player_name = "RED (Minimax)" if current_player == RED else "BLACK (Random)"
                print(f"Lượt {turn}: {player_name} di chuyển {best_move}")

            state = state.make_move(best_move)

        # Xác định người thắng
        if state.is_game_over():
            winner = -state.current_player
            if winner == RED:
                winner_name = "RED (Minimax)"
                self.red_wins += 1
            else:
                winner_name = "BLACK (Random)"
                self.black_wins += 1
        else:
            winner_name = "Hòa"
            self.draws += 1
            winner = 0

        self.total_moves += turn

        if verbose:
            print(f"✓ {winner_name} thắng sau {turn} lượt!\n")
        else:
            # In tiến độ mỗi 10 ván
            if game_num % 10 == 0:
                print(f"Đã chơi {game_num} ván... (RED: {self.red_wins}W, BLACK: {self.black_wins}W, Hòa: {self.draws})")

        return {
            'game_num': game_num,
            'winner': winner,
            'winner_name': winner_name,
            'total_turns': turn
        }

    def play_all_games(self, verbose: bool = False):
        """Chơi tất cả các ván"""
        print(f"\n{'#'*60}")
        print(f"# Bắt đầu chạy {self.num_games} ván chơi")
        print(f"# RED: Minimax (depth={self.max_depth})")
        print(f"# BLACK: Random Agent")
        print(f"{'#'*60}\n")

        results = []
        for game_num in range(1, self.num_games + 1):
            try:
                result = self.play_one_game(game_num, verbose=verbose)
                results.append(result)
            except Exception as e:
                print(f"❌ Lỗi khi chơi ván {game_num}: {e}")
                import traceback
                traceback.print_exc()

        return results

    def print_stats(self):
        """In thống kê kết quả"""
        print(f"\n{'='*60}")
        print("THỐNG KÊ KẾT QUẢ")
        print(f"{'='*60}")
        print(f"Tổng số ván: {self.num_games}")
        print(f"RED (Minimax) thắng: {self.red_wins} ván ({self.red_wins/self.num_games*100:.1f}%)")
        print(f"BLACK (Random) thắng: {self.black_wins} ván ({self.black_wins/self.num_games*100:.1f}%)")
        print(f"Hòa: {self.draws} ván ({self.draws/self.num_games*100:.1f}%)")
        print(f"Tổng số nước đi: {self.total_moves}")
        print(f"Trung bình nước đi/ván: {self.total_moves/self.num_games:.1f}")
        print(f"{'='*60}\n")


def main():
    # Chạy 100 ván
    tester = GameTester(num_games=100, max_depth=2)
    results = tester.play_all_games(verbose=False)
    tester.print_stats()


if __name__ == "__main__":
    main()
