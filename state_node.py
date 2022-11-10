class State:
    def __init__(self, board):
        self.board = board
        self.utility = 0
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def set_utility(self, utility):
        self.utility = utility
