import yaml
from copy import deepcopy


class Game:
    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def winner(self):
        return self.player

    def set_position(self, state):
        self.state = state


class Nim(Game):
    def __init__(self, cfg):
        super().__init__()
        self.batch_size = cfg["nim"]["g"]
        self.player = cfg["nim"]["p"]
        self.simulations = cfg["nim"]["m"]

        self.start_stones = 0
        self.max_remove_stones = 0

        self.generate_initial_state(cfg)
        self.state = self.start_stones  # This is the state

    def generate_initial_state(self, cfg):
        start_stones = cfg["nim"]["n"]
        max_remove_stones = cfg["nim"]["k"]
        min_remove_stones = 1

        if min_remove_stones <= max_remove_stones < start_stones:
            self.start_stones = start_stones
            self.max_remove_stones = max_remove_stones
            print("Start Pile: {} stones".format(self.start_stones))
        else:
            raise Exception(
                "Maximum number of stones that can be removed needs to be less than the starting number of pieces, "
                "and bigger than 1, was {], {} and {} ".format(
                    min_remove_stones, max_remove_stones, start_stones
                )
            )

    def generate_child_states(self, state):
        if self.game_over(state):
            return None

        child_states = []
        actions = self.get_legal_actions(state)

        for action in actions:
            child_states.append(state - action)

        return child_states

    def get_legal_actions(self, state):
        limit = min(state, self.max_remove_stones)
        actions = list(range(1, limit + 1))

        return actions

    def perform_action(self, action, player):
        reward = 0

        if self.is_legal_action(action):
            self.state -= action
            self.print_move(action, player)
        else:
            raise Exception(
                "That is not a legal action. Tried to remove {} stones, from a pile of {}".format(
                    action, self.state
                )
            )

        if self.state == 0:
            print("Player {} wins".format(player))
            reward = 1 if self.player == 1 else -1

        if not self.game_over():
            self.change_player()

        return reward

    def is_legal_action(self, action):
        return 1 <= action <= self.max_remove_stones

    def game_over(self, state):
        return state == 0

    def print_move(self, action):
        s = "Player {} selects {} stones: Remaining stones = {}".format(
            self.player, action, self.state
        )
        print(s)


class OldGold(Game):
    def __init__(self, cfg: object):
        self.state = self.generate_initial_state(cfg)
        self.batch_size = cfg["oldgold"]["g"]
        self.player = cfg["oldgold"]["p"]
        self.simulations = cfg["oldgold"]["m"]
        self.verbose = cfg["verbose"]

    def generate_initial_state(self, cfg: object):
        state = cfg["oldgold"]["b_init"]
        if state.count(2) != 1:
            raise Exception(
                "There must be only one gold coin in inital state. The number of gold coins were {}".format(
                    state.count(2)
                )
            )
        return state

    def get_legal_actions(self, state):
        actions = []

        if state[0] != 0:
            actions.append((0, 0))

        i = 0
        j = i + 1
        while j <= len(state):
            while state[i] != 0:
                i += 1
                j += 1
            while state[j] == 0:
                j += 1
            actions.extend([(j, x) for x in range(i, j)])
            i = j + 1
            j = i + 1

        return actions

    def generate_child_state(self, action):
        start = action[0]
        end = action[1]
        child_state = deepcopy(self.state)

        if start == end == 0:
            child_state[0] = 0
            return child_state

        child_state[end] = child_state[start]
        child_state[start] = 0

        return child_state

    def perform_action(self, action: tuple):
        start = action[0]
        end = action[1]
        reward = 0
        prev_state = deepcopy(self.state)

        if start == end == 0:
            self.state[0] = 0
            if self.game_over():
                reward = 1 if self.player == 1 else -1
        else:
            self.state[end] = self.state[start]
            self.state[start] = 0

        if self.verbose:
            self.print_move(prev_state, self.player, start, end)

        if not self.game_over():
            self.change_player()

        return reward

    def game_over(self):
        return self.state.count(2) == 0

    def print_move(self, prev_state, start, end):
        coin_type = "copper" if prev_state[start] == 1 else "gold"
        if start == end == 0:
            print(
                "Player {} picks up {} coin: {}".format(
                    self.player, coin_type, self.state
                )
            )
        else:
            print(
                "Player {} moves {} coin from {} to {}: {}".format(
                    self.player, coin_type, start, end, self.state
                )
            )
