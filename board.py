import pygame
import copy
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from constants import SCREEN_SIZE, WHITE, GRAY, RED, LIGHT_BLUE, piece_images


class Board:
    def __init__(self, initialize=True):
        if initialize:
            self.board = [
                [Rook('black', 0, 0), Knight('black', 1, 0), Bishop('black', 2, 0), Queen('black', 3, 0),
                 King('black', 4, 0), Bishop('black', 5, 0), Knight('black', 6, 0), Rook('black', 7, 0)],
                [Pawn('black', x, 1) for x in range(8)],
                [None] * 8, [None] * 8, [None] * 8, [None] * 8,
                [Pawn('white', x, 6) for x in range(8)],
                [Rook('white', 0, 7), Knight('white', 1, 7), Bishop('white', 2, 7), Queen('white', 3, 7),
                 King('white', 4, 7), Bishop('white', 5, 7), Knight('white', 6, 7), Rook('white', 7, 7)]
            ]
        else:
            self.board = None

        self.selected_piece = None
        self.current_player = 'white'
        self.last_move = None
        self.move_history = []
        self.half_move_counter = 0

    def reset_board(self):
        self.__init__()

    def get_piece(self, x, y):
        return self.board[y][x]

    def get_piece_color(self, piece):
        return None if piece is None else piece.color

    def get_possible_moves(self, x, y):
        piece = self.get_piece(x, y)
        if not piece:
            return []

        moves = [(move_x, move_y) for move_y in range(8) for move_x in range(8)
                 if self.valid_move(x, y, move_x, move_y)]
        return moves

    def valid_move(self, from_x, from_y, to_x, to_y):
        piece = self.board[from_y][from_x]
        target_piece = self.board[to_y][to_x]
        piece_color = self.get_piece_color(piece)

        if not piece or piece_color != self.current_player:
            return False

        if target_piece and piece_color == self.get_piece_color(target_piece):
            return False

        if not piece.is_valid_move(self, from_x, from_y, to_x, to_y):
            return False

        return piece.is_valid_move(self, from_x, from_y, to_x, to_y)

    def promote_pawn(self, x, y, piece_type):
        color = self.get_piece_color(self.board[y][x])
        self.board[y][x] = Board.create_piece(self, color, piece_type, x, y)

    def create_piece(self, color, piece_type, x, y):
        piece_symbol = piece_type.upper() if color == 'white' else piece_type.lower()

        if piece_symbol == 'queen':
            return Queen(color, x, y)
        elif piece_symbol == 'rook':
            return Rook(color, x, y)
        elif piece_symbol == 'bishop':
            return Bishop(color, x, y)
        elif piece_symbol == 'knight':
            return Knight(color, x, y)

    def find_king(self, color):
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.__class__.__name__ == 'king' and piece.color == color:
                    return x, y
        return None, None

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

    def select_piece(self, x, y):
        piece = self.board[y][x]
        if not piece:
            return False

        piece_color = self.get_piece_color(piece)
        if piece_color == self.current_player:
            self.selected_piece = (x, y)
            return True
        return False

    def move_piece(self, from_x, from_y, to_x, to_y, check_validity=True):
        if check_validity and not self.valid_move(from_x, from_y, to_x, to_y):
            return False
        piece = self.board[from_y][from_x]
        self.board[to_y][to_x] = piece
        piece.x = to_x
        piece.y = to_y
        self.board[from_y][from_x] = None
        return True

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def is_square_attacked(self, x, y, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(col, row)
                if piece and piece.color != color and piece.is_valid_move(self, col, row, x, y):
                    return True
        return False

    def is_in_check(self, player_color, board=None):
        if board is None:
            board = self

        king_position = None
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color == player_color:
                    king_position = (x, y)
                    break
            if king_position:
                break

        if king_position is None:
            return False

        return self.is_square_attacked(*king_position, player_color)

    def is_checkmate(self):
        current_player_color = self.current_player

        if not self.is_in_check(current_player_color):
            return False

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None and piece.color == current_player_color:
                    valid_moves = self.get_possible_moves(x, y)
                    if any(self.valid_move(x, y, *move) for move in valid_moves):
                        return False

        return True

    def is_stalemate(self):
        if len(self.move_history) >= 8:
            if self.move_history[-1] == self.move_history[-5] and self.move_history[-3] == self.move_history[-7] and \
                    self.move_history[-2] == self.move_history[-6] and self.move_history[-4] == self.move_history[-8]:
                return True

        if self.half_move_counter >= 100:
            return True

        kings_count = 0
        pieces_count = 0
        for row in self.board:
            for piece in row:
                if isinstance(piece, King):
                    kings_count += 1
                if piece is not None:
                    pieces_count += 1
        if kings_count == 2 and pieces_count == 2:
            return True

        current_player_color = self.current_player
        current_player_in_check = self.is_in_check(current_player_color)
        has_valid_moves = False
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None and self.get_piece_color(piece) == current_player_color:
                    valid_moves = self.get_possible_moves(x, y)
                    if any(self.valid_move(x, y, *move) for move in valid_moves):
                        has_valid_moves = True
                        break
            if has_valid_moves:
                break

        if not current_player_in_check and not has_valid_moves:
            return True

        return False
