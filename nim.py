from game import Game


class Nim(Game):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.max_remove_stones = 1

    def generate_initial_state(self, cfg):
        start_stones = self.cfg["nim"]["n"]
        max_remove_stones = self.cfg["nim"]["k"]
        min_remove_stones = 1

        if min_remove_stones <= max_remove_stones < start_stones:
            state = start_stones
            self.max_remove_stones = max_remove_stones
            if self.verbose:
                print("Start Pile: {} stones".format(self.start_stones))
        else:
            raise Exception(
                "Maximum number of stones that can be removed needs to be less than the starting number of pieces, "
                "and bigger than 1, was {], {} and {} ".format(
                    min_remove_stones, max_remove_stones, start_stones
                )
            )
        return state

    def generate_child_states(self, state):
        if self.game_over(state):
            return None

        child_states = []
        actions = self.get_legal_actions(state)

        for action in actions:
            child_states.append(state - action)

        return child_states

    def get_action(self, start_state, end_state):
        return start_state - end_state

    def get_legal_actions(self, state):
        limit = min(state, self.max_remove_stones)
        actions = list(range(1, limit + 1))

        return actions

    def perform_action(self, state, action, player: int):
        if self.is_legal_action(action):
            self.state -= action
            if self.verbose:
                self.print_move(action, self.player)
        else:
            raise Exception(
                "That is not a legal action. Tried to remove {} stones, from a pile of {}".format(
                    action, self.state
                )
            )

        if not self.game_over(self.state):
            self.change_player()

        return self.state

    def game_result(self, state):
        reward = None

        if state == 0:
            if self.verbose:
                print("Player {} wins".format(self.player))
            reward = 1 if self.player == 1 else -1

        return reward

    def is_legal_action(self, action):
        return 1 <= action <= self.max_remove_stones

    def game_over(self, state):
        return state == 0

    def print_move(self, action, player):
        s = "Player {} selects {} stones: Remaining stones = {}".format(
            player, action, self.state
        )
        print(s)
