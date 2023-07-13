class Piece():
    def __init__(self, color, piece_type, x, y):
        self.color = color
        self.piece_type = piece_type
        self.x = x
        self.y = y

    def move(self):
        pass

    def moved(self):
        pass


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'pawn', x, y)

    def move(self, board, from_x, from_y, to_x, to_y):
        target_piece = board.get_piece(to_x, to_y)
        direction = -1 if self.color == 'white' else 1
        last_move = board.last_move

        if from_x == to_x:
            if target_piece is None:
                if to_y - from_y == direction:
                    return True
                if from_y in {1, 6} and to_y - from_y == 2 * direction and board.get_piece(from_x, from_y + direction) is None:
                    return True
        elif abs(from_x - to_x) == 1 and to_y - from_y == direction:
            if target_piece is not None and target_piece.color != self.color:
                return True

        if last_move is not None:
            last_piece = board.get_piece(last_move[1][0], last_move[1][1])
            if isinstance(last_piece, Pawn) and last_piece.color != self.color:
                last_moved_piece_start_y = 6 if last_piece.color == 'white' else 1
                if (
                    abs(from_x - last_move[1][0]) == 1
                    and last_move[0][1] == last_moved_piece_start_y
                    and last_move[1][1] == last_moved_piece_start_y + 2 * direction
                    and to_x == last_move[1][0]
                    and to_y == last_moved_piece_start_y
                ):
                    return True

        return False


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'rook', x, y)
        self.has_moved = False

    def moved(self):
        super().moved()
        self.has_moved = True

    def move(self, board, from_x, from_y, to_x, to_y):
        target_piece = board.get_piece(to_x, to_y)

        if from_x == to_x and from_y != to_y:
            direction_y = 1 if to_y > from_y else -1
            if any(board.get_piece(from_x, y) is not None for y in range(from_y + direction_y, to_y, direction_y)):
                return False
            self.moved()
            return target_piece is None or target_piece.color != self.color

        if from_y == to_y and from_x != to_x:
            direction_x = 1 if to_x > from_x else -1
            if any(board.get_piece(x, from_y) is not None for x in range(from_x + direction_x, to_x, direction_x)):
                return False
            self.moved()
            return target_piece is None or target_piece.color != self.color

        return False


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'knight', x, y)

    def move(self, board, from_x, from_y, to_x, to_y):
        target_piece = board.get_piece(to_x, to_y)

        dx, dy = abs(from_x - to_x), abs(from_y - to_y)
        if dx == 2 and dy == 1 or dx == 1 and dy == 2:
            if target_piece is None or target_piece.color != self.color:
                return True
        return False


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'bishop', x, y)

    def move(self, board, from_x, from_y, to_x, to_y):
        target_piece = board.get_piece(to_x, to_y)

        if from_x == to_x or from_y == to_y:
            return False

        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)

        if dx != dy:
            return False

        direction_x = 1 if to_x > from_x else -1
        direction_y = 1 if to_y > from_y else -1

        current_x, current_y = from_x + direction_x, from_y + direction_y

        while current_x != to_x or current_y != to_y:
            if board.get_piece(current_x, current_y) is not None:
                return False
            current_x += direction_x
            current_y += direction_y

        return target_piece is None or target_piece.color != self.color


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'queen', x, y)

    def move(self, board, from_x, from_y, to_x, to_y):
        if from_x == to_x or from_y == to_y:
            return Rook(self.color, from_x, from_y).move(board, from_x, from_y, to_x, to_y)
        elif abs(from_x - to_x) == abs(from_y - to_y):
            return Bishop(self.color, from_x, from_y).move(board, from_x, from_y, to_x, to_y)
        return False


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, 'king', x, y)
        self.has_moved = False

    def moved(self):
        super().moved()
        self.has_moved = True

    def move(self, board, from_x, from_y, to_x, to_y):
        target_piece = board.get_piece(to_x, to_y)

        dx = abs(from_x - to_x)
        dy = abs(from_y - to_y)

        if dx <= 1 and dy <= 1 and (target_piece is None or target_piece.color != self.color) and not board.square_attacked(to_x, to_y):
            self.moved()
            return True

        if self.castling(board, from_x, from_y, to_x, to_y):
            return True

        return False

    def castling(self, board, from_x, from_y, to_x, to_y):
        piece = board.get_piece(to_x, to_y)
        if not isinstance(piece, King) or piece.has_moved:
            return False

        if abs(from_x - to_x) != 2 or from_y != to_y:
            return False

        if from_x < to_x:
            rook_x = 7
            step = 1
        else:
            rook_x = 0
            step = -1
        rook = board.get_piece(rook_x, from_y)
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        for x in range(from_x + step, rook_x, step):
            if board.get_piece(x, from_y) is not None or board.square_attacked(x, from_y):
                return False

        if board.square_attacked(from_x, from_y) or board.square_attacked(to_x, to_y):
            return False

        return True
