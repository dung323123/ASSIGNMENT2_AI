from abc import ABC, abstractmethod
from typing import Optional
from src.game.board import GameState, Move, Player

class BaseAgent(ABC):
    """
    Lớp trừu tượng đại diện cho một agent
    Tất cả loại agent (Random, Minimax, ML) đều phải kế thừa lớp này
    """

    def __init__(self, player_symbol: Player):
        """
        player_symbol = RED (1) hoặc BLACK (-1)
        Dùng cho agent có chiến lược phụ thuộc vào màu (ML/Minimax)
        """
        self.player_symbol = player_symbol

    def reset(self):
        """
        Dùng khi chơi nhiều ván liên tiếp
        Agent có bộ nhớ (như học tăng cường) sẽ cần reset
        Random agent hoặc Minimax không cần override
        """
        pass


    @abstractmethod
    def get_move(self, board: GameState) -> Optional[Move]:
        """
        [QUAN TRỌNG]
        Nhận trạng thái bàn cờ và trả về một nước đi (Movement).
        Nếu trả về None → nghĩa là agent không còn nước đi hợp lệ.
        """
        pass
