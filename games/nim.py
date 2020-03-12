from games.game import Game


class Nim(Game):
    def __init__(self, cfg):
        super().__init__(cfg["nim"])
        self.cfg = cfg
        self.batch_size = cfg["nim"]["g"]
        self.simulations = cfg["nim"]["m"]

        self.start_stones = 0
        self.max_remove_stones = 0

        self.generate_initial_state()
        self.state = self.start_stones

    def generate_initial_state(self):
        start_stones = self.cfg["nim"]["n"]
        max_remove_stones = self.cfg["nim"]["k"]
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

    def perform_action(self, action):
        if self.is_legal_action(action):
            self.state -= action
            self.print_move(action, self.player)
        else:
            raise Exception(
                "That is not a legal action. Tried to remove {} stones, from a pile of {}".format(
                    action, self.state
                )
            )

        if not self.game_over(self.state):
            self.change_player()

        reward = self.game_result()

        return reward

    def game_result(self):
        reward = None

        if self.state == 0:
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
