from nim import Nim
from old_gold import OldGold
from mcts import MCTS
import yaml
from copy import deepcopy


class StateManager:
    """
    Request state, child states and result from game
    """

    def __init__(self, cfg):
        self.game = self.initialize_game(cfg)
        self.initial_state = self.game.generate_initial_state(cfg)
        self.sim_game = deepcopy(self.game)
        self.state = self.initial_state
        self.batch_size = cfg["game"]["g"]
        self.simulations = cfg["game"]["m"]
        self.mcts = MCTS(cfg, self.sim_game, self.state, self.simulations)

    def initialize_game(self, cfg):
        game_type = cfg["game"]["type"]
        if game_type == "nim":
            game = Nim(cfg)
        else:
            game = OldGold(cfg)
        return game

    def play_game(self):
        for i in range(self.batch_size):
            self.state = self.initial_state
            while not self.game.game_over(self.state):
                # Do simulations and perform one move
                action = self.mcts.uct_search(self.state, self.game.player)
                self.state = self.game.perform_action(self.state, action)
            self.mcts.reset(self.state, self.sim_game)


def main():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    player = StateManager(cfg)
    player.play_game()


if __name__ == "__main__":
    main()
