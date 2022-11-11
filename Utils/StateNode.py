from anytree import Node

class State:
    def __init__(self, board):
        self.board = board
        self.utility = 0
        self.children: list[State] = []

    def has_next(self):
        if len(self.children) != 0:
            return True
        else:
            return False

    def add_child(self, child):
        self.children.append(child)

    def set_utility(self, utility):
        self.utility = utility

    def convert(self, parent: Node):
        for i in range(len(self.children)):
            node = Node(self.children[i].utility, parent)
            self.children[i].convert(node)
