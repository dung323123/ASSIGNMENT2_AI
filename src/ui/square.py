import pygame

from src.ui.const import *
from src.ui.piece import Piece

class Square:
    def __init__(self, row, col, piece: Piece = None):
        self.row = row
        self.col = col
        self.piece = piece
    
    def has_piece(self):
        return self.piece is not None
    
    def show_change(self, screen):
        pygame.draw.circle(
            screen,
            'orange',
            (self.col * SQUARE_SIZE + BOARD_OFFSET_X,
             self.row * SQUARE_SIZE + BOARD_OFFSET_Y),
            SQUARE_SIZE // 2,
            width=3
        )
        
        