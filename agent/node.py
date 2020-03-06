class Node:
    def __init__(self, state, parent):
        self.parent = parent
        self.state = state

        self.children = []

        self.q = 0
        self.visits = 0

    def insert(self, new_state):
        child = Node(state=new_state, parent=self)

        if child not in self.children:
            self.children.append(child)


    def get_node_by_state(self, state):
        if self.state == state:
            return self
        else:
            for child in self.children:
                return self.get_node_by_state(child)
        return None

    def get_action_to(self, chosen_child):
        for i, child in enumerate(self.children):
            if child.state == chosen_child.state:
                return self.actions[i]

    def is_terminal_node(self):
        self.state.game_over()

    def increase_visits(self):
        self.visits += 1

