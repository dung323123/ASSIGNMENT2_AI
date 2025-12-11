import pygame
import sys
from enum import Enum

from src.ui.const import *
from src.ui.game import Game
from src.ui.move import Move, Position
from src.game.board import GameState
from src.agents.random_agent import RandomAgent
from src.agents.minimax_agent import MinimaxAgent

class UIState(Enum):
    SELECT_AI = "select_ai"
    GAME = "game"
    
class TypeAgent(Enum):
    MINMAX = "minmax"
    MACHINE = "machine"
    
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Cờ tướng')
        self.ui_state = UIState.SELECT_AI
        self.btn_minmax = pygame.Rect(150, 150, 200, 50)
        self.btn_ml = pygame.Rect(150, 220, 200, 50)
        self.selected_agent = None
        
        self.btn_start = pygame.Rect(750, 150, 120, 40)
        self.btn_stop  = pygame.Rect(750, 210, 120, 40)
        self.btn_reset = pygame.Rect(750, 270, 120, 40)
        
        self.running = False
        
        self.game = Game() 
        self.playing = True # True if playing, False if stop
        self.agent_red = None # replace this agent by another AI agent
        self.agent_black =  RandomAgent(player_symbol=BLACK)
        self.winner=None
    
    def create_agent(self, agent_type):
        if agent_type == TypeAgent.MINMAX:
            return MinimaxAgent(player_symbol=RED) 
        if agent_type == TypeAgent.MACHINE:
            return RandomAgent(player_symbol=RED)
        raise ValueError("Unknown agent type")
    
    def draw_ai_selection(self):
        self.screen.fill((30, 30, 30))

        screen_w = self.screen.get_width()

        # ====== CĂN GIỮA NÚT ======
        self.btn_minmax.centerx = screen_w // 2
        self.btn_ml.centerx = screen_w // 2

        # ====== TITLE ======
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("SELECT TYPE OF AI AGENT", True, (255,255,255))
        title_rect = title.get_rect(center=(screen_w//2, 50))
        self.screen.blit(title, title_rect)

        # ====== BUTTON BACKGROUND ======
        pygame.draw.rect(self.screen, (100,100,100), self.btn_minmax, border_radius=8)
        pygame.draw.rect(self.screen, (100,100,100), self.btn_ml, border_radius=8)

        # ====== TEXT INSIDE BUTTONS ======
        font_btn = pygame.font.SysFont(None, 32)

        # Minimax
        text_minimax = font_btn.render("Minimax", True, (255,255,255))
        rect_minimax = text_minimax.get_rect(center=self.btn_minmax.center)
        self.screen.blit(text_minimax, rect_minimax)

        # Machine Learning
        text_ml = font_btn.render("Machine Learning", True, (255,255,255))
        rect_ml = text_ml.get_rect(center=self.btn_ml.center)
        self.screen.blit(text_ml, rect_ml)


        
    def draw_game_buttons(self): 
        pass
        # pygame.draw.rect(self.screen, (0,200,0), self.btn_start)
        # pygame.draw.rect(self.screen, (200,0,0), self.btn_stop)
        # pygame.draw.rect(self.screen, (0,0,200), self.btn_reset)

        # self.screen.blit(pygame.font.SysFont(None, 32).render("START", True, (255,255,255)), (770,158))
        # self.screen.blit(pygame.font.SysFont(None, 32).render("STOP",  True, (255,255,255)), (780,218))
        # self.screen.blit(pygame.font.SysFont(None, 32).render("RESET", True, (255,255,255)), (775,278))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # -----------------------
                #  MÀN HÌNH CHỌN AI
                # -----------------------
                if self.ui_state == "select_ai":

                    if self.btn_minmax.collidepoint(mx,my):
                        self.selected_agent = TypeAgent.MINMAX
                    elif self.btn_ml.collidepoint(mx,my):
                        self.selected_agent = TypeAgent.MACHINE

                    if self.selected_agent:
                        self.agent_red = self.create_agent(self.selected_agent)
                        self.ui_state = UIState.GAME

                # -----------------------
                #  MÀN HÌNH GAME
                # -----------------------
                elif self.ui_state == "game":
                    self.running = True

                    # if self.btn_start.collidepoint(mx, my):
                    #     self.running = True

                    # elif self.btn_stop.collidepoint(mx, my):
                    #     self.running = False

                    # elif self.btn_reset.collidepoint(mx, my):
                    #     self.running = False
                    #     self.game = Game()
                    #     self.selected_red_agent = None
                    #     self.selected_black_agent = None
                    #     self.ui_state = "select_ai"




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

        clock = pygame.time.Clock()
        state = GameState()

        while True:

            # =============================
            # HANDLE EVENTS
            # =============================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    # SELECT AI SCREEN
                    if self.ui_state == UIState.SELECT_AI:

                        if self.btn_minmax.collidepoint(mx, my):
                            self.selected_agent = TypeAgent.MINMAX

                        elif self.btn_ml.collidepoint(mx, my):
                            self.selected_agent = TypeAgent.MACHINE

                        if self.selected_agent:
                            self.agent_red = self.create_agent(self.selected_agent)
                            self.running = False
                            self.winner = None
                            self.ui_state = UIState.GAME

                    # GAME SCREEN
                    elif self.ui_state == UIState.GAME:
                        self.running = True

                        # if self.btn_start.collidepoint(mx, my):
                        #     self.running = True

                        # elif self.btn_stop.collidepoint(mx, my):
                        #     self.running = False

                        # elif self.btn_reset.collidepoint(mx, my):
                        #     self.running = False
                        #     self.selected_agent = None
                        #     self.game = Game()
                        #     state = GameState()
                        #     self.winner = None
                        #     self.ui_state = UIState.SELECT_AI


            # =============================
            # RENDER SCREEN
            # =============================

            if self.ui_state == UIState.SELECT_AI:
                self.draw_ai_selection()
                pygame.display.update()
                clock.tick(60)
                continue

            # GAME SCREEN
            self.game.show_bg(self.screen)
            self.game.show_pieces(self.screen)

            # vẽ button CHỈ 1 LẦN
            self.draw_game_buttons()

            # =============================
            # AI PLAYING — 1 move/frame
            # =============================
            if self.running and self.winner is None:

                agent = self.agent_red if state.current_player == RED else self.agent_black
                move = agent.get_move(state)

                if move is None:
                    self.winner = BLACK if state.current_player == RED else RED
                    self.running = False

                else:
                    state = state.make_move(move)
                    initial = Position(move[0][0], move[0][1])
                    final = Position(move[1][0], move[1][1])
                    self.game.show_move(self.screen, Move(initial, final))

            # =============================
            # SHOW WINNER
            # =============================
            if self.winner is not None and not self.running:
                self.show_winner(self.screen)

            pygame.display.update()
            clock.tick(60)


main = Main()
main.run()