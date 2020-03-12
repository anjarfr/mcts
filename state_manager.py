from nim import Nim
from old_gold import OldGold
from mcts import MCTS
import yaml


class StateManager:
    """
    Request state, child states and result from game
    """

    def __init__(self, cfg):
        self.verbose = cfg["verbose"]
        self.game = self.initialize_game(cfg, verbose=self.verbose)
        self.initial_state = self.game.generate_initial_state(cfg)
        self.sim_game = self.initialize_game(cfg, verbose=False)
        self.sim_game.generate_initial_state(cfg)
        self.state = self.initial_state
        self.batch_size = cfg["game"]["g"]
        self.simulations = cfg["game"]["m"]
        self.mcts = MCTS(cfg, self.sim_game, self.state, self.simulations)

    def initialize_game(self, cfg, verbose):
        game_type = cfg["game"]["type"]
        if game_type == "nim":
            game = Nim(cfg, verbose)
        else:
            game = OldGold(cfg, verbose)
        return game

    def play_game(self):
        for i in range(self.batch_size):
            if self.verbose:
                print("\n---- New game, {} ----".format(i + 1))
                print("Initial state is {}".format(self.initial_state))
            while not self.game.game_over(self.state):
                # Do simulations and perform one move
                action = self.mcts.uct_search(self.state, self.game.player)
                self.state = self.game.perform_action(self.state, action)
            self.mcts.reset(self.initial_state)
            self.state = self.initial_state
            self.game.player = self.game.initial_player


def main():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    player = StateManager(cfg)
    player.play_game()


if __name__ == "__main__":
    main()
