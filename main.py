import chess
board = chess.Board()
#board.push_san("e4")
#board.push_san("e5")
print(board)
import pygame

CELL = 78 # DEFAULT => 80 [only works with factors of >80]
WIDTH = HEIGHT = 9 * CELL
BORDER = CELL / (1440 * (CELL / 80))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
pygame.draw.rect(screen, "#543c2c", (0, 0, WIDTH, HEIGHT))
pygame.draw.rect(screen, "#b99d78", (BORDER * WIDTH, BORDER * HEIGHT, WIDTH - (2 * BORDER * WIDTH), HEIGHT - (2 * BORDER * HEIGHT)))



def find_positions(board, piece):
    positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == piece:
                positions.append((i, j, piece))
    return positions
for i in range(8):
    for j in range(8):
        index = (i % 2) + (j % 2)
        index = index if index < 2 else 0
        if index: pygame.draw.rect(screen, "#876247", (((i + 1) * CELL) - (BORDER * WIDTH), ((j + 1) * CELL) - (BORDER * HEIGHT), CELL, CELL))


        #print(i, j)
        #print(index, end="")
    #print("\n")
    #pygame.draw.rect(screen, "#d4770f", ((i * 80) + (BORDER * WIDTH * i), (j * 80) + (BORDER * HEIGHT * j), 80, 80))
def find_keys_by_value(dictionary, value):
    keys = [key for key, val in dictionary.items() if val == value]
    return keys

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    the_board = str(board)
    the_board = the_board.split("\n")
    for i in range(len(the_board)):
        the_board[i] = the_board[i].split(" ")
    for i in range(8):
        for j in range(8):
            the_board[i][j] = the_board[i][j].replace(".", "")

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
                print(k[2])
                #e = "#ffffff" if k[2] == "r" else "#e9c209" if k[2] == "b" else "#e8238f" if k[2] == "" else "#000000"
                e = "#000000"
                _map = {
                    "r": "#ffffff",
                    "b": "#fe314f",
                    "n": "#34f25e",
                    "q": "#9cf3b2",
                    "k": "#b32a5f",
                    "p": "#b2f39f",

                    "R": "#eeeeee",
                    "B": "#ee248e",
                    "N": "#37e26f",
                    "Q": "#2ef4b2",
                    "K": "#a32b7d",
                    "P": "#a4e4ae",
                }
                for l in _map:

                    e = _map[l] if k[2] == l else e
                pygame.draw.rect(screen, e, (((k[1] + 0.5) * CELL) + BORDER, ((k[0] + 0.5) * CELL) + BORDER, CELL, CELL))

    find_positions(the_board, "r")
    positions = find_positions(the_board, 'R')



    pygame.display.flip()
    #clock.tick(10000)
