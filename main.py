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
FLIPPED = True
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()



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

highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
curr_pos = highlighted_box
while True:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
            highlighted_box = pygame.mouse.get_pos()
            highlighted_box = (highlighted_box[0] - (CELL/2), highlighted_box[1] - (CELL/2))
            highlighted_box = ((highlighted_box[0] - (highlighted_box[0] % CELL)) + (BORDER * WIDTH), (highlighted_box[1] - (highlighted_box[1] % CELL)) + (BORDER * HEIGHT))
            curr_pos = ((highlighted_box[0] - (BORDER * WIDTH)) / 8) / (CELL / 8), ((highlighted_box[1] - (BORDER * HEIGHT)) / 8) / (CELL / 8)
            if not FLIPPED:
                curr_pos = (curr_pos[0], 7 - curr_pos[1])
            print(curr_pos)
            print(CELL/8)

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


    pygame.draw.rect(screen, "#e489f2", (highlighted_box[0], highlighted_box[1], CELL, CELL))

    pygame.draw.rect(screen, "#543c2c", (0, 0, WIDTH, HEIGHT * BORDER))
    pygame.draw.rect(screen, "#543c2c", (0, 0, WIDTH * BORDER, HEIGHT))
    pygame.draw.rect(screen, "#543c2c", (WIDTH - (BORDER * WIDTH), 0, WIDTH * BORDER, HEIGHT))
    pygame.draw.rect(screen, "#543c2c", (0, HEIGHT - (BORDER * HEIGHT), WIDTH, HEIGHT * BORDER))

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
    find_positions(the_board, "r")
    positions = find_positions(the_board, 'R')


    pygame.display.flip()
    screen.fill((0, 0, 0))
    #clock.tick(10000)
