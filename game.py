import pygame
from pygame import mixer
from board import Board
from constants import SCREEN_SIZE, FONTS_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT
from dialog import Dialog
from player import Player
from AI.test import Ai


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        self.running = True
        self.players = [Player('white'), Player('black')]
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index].color

        self.board = Board(self.current_player)
        self.ai = Ai(self.board)
        self.dialog = Dialog(self.screen)

        self.square_size = SCREEN_SIZE[1] // 8
        self.button_font = pygame.font.SysFont("Script MT Bold", FONTS_SIZE)
        self.button_text = "Proposal"
        self.button_x = SCREEN_SIZE[0] - BUTTON_WIDTH
        self.button_y = SCREEN_SIZE[1] - BUTTON_HEIGHT
        self.button_rect = pygame.Rect(self.button_x, self.button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def screen_to_board_coords(self, screen_x, screen_y):
        return screen_x // self.square_size, screen_y // self.square_size
    
    def draw_board(self):
        self.board.draw(self.screen)
        self.board.draw_extra_area(self.screen)
        self.dialog.draw_button(self.button_rect, self.button_text)

    def handle_click(self, pos):
        x, y = self.screen_to_board_coords(*pos)
        if self.button_rect.collidepoint(x, y):
            if self.dialog.show_proposal():
                self.dialog.show_message("Draw!")
                self.board.reset_board()

        if not (0 <= x < 8) or not (0 <= y < 8):
            return
        piece = self.board.get_piece(x, y)
        
        if self.board.selected_piece is None:
            if piece is not None and piece.color == self.current_player:
                self.board.select_piece(x, y)
        elif (x, y) == self.board.selected_piece:
            self.board.selected_piece = None
        else:
            if piece is not None and piece.color == self.current_player:
                self.board.selected_piece = None
                self.board.select_piece(x, y)
            else:
                if self.board.move_piece(self.board.selected_piece[0], self.board.selected_piece[1], x, y):
                    self.current_player_index = 1 - self.current_player_index
                    self.current_player = self.players[self.current_player_index].color
                    self.board.current_player = self.current_player
                    self.board.selected_piece = None

                    if self.board.stalemate():
                        self.dialog.show_message("Draw!")
                    elif self.board.checkmate():
                        if self.current_player == 'white':
                            self.dialog.show_message("Black Wins!")
                        else:
                            self.dialog.show_message("White Wins!")
                    elif self.board.is_king_captured(self.current_player):
                        if self.current_player == 'white':
                            self.dialog.show_message("Black Wins!")
                        else:
                            self.dialog.show_message("White Wins!")

                    pawn_to_promote = self.board.pawn_to_promote()
                    if pawn_to_promote[0] is not None and pawn_to_promote[1] is not None:
                        x, y = pawn_to_promote
                        self.dialog.show_promotion(x, y, self.board)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            self.draw_board()
            best_move = self.ai.get_best_move(depth=3)
            print(f'best_move: {best_move}')
            
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def change_music(self, music_file):
        mixer.music.stop()
        mixer.music.load(music_file)
        mixer.music.play(-1)
