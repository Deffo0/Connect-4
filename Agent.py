"""
Tic Tac Toe Player
"""
import copy
from scipy.signal import convolve2d
import numpy as np
import math

red = "red"
yellow = "yellow"
EMPTY = ""


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            ]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    red_count = 0
    blue_count = 0
    for row in board:
        for cell in row:
            if cell == red:
                red_count = red_count + 1
            elif cell == yellow:
                blue_count = blue_count + 1
    if red_count + blue_count == 42:
        return None
    elif red_count > blue_count:
        return yellow
    elif red_count == blue_count:
        return red


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == EMPTY:
                possible_moves.add(j)
    if len(possible_moves) == 0:
        return None
    else:
        return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = initial_state()
    for i in range(0, 6):
        for j in range(0, 7):
            new_board[i][j] = copy.deepcopy(board[i][j])

    for i in range(0, 6):
        if new_board[i][action] != EMPTY and i-1 >= 0:
            landing_index = i - 1
            new_board[landing_index][action] = player(board)
            break
        elif i == 5:
            landing_index = i
            new_board[landing_index][action] = player(board)

    return new_board


def get_kernels():
    horizontal_kernel = np.array([[1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
    return detection_kernels


def get_player_board(board, player_color):
    player_board = np.zeros(shape=(6, 7))
    for i in range(6):
        for j in range(7):
            if board[i][j] == player_color:
                player_board[i][j] = 1
            else:
                player_board[i][j] = 0
    return player_board


def get_score(board):
    """
    Returns the score of the game.
    """
    score = [0, 0]
    detection_kernels = get_kernels()
    for kernel in detection_kernels:
        if (convolve2d(get_player_board(board, red), kernel, mode="valid") == 4).any():
            score[0] = score[0] + 1
    for kernel in detection_kernels:
        if (convolve2d(get_player_board(board, yellow), kernel, mode="valid") == 4).any():
            score[1] = score[1] + 1
    return score


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    detection_kernels = get_kernels()
    for kernel in detection_kernels:
        if (convolve2d(get_player_board(board, red), kernel, mode="valid") == 4).any():
            return red
    for kernel in detection_kernels:
        if (convolve2d(get_player_board(board, yellow), kernel, mode="valid") == 4).any():
            return yellow
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or player(board) is None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) is True:
        winner_symbol = winner(board)
        if winner_symbol == red:
            return 1
        elif winner_symbol == yellow:
            return -1
        elif winner_symbol is None:
            return 0


def minimax(board, pruning, limited_depth):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == red:
        optimal = (-10, None)
        for action in actions(board):
            utility_value = min_value(result(board, action), optimal[0])
            if utility_value > optimal[0]:
                optimal = (utility_value, action)

    else:
        optimal = (10, None)
        for action in actions(board):
            utility_value = max_value(result(board, action), optimal[0])
            if utility_value < optimal[0]:
                optimal = (utility_value, action)

    return optimal[1]


def max_value(board, predecessor_v):
    if terminal(board):
        return utility(board)

    v = -10
    for action in actions(board):
        v = max(v, min_value(result(board, action), v))
        if v > predecessor_v:
            break
    return v


def min_value(board, predecessor_v):
    if terminal(board):
        return utility(board)

    v = 10
    for action in actions(board):
        v = min(v, max_value(result(board, action), v))
        if v < predecessor_v:
            break
    return v
