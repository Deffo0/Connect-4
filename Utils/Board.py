def prettyPrint(boardBin):
    for j in range(6):
        print(boardBin[j])


class Board:
    def __init__(self, first_turn):
        self.state = 0
        self.turn = first_turn

    def insert(self, col):
        player = self.turn
        col_shift = 6 - col
        index = 6 + col_shift * 9
        self.state = self.state + 2 ** index
        num_of_play = self.num_of_plays(col)
        if num_of_play > 6:
            return
        if player == 1:
            self.state += 2 ** (index - num_of_play)
            self.turn = 0
            return
        self.turn = 1
        

    def num_of_plays(self, col):
        col = 6 - col
        col_state = 0
        if col == 0:
            col_state = self.state & 511
        elif col == 1:
            col_state = self.state & 261632
        elif col == 2:
            col_state = self.state & 133955584
        elif col == 3:
            col_state = self.state & 68585259008
        elif col == 4:
            col_state = self.state & 35115652612096
        elif col == 5:
            col_state = self.state & 17979214137393152
        elif col == 6:
            col_state = self.state & 9205357638345293824
        index = 6 + col * 9
        return col_state >> index

    def retrieve(self, row, col):
        row = 5 - row
        col_shift = 6 - col
        index = 6 + col_shift * 9
        num_of_play = self.num_of_plays(col)
        if(row >= num_of_play):
            return -1
        player = self.state & (2 ** (index - row - 1))
        if(player == 0):
            return 0
        return 1


def get_board_bin(board):
    state = board.state
    str_num = '{0:063b}'.format(state)
    board_bin = []
    for i in range(7):
        board_bin.append(list())
        pre_garbage = board.num_of_plays(i)
        left_index = i * 9
        right_index = left_index + 9
        temp = str_num[left_index: right_index]
        for j in range(3, pre_garbage + 3):
            current = temp[j]
            if(current == '0'):
                board_bin[i].append("yellow")
            elif(current == '1'):
                board_bin[i].append("red")
        for j in range(pre_garbage + 3, 9):
            current = temp[j]
            board_bin[i].append("")
    
    board_bin_modified = []

    row_ctr = 0
    for i in range(6):
        board_bin_modified.append(list())
        for j in range(7):
            board_bin_modified[row_ctr].append(board_bin[j][5 - i])
        row_ctr += 1
    return board_bin_modified



