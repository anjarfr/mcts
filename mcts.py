from tree import Node
from math import log, sqrt
from game import Game
from random import randint


class MCTS:
    """
    Monte Carlo Tree Search
    """

    def __init__(self, cfg, init_state):
        self.tree = Node(state=init_state, parent=None)
        self.q = {}
        self.c = cfg["mcts"]["c"]

    def new_node(self, s0: Node, state, action, legal: list):
        s0.insert(state, action)
        new_node = s0.children[-1]

        new_node.actions.extend(legal)
        for action in legal:
            new_node.branch_visists[action] = 0
            self.q[(new_node, action)] = 0

    def u(self, node: Node, action, c: int):
        return c * sqrt(log(node.visits) / (1 + node.branch_visist[action]))

    def select_action(self, board: Game, node: Node, c: int):
        legal = board.get_legal_actions()
        chosen = self.target_policy[(node, legal[0])]
        if board.player == 1:
            for action in legal:
                current = self.q[(node, action)] + self.u(node, action, c)
                if current > chosen:
                    chosen = action
        else:
            for action in legal:
                current = self.q[(node, action)] - self.u(node, action, c)
                if current > chosen:
                    chosen = action
        return chosen

    def tree_search(self, board: Game):
        c = self.c
        t = 0
        a = None
        path = []
        while not board.game_over():
            s = board.state
            node = self.tree.get_node_by_state(s)
            path.append(node)
            if node is None:
                legal = board.get_legal_actions()
                self.new_node(s, a, legal)
                return path
            a = self.select_action(board, s, c)
            board.perform_action(a)
            t += 1
        return path

    def default_search(self, board: Game):
        """ Random simulation until termination """
        while not board.game_over():
            a = self.default_policy(board)
            board.perform_action(a)
        return board.winner()

    def default_policy(self, board: Game):
        """ Choose a random action """
        legal = board.get_legal_actions(board.state)
        i = randint(0, len(legal)-1)
        return legal[i]

    def leaf_evaluation(self, board: Game, s0):
        """ Perform tree policy to leaf node, and to a simualtion
        until game ends from that leaf node. Backpropagate the value """
        board.set_position(s0)
        path = self.tree_search(board)
        z = self.default_search(board)
        self.backpropagate(path, z)

    def backpropagate(self, path: list, z: int):
        """
        Update Q values in the path taken based on reward, z 
        Also update the number of visits for nodes and branches in the path
        """
        for i in range(len(path)-1):
            node = path[i]
            action = node.get_action_to(path[i+1])
            node.visits += 1
            node.branch_visist[action] += 1
            self.q[(node, action)] = (
                self.q[(node, action)]
                + (z - self.q[(node, action)]) / node.branch_visists[action]
            )

    def uct_search(self, s0):
        """ This is one move by one player in the game """
        # Her må vi kanskje legge til m, så den kjører m antall simuleringer per trekk. for i in range(m)
        self.leaf_evaluation(board, s0)
        board.set_position(s0)
        return self.select_action(board, s0, 0)

