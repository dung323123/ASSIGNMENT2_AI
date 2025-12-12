from src.game.board import GameState, RED, BLACK
from src.agents.ml_agent import MLAgent
from src.agents.random_agent import RandomAgent


class GameTester:
    def __init__(self, num_games: int = 10, model_path: str = "model.pkl"):
        """
        num_games: số ván chơi cần chạy
        """
        self.num_games = num_games
        self.red_agent = MLAgent(RED, model_path=model_path)
        self.black_agent = RandomAgent(player_symbol=BLACK)
        
        self.red_wins = 0
        self.black_wins = 0
        self.draws = 0
        self.total_moves = 0

    def play_one_game(self, game_num: int, verbose: bool = False) -> dict:
        state = GameState()
        turn = 0
        max_turns = 200

        while not state.is_game_over() and turn < max_turns:
            turn += 1
            current_player = state.current_player
            
            # Lấy nước đi từ agent tương ứng
            legal_moves = state.get_all_legal_moves()
            if not legal_moves:
                break
                
            if current_player == RED:
                best_move = self.red_agent.get_move(state)
            else:
                best_move = self.black_agent.get_move(state)
            
            if best_move is None:
                break

            state = state.make_move(best_move)

        # Xác định người thắng
        if state.is_game_over():
            winner = -state.current_player
            if winner == RED:
                self.red_wins += 1
                winner_name = "RED (MLAgent)"
            else:
                self.black_wins += 1
                winner_name = "BLACK (Random)"
        else:
            self.draws += 1
            winner = 0
            winner_name = "Hòa"

        self.total_moves += turn

        if verbose:
            print(f"Ván {game_num}: {winner_name} thắng sau {turn} nước đi")
        elif game_num % 10 == 0:
            print(f"Đã chơi {game_num} ván... "
                  f"(RED: {self.red_wins}W, BLACK: {self.black_wins}W, Hòa: {self.draws})")

        return {
            'game_num': game_num,
            'winner': winner,
            'winner_name': winner_name,
            'total_turns': turn
        }

    def play_all_games(self, verbose: bool = False):
        print(f"\n{'#'*60}")
        print(f"# Bắt đầu chạy {self.num_games} ván chơi")
        print(f"# RED: MLAgent (model.pkl)")
        print(f"# BLACK: Random Agent")
        print(f"{'#'*60}\n")

        results = []
        for game_num in range(1, self.num_games + 1):
            result = self.play_one_game(game_num, verbose=verbose)
            results.append(result)

        return results

    def print_stats(self):
        print(f"\n{'='*60}")
        print("THỐNG KÊ KẾT QUẢ")
        print(f"{'='*60}")
        print(f"Tổng số ván: {self.num_games}")
        print(f"RED (MLAgent) thắng: {self.red_wins} ({self.red_wins/self.num_games*100:.1f}%)")
        print(f"BLACK (Random) thắng: {self.black_wins} ({self.black_wins/self.num_games*100:.1f}%)")
        print(f"Hòa: {self.draws} ({self.draws/self.num_games*100:.1f}%)")
        print(f"Tổng số nước đi: {self.total_moves}")
        print(f"Trung bình mỗi ván: {self.total_moves/self.num_games:.1f}")
        print(f"{'='*60}\n")


def main():
    tester = GameTester(num_games=100, model_path="value_net.pt")
    tester.play_all_games(verbose=False)
    tester.print_stats()


if __name__ == "__main__":
    main()