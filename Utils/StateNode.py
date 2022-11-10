from treelib import Tree


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

    def convert(self, tree: Tree):
        for child in self.children:
            tree.create_node(child.utility, child.board, self.board)
            child.convert(tree)
