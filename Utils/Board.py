def prettyPrint(boardBin):
    for j in range(6):
        print(boardBin[j])


class Board:
    def __init__(self):
        self.state = 0
        self.turn = -1

    def insert(self, col, player):
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
        col_shift = 6 - col
        index = 6 + col_shift * 9
        num_of_play = self.num_of_plays(col)
        if(row >= num_of_play):
            return -1
        player = self.state & (2 ** (index - row - 1))
        # print(index - row - 1)
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
            board_bin[i].append(current)
        for j in range(pre_garbage + 3, 9):
            current = temp[j]
            board_bin[i].append(" ")
    
    board_bin_modified = []

    row_ctr = 0
    for i in range(6):
        board_bin_modified.append(list())
        for j in range(7):
            board_bin_modified[row_ctr].append(board_bin[j][5 - i])
        row_ctr += 1
    return board_bin_modified


board = Board()
board.insert(3, 0)
board.insert(3, 0)
board.insert(3, 0)
board.insert(3, 1)
board.insert(3, 0)
board.insert(3, 1)
board.insert(4, 1)
board.insert(4, 1)
board.insert(6, 1)
board.insert(6, 0)
board.insert(0, 0)



prettyPrint(get_board_bin(board))
print(board.retrieve(0, 0))
print(board.retrieve(0, 1))
print(board.retrieve(0, 2))
print(board.retrieve(0, 3))
print(board.retrieve(0, 4))
print(board.retrieve(0, 5))
print(board.retrieve(0, 6))

print(board.retrieve(1, 0))
print(board.retrieve(1, 1))
print(board.retrieve(1, 2))
print(board.retrieve(1, 3))
print(board.retrieve(1, 4))
print(board.retrieve(1, 5))
print(board.retrieve(1, 6))


print(board.retrieve(2, 0))
print(board.retrieve(2, 1))
print(board.retrieve(2, 2))
print(board.retrieve(2, 3))
print(board.retrieve(2, 4))
print(board.retrieve(2, 5))
print(board.retrieve(2, 6))


# board.retrieve(0, 0)
# board.retrieve(0, 1)
# board.retrieve(0, 2)
# board.retrieve(0, 3)
# board.retrieve(0, 4)
# board.retrieve(0, 5)
# board.retrieve(0, 6)


