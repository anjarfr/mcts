from node import Node
from math import log, sqrt
from game import Game
from random import randint


class MCTS:
    """
    Monte Carlo Tree Search
    """

    def __init__(self, cfg, sim_game, init_state, simulations):
        self.cfg = cfg
        self.game = sim_game
        self.root = Node(state=init_state, parent=None)
        self.simulations = simulations

        self.sim_root = self.root
        self.c = cfg["mcts"]["c"]

    def do_simulations(self, root_state, current_player):
        """ This is one move by one player in the game
        Return the child with highest visit count as action """
        """ Sets previous root as parent"""
        self.root = Node(root_state, self.root)
        self.game.set_player(current_player)
        for i in range(self.simulations):
            self.expand_node(self.root)
            self.sim_root = self.choose_child(self.root)
            result = self.leaf_evaluation(self.sim_root)
            self.backpropagate(self.sim_root, result)
        chosen_action = self.choose_action(self.root)
        return chosen_action