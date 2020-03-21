from node import Node
import random

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
        # self.expand_node(node)
        return node

    def expand_node(self, node: Node):  # aka node expansion
        """ Find the node's children and which actions lead to them
        The insert the child and add to node's children list """

        node.expanded = True
        child_states = self.game.generate_child_states(node.state)
        for sap in child_states:
            state = sap[0]
            action = sap[1]
            node.insert(state, action)

    def uct_search(self, player):
        """ This is one move by one player in the game
        Return the child with highest visit count as action """
        """ Sets previous root as parent """

        for i in range(self.simulations):
            self.game.set_player(player)
            self.current_node = self.root
            self.simulate()

        the_chosen_one = self.select_move(self.root, c=0)

        self.root = the_chosen_one
        return the_chosen_one.action

    def simulate(self):
        """ Do a simulation from a leaf node and update its
        value based on the finite state, z, from rollout """

        path = self.sim_tree()  # Her
        z = self.sim_default()
        self.backpropagate(path, z)

    def fully_expanded(self, node: Node):
        actions = len(self.game.get_legal_actions(node.state))
        children = len(node.children)

        expanded = actions == children
        if expanded:
            node.expanded = True

        return expanded

    def sim_tree(self):  # aka tree search
        """ Find a leaf node from the current root
        node and return the path to it """

        state = self.current_node.state
        path = [self.current_node]

        while not self.game.game_over(state):

            if not self.fully_expanded(self.current_node):

                child_states = self.game.generate_child_states(self.current_node.state)
                existing_child_actions = list(self.current_node.children.keys())

                missing_child_actions = []

                for sap in child_states:
                    action = sap[1]
                    if action not in existing_child_actions:
                        state = sap[0]
                        missing_child_actions.append((state, action))

                chosen = random.choice(missing_child_actions)
                self.current_node.insert(chosen[0], chosen[1])
                self.current_node = self.current_node.children[chosen[1]]
                state = self.current_node.state

                path.append(self.current_node)

                if not self.game.game_over(state):
                    self.game.change_player()

                return path

            else:
                self.current_node = self.select_move(self.current_node, self.c)
                path.append(self.current_node)
                state = self.current_node.state

            if not self.game.game_over(state):
                self.game.change_player()

        return path

    def select_move(self, node: Node, c: int):
        """ Returns the child of input node with the best Q + u value """

        legal = node.actions
        chosen_key = random.choice(list(node.children.keys()))
        chosen = node.children[chosen_key]

        best_value = chosen.Q() + chosen.U(c)

        if self.game.player == 1:
            for action in legal:
                current_node = node.children[action]
                current_value = current_node.Q() + current_node.U(c)

                if current_value > best_value:
                    chosen = current_node
                    best_value = current_value
        else:
            for action in legal:
                current_node = node.children[action]
                current_value = current_node.Q() - current_node.U(c)

                if current_value < best_value:
                    chosen = current_node
                    best_value = current_value

        return chosen

    def sim_default(self):  # aka leaf evaluation
        """ Perform a rollout
        Random simulation until termination
        Return end state, z """
        current_state = self.current_node.state

        while not self.game.game_over(current_state):
            new_state = self.default_policy(current_state)
            current_state = new_state[0]

            if not self.game.game_over(current_state):
                self.game.change_player()

        z = self.game.game_result()
        return z

    def default_policy(self, state):
        """ Choose a random child state """
        children = self.game.generate_child_states(state)
        chosen_child = random.choice(children)
        return chosen_child

    def backpropagate(self, path: list, z: int):
        """
        Update Q values in the path taken based on reward, z
        Also update the number of visits for nodes and branches in the path
        """

        for node in path:
            node.visits += 1
            node.t += z

    def reset(self, init_state):
        self.root = self.create_root_node(init_state)
        self.current_node = self.root
