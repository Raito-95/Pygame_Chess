import chess
import chess.engine


class Ai:
    def __init__(self, board):
        self.board = board
        self.chess_board = chess.Board()
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None:
                    self.chess_board.set_piece_at(chess.square(col, row), piece)

    def minimax(self, depth, maximizing_player=False):
        if depth == 0 or self.chess_board.is_game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.chess_board.legal_moves:
                self.chess_board.push(move)
                eval = self.minimax(depth - 1)
                self.chess_board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.chess_board.legal_moves:
                self.chess_board.push(move)
                eval = self.minimax(depth - 1, True)
                self.chess_board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self):
        score = 0
        for piece_type in chess.PIECE_TYPES:
            score += len(self.chess_board.pieces(piece_type, chess.WHITE)) - len(self.chess_board.pieces(piece_type, chess.BLACK))
        return score

    def get_best_move(self, depth):
        best_move = None
        max_eval = float('-inf')
        for move in self.chess_board.legal_moves:
            self.chess_board.push(move)
            eval = self.minimax(depth - 1)
            self.chess_board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move
