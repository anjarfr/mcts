class Tree:
    def __init__(self):
        pass


class Node:
    def __init__(self, node):
        self.parent = node
        self.children = []
        self.visits = 0

