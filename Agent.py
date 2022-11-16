"""
Tic Tac Toe Player
"""
import copy

import numpy as np
from scipy.signal import convolve2d
import Utils.StateNode
from Utils.Board import Board

max_level = 42
red = "red"
yellow = "yellow"
EMPTY = ""
tree_root = None
INFINITY = 9223372036854775807

# Heuristics----------------
board_weights = [
    [30, 40, 50, 70, 50, 40, 30],
    [40, 60, 80, 100, 80, 60, 40],
    [50, 80, 110, 130, 110, 80, 50],
    [50, 80, 110, 130, 110, 80, 50],
    [40, 60, 80, 100, 80, 60, 40],
    [30, 40, 50, 70, 50, 40, 30]
]

level4_heuristic = 1000000
level3_heuristic = 50000
level2_heuristic = 50
level1_heuristic = 5

RED = 1
YELLOW = 0
Empty = -1


# ---------------------------


def initial_state():
    """
    Returns starting state of the board.
    """
    # IS this an int board or a bin board ??????
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
    # KOTB WORK
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

    print("----------------heuristics----------------")
    boardx = []
    for i in range(6):
        dd = []
        for j in range(7):
            if board.retrieve(i, j) == 1:
                dd.append('R')
            elif board.retrieve(i, j) == 0:
                dd.append('Y')
            elif board.retrieve(i, j) == -1:
                dd.append(' ')
        boardx.append(dd)
    print(boardx)

    red_score = get_score(board)[0]
    yellow_score = get_score(board)[1]
    if red_score > yellow_score:
        return RED
    elif red_score < yellow_score:
        return -1
    red_total_value = 0
    yellow_total_value = 0
    """CHECK THIRD LEVEL"""
    # rowbyrow
    for i in range(5, -1, -1):
        for j in range(5):
            sum_of_red = 0
            sum_of_yellow = 0
            for k in range(3):
                if board.retrieve(i, j + k) == RED:
                    sum_of_red += 1
                elif board.retrieve(i, j + k) == YELLOW:
                    sum_of_yellow += 1
            # -rrr- has 4th level value
            if sum_of_red == 3:
                red_total_value += level_three_rowbyrow(board, i, j)
            elif sum_of_yellow == 3:
                yellow_total_value += level_three_rowbyrow(board, i, j)

    # colbycol
    for j in range(7):
        for i in range(5, 1, -1):
            sum_of_red = 0
            sum_of_yellow = 0
            for k in range(3):
                if board.retrieve(i - k, j) == RED:
                    sum_of_red += 1
                elif board.retrieve(i - k, j) == YELLOW:
                    sum_of_yellow += 1
            if sum_of_red == 3:
                if board.retrieve(i - 3, j) == Empty:
                    red_total_value += level3_heuristic
            elif sum_of_yellow == 3:
                if board.retrieve(i - 3, j) == Empty:
                    yellow_total_value += level3_heuristic

    # diagonally
    # first half this direction /
    for i in range(2, 6):
        for j in range(-1 + i):
            sum_of_red = 0
            sum_of_yellow = 0
            for k in range(3):
                if board.retrieve(i - k - j, j + k) == RED:
                    sum_of_red += 1
                elif board.retrieve(i - k - j, j + k) == YELLOW:
                    sum_of_yellow += 1
            if sum_of_red == 3:
                red_total_value += level_three_diagonal_smallAngle(board, i, j)
            if sum_of_yellow == 3:
                yellow_total_value += level_three_diagonal_smallAngle(board, i, j)

    # second half this direction /
    for j in range(1, 5):
        for k in range(5 - j):
            row = 5 - k
            row2 = row
            col = j + k
            col2 = col
            sum_of_red = 0
            sum_of_yellow = 0
            for i in range(3):
                if board.retrieve(row, col) == RED:
                    sum_of_red += 1
                elif board.retrieve(row, col) == YELLOW:
                    sum_of_yellow += 1
                row -= 1
                col += 1
            if sum_of_red == 3:
                red_total_value += level_three_diagonal_smallAngle(board, row2, col2)
            if sum_of_yellow == 3:
                yellow_total_value += level_three_diagonal_smallAngle(board, row2, col2)

    # \ this direction upper half
    for j in range(1, 6):
        for k in range(5 - j):
            row = k
            col = j + k
            row2 = row
            col2 = col
            sum_of_red = 0
            sum_of_yellow = 0
            for i in range(3):
                if board.retrieve(row, col) == RED:
                    sum_of_red += 1
                elif board.retrieve(row, col) == YELLOW:
                    sum_of_yellow += 1
                row += 1
                col += 1
            if sum_of_red == 3:
                red_total_value += level_three_diagonal_smallAngle(board, row2, col2)
            if sum_of_yellow == 3:
                yellow_total_value += level_three_diagonal_smallAngle(board, row2, col2)

    # \ this direction lower half
    for i in range(4):
        for k in range(4 - i):
            row = i + k
            col = k
            row2 = row
            col2 = col
            sum_of_red = 0
            sum_of_yellow = 0
            for j in range(3):
                if board.retrieve(row, col) == RED:
                    sum_of_red += 1
                elif board.retrieve(row, col) == YELLOW:
                    sum_of_yellow += 1
                row += 1
                col += 1
            if sum_of_red == 3:
                red_total_value += level_three_diagonal_smallAngle(board, row2, col2)
            if sum_of_yellow == 3:
                yellow_total_value += level_three_diagonal_smallAngle(board, row2, col2)

    """CHECK SECOND LEVEL AND FIRST LEVEL"""
    # rowbyrow
    for i in range(5, -1, -1):
        for j in range(6):
            sum_of_red = 0
            sum_of_yellow = 0
            red_locations_sum = 0
            yellow_locations_sum = 0
            for k in range(2):
                if board.retrieve(i, j + k) == RED:
                    sum_of_red += 1
                    red_locations_sum += board_weights[i][j + k]
                elif board.retrieve(i, j + k) == YELLOW:
                    sum_of_yellow += 1
                    yellow_locations_sum += board_weights[i][j + k]
            # -rrr- has 4th level value
            if sum_of_red == 2:
                # double
                red_total_value += red_locations_sum * level2_heuristic
            elif sum_of_yellow == 3:
                yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

    # colbycol
    for j in range(7):
        for i in range(5, 0, -1):
            sum_of_red = 0
            sum_of_yellow = 0
            red_locations_sum = 0
            yellow_locations_sum = 0
            for k in range(2):
                if board.retrieve(i - k, j) == RED:
                    sum_of_red += 1
                    red_locations_sum += board_weights[i - k][j]
                elif board.retrieve(i - k, j) == YELLOW:
                    sum_of_yellow += 1
                    yellow_locations_sum += board_weights[i - k][j]
            if sum_of_red == 2:
                # if one on the top is empty
                if board.retrieve(i - 2, j) == Empty:
                    red_total_value += red_locations_sum * level2_heuristic
            elif sum_of_yellow == 2:
                if board.retrieve(i - 2, j) == Empty:
                    yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

    # diagonally
    # first half this direction /
    for i in range(1, 6):
        for j in range(i):
            sum_of_red = 0
            sum_of_yellow = 0
            red_locations_sum = 0
            yellow_locations_sum = 0
            for k in range(2):
                if board.retrieve(i - k - j, j + k) == RED:
                    sum_of_red += 1
                    red_locations_sum += board_weights[i - k - j][j + k]
                elif board.retrieve(i - k - j, j + k) == YELLOW:
                    sum_of_yellow += 1
                    yellow_locations_sum += board_weights[i - k - j][j + k]
            if sum_of_red == 2:
                # double
                red_total_value += red_locations_sum * level2_heuristic
            elif sum_of_yellow == 3:
                yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

    # second half this direction /
    for j in range(1, 6):
        for k in range(6 - j):
            row = 5 - k
            col = j + k
            sum_of_red = 0
            sum_of_yellow = 0
            red_locations_sum = 0
            yellow_locations_sum = 0
            for i in range(2):
                if board.retrieve(row, col) == RED:
                    sum_of_red += 1
                    red_locations_sum += board_weights[row][col]
                elif board.retrieve(row, col) == YELLOW:
                    sum_of_yellow += 1
                    yellow_locations_sum += board_weights[row][col]
                row -= 1
                col += 1
            if sum_of_red == 2:
                # double
                red_total_value += red_locations_sum * level2_heuristic
            elif sum_of_yellow == 3:
                yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

    # \ this direction upper half
    for j in range(1, 7):
        for k in range(6 - j):
            row = k
            col = j + k
            sum_of_red = 0
            sum_of_yellow = 0
            red_locations_sum = 0
            yellow_locations_sum = 0
            for i in range(2):
                if board.retrieve(row, col) == RED:
                    sum_of_red += 1
                    red_locations_sum += board_weights[row][col]
                elif board.retrieve(row, col) == YELLOW:
                    sum_of_yellow += 1
                    yellow_locations_sum += board_weights[row][col]
                row += 1
                col += 1
            if sum_of_red == 2:
                # double
                red_total_value += red_locations_sum * level2_heuristic
            elif sum_of_yellow == 3:
                yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

    # \ this direction lower half
    for i in range(5):
        for k in range(5 - i):
            row = i + k
            col = k
            sum_of_red = 0
            sum_of_yellow = 0
            red_locations_sum = 0
            yellow_locations_sum = 0
            for j in range(2):
                if board.retrieve(row, col) == RED:
                    sum_of_red += 1
                    red_locations_sum += board_weights[row][col]
                elif board.retrieve(row, col) == YELLOW:
                    sum_of_yellow += 1
                    yellow_locations_sum += board_weights[row][col]
                row += 1
                col += 1
            if sum_of_red == 2:
                # double
                red_total_value += red_locations_sum * level2_heuristic
            elif sum_of_yellow == 3:
                yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

    print(f"***\nred total value: {red_total_value} \n yellow total value: {yellow_total_value}")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return red_total_value - yellow_total_value




def level_three_rowbyrow(board, i, j):
    sum = 0
    check1: bool = False
    check2: bool = False
    if j - 1 >= 0 and board.retrieve(i, j - 1) == Empty:
        check1 = True
    if j + 3 <= 6 and board.retrieve(i, j + 3) == Empty:
        check2 = True
    if check1 and check2:
        sum += level4_heuristic
        row = i + 1
        col = j - 1
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
        row = i + 1
        col = j + 3
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
    elif check1:
        sum += level3_heuristic
        row = i + 1
        col = j - 1
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
    elif check2:
        sum += level3_heuristic
        row = i + 1
        col = j + 3
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
    return sum





def level_three_diagonal_smallAngle(board, i, j):
    check1 = False
    check2 = False
    sum = 0
    if i-1>=0 and j-1>=0 and board.retrieve(i-1, j-1) == Empty:
        check1 = True
    if i+3<=5 and j+3<=6 and board.retrieve(i + 3, j + 3) == Empty:
        check2 = True
    if check1 and check2:
        sum += level4_heuristic / 5
        row = i + 1
        col = j - 1
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
        row = i + 1
        col = j + 3
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
    elif check1:
        sum += level3_heuristic
        row = i + 1
        col = j - 1
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1
    elif check2:
        row = i + 1
        col = j + 3
        while row < 5 and board.retrieve(row, col) == Empty:
            sum -= 5000
            row += 1

    return sum







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
    print("minmax")
    root = Utils.StateNode.State(board)
    global depth, tree_root

    depth = limited_depth
    if player(board) == red:
        optimal = (-INFINITY, None)
        for action in actions(board):
            child = Utils.StateNode.State(result(board, action))
            root.add_child(child)
            utility_value = min_value(child, optimal[0], pruning, 1 if limited_depth < max_level else -1)
            if utility_value > optimal[0]:
                optimal = (utility_value, action)
            root.set_utility(utility_value)

    else:
        optimal = (INFINITY, None)
        for action in actions(board):
            child = Utils.StateNode.State(result(board, action))
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
    v = -1*INFINITY
    for action in actions(child.board):
        ch_child = Utils.StateNode.State(result(child.board, action))
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
    v = INFINITY
    for action in actions(child.board):
        ch_child = Utils.StateNode.State(result(child.board, action))
        child.add_child(ch_child)
        v = min(v, max_value(ch_child, v, pruning, level_no + 1 if level_no != -1 else -1))
        child.set_utility(v)
        if v < predecessor_v and pruning:
            break
    return v


def get_tree():
    return tree_root
