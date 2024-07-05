import datetime
import pandas
import chess
import math
import time
import threading
import ctypes
import customtkinter as ctk
from win32mica import ApplyMica, MicaTheme, MicaStyle
board = chess.Board()
board.set_fen("8/8/3k4/8/8/8/5qK1/8 w - - 0 1")
#board.push_san("e5")
print(board)
import pygame

CELL = 78 # DEFAULT => 80 [only works with factors of >80]
WIDTH = HEIGHT = 9 * CELL
BORDER = CELL / (1440 * (CELL / 80))
FLIPPED = False
DEFAULT_PROMO = "q"
OVER = False
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

font = pygame.font.Font(None, 36)  # Default font, may not always work
if not pygame.font.get_init():
    pygame.font.init()  # Initialize fonts if not already done
if pygame.font.get_init():
    font = pygame.font.Font(None, 36)  # Try initializing with default font
else:
    font = pygame.font.SysFont("Arial", 36)  # Fallback to system font

def quit_now():
    print("GAME OVER")





start_time = datetime.datetime.now()
time_left = (start_time + datetime.timedelta(minutes=10)) - start_time  # Example value


def round_datetime(dt, rnd=1):
    # Calculate the number of microseconds that represent a hundredth of a second
    hundredth_of_second = 10000 if rnd == 2 else 1000000

    # Calculate the remainder of microseconds when divided by a hundredth of a second
    remainder = dt.microseconds % hundredth_of_second

    # Check if the remainder is greater than or equal to half of a hundredth of a second
    if remainder >= hundredth_of_second / 2:
        # Round up to the next hundredth of a second
        dt = dt + datetime.timedelta(microseconds=(hundredth_of_second - remainder))
    else:
        # Round down to the nearest hundredth of a second
        dt = dt - datetime.timedelta(microseconds=remainder)

    return dt
def start_customtkinter_window():
    # Initialize customtkinter
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Chess Info")

    # Apply Mica effect
    hwnd = root.winfo_id()
    ApplyMica(ctypes.windll.user32.GetForegroundWindow(root.winfo_id()), MicaTheme.AUTO, MicaStyle.ALT)

    # Create labels for time left and current turn
    time_left_label = ctk.CTkLabel(root, text="Time Left: ")
    time_left_label.pack(pady=10)

    turn_label = ctk.CTkLabel(root, text="Current Turn: ")
    turn_label.pack(pady=10)

    over_or_not = ctk.CTkLabel(root, text="Current Turn: ")
    over_or_not.pack(pady=10)
    def update_labels():
        # This function will update the labels with the latest info
        left = round_datetime((start_time + datetime.timedelta(minutes=10)) - datetime.datetime.now()) if not OVER else left
        time_left_label.configure(text=f"Time Left: {left}")

        turn_label.configure(text=f"Current Turn: {'White' if board.turn else 'Black'}")
        over_or_not.configure(text=f"Status: {'Stalemate' if board.result() == '1/2-1/2' else 'White Won' if board.result() == '1-0' else 'Black Won' if board.result() == '0-1' else 'Playing'} ")
        # Schedule the function to be called again after 1 second
        root.after(1, update_labels)

    # Start updating the labels
    update_labels()

    # Start the customtkinter event loop
    root.mainloop()

# Start the customtkinter window in a separate thread
tk_thread = threading.Thread(target=start_customtkinter_window)
tk_thread.daemon = True  # This makes sure the thread will exit when the main program exits
tk_thread.start()













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
            print(board.result(), "E")
            print(board.is_legal(chess.Move.from_uci("e4e5q")))
            try:
                move = chess.Move.from_uci(f"{is_selected[1]}{is_selected[2]}")

                if board.is_legal(move):
                    board.push(move)
                else:
                    move = chess.Move.from_uci(f"{is_selected[1]}{is_selected[2]}{DEFAULT_PROMO.lower()}")
                    if board.is_legal(move):
                        board.push(move)
                    else:
                        move = chess.Move.from_uci(f"{is_selected[1]}{is_selected[2]}{DEFAULT_PROMO.upper()}")
                is_selected[1] = is_selected[2] = ""
                print(board.legal_moves)
            except:
                print("e")
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
    if board.result() == "1/2-1/2":
        print("Draw")
        threading.Thread(target=quit_now()).start()
        OVER = True
    elif board.result() == "0-1":
        print("Black Won")
        threading.Thread(target=quit_now()).start()
        OVER = True
    elif board.result() == "1-0":
        print("White Won")
        threading.Thread(target=quit_now()).start()
        OVER = True

    pygame.display.flip()
    screen.fill((0, 0, 0))
    #clock.tick(10000)
