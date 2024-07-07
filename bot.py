import chess
import random
import numpy as np
b = chess.Board()
import chess
import random
import numpy as np
from collections import defaultdict
import multiprocessing

import chess
import random
import numpy as np

# Piece-square tables for different stages of the game
PAWN_TABLE_BEGINNING = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

KNIGHT_TABLE_BEGINNING = np.array([
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
])

BISHOP_TABLE_BEGINNING = np.array([
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
])

ROOK_TABLE_BEGINNING = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0, 0, 0, 0.5, 0.5, 0, 0, 0]
])

QUEEN_TABLE_BEGINNING = np.array([
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
])

KING_TABLE_BEGINNING = np.array([
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2]
])


# Mirror tables for black pieces
def mirror_table(table):
    return np.flip(table)


PAWN_TABLE_BEGINNING_BLACK = mirror_table(PAWN_TABLE_BEGINNING)
KNIGHT_TABLE_BEGINNING_BLACK = mirror_table(KNIGHT_TABLE_BEGINNING)
BISHOP_TABLE_BEGINNING_BLACK = mirror_table(BISHOP_TABLE_BEGINNING)
ROOK_TABLE_BEGINNING_BLACK = mirror_table(ROOK_TABLE_BEGINNING)
QUEEN_TABLE_BEGINNING_BLACK = mirror_table(QUEEN_TABLE_BEGINNING)
KING_TABLE_BEGINNING_BLACK = mirror_table(KING_TABLE_BEGINNING)


# Define similar tables for middle and endgame if needed

# Evaluation function incorporating heatmaps
def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -9999  # Black wins
        else:
            return 9999  # White wins
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0  # Draw

    material = 0
    positional = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = get_piece_value(piece)
            material += value
            positional += get_positional_value(piece, square)

    return material + positional


def get_piece_value(piece):
    if piece is None:
        return 0
    value = 0
    if piece.piece_type == chess.PAWN:
        value = 100
    elif piece.piece_type == chess.KNIGHT:
        value = 320
    elif piece.piece_type == chess.BISHOP:
        value = 330
    elif piece.piece_type == chess.ROOK:
        value = 500
    elif piece.piece_type == chess.QUEEN:
        value = 900
    value = value if piece.color == chess.WHITE else -value
    return value


def get_positional_value(piece, square):
    if piece.piece_type == chess.PAWN:
        table = PAWN_TABLE_BEGINNING if piece.color == chess.WHITE else PAWN_TABLE_BEGINNING_BLACK
    elif piece.piece_type == chess.KNIGHT:
        table = KNIGHT_TABLE_BEGINNING if piece.color == chess.WHITE else KNIGHT_TABLE_BEGINNING_BLACK
    elif piece.piece_type == chess.BISHOP:
        table = BISHOP_TABLE_BEGINNING if piece.color == chess.WHITE else BISHOP_TABLE_BEGINNING_BLACK
    elif piece.piece_type == chess.ROOK:
        table = ROOK_TABLE_BEGINNING if piece.color == chess.WHITE else ROOK_TABLE_BEGINNING_BLACK
    elif piece.piece_type == chess.QUEEN:
        table = QUEEN_TABLE_BEGINNING if piece.color == chess.WHITE else QUEEN_TABLE_BEGINNING_BLACK
    elif piece.piece_type == chess.KING:
        table = KING_TABLE_BEGINNING if piece.color == chess.WHITE else KING_TABLE_BEGINNING_BLACK
    return table[chess.square_rank(square)][chess.square_file(square)]


def order_moves(board, legal_moves):
    captures = []
    checks = []
    others = []

    for move in legal_moves:
        if board.is_capture(move):
            captures.append(move)
        elif board.gives_check(move):
            checks.append(move)
        else:
            others.append(move)

    captures.sort(key=lambda move: get_piece_value(board.piece_at(move.to_square)), reverse=True)

    return captures + checks + others


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = order_moves(board, list(board.legal_moves))

    if maximizing_player:
        max_eval = -9999
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 9999
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board, depth):
    best_move = None
    best_value = -9999 if board.turn == chess.WHITE else 9999
    alpha = -10000
    beta = 10000

    legal_moves = order_moves(board, list(board.legal_moves))

    for move in legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, alpha, beta, board.turn == chess.BLACK)
        board.pop()

        if board.turn == chess.WHITE:
            if board_value > best_value:
                best_value = board_value
                best_move = move
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move

    return best_move


def return_move(fen, depth=3):
    b.set_fen(fen)
    best_move = find_best_move(b, depth)
    return b.san(best_move)


# Example usage
fen = b.fen()  # Use the current position for demonstration
print(return_move(fen, depth=3))