import numpy as np
from typing import List, Tuple

BOARD_ROWS, BOARD_COLS = 10, 9
RED, BLACK = 1, -1
EMPTY = 0

# Giá trị quân cờ
TUONG = 7      # Tướng/Soái
SI = 6         # Sĩ
TUONG_KINH = 5 # Tượng
XE = 4         # Xe
PHAO = 3       # Pháo
MA = 2         # Mã
TOT = 1        # Tốt/Binh

Position = Tuple[int, int]
Move = Tuple[Position, Position]
Player = int


'''
Quy ước: Hệ tọa độ ở góc trên trái bàn cờ, (r,c) = (hàng, cột)
    - Đi xuống: r + 1
    - Sang phải: c + 1
'''


class GameState:

    def __init__(self, initial_board: np.ndarray = None, current_player: Player = RED, history: List[Move] = None):
        """
        Khởi tạo 1 trạng thái bàn cờ:
        - initial_board: mảng 10x9 nếu muốn set trạng thái tùy ý, nếu None → set vị trí ban đầu
        - current_player: RED (1) hay BLACK (-1) đang đến lượt đi
        - history: danh sách các nước đã đi 
        """
        self.board: np.ndarray = initial_board if initial_board is not None else self._setup_initial_board()
        self.current_player: Player = current_player
        self.history: List[Move] = history if history is not None else []


    def is_on_board(self, r: int, c: int) -> bool:
        """Kiểm tra tọa độ có nằm trong phạm vi bàn cờ hay không."""
        return 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS

    def is_in_palace(self, r: int, c: int, player: Player) -> bool:
        """
        Kiểm tra xem vị trí (r, c) có nằm trong Cung Tướng hay không
        RED: r = 7..9, c = 3..5
        BLACK: r = 0..2, c = 3..5
        """
        if 3 <= c <= 5:
            if player == RED and 7 <= r <= 9:
                return True
            if player == BLACK and 0 <= r <= 2:
                return True
        return False

    def get_piece_at(self, pos: Position) -> int:
        """Lấy quân cờ tại một ô; trả về EMPTY nếu tọa độ không hợp lệ"""
        r, c = pos
        return self.board[r, c] if self.is_on_board(r, c) else EMPTY

    def _get_general_position(self, player: Player) -> Position:
        """
        Trả về vị trí Tướng của RED hoặc BLACK.
        Nếu Tướng đã bị ăn → trả về (-1, -1)
        """
        r, c = np.where(self.board == TUONG * player)
        return (r[0], c[0]) if len(r) > 0 else (-1, -1)

   
    def _setup_initial_board(self) -> np.ndarray:
        """
        Thiết lập bàn cờ ban đầu
        Cài đặt vị trí quân cờ
        """
        board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
        setup_pieces = [XE, MA, TUONG_KINH, SI, TUONG, SI, TUONG_KINH, MA, XE]

        # Đen (Black)
        board[0] = [-p for p in setup_pieces]
        board[2, 1] = board[2, 7] = -PHAO
        board[3, 0::2] = -TOT

        # Đỏ (Red)
        board[9] = setup_pieces
        board[7, 1] = board[7, 7] = PHAO
        board[6, 0::2] = TOT

        return board

    def _get_moves_for_piece(self, r: int, c: int) -> List[Move]:
        """
        Lấy danh sách các vị trí quân có thể đi đến dựa trên luật di chuyển của riêng loại quân đó
        Chưa kiểm tra:
        - Tướng bị chiếu sau khi đi
        - Hai Tướng đối mặt
        Các điều kiện đó xử lý ở get_all_legal_moves()
        """
        piece = self.board[r, c]
        if piece == EMPTY:
            return []

        player = RED if piece > 0 else BLACK
        abs_piece = abs(piece)
        moves: List[Move] = []
        source = (r, c)
        river_limit = 5 if player == RED else 4

        # Các luật di chuyển tuân theo chương 1
        
        # Tướng và Sĩ
        if abs_piece == TUONG or abs_piece == SI:
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)] if abs_piece == TUONG else \
                   [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if self.is_on_board(nr, nc) and self.is_in_palace(nr, nc, player):
                    tp = self.get_piece_at((nr, nc))
                    if (piece * tp) <= 0:
                        moves.append((source, (nr, nc)))

        # Tượng
        elif abs_piece == TUONG_KINH:
            for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                nr, nc = r + dr, c + dc
                br, bc = r + dr // 2, c + dc // 2
                if self.is_on_board(nr, nc) and ((player == RED and nr >= 5) or (player == BLACK and nr <= 4)):
                    if self.get_piece_at((br, bc)) == EMPTY:
                        tp = self.get_piece_at((nr, nc))
                        if (piece * tp) <= 0:
                            moves.append((source, (nr, nc)))

        # Xe
        elif abs_piece == XE:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                for step in range(1, BOARD_ROWS):
                    nr, nc = r + dr * step, c + dc * step
                    if not self.is_on_board(nr, nc):
                        break
                    tp = self.get_piece_at((nr, nc))
                    if tp == EMPTY:
                        moves.append((source, (nr, nc)))
                    elif (piece * tp) < 0:
                        moves.append((source, (nr, nc)))
                        break
                    else:
                        break

        # Pháo
        elif abs_piece == PHAO:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                saw_mount = False
                for step in range(1, BOARD_ROWS):
                    nr, nc = r + dr * step, c + dc * step
                    if not self.is_on_board(nr, nc):
                        break
                    tp = self.get_piece_at((nr, nc))
                    if not saw_mount:
                        if tp == EMPTY:
                            moves.append((source, (nr, nc)))
                        else:
                            saw_mount = True
                    else:
                        if tp == EMPTY:
                            continue
                        elif (piece * tp) < 0:
                            moves.append((source, (nr, nc)))
                            break
                        else:
                            break

        # Mã
        elif abs_piece == MA:
            patterns = [(2, 1, 1, 0), (2, -1, 1, 0), (-2, 1, -1, 0), (-2, -1, -1, 0),
                        (1, 2, 0, 1), (-1, 2, 0, 1), (1, -2, 0, -1), (-1, -2, 0, -1)]
            for dr, dc, br, bc in patterns:
                nr, nc = r + dr, c + dc
                brd, bcd = r + br, c + bc
                if self.is_on_board(nr, nc) and self.get_piece_at((brd, bcd)) == EMPTY:
                    tp = self.get_piece_at((nr, nc))
                    if (piece * tp) <= 0:
                        moves.append((source, (nr, nc)))

        # Tốt
        elif abs_piece == TOT:
            d = -1 if player == BLACK else 1
            targets = [(r + d, c)]
            if (player == RED and r < river_limit) or (player == BLACK and r > river_limit):
                targets.extend([(r, c + 1), (r, c - 1)])
            for nr, nc in targets:
                if self.is_on_board(nr, nc):
                    tp = self.get_piece_at((nr, nc))
                    if (piece * tp) <= 0:
                        moves.append((source, (nr, nc)))

        return moves

    # KIỂM TRA CHIẾU & TƯỚNG ĐỐI MẶT
    # ─────────────────────────────────────────────────────────────
    def is_check(self, board: np.ndarray, player: Player) -> bool:
        """
        Kiểm tra xem Tướng của `player` có đang bị chiếu không.
        Ý tưởng: lấy tất cả nước đi PHI NƯỚC CHỐT của quân địch, nếu có quân địch nào
        có thể bắt đúng ô tướng → player đang bị chiếu.
        """
        general_pos = self._get_general_position(player)
        if general_pos == (-1, -1):
            return False
        opponent = -player
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece = board[r, c]
                if piece * opponent > 0:
                    for _, target in self._get_moves_for_piece(r, c):
                        if target == general_pos:
                            return True
        return False

    def is_general_facing(self) -> bool:
        """
        Kiểm tra luật “hai Tướng không được nhìn thẳng nhau”.
        Nếu hai Tướng cùng cột và không có quân nào ở giữa → nước đi không hợp lệ.
        """
        rp = self._get_general_position(RED)
        bp = self._get_general_position(BLACK)
        if rp[1] != bp[1]:
            return False
        c = rp[1]
        for r in range(min(rp[0], bp[0]) + 1, max(rp[0], bp[0])):
            if self.board[r, c] != EMPTY:
                return False
        return True

    # API CHÍNH CHO MINIMAX / ML / RANDOM
    # ─────────────────────────────────────────────────────────────
    def make_move(self, move: Move) -> 'GameState':
        """
        Tạo ra 1 trạng thái bàn cờ MỚI sau khi thực hiện nước đi
        Không mutate trạng thái hiện tại (để Minimax hoạt động đúng)
        """
        new_state = GameState(
            initial_board=self.board.copy(),
            current_player=-self.current_player,
            history=self.history + [move]
        )
        src, dst = move
        new_state.board[dst] = self.get_piece_at(src)
        new_state.board[src] = EMPTY
        return new_state

    def get_all_legal_moves(self) -> List[Move]:
        """
        Lấy tất cả nước đi hợp lệ của người chơi hiện tại:
        1) Lấy nước đi thô của từng quân
        2) Giả lập nước đi → check xem có khiến Tướng mình bị chiếu không
        3) Check luật Tướng đối mặt
        Chỉ nước thỏa lệ mới được giữ lại.
        """
        legal: List[Move] = []
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece = self.board[r, c]
                if piece * self.current_player > 0:
                    raw_moves = self._get_moves_for_piece(r, c)
                    for move in raw_moves:
                        test_state = self.make_move(move)
                        if not test_state.is_check(test_state.board, self.current_player) and not test_state.is_general_facing():
                            legal.append(move)
        return legal

    def is_game_over(self) -> bool:
        """
        Trò chơi kết thúc khi người chơi tới lượt:
        - Không còn nước đi hợp lệ → thua (chiếu bí hoặc bị vây)
        """
        return not self.get_all_legal_moves()

    def evaluate_heuristic(self, player: Player) -> float:
        """
        Heuristic cơ bản cho Minimax:
        Tính tổng giá trị vật chất quân cờ (không xét vị trí)
        Note: Minimax tự mplement lại cho phù hợp
        """
        values = {TUONG: 1000, XE: 9, PHAO: 4.5, MA: 4, SI: 2, TUONG_KINH: 2, TOT: 1}
        score = 0
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece = self.board[r, c]
                if piece != EMPTY:
                    score += values[abs(piece)] * (1 if piece * player > 0 else -1)
        return score

    def to_features(self) -> np.ndarray:
        """
        Chuyển bàn cờ thành vector 1D — phục vụ ML/RL
        """
        return self.board.flatten()
