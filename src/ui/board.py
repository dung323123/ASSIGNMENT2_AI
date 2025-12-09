import pygame

from src.ui.const import *
from src.ui.square import Square
from src.ui.piece import *
from src.ui.move import Move

class Board:
    def __init__(self):
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]        
        self._create()
        self._add_pieces('red')
        self._add_pieces('black')
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
            
    def _add_pieces(self, color):
        
        # Đảo ngược quy ước: Đỏ ở DƯỚI (hàng 9), Đen ở TRÊN (hàng 0)
        
        # ─────────────────────────────────────────────────────────────
        # 1. TỐT/BINH (Soldiers/Zus)
        # RED (Đỏ): Hàng 6 (Hàng Tốt dưới)
        # BLACK (Đen): Hàng 3 (Hàng Tốt trên)
        for i in range(0, COLS, 2):
            if color == 'red':
                self.squares[6][i] = Square(6, i, Soldier(color)) # Đã sửa từ [3][i] -> [6][i]
            else:
                self.squares[3][i] = Square(3, i, Soldier(color)) # Đã sửa từ [6][i] -> [3][i]
        
        # ─────────────────────────────────────────────────────────────
        # 2. PHÁO (Cannons)
        # RED (Đỏ): Hàng 7
        # BLACK (Đen): Hàng 2
        for i in [1, 7]:
            if color == 'red':
                self.squares[7][i] = Square(7, i, Cannon(color)) # Đã sửa từ [2][i] -> [7][i]
            else:
                self.squares[2][i] = Square(2, i, Cannon(color)) # Đã sửa từ [7][i] -> [2][i]
        
        # ─────────────────────────────────────────────────────────────
        # 3. CÁC QUÂN CƠ BẢN (Xe, Mã, Tượng, Sĩ, Tướng)
        # RED (Đỏ): Hàng 9
        # BLACK (Đen): Hàng 0
        
        base_row = 9 if color == 'red' else 0 # Xác định hàng cơ sở
        
        # Add chariots (Xe)
        for i in [0, 8]:
            self.squares[base_row][i] = Square(base_row, i, Chariot(color))
        
        # Add horses (Mã)
        for i in [1, 7]:
            self.squares[base_row][i] = Square(base_row, i, Horse(color))
        
        # Add elephants (Tượng)
        for i in [2, 6]:
            self.squares[base_row][i] = Square(base_row, i, Elephant(color))
        
        # Add advisors (Sĩ)
        for i in [3, 5]:
            self.squares[base_row][i] = Square(base_row, i, Advisor(color))
        
        # Add general (Tướng)
        self.squares[base_row][4] = Square(base_row, 4, General(color))
        
board = Board()