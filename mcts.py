from node import Node
from math import log, sqrt, inf
import random
from numpy import log

random.seed(2020)


class MCTS:
    """
    Monte Carlo Tree Search
    """

    def __init__(self, cfg, game, init_state, simulations):
        self.cfg = cfg
        self.game = game
        self.root = self.create_root_node(init_state)
        self.current_node = self.root
        self.simulations = simulations
        self.c = cfg["mcts"]["c"]

    def create_root_node(self, init_state):
        """ Initialize q and N(s,a) for the root node. Expand the node """
        node = Node(state=init_state, parent=None, action=None)
        legal_actions = self.game.get_legal_actions(init_state)
        node.actions = legal_actions
        for action in legal_actions:
            node.q[action] = 0
        self.expand_node(node)
        return node

    def uct_search(self, player):
        """ This is one move by one player in the game
        Return the child with highest visit count as action """
        """ Sets previous root as parent """
        self.game.player = player
        for i in range(self.simulations):
            self.simulate()
        the_chosen_one = self.select_move(self.root, c=0)

        #self.root.print_tree()
        self.root = the_chosen_one
        return the_chosen_one.action

    def simulate(self):
        """ Do a simulation from a leaf node and update its
        value based on the finite state, z, from rollout """
        path = self.sim_tree()
        z = self.sim_default()
        self.backpropagate(path, z)

    def u(self, node: Node, c: int):
        """ Exploration bonus """
        if node.visits == 0:
            return inf
        return c * 2 * sqrt(log(node.parent.visits)/node.visits)

    def select_move(self, node: Node, c: int):
        """ Returns the child of input node with the best Q + u value """

        legal = node.actions
        chosen = node.children[0]
        action = chosen.action
        best_value = node.q[action] + self.u(chosen, c)

        if self.game.player == 1:
            for i, action in enumerate(legal):
                current_node = node.children[i]
                current_value = node.q[action] + self.u(current_node, c)
                if current_value > best_value:
                    chosen = current_node
                    best_value = current_value
        else:
            for i, action in enumerate(legal):
                current_node = node.children[i]
                current_value = node.q[action] - self.u(current_node, c)
                if current_value < best_value:
                    chosen = current_node
                    best_value = current_value
        return chosen

    def sim_tree(self):  # aka tree search
        """ Find a leaf node from the current root
        node and return the path to it """
        self.current_node = self.root
        state = self.current_node.state
        path = [self.root]

        while not self.game.game_over(state):
            if not len(self.current_node.children):
                self.expand_node(self.current_node)     # Bør vi expande her?
                return path

            self.current_node = self.select_move(self.current_node, self.c)
            path.append(self.current_node)
            state = self.current_node.state
            if not self.game.game_over(state):
                self.game.change_player()

        return path

    def expand_node(self, node: Node):  # aka node expansion
        """ Find the node's children and which actions lead to them
        The insert the child and add to node's children list """
        child_states = self.game.generate_child_states(node.state)
        for sap in child_states:
            state = sap[0]
            action = sap[1]
            actions_from_child = self.game.get_legal_actions(state)
            node.insert(state, action, actions_from_child)

    def sim_default(self):  # aka leaf evaluation
        """ Perform a rollout
        Random simulation until termination
        Return end state, z """
        current_state = self.current_node.state
        while not self.game.game_over(current_state):
            new_state = self.default_policy(current_state)
            current_state = new_state[0]
            self.game.change_player()
        z = self.game.game_result()
        return z

    def default_policy(self, state):
        """ Choose a random child state """
        children = self.game.generate_child_states(state)
        i = random.randint(0, len(children) - 1)
        return children[i]

    def backpropagate(self, path: list, z: int):
        """
        Update Q values in the path taken based on reward, z
        Also update the number of visits for nodes and branches in the path
        """

        for node in path:
            action = node.action
            node.visits += 1
            node.t += z
            if node.parent:
                node.parent.q[action] += z

    def reset(self, init_state):
        self.root = self.create_root_node(init_state)
        self.current_node = self.root
