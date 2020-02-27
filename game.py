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

        self.start_stones = 0
        self.max_remove_stones = 0

        self.generate_initial_state()
        self.remaining_stones = self.start_stones  # This is the state

    def generate_initial_state(self):
        start_stones = cfg['nim']['n']
        max_remove_stones = cfg['nim']['k']
        min_remove_stones = 1

        if min_remove_stones <= max_remove_stones < start_stones:
            self.start_stones = start_stones
            self.max_remove_stones = max_remove_stones
            print("Start Pile: {} stones".format(self.start_stones))
        else:
            raise Exception(
                "Maximum number of stones that can be removed needs to be less than the starting number of pieces, "
                "and bigger than 1, was {], {} and {} ".format(min_remove_stones, max_remove_stones, start_stones)
            )

    def get_legal_actions(self):
        limit = min(self.remaining_stones, self.max_remove_stones)
        actions = list(range(1, limit))

        return actions

    def perform_action(self, action, player):
        reward = 0

        if self.is_legal_action(action):
            self.remaining_stones -= action
            self.print_move(action, player)
        else:
            raise Exception(
                "That is not a legal action. Tried to remove {} stones, from a pile of {}".format(
                    action, self.remaining_stones)
            )

        if self.is_finished():
            print("Player {} wins".format(player))
            reward = 100

        return reward

    def is_legal_action(self, action):
        return 1 <= action <= self.max_remove_stones

    def is_finished(self):
        return self.remaining_stones == 0

    def print_move(self, action, current_player):
        s = "Player {} selects {} stones: Remaining stones = {}".format(current_player, action, self.remaining_stones)
        print(s)


class OldGold(Game):
    def __init__(self):
        super().__init__()
        self.state = cfg['oldgold']['b_init']



