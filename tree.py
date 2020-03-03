class Node:
    def __init__(self, state, parent: Node):
        self.parent = node
        self.state = state

        self.children = []
        self.actions = []

        self.q = 0
        self.visits = 0
        self.branch_visists = {}

    def insert(self, new_state, action):
        self.actions.append(action)
        self.children.append(Node(state=new_state, parent=self))


