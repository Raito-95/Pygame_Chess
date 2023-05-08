import pygame
import pygame.mixer as mixer
from board import Board
from constants import SCREEN_SIZE
from dialog import Dialog
from player import Player


class Game:
    def __init__(self, screen):
        # Pygame-related attributes
        self.screen = screen
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        # Game state attributes
        self.running = True
        self.players = [Player('white'), Player('black')]
        self.current_player_index = 0

        # Game objects and data structures
        self.board = Board()
        self.dialog = Dialog(self.screen)  # Initialize the dialog object

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    # Utility Functions
    def screen_to_board_coords(self, screen_x, screen_y):
        square_size = SCREEN_SIZE[1] // 8
        return screen_x // square_size, screen_y // square_size

    # Drawing Functions
    def draw_board(self):
        self.board.draw(self.screen)
        self.board.draw_extra_area(self.screen)

    # Handling Input
    def handle_click(self, pos):
        x, y = self.screen_to_board_coords(*pos)
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return
        piece = self.board.board[y][x]
        if piece and not self.board.selected_piece and self.board.get_piece_color(piece) == self.current_player.color:
            self.board.select_piece(x, y)
        elif self.board.selected_piece:
            if (x, y) == self.board.selected_piece:
                self.board.selected_piece = None
            else:
                if self.board.valid_move(self.board.selected_piece[0], self.board.selected_piece[1], x, y):
                    self.board.move_piece(self.board.selected_piece[0], self.board.selected_piece[1], x, y)
                    self.board.switch_player()
                    self.current_player_index = 1 - self.current_player_index
                else:
                    if piece and self.board.get_piece_color(piece) == self.current_player.color:
                        self.board.select_piece(x, y)

    # Game Loop Functions
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            if self.board.is_stalemate():
                self.dialog.show_message("Draw!")
            elif self.board.is_checkmate():
                if self.current_player.color == 'white':
                    self.dialog.show_message("Black Wins!")
                else:
                    self.dialog.show_message("White Wins!")

            pawn_to_promote = self.board.get_pawn_to_promote()
            if pawn_to_promote:
                x, y = pawn_to_promote
                self.dialog.show_promotion_dialog(x, y, self.board)

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def change_music(self, music_file):
        mixer.music.stop()
        mixer.music.load(music_file)
        mixer.music.play(-1)
