import yaml
import deepcopy

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
    def __init__(self, cfg: object):
        self.state = cfg["nim"]["n"]
        self.k = cfg["nim"]["k"]


class OldGold(Game):
    def __init__(self, cfg: object):
        self.state = self.generate_initial_state(cfg)
        self.batch_size = cfg["oldgold"]["g"]
        self.player = cfg["oldgold"]["p"]
        self.simulations = cfg["oldgold"]["m"]

    def generate_initial_state(self, cfg: object):
        state = cfg["oldgold"]["b_init"]
        if state.count(2) != 1:
            raise Exception(
                "There must be only one gold coin in inital state. The number of gold coins were {}".format(
                    state.count(2)
                )
            )
        return state

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

    def get_legal_actions(self):
        actions = []

        if self.state[0] != 0:
            actions.append((0, 0))

        i = 0
        j = i + 1
        while j <= len(self.state):
            while self.state[i] != 0:
                i += 1
                j += 1
            while self.state[j] == 0:
                j += 1
            actions.extend([(j, x) for x in range(i, j)])
            i = j + 1
            j = i + 1

        return actions

    def perform_action(self, action: tuple):
        start = action[0]
        end = action[1]
        reward = 0

        if start == end == 0:
            self.state[0] = 0
            if self.is_finished():
                reward = 1
            return reward

        self.state[end] = self.state[start]
        self.state[start] = 0

        return reward

    def is_finished(self):
        return self.state.count(2) == 0


og = OldGold(cfg)
print(og.get_legal_actions())
