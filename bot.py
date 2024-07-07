import chess
import random
import numpy as np
b = chess.Board()
import chess
import random
import numpy as np
from collections import defaultdict
import multiprocessing

# Transposition Table
transposition_table = {}

# Piece-square tables for different stages of the game
PAWN_TABLE_BEGINNING = np.array([...])
KNIGHT_TABLE_BEGINNING = np.array([...])
BISHOP_TABLE_BEGINNING = np.array([...])
ROOK_TABLE_BEGINNING = np.array([...])
QUEEN_TABLE_BEGINNING = np.array([...])
KING_TABLE_BEGINNING = np.array([...])


# Mirror tables for black pieces
def mirror_table(table):
    return np.flip(table)


PAWN_TABLE_BEGINNING_BLACK = mirror_table(PAWN_TABLE_BEGINNING)
KNIGHT_TABLE_BEGINNING_BLACK = mirror_table(KNIGHT_TABLE_BEGINNING)
BISHOP_TABLE_BEGINNING_BLACK = mirror_table(BISHOP_TABLE_BEGINNING)
ROOK_TABLE_BEGINNING_BLACK = mirror_table(ROOK_TABLE_BEGINNING)
QUEEN_TABLE_BEGINNING_BLACK = mirror_table(QUEEN_TABLE_BEGINNING)
KING_TABLE_BEGINNING_BLACK = mirror_table(KING_TABLE_BEGINNING)


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


def quiescence_search(board, alpha, beta):
    stand_pat = evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        if board.is_capture(move) or board.gives_check(move):
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

    return alpha


def pvs(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return quiescence_search(board, alpha, beta)

    legal_moves = order_moves(board, list(board.legal_moves))
    first_move = True

    if maximizing_player:
        for move in legal_moves:
            board.push(move)
            if first_move:
                score = -pvs(board, depth - 1, -beta, -alpha, not maximizing_player)
                first_move = False
            else:
                score = -pvs(board, depth - 1, -alpha - 1, -alpha, not maximizing_player)
                if alpha < score < beta:
                    score = -pvs(board, depth - 1, -beta, -score, not maximizing_player)
            board.pop()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return alpha
    else:
        for move in legal_moves:
            board.push(move)
            if first_move:
                score = -pvs(board, depth - 1, -beta, -alpha, not maximizing_player)
                first_move = False
            else:
                score = -pvs(board, depth - 1, -alpha - 1, -alpha, not maximizing_player)
                if alpha < score < beta:
                    score = -pvs(board, depth - 1, -beta, -score, not maximizing_player)
            board.pop()
            beta = min(beta, score)
            if alpha >= beta:
                break
        return beta


def iterative_deepening(board, max_depth):
    best_move = None
    for depth in range(1, max_depth + 1):
        best_move = find_best_move(board, depth)
    return best_move


def parallel_find_best_move(board, depth):
    with multiprocessing.Pool() as pool:
        results = pool.map(parallel_search,
                           [(board.copy(), move, depth) for move in order_moves(board, list(board.legal_moves))])
    best_move = max(results, key=lambda x: x[1])[0]
    return best_move


def parallel_search(args):
    board, move, depth = args
    board.push(move)
    score = pvs(board, depth - 1, -10000, 10000, board.turn == chess.WHITE)
    return (move, score)


def find_best_move(board, depth):
    best_move = None
    best_value = -9999 if board.turn == chess.WHITE else 9999
    alpha = -10000
    beta = 10000

    legal_moves = order_moves(board, list(board.legal_moves))

    for move in legal_moves:
        board.push(move)
        board_value = pvs(board, depth - 1, alpha, beta, board.turn == chess.BLACK)
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
    best_move = parallel_find_best_move(b, depth)
    return b.san(best_move)