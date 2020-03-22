from game import Game
from copy import deepcopy


class OldGold(Game):
    def __init__(self, cfg: object, verbose):
        super().__init__(cfg, verbose)

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
        for i in range(len(state)):
            if state[i] == 0:
                for j in range(i+1, len(state)):
                    if state[j] != 0:
                        actions.append((j, i))
                        break
        return actions

    def generate_child_states(self, state):
        """ Find all child states of a state based on legal actions from state.
        Returns list of tuples, [(child state, action to child state)]"""
        if self.game_over(state):
            return None
        actions = self.get_legal_actions(state)
        child_states = []
        for action in actions:
            start = action[0]
            end = action[1]
            child_state = deepcopy(state)
            if start == end == 0:
                child_state[0] = 0
            else:
                child_state[end] = child_state[start]
                child_state[start] = 0
            child_states.append((child_state, action))
        return child_states

    def perform_action(self, state, action: tuple):
        """ Edit state based on chosen action and return resulting state """
        start = action[0]
        end = action[1]
        prev_state = deepcopy(state)
        if start == end == 0:
            state[0] = 0
        else:
            state[end] = state[start]
            state[start] = 0
        if self.verbose:
            self.print_move(prev_state, state, start, end)
        if not self.game_over(state):
            self.change_player()
        return state

    def game_over(self, state):
        return state.count(2) == 0

    def print_move(self, prev_state, state, start, end):
        coin_type = "copper" if prev_state[start] == 1 else "gold"
        if start == end == 0:
            print(
                "Player {} picks up {} coin:\t\t\t\t{}".format(
                    self.player, coin_type, state
                )
            )
        else:
            print(
                "Player {} moves {} coin from {} to {}:\t\t{}".format(
                    self.player, coin_type, start, end, state
                )
            )
