from nim import Nim
from old_gold import OldGold
from mcts import MCTS
import yaml
from random import randint


class StateManager:
    """
    Request state, child states and result from game
    """

    def __init__(self, cfg):
        self.game = self.initialize_game(cfg, True)
        # self.sim_game = self.initialize_game(cfg, False)
        self.initial_state = self.game.generate_initial_state(cfg)
        self.state = self.initial_state
        self.simulations = self.game.simulations
        self.player = cfg["game"]["p"]
        self.set_initial_player()

        self.mcts = MCTS(cfg, self.sim_game, self.state, self.simulations)

    def initialize_game(self, cfg, verbose):
        game_type = cfg["game"]["type"]
        if game_type == "nim":
            game = Nim(cfg, verbose)
        else:
            game = OldGold(cfg, verbose)
        return game

    def set_initial_player(self):
        if self.player == 3:
            self.player = randint(1, 2)
        if self.player not in [1, 2, 3]:
            raise Exception(
                "That is not a valid start player, please choose 1, 2 or 3. You chose {}".format(
                    self.player
                )
            )

    def set_player(self, player):
        self.player = player

    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def winner(self):
        return self.player

    def play_game(self):

        """ For each batch (= episode (?)) """
        for i in range(self.game.batch_size):

            print("New game")
            self.state = self.initial_state

            print(self.state)

            """ Play game until termination """
            while not self.game.game_over(self.state):

                """ Do simulations and perform one move """
                action = self.mcts.do_simulation(self.state, self.player)
                self.state = self.game.perform_action(self.state, action)

            self.mcts.reset(self.state, self.sim_game)


def main():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    player = StateManager(cfg)
    player.play_game()


if __name__ == "__main__":
    main()
