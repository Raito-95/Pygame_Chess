import chess
import chess.engine


class Ai:
    def __init__(self):
        self.chess_board = chess.Board()

    def minimax(self, depth, alpha, beta, maximizing_player=False):
        if depth == 0 or self.chess_board.is_game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.chess_board.legal_moves:
                self.chess_board.push(move)
                eval = self.minimax(depth - 1, alpha, beta)
                self.chess_board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.chess_board.legal_moves:
                self.chess_board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.chess_board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self):
        score = 0
        for piece_type in chess.PIECE_TYPES:
            score += len(self.chess_board.pieces(piece_type, chess.WHITE)) - len(self.chess_board.pieces(piece_type, chess.BLACK))
        return score

    def get_best_move(self, depth):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in self.chess_board.legal_moves:
            self.chess_board.push(move)
            eval = self.minimax(depth - 1, alpha, beta)
            self.chess_board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
        return best_move
