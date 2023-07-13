import time
from AI.minimax import Ai

ai = Ai()

while True:
    best_move = ai.get_best_move(depth=6)

    if best_move is not None:
        ai.chess_board.push(best_move)

    print(ai.chess_board)

    time.sleep(1)