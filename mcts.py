from tree import Node
from math import log, sqrt
from game import Game


class MCTS:
    """
    Monte Carlo Tree Search
    """

    def __init__(self, cfg, init_state):
        self.tree_policy = {}
        self.default_policy = {}
        self.target_policy = {}
        self.tree = Node(state=init_state, parent=None)
        self.q = {}
        self.u = {}
        self.c = cfg["mcts"]["c"]

    def new_node(self, s0: Node, state, action: tuple, legal: list, succ_states: list):
        s0.insert(state, ation)
        new_node = s0.children[-1]

        new_node.actions.extend(legal)
        for action in legal:
            new_node.branch_visists[action] = 0
            self.q[(new_node, action)] = 0

        new_node.children.extend([Node(state, node) for state in succ_states])

    def calculate_u(self, state: Node, action: tuple):
        return self.c * sqrt(log(state.visits) / (1 + state.branch_visist[action]))

    def select_action(self, board: Game, state: Node):
        legal = board.get_legal_actions()
        chosen = self.target_policy[(state, legal[0])]
        if board.player == 1:
            for action in legal:
                current = self.q[(state, action)] + self.calculate_u(state, action)
                    if current > chosen:
                        chosen = current
        else:
            for action in legal:
                current = self.q[(state, action)] - self.calculate_u(state, action)
                    if current > chosen:
                        chosen = current
        return chosen

    def tree_search(self, board: Game):
        t = 0
        SAP_path = []
        while not board.game_over():
            SAP_path.append(board.state)

        return chosen

    def leaf_evaluation(self):
        pass

    def default_search(self, board: Game):
        while not board.game_over():
            a = self.default_policy[board.state]
            board.perform_action(a)
        return board.winner()

    def backpropagate(self, SAP_path: list, z: int):
        for SAP in SAP_path:
            state = SAP[0]
            action = SAP[1]
            state.visits += 1
            state.branch_visist[action] += 1
            self.q[(state, action)] = (
                self.q[(state, action)]
                + (z - self.q[(state, action)]) / state.branch_visists[action]
            )
