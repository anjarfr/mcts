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
        self.root = Node(state=init_state, parent=None)
        self.current_node = self.root
        self.simulations = simulations
        self.c = cfg["mcts"]["c"]

    def do_simulations(self, state, player):
        """ This is one move by one player in the game
        Return the child with highest visit count as action """
        """ Sets previous root as parent"""
        self.root = self.root.get_node_by_state(state)
        for i in range(self.simulations):
            pass
        the_chosen_one = self.select_move(self.root, c=0)
        self.root = 0
        return the_chosen_one.action

    def u(self, node: Node, action, c: int):
        return c * sqrt(log(node.visits) / (1 + node.branch_visist[action]))

    def select_move(self, node: Node, c: int):
        # Returns the Node with the best Q + u value
        legal = node.actions
        chosen = node.children[0]
        value = self.calculate_value(node=node, action=legal[0], c=c)
        if self.player == 1:
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

    def tree_search(self, node: Node):
        """  """
        state = node.state
        game_over = self.game.game_over(state)
        path = []
        while not game_over:
            node = self.root.get_node_by_state(state)
            if Node is None:
                self.new_node(node)
                return path
            self.current_node = self.select_move(node)
            path.append[self.current_node]
            state = self.game.perform_action(state=node, self.current_node.action, )
            game_over = self.game.game_over(state)
        return path
    
    def default_search(self, sim_root: Node):
        """ Perform a rollout
        Random simulation until termination
        Return leaf node, z """
        current_state = sim_root.state
        while not self.game.game_over(current_state):
            self.game.change_player()
            child = self.default_policy(current_state)
            current_state = child
        leaf_node = current_state
        return leaf_node

    def default_policy(self, state):
        """ Choose a random child state """
        children = self.game.generate_child_states(state)
        i = randint(0, len(children) - 1)
        return children[i]
