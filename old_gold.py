from game import Game
from copy import deepcopy


class OldGold(Game):
    def __init__(self, cfg: object):
        super().__init__(cfg)

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

    def perform_action(self, state, action: tuple, player: int):
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
