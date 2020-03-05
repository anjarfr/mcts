from environment.nim import Nim
from environment.old_gold import OldGold
from agent.mcts import MCTS
import yaml


class StateManager:
    """
    Request state, child states and result from game
    """

    def __init__(self, cfg):
        self.game = self.initialize_game(cfg)
        self.state = self.game.state
        self.simulations = self.game.simulations

        self.mcts = MCTS(cfg, self.state, self.simulations)

    def initialize_game(self, cfg):
        game_type = cfg["game"]
        if game_type == "nim":
            game = Nim(cfg)
        else:
            game = OldGold(cfg)
        return game
    
    def play_game(self):
        for i in range(self.game.batch_size):
            self.mcts.uct_search(self.state)
            self.state = self.mcts.select_action(self.state)
        

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
