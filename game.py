import pygame
import pygame.mixer as mixer
from board import Board
from constants import SCREEN_SIZE, BUTTON_WIDTH_RATIO, BUTTON_HEIGHT_RATIO, GRAY
from dialog import Dialog
from player import Player


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        self.running = True
        self.players = [Player('white'), Player('black')]
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.board = Board(self.current_player)
        self.dialog = Dialog(self.screen)

        self.square_size = SCREEN_SIZE[1] // 8
        self.button_width = SCREEN_SIZE[0] * BUTTON_WIDTH_RATIO
        self.button_height = SCREEN_SIZE[1] * BUTTON_HEIGHT_RATIO
        self.button_x = SCREEN_SIZE[1] + ((SCREEN_SIZE[0] - SCREEN_SIZE[1]) // 2) - (self.button_width // 2)
        self.button_y = SCREEN_SIZE[1] * BUTTON_HEIGHT_RATIO * 7
        self.button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)

    def screen_to_board_coords(self, screen_x, screen_y):
        return screen_x // self.square_size, screen_y // self.square_size

    def draw_board(self):
        self.board.draw(self.screen)
        self.board.draw_extra_area(self.screen)
        
        pygame.draw.rect(self.screen, GRAY, self.button_rect)

    def handle_click(self, pos):
        x, y = self.screen_to_board_coords(*pos)
        if not (0 <= x < 8) or not (0 <= y < 8):
            return
        piece = self.board[y][x]
        if self.board.selected_piece is None:
            if piece.color == self.current_player:
                self.board.select_piece(x, y)
        elif (x, y) == self.board.selected_piece:
            self.board.selected_piece = None
        else:
            if piece.color == self.current_player:
                self.board.selected_piece = None
                self.board.select_piece(x, y)
            else:
                self.board.move_piece(self.board.selected_piece[0], self.board.selected_piece[1], x, y)
                self.current_player_index = 1 - self.current_player_index

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            if self.board.stalemate(self.current_player):
                self.dialog.show_message("Draw!")
            elif self.board.checkmate(self.current_player):
                if self.current_player.color == 'white':
                    self.dialog.show_message("Black Wins!")
                else:
                    self.dialog.show_message("White Wins!")

            pawn_to_promote = self.board.pawn_to_promote()
            if pawn_to_promote:
                x, y = pawn_to_promote
                self.dialog.show_promotion(x, y, self.board)

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def change_music(self, music_file):
        mixer.music.stop()
        mixer.music.load(music_file)
        mixer.music.play(-1)
