from tree import Node


class MCTS:
    def __init__(self, init_state):
        self.tree_policy = {}
        self.default_policy = {}
        self.target_policy = {}
        self.tree = Node(state=init_state, parent=None)
        self.u = {}
        self.Q = {}

    def tree_search(self):
        chosen = node.children[0]
        best = self.tree_policy[next_node]

        for child in node.children:
            if self.tree_policy[child] > best:
                best = self.tree_policy[child]
                chosen = child

        if len(chosen.children) > 0:
            chosen = tree_search(chosen)

        return chosen

    def node_expansion(self, node, actions, succ_states):
        node.actions.extend(actions)
        node.children.extend([Node(state, node) for state in succ_states])

    def leaf_evaluation(self):
        pass

    def backpropagate(self):
        pass
