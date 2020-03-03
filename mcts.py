from tree import Node
from math import log, sqrt
from game import Game


class MCTS:
    """
    Monte Carlo Tree Search
    """

    def __init__(self, cfg):
        self.tree_policy = {}
        self.default_policy = {}
        self.target_policy = {}
        self.tree = Node(state=init_state, parent=None)
        self.q = {}
        self.u = {}
        self.c = cfg["mcts"]["c"]

    def new_node(self, s0: Node, state, action: tuple, legal: list):
        s0.insert(state, ation)
        new_node = s0.children[-1]

        new_node.actions.extend(legal)
        for action in legal:
            new_node.branch_visists[action] = 0
            self.q[(new_node, action)] = 0

    def calculate_u(self, state: Node, action: tuple, c: int):
        return c * sqrt(log(state.visits) / (1 + state.branch_visist[action]))

    def select_action(self, board: Game, state: Node, c: int):
        legal = board.get_legal_actions()
        chosen = self.target_policy[(state, legal[0])]
        if board.player == 1:
            for action in legal:
                current = self.q[(state, action)] + self.calculate_u(state, action, c)
                    if current > chosen:
                        chosen = current
        else:
            for action in legal:
                current = self.q[(state, action)] - self.calculate_u(state, action, c)
                    if current > chosen:
                        chosen = current
        return chosen

    def tree_search(self, board: Game):
        c = self.c
        t = 0
        a = None
        state_path = []
        while not board.game_over():
            s = board.state
            node = self.tree.get_node_by_state(s)
            state_path.append(node)
            if node is None:
                legal = board.get_legal_actions()
                self.new_node(s, a, legal)
                return state_path
            a = self.select_action(board, s, c)
            board.perform_action(a)
            t += 1
        return state_path

    def default_search(self, board: Game):
        while not board.game_over():
            a = self.default_policy[board.state]
            board.perform_action(a)
        return board.winner()
    
    def leaf_evaluation(self, board: Game, s0):
        board.set_position(s0)
        path = self.tree_search(board)
        z = self.default_search(board)
        self.backpropagate(path, z)

    def backpropagate(self, state_path: list, z: int):
        for i in range(len(state_path)-1):
            state = state_path[i]
            action = state.get_action_to(state_path[i+1])
            state.visits += 1
            state.branch_visist[action] += 1
            self.q[(state, action)] = (
                self.q[(state, action)]
                + (z - self.q[(state, action)]) / state.branch_visists[action]
            )

    def uct_search(self, s0):
        time = 1000
        while time != 0:
            self.leaf_evaluation(board, s0)
            time -= 1
        board.set_position(s0)
        return self.select_action(board, s0, 0)

