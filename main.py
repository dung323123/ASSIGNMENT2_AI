from src.game.board import GameState
from src.agents.random_agent import RandomAgent

RED = 1
BLACK = -1



def play_game(agent_red, agent_black, max_turns=2000):
    """
    Chạy 1 ván đấu giữa 2 agent
    Trả về agent thắng ('red' / 'black') hoặc 'draw'-hòa
    Note: max_turns không có trong luật chính thức, chỉ dùng để tránh chương trình bị kẹt
    """
    state = GameState()

    for turn in range(max_turns):
        # Xác định agent đang đi
        agent = agent_red if state.current_player == RED else agent_black

        # Agent chọn nước đi
        move = agent.get_move(state)

        if move is None:
            # Hết nước → bên đang đi thua
            return "black" if state.current_player == RED else "red"

        # Cập nhật trạng thái sau nước đi
        state = state.make_move(move)

        print(f"{turn:03d} | {agent} đi {move}")

    return "draw"  # Quá số nước → hoà

if __name__ == "__main__":
    agent_red = RandomAgent(player_symbol=RED)
    agent_black = RandomAgent(player_symbol=BLACK)

    result = play_game(agent_red, agent_black)

    print("BÊN THẮNG:", result.upper())
