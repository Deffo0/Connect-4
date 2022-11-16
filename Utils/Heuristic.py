import numpy as np
from scipy.signal import convolve2d

board_weights = [
    [30, 40, 50, 70, 50, 40, 30],
    [40, 60, 80, 100, 80, 60, 40],
    [50, 80, 110, 130, 110, 80, 50],
    [50, 80, 110, 130, 110, 80, 50],
    [40, 60, 80, 100, 80, 60, 40],
    [30, 40, 50, 70, 50, 40, 30]
]

level4_heuristic = 100000000
level3_heuristic = 5000
level2_heuristic = 20
level1_heuristic = 5

RED = 1
YELLOW = 0
Empty = -1


def expected_utility(board):
    """
    Returns the expected utility of some node where we cut the tree
    TODO: implement this function
    """

    red_score = get_score(board)[0] * level4_heuristic
    yellow_score = get_score(board)[1] * level4_heuristic
    if red_score != yellow_score:
        return red_score - yellow_score
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
            elif sum_of_yellow == 2:
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
            elif sum_of_yellow == 2:
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
            elif sum_of_yellow == 2:
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
            elif sum_of_yellow == 2:
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
            elif sum_of_yellow == 2:
                yellow_total_value += yellow_locations_sum * level2_heuristic
            else:
                # single
                red_total_value += red_locations_sum * level1_heuristic
                yellow_total_value += yellow_locations_sum * level1_heuristic

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
    if i - 1 >= 0 and j - 1 >= 0 and board.retrieve(i - 1, j - 1) == Empty:
        check1 = True
    if i + 3 <= 5 and j + 3 <= 6 and board.retrieve(i + 3, j + 3) == Empty:
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
    if player_color == "red":
        player_color = 1
    elif player_color == "yellow":
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
        red_matches = (convolve2d(get_player_board(board, "red"), kernel, mode="valid") == 4)
        if red_matches.any():
            score[0] = score[0] + red_matches.sum()
    for kernel in detection_kernels:
        yellow_matches = (convolve2d(get_player_board(board, "yellow"), kernel, mode="valid") == 4)
        if yellow_matches.any():
            score[1] = score[1] + yellow_matches.sum()
    return score
