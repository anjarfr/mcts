from games.nim import Nim
from games.old_gold import OldGold
from agent.mcts import MCTS
import yaml


class StateManager:
    def __init__(self, cfg):
        self.game = self.initialize_game(cfg)
        self.actual_state = self.game.state
        self.mcts = MCTS(cfg, self.actual_state)
        self.sim_state = None

    def initialize_game(self, cfg):
        game_type = cfg["game"]
        if game_type == "nim":
            game = Nim(cfg)
        else:
            game = OldGold(cfg)
        return game

    def play_game(self):
        for i in range(self.game.batch_size):
            while not self.actual_game.game_over():
                self.mcts.uct_search()


def main():
    with open("../config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    player = StateManager(cfg)
    player.play_game()

    # -- TESTING PURPOSES --
    og = OldGold(cfg)
    legal = og.get_legal_actions()
    og.perform_action(legal[0])


if __name__ == "__main__":
    main()
