import chess
import random
board = chess.Board()

def return_move(fen):
    board.set_fen(fen)

    #print(b., "hello")
    return board.san(random.choice(list(board.legal_moves)))