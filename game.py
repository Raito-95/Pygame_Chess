import pygame
import pygame.mixer as mixer
from board import Board
from constants import SCREEN_SIZE
from piece import Pawn

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.selected_piece = None
        self.current_player = 'white'
        self.running = True
        self.board = Board()
        self.fonts = {}
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(None, size)
        return self.fonts[size]

    def draw_button(self, overlay, rect, text, text_color, bg_color):
        pygame.draw.rect(overlay, bg_color, rect)
        label = self.render_text(text, 36, text_color)
        overlay.blit(label, label.get_rect(center=rect.center))

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
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return
        piece = self.board.board[y][x]
        if piece and not self.selected_piece and self.board.get_piece_color(piece) == self.current_player:
            self.selected_piece = (x, y)
        elif self.selected_piece:
            if (x, y) == self.selected_piece:
                self.selected_piece = None
            else:
                if self.board.valid_move(self.selected_piece[0], self.selected_piece[1], x, y):
                    self.board.move_piece(self.selected_piece[0], self.selected_piece[1], x, y)
                    self.board.switch_player()
                    self.current_player = 'black' if self.current_player == 'white' else 'white'
                else:
                    if piece and self.board.get_piece_color(piece) == self.current_player:
                        self.selected_piece = (x, y)


    def render_text(self, text, size, color):
        # Get the appropriate font for the given size
        font = self.get_font(size)
        text_surface = font.render(text, True, color)
        return text_surface

    def show_dialog(self, message, options):
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        text_surface = self.render_text(message, 36, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 40))
        overlay.blit(text_surface, text_rect)

        button_colors = (255, 255, 255)
        for idx, (label, action) in enumerate(options):
            button_rect = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2 + 50 * idx, 160, 40)
            self.draw_button(overlay, button_rect, label, (0, 0, 0), button_colors)
            action['rect'] = button_rect

        self.screen.blit(overlay, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for option in options:
                            if option['rect'].collidepoint(event.pos):
                                return option['action']
                elif event.type == pygame.QUIT:
                    self.running = False
                    return None

    def show_promotion_dialog(self, x, y):
        self.overlay.fill((0, 0, 0, 128))

        options = [
            {"label": "Rook", "action": "rook"},
            {"label": "Knight", "action": "knight"},
            {"label": "Bishop", "action": "bishop"},
            {"label": "Queen", "action": "queen"},
        ]

        spacing = 50
        start_x = SCREEN_SIZE[1] + (SCREEN_SIZE[0] - SCREEN_SIZE[1]) // 2 - 80
        start_y = 100

        for idx, option in enumerate(options):
            button_rect = pygame.Rect(start_x, start_y + spacing * idx, 160, 40)
            self.draw_button(self.overlay, button_rect, option['label'], (0, 0, 0), (255, 255, 255))
            option['rect'] = button_rect

        self.screen.blit(self.overlay, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for option in options:
                            if option['rect'].collidepoint(*event.pos):
                                self.board.promote_pawn(x, y, option['action'])
                                return
                elif event.type == pygame.QUIT:
                    self.running = False
                    return
    def end_game(self, message):
        options = [
            {"label": "Restart", "action": "restart"},
            {"label": "Quit", "action": "quit"},
        ]

        action = self.show_dialog(message, options)
        if action == 'restart':
            self.board.reset_board()
            self.current_player = 'white'
        elif action == 'quit':
            self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)

            if self.board.is_stalemate():
                options = [
                    {"label": "Restart", "action": "restart"},
                    {"label": "Quit", "action": "quit"},
                ]
                self.show_dialog("Draw!", options)
            elif self.board.is_checkmate():
                options = [
                    {"label": "Restart", "action": "restart"},
                    {"label": "Quit", "action": "quit"},
                ]
                if self.current_player == 'white':
                    self.show_dialog("Black Wins!", options)
                else:
                    self.show_dialog("White Wins!", options)

            for y in range(8):
                for x in range(8):
                    piece = self.board.board[y][x]
                    if isinstance(piece, Pawn) and ((self.board.get_piece_color(piece) == 'white' and y == 0) or
                                                    (self.board.get_piece_color(piece) == 'black' and y == 7)):
                        self.show_promotion_dialog(x, y)

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)  # limits the frame rate to 30 FPS

        pygame.quit()
