"""
Connect-4
"""
import copy

import numpy as np
from scipy.signal import convolve2d
from Utils.StateNode import State
from Utils.Board import Board
from Utils.Heuristic import expected_utility

max_level = 42
red = "red"
yellow = "yellow"
EMPTY = ""
tree_root = None
depth = 0
nodes_explored = 0
INFINITY = 9223372036854775807


def initial_state():
    """
    Returns starting state of the board.
    """
    return Board(1)


def player(board):
    """
    Returns player who has the next turn on a board.
    TODO: UPDATE FOR BITS REPRESENTATION (DONE)
    """
    terminal = True
    for i in range(7):
        if board.num_of_plays(i) < 6:
            terminal = False
            break
    if terminal:
        return None

    if board.turn == 0:
        return yellow
    elif board.turn == 1:
        return red


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    TODO: UPDATE FOR BITS REPRESENTATION (DONE)
    """
    possible_moves = set()

    for i in range(7):
        if board.num_of_plays(i) < 6:
            possible_moves.add(i)

    return possible_moves


def result(board: Board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    TODO: UPDATE FOR BITS REPRESENTATION (DONE)
    """
    new_board = Board(copy.deepcopy(board.turn))
    new_board.state = copy.deepcopy(board.state)
    new_board.insert(action)
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
    TODO: UPDATE FOR BITS REPRESENTATION (DONE)
    """
    if player_color == red:
        player_color = 1
    elif player_color == yellow:
        player_color = 0
    player_board = np.zeros(shape=(6, 7))
    for i in range(6):
        for j in range(7):
            if board.retrieve(i, j) == player_color:
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
    Returns +ve if red has won the game, -ve if yellow has won, 0 otherwise.
    """
    score = get_score(board)
    return score[0] - score[1]


def limited_terminal(level, max_depth):
    """
    Returns True if the game is over, False otherwise.
    note: it works for limited and unlimited search
    """
    return max_depth == 0 or level == max_depth


def unlimited_terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if player(board) is None:
        return True
    else:
        return False


def minimax(board, pruning, limited_depth):
    """
    Returns the optimal action for the current player on the board.
    """
    root = State(board)
    global depth, tree_root, nodes_explored
    depth = limited_depth
    if player(board) == red:
        optimal = (-INFINITY, None)
        for action in actions(board):
            child = State(result(board, action))
            nodes_explored = nodes_explored + 1
            root.add_child(child)
            utility_value = min_value(child, optimal[0], pruning, 1)
            if utility_value > optimal[0]:
                optimal = (utility_value, action)
                root.set_utility(optimal[0])

    else:
        optimal = (INFINITY, None)
        for action in actions(board):
            child = State(result(board, action))
            nodes_explored = nodes_explored + 1
            root.add_child(child)
            utility_value = max_value(child, optimal[0], pruning, 1)
            if utility_value < optimal[0]:
                optimal = (utility_value, action)
                root.set_utility(optimal[0])

    tree_root = root
    print("Nodes Explored: " + str(nodes_explored))
    return optimal[1], tree_root


def max_value(child, predecessor_v, pruning, level_no):
    global nodes_explored
    if unlimited_terminal(child.board):
        v = exact_utility(child.board)
        child.set_utility(v)
        return v
    if limited_terminal(level_no, depth):
        v = expected_utility(child.board)
        child.set_utility(v)
        return v

    v = -1 * INFINITY
    for action in actions(child.board):
        ch_child = State(result(child.board, action))
        nodes_explored = nodes_explored + 1
        child.add_child(ch_child)
        v = max(v, min_value(ch_child, v, pruning, level_no + 1))
        child.set_utility(v)
        if v >= predecessor_v and pruning:
            break
    return v


def min_value(child, predecessor_v, pruning, level_no):
    global nodes_explored
    if unlimited_terminal(child.board):
        v = exact_utility(child.board)
        child.set_utility(v)
        return v
    if limited_terminal(level_no, depth):
        v = expected_utility(child.board)
        child.set_utility(v)
        return v

    v = INFINITY
    for action in actions(child.board):
        ch_child = State(result(child.board, action))
        nodes_explored = nodes_explored + 1
        child.add_child(ch_child)
        v = min(v, max_value(ch_child, v, pruning, level_no + 1))
        child.set_utility(v)
        if v <= predecessor_v and pruning:
            break
    return v


def get_tree():
    return tree_root
