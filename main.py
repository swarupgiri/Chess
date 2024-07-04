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

the_board = str(board)
the_board = the_board.split("\n")
for i in range(len(the_board)):
    the_board[i] = the_board[i].split(" ")
for i in range(8):
    for j in range(8):
        the_board[i][j] = the_board[i][j].replace(".", "")

print(the_board)

for i in range(8):
    for j in range(8):
        index = (i % 2) + (j % 2)
        index = index if index < 2 else 0
        if index: pygame.draw.rect(screen, "#876247", (((i + 1) * CELL) - (BORDER * WIDTH), ((j + 1) * CELL) - (BORDER * HEIGHT), CELL, CELL))


        #print(i, j)
        #print(index, end="")
    #print("\n")
    #pygame.draw.rect(screen, "#d4770f", ((i * 80) + (BORDER * WIDTH * i), (j * 80) + (BORDER * HEIGHT * j), 80, 80))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()





    pygame.display.flip()
    #clock.tick(10000)
