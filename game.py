import random

PLAYER = "X"
COMPUTER = "O"


def new_board():
    return [""] * 9


def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for line in lines:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], list(line)

    return None, []


def is_draw(board):
    winner, _ = check_winner(board)
    return winner is None and all(board)


def available_moves(board):
    return [i for i, cell in enumerate(board) if not cell]


def play_player_move(board, cell):
    if cell not in range(9) or board[cell]:
        return False

    winner, _ = check_winner(board)
    if winner or is_draw(board):
        return False

    board[cell] = PLAYER
    return True


def play_computer_turn(board, difficulty):
    moves = available_moves(board)
    if not moves:
        return

    if difficulty == "medium":
        move = find_best_move(board)
    else:
        move = random.choice(moves)

    board[move] = COMPUTER


def find_best_move(board):
    # Win if possible.
    for move in available_moves(board):
        board[move] = COMPUTER
        if check_winner(board)[0] == COMPUTER:
            board[move] = ""
            return move
        board[move] = ""

    # Block the player if needed.
    for move in available_moves(board):
        board[move] = PLAYER
        if check_winner(board)[0] == PLAYER:
            board[move] = ""
            return move
        board[move] = ""

    # Prefer center, then corners, then any free cell.
    if board[4] == "":
        return 4

    corners = [0, 2, 6, 8]
    free_corners = [m for m in corners if board[m] == ""]
    if free_corners:
        return random.choice(free_corners)

    return random.choice(available_moves(board))
