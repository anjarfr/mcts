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

    def insert(self, new_state, action, legal_actions):
        child = Node(state=new_state, parent=self, action=action)
        child.actions = legal_actions
        for action in legal_actions:
            child.q[action] = 0
            child.branch_visits[action] = 0
        
        self.children.append(child)
        self.actions.append(action)

    def get_node_by_state(self, state):
        if self.state == state:
            return self
        elif len(self.children):
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
