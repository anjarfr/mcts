class Node:

    """ Node for generating tree structure """

    def __init__(self, state, parent, action):

        """ Description
        :state:         The game state in this node. Can be any type
        :parent:        Parent Node of type Node
        :action:        The action leading from the parent to this node
        :children:      List of Nodes generated from this node
        :actions:       List of actions (any type) that can be taken from this node
        :q:             Dictionary with {'action': q(s,a)} where s is self.state
        :visits:        Integer N(s). Number of times this node has been visited
        :branch_visits: Dictionary with {'action': N(s,a)}. Number of times a
                        branch from this node has been visited
        """
        self.parent = parent
        self.state = state
        self.action = action
        self.children = []
        self.actions = []
        self.q = {}
        self.visits = 1
        self.branch_visits = {}

    def insert(self, child_state, action_to_child, actions_from_child):
        """ Insert a new node into the tree. Updates the child's q and N(s,a)
        values. Appends all legal actions the child can take but no resulting
        state """
        child = Node(state=child_state, parent=self, action=action_to_child)
        child.actions = actions_from_child
        for action in actions_from_child:
            child.q[action] = 0
            child.branch_visits[action] = 0

        self.children.append(child)

    def get_node_by_state(self, state):
        if self.state == state:
            return self
        if len(self.children):
            for child in self.children:
                return self.get_node_by_state(child)
        return None

    def get_child_by_state(self, state):
        for child in self.children:
            if child.state == state:
                return child
        return None

    def get_action_to(self, chosen_child):
        for i, child in enumerate(self.children):
            if child.state == chosen_child.state:
                return self.actions[i]
