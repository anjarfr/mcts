from game import Nim, OldGold
from mcts import MCTS
import yaml


class Player:
    def __init__(self, cfg):
        self.game = self.initialize_game(cfg)
        self.mcts = MCTS(cfg)

    def initialize_game(self, cfg):
        game_type = cfg["game"]
        if game_type == "nim":
            game = Nim(cfg)
        else:
            game = OldGold(cfg)
        return game
    
    def play_game(self):
        pass
        




def main():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    player = Player(cfg)
    player.play_game()

    # -- TESTING PURPOSES --
    og = OldGold(cfg)
    legal = og.get_legal_actions()
    og.perform_action(legal[0])


if __name__ == "__main__":
    main()
