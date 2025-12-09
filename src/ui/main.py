import pygame
import sys

from src.ui.const import *
from src.ui.game import Game
from src.ui.move import Move, Position
from src.game.board import GameState
from src.agents.random_agent import RandomAgent
from src.agents.minimax_agent import MinimaxAgent
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Cờ tướng')
        
        self.game = Game() 
        self.playing = True # True if playing, False if stop
        self.agent_red = MinimaxAgent(player_symbol=RED)
        self.agent_black = RandomAgent(player_symbol=BLACK) # replace this agent by another AI agent
        self.winner=None

    def show_winner(self, screen):
        if self.winner == RED:
            text = "Winner: AI Agent"
        elif self.winner == BLACK:
            text = "Winner: Random Agent"
        else:
            text = "DRAW"

        # Tạo font
        font = pygame.font.Font(None, 50)  # None = font mặc định, 50 = size
        text_surface = font.render(text, True, RED_COLOR)  # màu chữ đỏ

        # Vị trí hiển thị (ở giữa màn hình)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Vẽ lên màn hình
        screen.blit(text_surface, text_rect)
        pygame.display.update()  
    
    def run(self, max_turns=MAX_TURN):
        
        """
        Random agent chơi game với AI
        """   
         
        # print("Start")
        
        state = GameState()
        for _ in range(max_turns):
            self.game.show_bg(self.screen)
            self.game.show_pieces(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            # Xác định agent đang đi
            agent = self.agent_red if state.current_player == RED else self.agent_black
            
            move = agent.get_move(state)

            if move is None:
                # Hết nước → bên đang đi thua
                self.winner = BLACK if state.current_player == RED else RED
                break
            # else:
            #     state = state.make_move(move)
            #     self.game.board.move_piece(self.screen,Move(Position(move[0][0], move[0][1]), Position(move[1][0], move[1][1]))) 
            #     self.game.show_bg(self.screen)
            #     self.game.show_pieces(self.screen) 
            #     self.game.board.squares[move[0][0]][move[0][1]].show_change(self.screen)
            #     self.game.board.squares[move[1][0]][move[1][1]].show_change(self.screen)
            #     pygame.display.update()
            #     pygame.time.delay(0)
            else:
                state = state.make_move(move)
                initial = Position(move[0][0], move[0][1])
                final = Position(move[1][0], move[1][1])
                self.game.show_move(self.screen,Move(initial, final))
        else:
            self.winner = 0  # Quá số nước → hoà
        self.show_winner(self.screen)

        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)  
main = Main()
main.run()