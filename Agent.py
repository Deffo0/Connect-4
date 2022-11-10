"""
Tic Tac Toe Player
"""
import copy

import numpy as np
from scipy.signal import convolve2d
from Utils.StateNode import State

max_level = 42
red = "red"
yellow = "yellow"
EMPTY = ""
tree_root = None


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
    TODO: UPDATE FOR BITS REPRESENTATION
    """
    red_count = 0
    yellow_count = 0
    for row in board:
        for cell in row:
            if cell == red:
                red_count = red_count + 1
            elif cell == yellow:
                yellow_count = yellow_count + 1
    if red_count + yellow_count == 42:
        return None
    elif red_count > yellow_count:
        return yellow
    elif red_count == yellow_count:
        return red


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    TODO: UPDATE FOR BITS REPRESENTATION
    """
    possible_moves = set()
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == EMPTY:
                possible_moves.add(j)
    if len(possible_moves) == 0:
        print(board)
        return None
    else:
        return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    TODO: UPDATE FOR BITS REPRESENTATION
    """
    new_board = initial_state()
    for i in range(0, 6):
        for j in range(0, 7):
            new_board[i][j] = copy.deepcopy(board[i][j])

    for i in range(0, 6):
        if new_board[i][action] != EMPTY and i - 1 >= 0:
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
    main_diag_kernel = np.eye(4, dtype=np.uint8)
    flip_main_diag_kernel = np.fliplr(main_diag_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, main_diag_kernel, flip_main_diag_kernel]
    return detection_kernels


def get_player_board(board, player_color):
    """
    TODO: UPDATE FOR BITS REPRESENTATION
    """
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
        red_matches = (convolve2d(get_player_board(board, red), kernel, mode="valid") == 4)
        if red_matches.any():
            score[0] = score[0] + red_matches.sum()
    for kernel in detection_kernels:
        yellow_matches = (convolve2d(get_player_board(board, yellow), kernel, mode="valid") == 4)
        if yellow_matches.any():
            score[1] = score[1] + yellow_matches.sum()
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


def exact_utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_symbol = winner(board)
    if winner_symbol == red:
        return 1
    elif winner_symbol == yellow:
        return -1
    elif winner_symbol is None:
        return 0


def expected_utility(board):
    """
    Returns the expected utility of some node where we cut the tree
    TODO: implement this function
    """

    return 0


def limited_terminal(level, max_depth):
    """
    Returns True if the game is over, False otherwise.
    note: it works for limited and unlimited search
    """
    return max_level == 0 or level == max_depth + 1


def unlimited_terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or player(board) is None:
        return True
    else:
        return False


def minimax(board, pruning, limited_depth):
    """
    Returns the optimal action for the current player on the board.
    """
    root = State(board)
    global depth, tree_root
    if (unlimited_terminal(board) and limited_depth >= max_level) or (
            limited_terminal(0, limited_depth) and limited_depth < max_level):
        return None
    depth = limited_depth
    if player(board) == red:
        optimal = (-10, None)
        for action in actions(board):
            child = State(result(board, action))
            root.add_child(child)
            utility_value = min_value(child, optimal[0], pruning, 1 if limited_depth < max_level else -1)
            if utility_value > optimal[0]:
                optimal = (utility_value, action)
            root.set_utility(utility_value)

    else:
        optimal = (10, None)
        for action in actions(board):
            child = State(result(board, action))
            root.add_child(child)
            utility_value = max_value(child, optimal[0], pruning, 1 if limited_depth < max_level else -1)
            if utility_value < optimal[0]:
                optimal = (utility_value, action)
            root.set_utility(utility_value)

    tree_root = root
    return optimal[1], tree_root


def max_value(child, predecessor_v, pruning, level_no=-1):
    if level_no != -1 and limited_terminal(level_no, depth):
        return expected_utility(child.board)
    if level_no == -1 and unlimited_terminal(child.board):
        return exact_utility(child.board)
    v = -10
    for action in actions(child.board):
        ch_child = State(result(child.board, action))
        child.add_child(ch_child)
        v = max(v, min_value(ch_child, v, pruning, level_no + 1 if level_no != -1 else -1))
        child.set_utility(v)
        if v > predecessor_v and pruning:
            break
    return v


def min_value(child, predecessor_v, pruning, level_no=-1):
    if level_no != -1 and limited_terminal(level_no, depth):
        return expected_utility(child.board)
    if level_no == -1 and unlimited_terminal(child.board):
        return exact_utility(child.board)
    v = 10
    for action in actions(child.board):
        ch_child = State(result(child.board, action))
        child.add_child(ch_child)
        v = min(v, max_value(ch_child, v, pruning, level_no + 1 if level_no != -1 else -1))
        child.set_utility(v)
        if v < predecessor_v and pruning:
            break
    return v


def get_tree():
    return tree_root
