import os
class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'red' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.set_texture()
        self.textture_rect = texture_rect
        
    def set_texture(self):
        self.texture = os.path.join('src','ui','images', f'{self.color}_{self.name.lower()}.png')
        
class General(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1 # 1: red (down), -1: black (up)
        super().__init__('General', color, 7)

class Advisor(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1
        super().__init__('Advisor', color, 6)

class Elephant(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1
        super().__init__('Elephant', color, 5)

class Horse(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1
        super().__init__('Horse', color, 2)
        
class Chariot(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1
        super().__init__('Chariot', color, 4)
        
class Cannon(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1
        super().__init__('Cannon', color, 3)

class Soldier(Piece):
    def __init__(self, color):
        self.dir =1 if color == 'red' else -1
        super().__init__('Soldier', color, 1)

        
        