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

    def show_draw_dialog(self):
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        font = pygame.font.Font(None, 36)

        text_surface = font.render("Draw!", True, (255, 255, 255))

        text_rect = text_surface.get_rect(
            center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 40))

        overlay.blit(text_surface, text_rect)

        restart_button = pygame.Rect(
            SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2, 160, 40)
        quit_button = pygame.Rect(
            SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2 + 50, 160, 40)

        pygame.draw.rect(overlay, (255, 255, 255), restart_button)
        pygame.draw.rect(overlay, (255, 255, 255), quit_button)

        restart_text = font.render("Restart", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))

        overlay.blit(restart_text, restart_text.get_rect(
            center=restart_button.center))
        overlay.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        self.screen.blit(overlay, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if restart_button.collidepoint(event.pos):
                            self.board.reset_board()
                            return
                        elif quit_button.collidepoint(event.pos):
                            self.running = False
                            return
                elif event.type == pygame.QUIT:
                    self.running = False
                    return

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

            if self.board.is_stalemate():
                self.show_draw_dialog()

        pygame.quit()
