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

    # def new_node(self, s0: Node, state, action, legal: list):
    #     s0.insert(state, action)
    #     new_node = s0.children[-1]
    #
    #     new_node.actions.extend(legal)
    #     for action in legal:
    #         new_node.branch_visists[action] = 0
    #         self.q[(new_node, action)] = 0
    #

    def calculate_u(self, node: Node, action, c: int):
        return c * sqrt(log(node.visits) / (1 + node.branch_visist[action]))
    
    def select_action(self, board: Game, node: Node, c: int):
        legal = board.get_legal_actions()
        chosen = self.target_policy[(node, legal[0])]
        if board.player == 1:
            for action in legal:
                current = self.q[(node, action)] + self.calculate_u(node, action, c)
                if current > chosen:
                    chosen = current
        else:
            for action in legal:
                current = self.q[(node, action)] - self.calculate_u(node, action, c)
                if current > chosen:
                    chosen = current
        return chosen
    
    # def tree_search(self, board: Game):
    #     c = self.c
    #     t = 0
    #     a = None
    #     path = []
    #     while not board.game_over(self.root):
    #         s = board.state
    #         node = self.root.get_node_by_state(s)
    #         path.append(node)
    #         if node is None:
    #             legal = board.get_legal_actions()
    #             self.new_node(s, a, legal)
    #             return path
    #         a = self.select_action(board, s, c)
    #         board.perform_action(a)
    #         t += 1
    #     return path

    # def leaf_evaluation(self, board: Game, s0):
    #     """ Perform tree policy to leaf node, and to a simualtion
    #     until game ends from that leaf node. Backpropagate the value """
    #
    #     board.set_position(s0)
    #     path = self.tree_search(board)
    #     z = self.default_search(board)
    #     self.backpropagate(path, z)
    #
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

    def reset(self, state, sim_game):
        self.root = Node(state=state, parent=None)
        self.sim_root = self.root
        self.game = sim_game

    def expand_node(self, node):
        """ Generating child states and connecting them to parent
        Also adding them to the tree policy"""
        children = self.game.generate_child_states(node.state)
        for child in children:
            node.insert(child)

    # def choose_child(self, node):
    #     """ Choose child with highest visit count"""
    #     current_node = node
    #     while len(current_node.children) != 0:
    #         self.game.change_player()
    #         highest_visit = 0
    #         highest_node = current_node.children[0]
    #         for child in current_node.children:
    #             if child.visits > highest_visit:
    #                 highest_visit = child.visits
    #                 highest_node = child
    #         current_node = highest_node
    #     return current_node

    def default_search(self, sim_root: Node):
        """ Perform a rollout
        Random simulation until termination
        Return leaf node"""
        current_state = sim_root.state
        while not self.game.game_over(current_state):
            print("Not finished")
            self.game.change_player()
            child = self.default_policy(current_state)
            current_state = child
        print("Finihsed!")
        leaf_node = current_state
        return leaf_node

    def default_policy(self, state):
        """ Choose a random child state """
        children = self.game.generate_child_states(state)
        i = randint(0, len(children) - 1)
        return children[i]

    def leaf_evaluation(self, sim_root):
        """ Return result of terminated game by doing a default search """
        leaf_node = self.default_search(sim_root)
        result = self.game.game_result(leaf_node)
        return result

    def backpropagate(self, sim_root: Node, result: int):
        current_node = sim_root
        while current_node.parent is not None:
            current_node.increase_visits()
            current_node.q += (result - current_node.q) / current_node.visits
            current_node = current_node.parent

    def choose_action(self, root: Node):
        succ_node = self.choose_child(root)
        action = self.game.get_action(root.state, succ_node.state)
        return action

    def do_simulation(self, root_state, current_player):
        """ This is one move by one player in the game
        Return the child with highest visit count as action """
        """ Sets previous root as parent"""
        self.root = Node(root_state, self.root)
        for i in range(self.simulations):
            self.expand_node(self.root)
            self.sim_root = self.choose_child(self.root)
            result = self.leaf_evaluation(self.sim_root)
            self.backpropagate(self.sim_root, result)
        chosen_action = self.choose_action(self.root)
        return chosen_action

