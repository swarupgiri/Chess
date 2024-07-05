import chess
import math
import time
board = chess.Board()

#board.push_san("e5")
print(board)
import pygame

CELL = 78 # DEFAULT => 80 [only works with factors of >80]
WIDTH = HEIGHT = 9 * CELL
BORDER = CELL / (1440 * (CELL / 80))
FLIPPED = False
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
is_selected = [False, "", ""]


def find_positions(board, piece):
    positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == piece:
                positions.append((i, j, piece))
    return positions



        #print(i, j)
        #print(index, end="")
    #print("\n")
    #pygame.draw.rect(screen, "#d4770f", ((i * 80) + (BORDER * WIDTH * i), (j * 80) + (BORDER * HEIGHT * j), 80, 80))
def find_keys_by_value(dictionary, value):
    keys = [key for key, val in dictionary.items() if val == value]
    return keys
def get_cur_pos(zero, one):
    ret = ((zero - (BORDER * WIDTH)) / 8) / (CELL / 8), ((one - (BORDER * HEIGHT)) / 8) / (CELL / 8)
    if not FLIPPED:
        ret = (ret[0], 7 - ret[1])
    mapping = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return f"{mapping.get(int(ret[0]))}{int(ret[1]) + 1}"
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_piece_at(square):
    # Convert the square notation (e.g., 'd4') to a square index
    try:
        square_index = chess.parse_square(square)
    except:
        return None
    # Get the piece at the given square
    piece = board.piece_at(square_index)

    if piece:
        return piece.symbol()  # Return the piece symbol

highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
highlighted_box_2 = (WIDTH * WIDTH, HEIGHT * HEIGHT)
curr_pos = highlighted_box
while True:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
            highlighted_box = pygame.mouse.get_pos()
            highlighted_box = (highlighted_box[0] - (CELL/2), highlighted_box[1] - (CELL/2))
            highlighted_box = ((highlighted_box[0] - (highlighted_box[0] % CELL)) + (BORDER * WIDTH), (highlighted_box[1] - (highlighted_box[1] % CELL)) + (BORDER * HEIGHT))
            curr_pos = get_cur_pos(highlighted_box[0], highlighted_box[1])
            #board.push_san("e4")
            #board.push_san("d5")
            #board.push(chess.Move.from_uci("e4d5")) # start to end
            #board.push_san("e4xd5")
            if get_piece_at(curr_pos) == None:
                highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
                break
            print(board.legal_moves)
            print()
            is_selected[0] = True
            is_selected[1] = curr_pos
            print("FDSKJ")
            print(curr_pos)
            print(CELL/8)
        if event.type == pygame.MOUSEBUTTONUP:
            is_selected[0] = False
            curr_pos = pygame.mouse.get_pos()
            curr_pos = (curr_pos[0] - (CELL / 2), curr_pos[1] - (CELL / 2))
            curr_pos = ((curr_pos[0] - (curr_pos[0] % CELL)) + (BORDER * WIDTH),
                               (curr_pos[1] - (curr_pos[1] % CELL)) + (BORDER * HEIGHT))
            curr_pos = get_cur_pos(curr_pos[0], curr_pos[1])
            print(curr_pos)
            is_selected[2] = curr_pos
            try:
                move = chess.Move.from_uci(f"{is_selected[1]}{is_selected[2]}")
                if board.is_legal(move):
                    board.push(move)
                is_selected[1] = is_selected[2] = ""
            except:
                print("hi")
            highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        #    highlighted_box_2 = (WIDTH * WIDTH, HEIGHT * HEIGHT)
        #    highlighted_box_2 = pygame.mouse.get_pos()
        #    highlighted_box_2 = (highlighted_box_2[0] - (CELL/2), highlighted_box_2[1] - (CELL/2))
        #    highlighted_box_2 = ((highlighted_box_2[0] - (highlighted_box_2[0] % CELL)) + (BORDER * WIDTH), (highlighted_box_2[1] - (highlighted_box_2[1] % CELL)) + (BORDER * HEIGHT))
        #    curr_pos = get_cur_pos(highlighted_box_2[0], highlighted_box_2[1])
        #    #board.push_san("e4")
        #    #board.push_san("d5")
        #    #board.push(chess.Move.from_uci("e4d5")) # start to end
        #    #board.push_san("e4xd5")
        #    print(board.legal_moves)
        #
        #    print(curr_pos)
        #    print(CELL/8)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            highlighted_box = highlighted_box_2 = (WIDTH * WIDTH, HEIGHT * HEIGHT)

    #pygame.draw.rect(screen, "#543c2c", (0, 0, WIDTH, HEIGHT))
    c = ["#b99d78", "#876247"]
    if FLIPPED: c = c[::-1]
    pygame.draw.rect(screen, c[0],
                     (BORDER * WIDTH, BORDER * HEIGHT, WIDTH - (2 * BORDER * WIDTH), HEIGHT - (2 * BORDER * HEIGHT)))
    for i in range(8):
        for j in range(8):
            index = (i % 2) + (j % 2)
            index = index if index < 2 else 0
            if index: pygame.draw.rect(screen, c[1], (
            ((i + 1) * CELL) - (BORDER * WIDTH), ((j + 1) * CELL) - (BORDER * HEIGHT), CELL, CELL))
    the_board = str(board)
    the_board = the_board.split("\n")
    for i in range(len(the_board)):
        the_board[i] = the_board[i].split(" ")
    for i in range(8):
        for j in range(8):
            the_board[i][j] = the_board[i][j].replace(".", "")
    if FLIPPED: the_board = the_board[::-1]
    _all = [
        [
            find_positions(the_board, "r"),
            find_positions(the_board, "n"),
            find_positions(the_board, "b"),
            find_positions(the_board, "q"),
            find_positions(the_board, "k"),
            find_positions(the_board, "p")
        ],
        [
            find_positions(the_board, "R"),
            find_positions(the_board, "N"),
            find_positions(the_board, "B"),
            find_positions(the_board, "Q"),
            find_positions(the_board, "K"),
            find_positions(the_board, "P")
        ]
    ]
    #pygame.draw.rect(screen, "#e489f2", (highlighted_box[0], highlighted_box[1], CELL, CELL))
    #pygame.draw.rect(screen, "#f2a389", (highlighted_box_2[0], highlighted_box_2[1], CELL, CELL))
    pygame.draw.ellipse(screen, "#e489f2", (highlighted_box[0], highlighted_box[1], CELL, CELL))
    for i in _all:
        for j in i:
            for k in j:
                #e = "#ffffff" if k[2] == "r" else "#e9c209" if k[2] == "b" else "#e8238f" if k[2] == "" else "#000000"
                e = "#000000"
                _map = {
                    "r": "black-rook",
                    "b": "black-bishop",
                    "n": "black-knight",
                    "q": "black-queen",
                    "k": "black-king",
                    "p": "black-pawn",

                    "R": "white-rook",
                    "B": "white-bishop",
                    "N": "white-knight",
                    "Q": "white-queen",
                    "K": "white-king",
                    "P": "white-pawn",
                }
                for l in _map:

                    e = _map[l] if k[2] == l else e
                #pygame.draw.rect(screen, e, (((k[1] + 0.5) * CELL) + BORDER, ((k[0] + 0.5) * CELL) + BORDER, CELL, CELL))
                imp = pygame.transform.scale(pygame.image.load(f"pieces\\{e}.png").convert_alpha(), (CELL, CELL))
                screen.blit(imp, (((k[1] + 0.5) * CELL) + BORDER, ((k[0] + 0.5) * CELL) + BORDER, CELL, CELL))


    pygame.draw.rect(screen, "#543c2c", (0, 0, WIDTH, HEIGHT * BORDER))
    pygame.draw.rect(screen, "#543c2c", (0, 0, WIDTH * BORDER, HEIGHT))
    pygame.draw.rect(screen, "#543c2c", (WIDTH - (BORDER * WIDTH), 0, WIDTH * BORDER, HEIGHT))
    pygame.draw.rect(screen, "#543c2c", (0, HEIGHT - (BORDER * HEIGHT), WIDTH, HEIGHT * BORDER))


    pygame.display.flip()
    screen.fill((0, 0, 0))
    #clock.tick(10000)
