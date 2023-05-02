import pygame
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from constants import SCREEN_SIZE, WHITE, GRAY, RED, LIGHT_BLUE, piece_images


class Board:
    def __init__(self):
        self.board = [[Rook('black', 0, 0), Knight('black', 1, 0), Bishop('black', 2, 0), Queen('black', 3, 0),
                       King('black', 4, 0), Bishop('black', 5, 0), Knight('black', 6, 0), Rook('black', 7, 0)],
                      [Pawn('black', x, 1) for x in range(8)],
                      [None] * 8, [None] * 8, [None] * 8, [None] * 8,
                      [Pawn('white', x, 6) for x in range(8)],
                      [Rook('white', 0, 7), Knight('white', 1, 7), Bishop('white', 2, 7), Queen('white', 3, 7),
                       King('white', 4, 7), Bishop('white', 5, 7), Knight('white', 6, 7), Rook('white', 7, 7)]]
        self.selected_piece = None
        self.current_player = 'white'
        self.last_move = None

    def get_piece(self, x, y):
        return self.board[y][x]

    def get_piece_color(self, piece):
        return None if piece is None else piece.color

    def is_square_attacked(self, board, x, y, color):
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color != color and piece.is_valid_move(board, row, col, x, y):
                    return True
        return False

    def get_possible_moves(self, x, y):
        piece = self.get_piece(x, y)
        if not piece:
            return []

        moves = [(move_x, move_y) for move_y in range(8) for move_x in range(8)
                 if self.valid_move(x, y, move_x, move_y)]
        return moves

    def draw(self, screen, selected_piece):
        square_size = SCREEN_SIZE[1] // 8

        for y, x in [(y, x) for y in range(8) for x in range(8)]:
            rect = pygame.Rect(x * square_size, y *
                               square_size, square_size, square_size)
            pygame.draw.rect(screen, WHITE if (x + y) % 2 == 0 else GRAY, rect)

            piece = self.board[y][x]
            if piece:
                piece_image = piece_images[f"{piece.color}_{piece.piece_type}"]
                piece_rect = piece_image.get_rect()
                piece_rect.center = rect.center
                screen.blit(piece_image, piece_rect)

                if selected_piece and selected_piece == (x, y):
                    pygame.draw.rect(screen, RED, rect, 4)

        if selected_piece:
            possible_moves = self.get_possible_moves(*selected_piece)
            for move_x, move_y in possible_moves:
                highlight_surface = pygame.Surface(
                    (square_size, square_size), pygame.SRCALPHA)
                highlight_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(highlight_surface, LIGHT_BLUE +
                                 (100,), (0, 0, square_size, square_size), 0)
                screen.blit(highlight_surface, (move_x *
                            square_size, move_y * square_size))

        pygame.display.update()

    def draw_extra_area(self, screen):
        extra_area_width = SCREEN_SIZE[0] - SCREEN_SIZE[1]
        extra_area_height = SCREEN_SIZE[1]
        extra_area_rect = pygame.Rect(
            SCREEN_SIZE[1], 0, extra_area_width, extra_area_height)
        pygame.draw.rect(screen, (200, 200, 200), extra_area_rect)

    def valid_move(self, from_x, from_y, to_x, to_y):
        piece = self.board[from_y][from_x]
        target_piece = self.board[to_y][to_x]
        piece_color = self.get_piece_color(piece)

        if not piece or piece_color != self.current_player:
            return False

        if target_piece and piece_color == self.get_piece_color(target_piece):
            return False

        return piece.is_valid_move(self, from_x, from_y, to_x, to_y)

    def select_piece(self, x, y):
        piece = self.board[y][x]
        if not piece:
            return False

        piece_color = self.get_piece_color(piece)
        if piece_color == self.current_player:
            self.selected_piece = (x, y)
            return True
        return False

    def move_piece(self, from_x, from_y, to_x, to_y):
        if self.valid_move(from_x, from_y, to_x, to_y):
            self.board[to_y][to_x] = self.board[from_y][from_x]
            self.board[from_y][from_x] = None
            self.last_move = ((from_x, from_y), (to_x, to_y))
            self.selected_piece = None
            self.switch_player()

            return True
        return False

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def is_checkmate(self):
        current_player_color = self.current_player
        king_position = None

        for y, x in [(y, x) for y in range(8) for x in range(8)]:
            piece = self.get_piece(x, y)
            if isinstance(piece, King) and piece.color == current_player_color:
                king_position = (x, y)
                break

        if not king_position:
            return False

        king_moves = self.get_possible_moves(*king_position)
        if any(not self.is_in_check(*move) for move in king_moves):
            return False

        for y, x in [(y, x) for y in range(8) for x in range(8)]:
            piece = self.get_piece(x, y)
            if piece and piece.color == current_player_color:
                possible_moves = self.get_possible_moves(x, y)
                if any(self.valid_move(x, y, *move) and not self.is_in_check_after_move(x, y, *move)
                       for move in possible_moves):
                    return False

        return True

    def is_in_check(self, x, y, board=None):
        if board is None:
            board = self
        current_player_color = self.current_player
        return self.is_square_attacked(board, x, y, current_player_color)

    def is_in_check_after_move(self, from_x, from_y, to_x, to_y):
        temp_board = [[piece for piece in row] for row in self.board]
        temp_board[to_y][to_x] = temp_board[from_y][from_x]
        temp_board[from_y][from_x] = None

        moved_piece = temp_board[to_y][to_x]
        if isinstance(moved_piece, King):
            return self.is_in_check(to_x, to_y, board=temp_board)

        current_player_color = self.current_player
        king_position = None

        for y, x in [(y, x) for y in range(8) for x in range(8)]:
            piece = temp_board[y][x]
            if isinstance(piece, King) and piece.color == current_player_color:
                king_position = (x, y)
                break

        return self.is_in_check(*king_position, board=temp_board)
