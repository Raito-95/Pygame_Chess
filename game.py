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
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            # Click is outside the board, do nothing
            return
        piece = self.board.board[y][x]
        if piece and not self.selected_piece and self.board.get_piece_color(piece) == self.current_player:
            self.selected_piece = (x, y)
        elif self.selected_piece:
            if (x, y) == self.selected_piece:
                self.selected_piece = None
            else:
                if self.board.valid_move(self.selected_piece[0], self.selected_piece[1], x, y):
                    if self.board.get_piece(x, y) == 'pawn' and ((self.board.get_piece_color(x, y) == 'white' and y == 0) or (self.board.get_piece_color(x, y) == 'black' and y == 7)):
                        self.show_promotion_dialog(x, y)
                    else:
                        self.board.move_piece(self.selected_piece[0], self.selected_piece[1], x, y)
                        self.selected_piece = None
                        self.current_player = 'black' if self.current_player == 'white' else 'white'
                else:
                    if piece and self.board.get_piece_color(piece) == self.current_player:
                        self.selected_piece = (x, y)

    def render_text(self, text, size, color):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        return text_surface

    def show_dialog(self, message):
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        text_surface = self.render_text(message, 36, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 40))

        overlay.blit(text_surface, text_rect)

        restart_button = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2, 160, 40)
        quit_button = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2 + 50, 160, 40)

        pygame.draw.rect(overlay, (255, 255, 255), restart_button)
        pygame.draw.rect(overlay, (255, 255, 255), quit_button)

        restart_text = self.render_text("Restart", 36, (0, 0, 0))
        quit_text = self.render_text("Quit", 36, (0, 0, 0))

        overlay.blit(restart_text, restart_text.get_rect(center=restart_button.center))
        overlay.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        self.screen.blit(overlay, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if restart_button.collidepoint(event.pos):
                            self.board.reset_board()
                            return True
                        elif quit_button.collidepoint(event.pos):
                            self.running = False
                            return False
                elif event.type == pygame.QUIT:
                    self.running = False
                    return False

    def end_game(self, message):
        restart = self.show_dialog(message)
        if restart:
            self.board.reset_board()
            self.current_player = 'white'

    def show_promotion_dialog(self, x, y):
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        font = pygame.font.Font(None, 36)

        text_surface = font.render("Promote pawn to:", True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 80))

        overlay.blit(text_surface, text_rect)

        queen_button = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2, 160, 40)
        rook_button = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2 + 50, 160, 40)
        bishop_button = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2 + 100, 160, 40)
        knight_button = pygame.Rect(SCREEN_SIZE[0] // 2 - 80, SCREEN_SIZE[1] // 2 + 150, 160, 40)

        pygame.draw.rect(overlay, (255, 255, 255), queen_button)
        pygame.draw.rect(overlay, (255, 255, 255), rook_button)
        pygame.draw.rect(overlay, (255, 255, 255), bishop_button)
        pygame.draw.rect(overlay, (255, 255, 255), knight_button)

        queen_text = font.render("Queen", True, (0, 0, 0))
        rook_text = font.render("Rook", True, (0, 0, 0))
        bishop_text = font.render("Bishop", True, (0, 0, 0))
        knight_text = font.render("Knight", True, (0, 0, 0))

        overlay.blit(queen_text, queen_text.get_rect(center=queen_button.center))
        overlay.blit(rook_text, rook_text.get_rect(center=rook_button.center))
        overlay.blit(bishop_text, bishop_text.get_rect(center=bishop_button.center))
        overlay.blit(knight_text, knight_text.get_rect(center=knight_button.center))

        self.screen.blit(overlay, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if queen_button.collidepoint(event.pos):
                            self.board.promote_pawn(x, y, 'queen')
                            return
                        elif rook_button.collidepoint(event.pos):
                            self.board.promote_pawn(x, y, 'rook')
                            return
                        elif bishop_button.collidepoint(event.pos):
                            self.board.promote_pawn(x, y, 'bishop')
                            return
                        elif knight_button.collidepoint(event.pos):
                            self.board.promote_pawn(x, y, 'knight')
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

            # if self.board.is_stalemate():
            #     self.show_dialog("Draw!")
            # elif self.board.is_checkmate():
            #     if self.current_player == 'white':
            #         self.show_dialog("Black Wins!")
            #     else:
            #         self.show_dialog("White Wins!")

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
