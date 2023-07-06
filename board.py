import pygame
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from constants import SCREEN_SIZE, WHITE, GRAY, RED, LIGHT_BLUE, piece_images
from player import Player

class Board:
    def __init__(self, current_player, initialize=True):
        self.players = {
            'white': Player('white'),
            'black': Player('black')
        }
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

        self.current_player = current_player
        self.selected_piece = None
        self.last_move = None
        self.move_history = []
        self.half_move_counter = 0

    def reset_board(self):
        self.__init__()

    def possible_moves(self, x, y):
        piece = self.board[y][x]
        if not piece:
            return []

        moves = [(move_x, move_y) for move_y in range(8) for move_x in range(8)
                 if self.valid_move(x, y, move_x, move_y)]
        return moves

    def move_piece(self, from_x, from_y, to_x, to_y):
        piece = self.board[from_y][from_x]
        target_piece = self.board[to_y][to_x]

        if piece.move(self, from_x, from_y, to_x, to_y):
            self.board[to_y][to_x] = piece
            self.board[from_y][from_x] = None

            self.last_move = ((from_x, from_y), (to_x, to_y))

            if isinstance(piece, King) and abs(to_x - from_x) == 2:
                rook_from_x = 0 if to_x > from_x else 7
                rook_to_x = (from_x + to_x) // 2

                rook = self.board[rook_from_x][from_y]
                self.board[rook_to_x][from_y] = rook
                self.board[rook_from_x][from_y] = None

            if isinstance(piece, Pawn) and abs(from_y - to_y) == 1 and abs(from_x - to_x) == 1:
                if isinstance(target_piece, Pawn):
                    self.board[to_x][from_y] = None
            return True
        else:
            return False

    def pawn_to_promote(self):
        for y, row in enumerate(self.board):
            if y == 0 or y == 7:
                for x, piece in enumerate(row):
                    if isinstance(piece, Pawn):
                        return x, y
        return None, None

    def promote_pawn(self, x, y, piece_type):
        color = self.get_piece_color(self.board[y][x])
        self.board[y][x] = self.create_piece(self, color, piece_type, x, y)

    def create_piece(self, color, piece_type, x, y):
        if piece_type == 'queen':
            return Queen(color, x, y)
        elif piece_type == 'rook':
            return Rook(color, x, y)
        elif piece_type == 'bishop':
            return Bishop(color, x, y)
        elif piece_type == 'knight':
            return Knight(color, x, y)

    def draw(self, screen, selected_piece):
        square_size = SCREEN_SIZE[1] // 8

        for y, x in [(y, x) for y in range(8) for x in range(8)]:
            rect = pygame.Rect(x * square_size, y * square_size, square_size, square_size)
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
                highlight_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(highlight_surface, LIGHT_BLUE + (100,), (0, 0, square_size, square_size), 0)
                screen.blit(highlight_surface, (move_x * square_size, move_y * square_size))

        pygame.display.update()

    def draw_extra_area(self, screen):
        extra_area_width = SCREEN_SIZE[0] - SCREEN_SIZE[1]
        extra_area_height = SCREEN_SIZE[1]
        extra_area_rect = pygame.Rect(SCREEN_SIZE[1], 0, extra_area_width, extra_area_height)
        pygame.draw.rect(screen, (240, 240, 240), extra_area_rect)

    def select_piece(self, x, y):
        piece = self.board[y][x]

        if piece.color == self.current_player:
            self.selected_piece = (x, y)
            return True
        
        return False

    def square_attacked(self, x, y, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(col, row)
                if piece and piece.color != color and piece.move(self, col, row, x, y):
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

        return self.square_attacked(*king_position, player_color)

    def checkmate(self, current_player):
        if not self.is_in_check(current_player):
            return False

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None and piece.color == current_player:
                    valid_moves = self.get_possible_moves(x, y)
                    if any(self.valid_move(x, y, *move) for move in valid_moves):
                        return False

        return True

    def stalemate(self, current_player):
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

        current_player_in_check = self.is_in_check(current_player)
        has_valid_moves = False
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece is not None and self.get_piece_color(piece) == current_player:
                    valid_moves = self.get_possible_moves(x, y)
                    if any(self.valid_move(x, y, *move) for move in valid_moves):
                        has_valid_moves = True
                        break
            if has_valid_moves:
                break

        if not current_player_in_check and not has_valid_moves:
            return True

        return False
