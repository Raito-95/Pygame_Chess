# Define the evaluation function
def evaluate_board(board):
    # Count the number of pieces on each side
    white_pieces = sum(board[i].isupper() for i in range(64))
    black_pieces = sum(board[i].islower() for i in range(64))

    # Return the difference in piece count
    return white_pieces - black_pieces

# Define the Minimax algorithm


def minimax(board, depth, alpha, beta, maximizing_player):
    # Base case: maximum depth reached or game is over
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    # Recursive case: search for the best move
    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Define the AI player function


def ai_player(board, depth):
    best_move = None
    max_eval = float('-inf')
    for move in generate_moves(board):
        new_board = make_move(board, move)
        eval = minimax(new_board, depth - 1,
                       float('-inf'), float('inf'), False)
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move


# Generate possible moves for a given board position
def generate_moves(board):
    moves = []
    for i in range(64):
        if board[i].islower():
            for move in generate_piece_moves(board, i):
                moves.append((i, move))
    return moves

# Generate possible moves for a given piece on the board


def generate_piece_moves(board, i):
    piece = board[i]
    if piece == 'p':
        return generate_pawn_moves(board, i)
    elif piece == 'r':
        return generate_rook_moves(board, i)
    elif piece == 'n':
        return generate_knight_moves(board, i)
    elif piece == 'b':
        return generate_bishop_moves(board, i)
    elif piece == 'q':
        return generate_queen_moves(board, i)
    elif piece == 'k':
        return generate_king_moves(board, i)

# Generate possible moves for a pawn


def generate_pawn_moves(board, i):
    moves = []
    if board[i - 8] == '.':
        moves.append(i - 8)
        if i >= 48 and board[i - 16] == '.':
            moves.append(i - 16)
    if i % 8 != 0 and board[i - 9].isupper():
        moves.append(i - 9)
    if i % 8 != 7 and board[i - 7].isupper():
        moves.append(i - 7)
    return moves

# Generate possible moves for a rook


def generate_rook_moves(board, i):
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        x, y = i % 8, i // 8
        for j in range(1, 8):
            nx, ny = x + j * dx, y + j * dy
            if nx < 0 or nx >= 8 or ny < 0 or ny >= 8:
                break
            ni = ny * 8 + nx
            if board[ni] == '.':
                moves.append(ni)
            elif board[ni].isupper() != board[i].isupper():
                moves.append(ni)
                break
            else:
                break
    return moves

# Generate possible moves for a knight


def generate_knight_moves(board, i):
    moves = []
    directions = [(1, 2), (2, 1), (-1, 2), (-2, 1),
                  (1, -2), (2, -1), (-1, -2), (-2, -1)]
    x, y = i % 8, i // 8
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= 8 or ny < 0 or ny >= 8:
            continue
        ni = ny * 8 + nx
        if board[ni] == '.' or board[ni].isupper() != board[i].isupper():
            moves.append(ni)
    return moves

# Generate possible moves for a bishop


def generate_bishop_moves(board, i):
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    x, y = i % 8, i // 8
    for dx, dy in directions:
        for j in range(1, 8):
            nx, ny = x + j * dx, y + j * dy
            if nx < 0 or nx >= 8 or ny < 0 or ny >= 8:
                break
            ni = ny * 8 + nx
            if board[ni] == '.':
                moves.append(ni)
            elif board[ni].isupper() != board[i].isupper():
                moves.append(ni)
                break
            else:
                break
    return moves

# Generate possible moves for a queen


def generate_queen_moves(board, i):
    return generate_rook_moves(board, i) + generate_bishop_moves(board, i)

# Generate possible moves for a king


def generate_king_moves(board, i):
    moves = []
    directions = [(1, 1), (1, 0), (0, 1), (-1, -1),
                  (-1, 0), (0, -1), (1, -1), (-1, 1)]
    x, y = i % 8, i // 8
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= 8 or ny < 0 or ny >= 8:
            continue
        ni = ny * 8 + nx
        if board[ni] == '.' or board[ni].isupper() != board[i].isupper():
            moves.append(ni)
    return moves
