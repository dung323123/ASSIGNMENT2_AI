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
        # Add soldiers
        for i in range(0, COLS, 2):
            if color == 'red':
                self.squares[3][i] = Square(3, i, Soldier(color))
            else:
                self.squares[6][i] = Square(6, i, Soldier(color))
        
        # Add cannons
        for i in [1, 7]:
            if color == 'red':
                self.squares[2][i] = Square(2, i, Cannon(color))
            else:
                self.squares[7][i] = Square(7, i, Cannon(color))
        
        # Add chariots
        for i in [0, 8]:
            if color == 'red':
                self.squares[0][i] = Square(0, i, Chariot(color))
            else:
                self.squares[9][i] = Square(9, i, Chariot(color))
        
        # Add horses
        for i in [1, 7]:
            if color == 'red':
                self.squares[0][i] = Square(0, i, Horse(color))
            else:                
                self.squares[9][i] = Square(9, i, Horse(color))
        
        # Add elephants
        for i in [2, 6]:
            if color == 'red':
                self.squares[0][i] = Square(0, i, Elephant(color))
            else:
                self.squares[9][i] = Square(9, i, Elephant(color))
        
        # Add advisors
        for i in [3, 5]:
            if color == 'red':
                self.squares[0][i] = Square(0, i, Advisor(color))
            else:
                self.squares[9][i] = Square(9, i, Advisor(color))
        
        # Add general
        if color == 'red':
            self.squares[0][4] = Square(0, 4, General(color))
        else:
            self.squares[9][4] = Square(9, 4, General(color)) 
        
board = Board()