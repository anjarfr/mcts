import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class Game:
    def __init__(self):
        pass

    def generate_child_state(self, state):
        pass

    def is_finished(self):
        pass

    def print(self):
        pass


class Nim(Game):
    def __init__(self):
        super().__init__()
        self.games = cfg['nim']['g']
        self.start_player = cfg['nim']['p']
        self.simulations = cfg['nim']['m']
        self.start_stones = cfg['nim']['n']
        self.remove_stones = cfg['nim']['k']

        self.remaining_stones = self.start_stones

    def init_game(self):
        print("Start Pile: {} stones".format(self.start_stones))

    def perform_action(self, action, player):
        # Action = 1 <= int <= Remove_stones
        if self.is_legal_action(action):
            self.remaining_stones -= action
            self.print_move(action, player)

    def is_legal_action(self, action):
        return 1 <= action <= self.remove_stones

    def print_move(self, action, current_player):
        s = "Player {} selects {} stones: Remaining stones = {}".format(current_player, action, self.remaining_stones)
        print(s)


class OldGold(Game):
    def __init__(self):
        super().__init__()
        self.state = cfg['oldgold']['b_init']


Nim().init_game()
Nim().perform_action(9, 2)
