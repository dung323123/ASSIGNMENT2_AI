class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
class Move:
    def __init__(self, initial: Position, final: Position):
        self.initial = initial
        self.final = final
    