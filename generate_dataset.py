"""
Script để sinh dataset từ các ván chơi Minimax vs Minimax
Lưu dữ liệu vào file CSV để sử dụng cho huấn luyện ML agent
"""

import csv
import json
import os
from typing import List, Dict, Any
import numpy as np
from src.game.board import GameState, RED, BLACK
from src.agents.minimax_agent import MinimaxAgent
from src.agents.random_agent import RandomAgent
from src.agents.base_agent import BaseAgent


class DatasetGenerator:
    def __init__(self, num_games: int = 10, max_depth: int = 2, output_file: str = "dataset.csv"):
        """
        num_games: số ván chơi cần sinh
        max_depth: độ sâu của minimax
        output_file: tên file lưu dataset
        
        Note: RED là Minimax agent, BLACK là Random agent (cố định)
              Chỉ lưu dữ liệu nước đi của Minimax (RED)
        """
        self.num_games = num_games
        self.max_depth = max_depth
        self.output_file = output_file
        self.current_game_number = 0  # Đếm số ván chơi
        
        # RED luôn là Minimax (để tạo dataset)
        self.red_agent = MinimaxAgent(RED, max_depth=max_depth)
        
        # BLACK luôn là Random agent
        self.black_agent = RandomAgent(player_symbol=BLACK)
        
        self.dataset = []
        self.move_count = 0

    def board_to_string(self, board: np.ndarray) -> str:
        """Chuyển board numpy array thành string để lưu vào CSV"""
        return board.flatten().tobytes().hex()

    def board_from_string(self, board_str: str) -> np.ndarray:
        """Chuyển string về lại numpy array"""
        if not board_str:
            return np.zeros((10, 9), dtype=int)
        board_bytes = bytes.fromhex(board_str)
        return np.frombuffer(board_bytes, dtype=int).reshape(10, 9)

    def move_to_string(self, move) -> str:
        """Chuyển move thành string"""
        if move is None:
            return "None"
        return f"{move[0]},{move[1]}"

    def play_one_game(self) -> Dict[str, Any]:
        """
        Chơi 1 ván đầy đủ giữa RED minimax vs BLACK random agent
        Chỉ lưu dữ liệu nước đi của RED (Minimax)
        Trả về kết quả ván (thắng/thua/hòa)
        """
        self.current_game_number += 1
        state = GameState()
        move_history = []
        game_data = []

        print(f"\n{'='*60}")
        print(f"Ván chơi #{self.current_game_number}")
        print(f"{'='*60}")

        turn = 0
        max_turns = 200  # Tránh vòng lặp vô hạn

        while not state.is_game_over() and turn < max_turns:
            turn += 1
            current_player = state.current_player
            
            if current_player == RED:
                # RED: Minimax agent
                move_data = self.red_agent.get_move_with_data(state)

                if not move_data['has_legal_moves']:
                    print(f"Lượt {turn}: RED (Minimax) không có nước đi hợp lệ → Thua!")
                    break

                best_move = move_data['best_move']
                best_score = move_data['best_score']

                # Lưu dữ liệu nước đi của Minimax
                data_point = {
                    'board': self.board_to_string(move_data['board']),
                    'current_player': current_player,
                    'all_legal_moves': str(move_data['all_legal_moves']),
                    'best_move': self.move_to_string(best_move),
                    'best_score': best_score,
                    'is_maximizing': move_data['is_maximizing'],
                    'turn': turn
                }
                game_data.append(data_point)

                print(f"Lượt {turn}: RED (Minimax) di chuyển {best_move}, score={best_score}")

            else:
                # BLACK: Random agent (không lưu dữ liệu)
                legal_moves = state.get_all_legal_moves()
                if not legal_moves:
                    print(f"Lượt {turn}: BLACK (Random) không có nước đi hợp lệ → Thua!")
                    break

                best_move = self.black_agent.get_move(state)
                print(f"Lượt {turn}: BLACK (Random) di chuyển {best_move}")

            move_history.append(best_move)
            self.move_count += 1

            # Thực hiện nước đi
            state = state.make_move(best_move)

        # Xác định người thắng
        if state.is_game_over():
            winner = -state.current_player  # Người trước đó là người thắng
            winner_name = "RED (Minimax)" if winner == RED else "BLACK (Random)"
            print(f"\n✓ {winner_name} thắng sau {turn} lượt!")
        else:
            winner_name = "Hòa (vượt quá 200 lượt)"
            winner = 0
            print(f"\n✗ {winner_name}")

        return {
            'winner': winner,
            'winner_name': winner_name,
            'total_turns': turn,
            'move_history': move_history,
            'game_data': game_data
        }

    def generate_dataset(self):
        """Sinh dataset từ nhiều ván chơi"""
        print(f"\n{'#'*60}")
        print(f"# Bắt đầu sinh dataset: {self.num_games} ván chơi")
        print(f"# RED: Minimax (depth={self.max_depth})")
        print(f"# BLACK: Random Agent")
        print(f"# Chỉ lưu dữ liệu nước đi của RED (Minimax)")
        print(f"{'#'*60}")

        game_results = []

        for game_num in range(self.num_games):
            try:
                game_result = self.play_one_game()
                game_results.append(game_result)

                # Thêm dữ liệu từ ván này vào dataset
                for data_point in game_result['game_data']:
                    # Thêm thông tin kết quả ván
                    data_point['game_result'] = game_result['winner_name']
                    self.dataset.append(data_point)

            except Exception as e:
                print(f"❌ Lỗi khi chơi ván {game_num + 1}: {e}")
                import traceback
                traceback.print_exc()

        print(f"\n{'#'*60}")
        print(f"# Hoàn thành sinh dataset")
        print(f"# Số ván chơi: {len(game_results)}")
        print(f"# Tổng số nước đi: {self.move_count}")
        print(f"# Tổng số dữ liệu: {len(self.dataset)}")
        print(f"{'#'*60}")

        return game_results

    def save_to_csv(self):
        """Lưu dataset vào CSV"""
        if not self.dataset:
            print("❌ Dataset rỗng! Không thể lưu.")
            return

        try:
            output_path = os.path.join(os.path.dirname(__file__), self.output_file)

            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'board',
                    'current_player',
                    'all_legal_moves',
                    'best_move',
                    'best_score',
                    'is_maximizing',
                    'turn',
                    'game_result'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.dataset)

            print(f"✓ Dataset đã lưu vào: {output_path}")
            print(f"  Số dòng dữ liệu: {len(self.dataset)}")

        except Exception as e:
            print(f"❌ Lỗi khi lưu CSV: {e}")
            import traceback
            traceback.print_exc()

    def save_to_json(self):
        """Lưu dataset vào JSON (có thể lưu trữ board dưới dạng mảng)"""
        if not self.dataset:
            print("❌ Dataset rỗng! Không thể lưu.")
            return

        try:
            output_path = os.path.join(os.path.dirname(__file__), 
                                      self.output_file.replace('.csv', '.json'))

            json_data = []
            for data_point in self.dataset:
                json_point = data_point.copy()
                # Chuyển board từ string hex về list
                json_point['board'] = self.board_from_string(data_point['board']).tolist()
                json_data.append(json_point)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            print(f"✓ Dataset đã lưu vào: {output_path}")
            print(f"  Số dòng dữ liệu: {len(json_data)}")

        except Exception as e:
            print(f"❌ Lỗi khi lưu JSON: {e}")
            import traceback
            traceback.print_exc()


def main():
    # Khởi tạo generator
    generator = DatasetGenerator(
        num_games=5,                    # Sinh 5 ván chơi
        max_depth=2,                    # Minimax depth = 2
        output_file="dataset_minimax_vs_random.csv"
    )

    # Sinh dataset
    game_results = generator.generate_dataset()

    # Lưu vào CSV và JSON
    generator.save_to_csv()
    generator.save_to_json()

    # Thống kê kết quả
    print(f"\n{'='*60}")
    print("THỐNG KÊ KẾT QUẢ")
    print(f"{'='*60}")
    
    red_wins = sum(1 for g in game_results if g['winner'] == RED)
    black_wins = sum(1 for g in game_results if g['winner'] == BLACK)
    draws = len(game_results) - red_wins - black_wins

    print(f"RED (Minimax) thắng: {red_wins}")
    print(f"BLACK (Random) thắng: {black_wins}")
    print(f"Hòa: {draws}")
    print(f"Tổng ván: {len(game_results)}")


if __name__ == "__main__":
    main()
