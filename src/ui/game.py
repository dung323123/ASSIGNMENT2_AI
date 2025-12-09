import pygame

from src.ui.const import *
from src.ui.board import Board
from src.ui.move import Move
# AI agent ở đây

class Game:
    def __init__(self):
        self.board = Board()        
        
    def show_bg(self, screen):
        screen.fill(BG_COLOR)

        ox = BOARD_OFFSET_X
        oy = BOARD_OFFSET_Y

        # ================== VẼ ĐƯỜNG DỌC (CÓ CHỪA SÔNG) ==================
        for col in range(COLS):
            x = ox + col * SQUARE_SIZE

            # Phần trên sông
            pygame.draw.line(
                screen, LINE_COLOR,
                (x, oy),
                (x, oy + 4 * SQUARE_SIZE),
                2
            )

            # Phần dưới sông
            pygame.draw.line(
                screen, LINE_COLOR,
                (x, oy + 5 * SQUARE_SIZE),
                (x, oy + BOARD_HEIGHT),
                2
            )

        # ================== VẼ ĐƯỜNG NGANG ==================
        for row in range(ROWS):
            y = oy + row * SQUARE_SIZE
            pygame.draw.line(
                screen, LINE_COLOR,
                (ox, y),
                (ox + BOARD_WIDTH, y),
                2
            )

        # ================== CUNG TƯỚNG TRÊN ==================
        pygame.draw.line(screen, LINE_COLOR,
                        (ox + 3 * SQUARE_SIZE, oy),
                        (ox + 5 * SQUARE_SIZE, oy + 2 * SQUARE_SIZE), 2)

        pygame.draw.line(screen, LINE_COLOR,
                        (ox + 5 * SQUARE_SIZE, oy),
                        (ox + 3 * SQUARE_SIZE, oy + 2 * SQUARE_SIZE), 2)

        # ================== CUNG TƯỚNG DƯỚI ==================
        pygame.draw.line(screen, LINE_COLOR,
                        (ox + 3 * SQUARE_SIZE, oy + 7 * SQUARE_SIZE),
                        (ox + 5 * SQUARE_SIZE, oy + 9 * SQUARE_SIZE), 2)

        pygame.draw.line(screen, LINE_COLOR,
                        (ox + 5 * SQUARE_SIZE, oy + 7 * SQUARE_SIZE),
                        (ox + 3 * SQUARE_SIZE, oy + 9 * SQUARE_SIZE), 2)
        
        font = pygame.font.Font(None, 36)
        text_top = font.render("Random Agent", True, RED_COLOR)  # màu đỏ cho quân trên
        text_bottom = font.render("AI Agent", True, BLACK_COLOR)     # màu đen cho quân dưới

        # Vị trí chữ: căn giữa theo bàn cờ
        screen.blit(text_top, (ox + BOARD_WIDTH // 2 - text_top.get_width() // 2, 10))
        screen.blit(text_bottom, (ox + BOARD_WIDTH // 2 - text_bottom.get_width() // 2, SCREEN_HEIGHT- 30))

    def show_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    img = pygame.image.load(piece.texture)
                    img = pygame.transform.scale(img, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
                    img_center = col * SQUARE_SIZE + BOARD_OFFSET_X, row * SQUARE_SIZE + BOARD_OFFSET_Y
                    piece.texture_rect = img.get_rect(center=img_center)
                    screen.blit(img, piece.texture_rect) 
         
    def show_move(self, screen, move: Move):
        piece = self.board.squares[move.initial.row][move.initial.col].piece
        if piece is None:
            return
        # print(f"Move {self.board.squares[move.initial.row][move.initial.col].piece.name} from ({move.initial.row},{move.initial.col}) to ({move.final.row},{move.final.col})")
                
        self.board.squares[move.initial.row][move.initial.col].piece = None
        image = pygame.image.load(piece.texture).convert_alpha()
        image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))      
        #show new game state
        self.show_bg(screen)
        self.show_pieces(screen) 
        #show move linear
        
        start_x = BOARD_OFFSET_X+ move.initial.col*SQUARE_SIZE
        start_y = BOARD_OFFSET_Y+ move.initial.row*SQUARE_SIZE
        end_x = BOARD_OFFSET_X+move.final.col*SQUARE_SIZE
        end_y =BOARD_OFFSET_Y+move.final.row*SQUARE_SIZE
        
        steps=5
        for i in range (1, steps+1):
            x=start_x+(end_x-start_x)*i/steps
            y=start_y+(end_y-start_y)*i/steps
            
            self.show_bg(screen)
            self.show_pieces(screen)
            self.board.squares[move.initial.row][move.initial.col].show_change(screen)
            self.board.squares[move.final.row][move.final.col].show_change(screen)
            screen.blit(
                image,
                (
                    x - image.get_width() // 2,
                    y - image.get_height() // 2
                )
            )
            pygame.display.update()
            pygame.time.delay(SMOOTH_DELAY)
        self.board.squares[move.final.row][move.final.col].piece = piece

        pygame.display.update()
        pygame.time.delay(STEP_DELAY) 

