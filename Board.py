
class Board:
    def __init__(self):
        self.state = 0

    def insert(self, col, player):
        # if(num_of_play >= 6):
        #     return
        index = 6 + col * 9
        self.state = self.state + 2 ** index
        num = 0
        num_of_play = self.numOfPlays(col)
        print(num_of_play)
        if(num_of_play > 6):
            return
        if(player == 1):
            self.state += 2 ** (index - num_of_play)
            print(num_of_play)

    def numOfPlays(self, col):
        col_state = 0
        if(col == 0):
            col_state = self.state & 511
        elif(col == 1):
            col_state = self.state & 261632
        elif(col == 2):
            col_state = self.state & 133955584
        elif(col == 3):
            col_state = self.state & 68585259008
        elif(col == 4):
            col_state = self.state & 35115652612096
        elif(col == 5):
            col_state = self.state & 17979214137393152
        elif(col == 6):
            col_state = self.state & 9205357638345293824
        index = 6 + col * 9
        return col_state >> index

        

  
def getBoardBin(board):
    state = board.state
    str_num = '{0:063b}'.format(state)    
    board_bin = []
    ctr = 0
    for i in range(7):
        board_bin.append(list())
        index = 6 + i * 9
        pre_garbage = board.numOfPlays(i)
        ctr = 0
        left_index = 63 - (i * 9) - 9
        right_index = 63 - (i * 9)
        temp = str_num[left_index : right_index]
        for j in range(3, pre_garbage + 3):
            board_bin[i].append(temp[j])
            ctr += 1
        
    return board_bin

    



board = Board()
board.insert(3, 0)
board.insert(3, 0)
board.insert(3, 0)
board.insert(3, 1)
board.insert(3, 0)
board.insert(3, 1)










print(getBoardBin(board))
print(board.state)




