from random import randint


class Game:
    """
    Interface for the two games, including common methods
    """

    def __init__(self, cfg):
        self.verbose = cfg["verbose"]

    def set_position(self, state):
        self.state = state

    def generate_initial_state(self):
        """
        :return: state of the initial game, as stated in configuration file
        """
        pass

    def get_legal_actions(self, state):
        """
        :param state: current state
        :return: list of legal actions from given state
        """
        pass

    def game_over(self, state):
        """
        :return: boolean
        """
        pass

    def perform_action(self, state, action, player):
        """
        :return: new game state
        """
        pass

    def game_result(self, state):
        """
        :return: int (1 or -1 depending on who won)
        """
        pass

    def generate_child_states(self, state):
        """
        :return: List containing all child states of given state
        """
        pass
    

