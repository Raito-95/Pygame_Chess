import pygame
import pygame.mixer as mixer
from board import Board
from constants import SCREEN_SIZE


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.selected_piece = None
        self.current_player = 'white'
        self.running = True

    def change_music(self, music_file):
        mixer.music.stop()
        mixer.music.load(music_file)
        mixer.music.play(-1)

    def draw_board(self):
        self.board.draw(self.screen, self.selected_piece)
        self.board.draw_extra_area(self.screen)

    def screen_to_board_coords(self, screen_x, screen_y):
        square_size = SCREEN_SIZE[1] // 8
        return screen_x // square_size, screen_y // square_size

    def handle_click(self, pos):
        x, y = self.screen_to_board_coords(*pos)
        piece = self.board.board[y][x]
        if piece and not self.selected_piece and self.board.get_piece_color(piece) == self.current_player:
            self.selected_piece = (x, y)
        elif self.selected_piece:
            from_x, from_y = self.selected_piece

            if (x, y) == (from_x, from_y):
                self.selected_piece = None
            else:
                if self.board.valid_move(from_x, from_y, x, y):
                    self.board.move_piece(from_x, from_y, x, y)
                    self.current_player = 'black' if self.current_player == 'white' else 'white'
                else:
                    if piece and self.board.get_piece_color(piece) == self.current_player:
                        self.selected_piece = (x, y)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
