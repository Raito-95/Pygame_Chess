class Piece():
    def __init__(self, color, piece_type, x, y):
        self.color = color
        self.piece_type = piece_type
        self.x = x
        self.y = y

    def move(self, to_x, to_y):
        self.x = to_x
        self.y = to_y


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'pawn', x, y)

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        piece = board.get_piece(from_x, from_y)
        target_piece = board.get_piece(to_x, to_y)
        piece_color = piece.color
        direction = -1 if piece_color == 'white' else 1

        if from_x == to_x:
            if target_piece is None:
                if from_y + direction == to_y:
                    return True
                if from_y in {1, 6} and from_y + 2 * direction == to_y and board.get_piece(from_x, from_y + direction) is None:
                    return True
        elif abs(from_x - to_x) == 1 and from_y + direction == to_y:
            if target_piece is not None and target_piece.color != piece_color:
                return True
        elif board.last_move and isinstance(board.get_piece(*board.last_move[1]), Pawn):
            last_moved_piece_start_y = 1 if piece_color == 'white' else 6
            if abs(from_x - to_x) == 1 and from_y + direction == to_y and \
               board.last_move[0][1] == last_moved_piece_start_y and board.last_move[1][1] == last_moved_piece_start_y + 2 * direction and board.last_move[1][0] == to_x:
                return True

        return False
    
    def en_passant_capture(self, board, from_x, from_y, to_x, to_y):
        piece_color = self.color
        direction = -1 if piece_color == 'white' else 1
        captured_pawn_x = to_x
        captured_pawn_y = from_y

        captured_pawn = board.get_piece(captured_pawn_x, captured_pawn_y)
        if captured_pawn is not None and captured_pawn.color != piece_color and isinstance(captured_pawn, Pawn):
            board.board[captured_pawn_y][captured_pawn_x] = None



class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'rook', x, y)
        self.has_moved = False

    def move(self, to_x, to_y):
        super().move(to_x, to_y)
        self.has_moved = True

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        piece = board.get_piece(from_x, from_y)
        target_piece = board.get_piece(to_x, to_y)

        if from_x == to_x and from_y != to_y:
            direction_y = 1 if to_y > from_y else -1
            for y in range(from_y + direction_y, to_y, direction_y):
                if board.get_piece(from_x, y) is not None:
                    return False
            return target_piece is None or target_piece.color != piece.color
        elif from_y == to_y and from_x != to_x:
            direction_x = 1 if to_x > from_x else -1
            for x in range(from_x + direction_x, to_x, direction_x):
                if board.get_piece(x, from_y) is not None:
                    return False
            return target_piece is None or target_piece.color != piece.color
        else:
            return False


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'knight', x, y)

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        piece = board.get_piece(from_x, from_y)
        target_piece = board.get_piece(to_x, to_y)

        dx, dy = abs(from_x - to_x), abs(from_y - to_y)
        if dx == 2 and dy == 1 or dx == 1 and dy == 2:
            if target_piece is None or target_piece.color != piece.color:
                return True
        return False


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'bishop', x, y)

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        piece = board.get_piece(from_x, from_y)
        target_piece = board.get_piece(to_x, to_y)

        if from_x == to_x or from_y == to_y:
            return False

        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)

        if dx != dy:
            return False

        direction_x = int((to_x - from_x) / dx)
        direction_y = int((to_y - from_y) / dy)

        current_x, current_y = from_x + direction_x, from_y + direction_y

        while current_x != to_x or current_y != to_y:
            if board.get_piece(current_x, current_y) is not None:
                return False
            current_x += direction_x
            current_y += direction_y

        return target_piece is None or target_piece.color != piece.color


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'queen', x, y)

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        if from_x == to_x or from_y == to_y:
            return Rook.is_valid_move(self, board, from_x, from_y, to_x, to_y)
        elif abs(from_x - to_x) == abs(from_y - to_y):
            return Bishop.is_valid_move(self, board, from_x, from_y, to_x, to_y)
        else:
            return False


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'king', x, y)
        self.has_moved = False

    def move(self, to_x, to_y):
        super().move(to_x, to_y)
        self.has_moved = True

    def is_valid_move(self, board, from_x, from_y, to_x, to_y):
        piece = board.get_piece(from_x, from_y)
        target_piece = board.get_piece(to_x, to_y)

        # Check if the move is within one square and is not attacking a square under attack by opponent
        if abs(from_x - to_x) <= 1 and abs(from_y - to_y) <= 1:
            if target_piece is None or target_piece.color != piece.color:
                if not board.is_square_attacked(to_x, to_y, piece.color):
                    return True

        # Check if the move is a valid castling move
        if self.is_valid_castling(board, from_x, from_y, to_x, to_y):
            return True

        return False

    def is_valid_castling(self, board, from_x, from_y, to_x, to_y):
        # Check if the piece is a king and hasn't moved before
        piece = board.get_piece(from_x, from_y)
        if not isinstance(piece, King) or piece.has_moved:
            return False

        # Check if the king is moving two squares horizontally and not vertically
        if abs(from_x - to_x) != 2 or from_y != to_y:
            return False

        # Check if the rook is in the correct position and hasn't moved before
        if from_x < to_x:
            rook_x = 7
            step = 1
        else:
            rook_x = 0
            step = -1
        rook = board.get_piece(rook_x, from_y)
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Check if there are no pieces between the king and the rook, and no squares are attacked by the opponent's pieces
        for x in range(from_x + step, rook_x, step):
            if board.get_piece(x, from_y) is not None or board.is_square_attacked(x, from_y, piece.color):
                return False

        # Check if the king or the squares it passes through or lands on are attacked by the opponent's pieces
        if board.is_square_attacked(from_x, from_y, piece.color) or board.is_square_attacked(to_x, to_y, piece.color):
            return False

        # If all checks pass, return True
        return True
