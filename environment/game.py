from random import randint


class Game:
    """
    Interface for the two games, including common methods
    """

    def __init__(self, cfg):
        self.player = cfg["p"]
        self.set_initial_player()
        self.state = 0

    def set_initial_player(self):
        if self.player == 3:
            self.player = randint(1, 2)
        if self.player not in [1, 2, 3]:
            raise Exception(
                "That is not a valid start player, please choose 1, 2 or 3. You chose {}".format(self.player)
            )

    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def winner(self):
        return self.player

    def set_position(self, state):
        self.state = state

    def generate_initial_state(self):
        """
        :return: state of the initial game
        """
        pass

    def get_legal_actions(self, state):
        """
        :param state:
        :return: list of legal actions from given state
        """
        pass

    def game_over(self, state):
        """
        :return: boolean
        """
        pass

    def perform_action(self, state, action):
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



