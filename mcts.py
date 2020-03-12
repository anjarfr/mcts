from node import Node
from math import log, sqrt
from game import Game
from random import randint


class MCTS:
    """
    Monte Carlo Tree Search
    """

    def __init__(self, cfg, game, init_state, simulations):
        self.cfg = cfg
        self.game = game
        self.root = Node(state=init_state, parent=None, action=None)
        self.current_node = self.root
        self.simulations = simulations
        self.c = cfg["mcts"]["c"]

    def uct_search(self, state, player):
        """ This is one move by one player in the game
        Return the child with highest visit count as action """
        """ Sets previous root as parent """
        self.game.player = player
        self.root = self.root.get_node_by_state(state)
        for i in range(self.simulations):
            self.simulate()
        the_chosen_one = self.select_move(self.root, c=0)
        return the_chosen_one.action

    def simulate(self):
        path = self.sim_tree()
        z = self.sim_default()
        self.backpropagate(path, z)

    def u(self, node: Node, action, c: int):
        return c * sqrt(log(node.visits) / (1 + node.branch_visist[action]))

    def select_move(self, node: Node, c: int):
        # Returns the Node with the best Q + u value
        legal = node.actions
        chosen = node.children[0]
        value = self.calculate_value(node=node, action=legal[0], c=c)
        if self.game.player == 1:
            for i, action in enumerate(legal):
                current = node.q[action] + self.u(node, action, c)
                if current > value:
                    chosen = node.children[i]
        else:
            for i, action in enumerate(legal):
                current = node.q[action] - self.u(node, action, c)
                if current < chosen:
                    chosen = current
        return chosen

    def sim_tree(self):  # aka tree search
        """  """
        state = self.current_node.state
        path = []
        while not self.game.game_over(state):
            node = self.current_node.get_node_by_state(state)
            if node is None:
                self.expand_node(self.current_node)
                return path
            self.current_node = self.select_move(node, self.c)
            path.append[self.current_node]
            state = self.current_node.state
            if not self.game.game_over(state):
                self.game.change_player()
        return path

    def expand_node(self, node: Node):  # aka node expansion
        child_states = self.game.generate_child_states(node.state)
        for sap in child_states:
            state = sap[0]
            action = sap[1]
            self.current_node.insert(state, action)

    def sim_default(self):  # aka leaf evaluation
        """ Perform a rollout
        Random simulation until termination
        Return leaf node, z """
        current_state = self.current_node.state
        while not self.game.game_over(current_state):
            child = self.default_policy()
            current_state = child.state
            self.game.change_player()
        z = self.game.game_result(current_state)
        return z

    def default_policy(self, node: Node):
        """ Choose a random child state """
        children = self.game.generate_child_states(node)
        i = randint(0, len(children) - 1)
        return children[i]

    def backpropagate(self, path: list, z: int):
        """
        Update Q values in the path taken based on reward, z
        Also update the number of visits for nodes and branches in the path
        """
        for i in range(len(path) - 1):
            node = path[i]
            action = node.get_action_to(path[i + 1])
            node.visits += 1
            node.branch_visists[action] += 1
            node.q[action] = (
                node.q[action] + (z - node.q[action]) / node.branch_visists[action]
            )

    def reset(self, state, game):
        self.root = Node(state=state, parent=None, action=None)
        self.current_node = self.root
        self.game = game
