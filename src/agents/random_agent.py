import random
from typing import Optional
from src.agents.base_agent import BaseAgent
from src.game.board  import GameState, Move 

class RandomAgent(BaseAgent):
    """
    Agent chọn ngẫu nhiên 1 nước đi hợp lệ từ GameState
    """

    def __init__(self, player_symbol: str = "BLACK", name: str = "RandomAgent"):
        self.player_symbol = player_symbol
        self.name = name

    def get_move(self, state: GameState) -> Optional[Move]:
        """
        Trả về một nước đi hợp lệ ngẫu nhiên.
        Nếu không có nước đi (hết nước → thua) thì trả về None.
        """
        legal_moves = state.get_all_legal_moves()
        if not legal_moves:
            return None
        return random.choice(legal_moves)

    def __str__(self):
        return f"{self.name}"
