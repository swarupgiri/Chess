import datetime
import pandas
import chess
import math
import time
import threading
import ctypes
import customtkinter as ctk
from win32mica import ApplyMica, MicaTheme, MicaStyle
import bot
board = chess.Board()
#board.set_fen("8/8/3k4/8/8/8/5qK1/8 w - - 0 1")
#board.push_san("e5")
print(board)
import pygame

CELL = 78 # DEFAULT => 80 [only works with factors of >80]
WIDTH = HEIGHT = 9 * CELL
BORDER = CELL / (1440 * (CELL / 80))
FLIPPED = False
DEFAULT_PROMO = "q"
OVER = False
PLAY_WITH_BOT = True
BOT_PLAYS_AS = 0 # w=1, b=0
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
def reset():
    board.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    global start_time
    start_time = datetime.datetime.now()
def load_fen_notation(fen):
    board.set_fen(fen)

def algebraic_to_coords(pos):
    pos = str(board.parse_san(pos))
    pos = pos[2] + pos[3]
    print(pos, len(pos))
    #if len(pos) == 4:
    #    if "+" in pos:
    #        pos = pos[1] + pos[2]
    #    else:
    #        pos = pos[2] + pos[3]
    #elif len(pos) == 3:
    #    if "+" in pos:
    #        pos = pos[0] + pos[1]
    #    else:
    #        pos = pos[1] + pos[2]
    #elif len(pos) == 5:
    #    if "+" in pos:
    #        pos = pos[2] + pos[3]
    #    else:
    #        pos = pos[3] + pos[4]
    mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    file_letter = pos[0]
    rank_number = int(pos[1]) - 1  # Convert rank number to zero-indexed

    file_index = mapping.get(file_letter)
    if file_index is None or rank_number < 0 or rank_number > 7:
        raise ValueError("Invalid algebraic notation position")

    if FLIPPED:
        file_index = 7 - file_index
        rank_number = 7 - rank_number

    return (file_index, rank_number)
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
def check_():
    global FLIPPED
    FLIPPED = not FLIPPED
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

    checkbox = ctk.CTkCheckBox(master=root, text="Flipped", command=check_,
                                         onvalue="on", offvalue="off")
    checkbox.pack(padx=20, pady=10)

    button = ctk.CTkButton(root, text="Reset", command=reset)
    button.pack(pady=10)

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
white_left = datetime.timedelta(minutes=10)
def white():
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

    def update_labels():
        # This function will update the labels with the latest info
        global white_left
        white_left = white_left - datetime.timedelta(seconds=1)
        time_left_label.configure(text=f"Time Left: {white_time}")

        # Schedule the function to be called again after 1 second
        root.after(1000, update_labels)

    # Start updating the labels
    update_labels()

    # Start the customtkinter event loop
    root.mainloop()




# Start the customtkinter window in a separate thread
tk_thread = threading.Thread(target=start_customtkinter_window)
tk_thread.daemon = True  # This makes sure the thread will exit when the main program exits
tk_thread.start()

#white_time = threading.Thread(target=white)
#white_time.daemon = True  # This makes sure the thread will exit when the main program exits
#white_time.start()

#black_time = threading.Thread(target=black)
#black_time.daemon = True  # This makes sure the thread will exit when the main program exits
#black_time.start()


def get_legal_moves(square):
    piece_moves = []
    for move in board.legal_moves:
        if move.from_square == square:
            piece_moves.append(move)
    return piece_moves





highlight_moves = []


while True:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
        if PLAY_WITH_BOT and BOT_PLAYS_AS == board.turn:
            pass
        else:
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
                #print(get_piece_at(curr_pos))
                legal_moves = get_legal_moves(chess.parse_square(curr_pos))
                #print(legal_moves[1], "E")
                #print(algebraic_to_coords("a1"))
                # Print the legal moves
                for move in legal_moves:
                    #print(board.san(move))
                    m = algebraic_to_coords(board.san(move))
                    highlight_moves.append(m)

                    #pygame.draw.rect(screen, "#ffffff", (0, 0, 10000, 10000))
                    #print(board.san(move))
                is_selected[0] = True
                is_selected[1] = curr_pos
            if event.type == pygame.MOUSEBUTTONUP:
                is_selected[0] = False
                curr_pos = pygame.mouse.get_pos()
                curr_pos = (curr_pos[0] - (CELL / 2), curr_pos[1] - (CELL / 2))
                curr_pos = ((curr_pos[0] - (curr_pos[0] % CELL)) + (BORDER * WIDTH),
                                   (curr_pos[1] - (curr_pos[1] % CELL)) + (BORDER * HEIGHT))
                curr_pos = get_cur_pos(curr_pos[0], curr_pos[1])
                is_selected[2] = curr_pos
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
                except:
                    pass
                highlighted_box = (WIDTH * WIDTH, HEIGHT * HEIGHT)
                highlight_moves = []
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


    for i in highlight_moves:
        rec = ((((i[0]) * CELL) + (0.5 * CELL)) + 0.25 * CELL, (((7 - i[1]) * CELL) + (0.5 * CELL)) + 0.25 * CELL, CELL / 2, CELL / 2)
        if FLIPPED:
            rec = ((((7 - i[0]) * CELL) + (0.5 * CELL)) + 0.25 * CELL, (((7 - i[1]) * CELL) + (0.5 * CELL)) + 0.25 * CELL, CELL / 2, CELL / 2)
        pygame.draw.ellipse(screen, "#e489f2", rec)
        #print(i)


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
        threading.Thread(target=quit_now()).start()
        OVER = True
    elif board.result() == "0-1":
        threading.Thread(target=quit_now()).start()
        OVER = True
    elif board.result() == "1-0":
        threading.Thread(target=quit_now()).start()
        OVER = True

    if (BOT_PLAYS_AS == board.turn):
        tk_thread = threading.Thread(target=lambda: board.push_san(bot.return_move(board.fen())))
        tk_thread.daemon = True  # This makes sure the thread will exit when the main program exits
        tk_thread.start()


    pygame.display.flip()
    screen.fill((0, 0, 0))
    #clock.tick(10000)
