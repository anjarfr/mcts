class Game:
    def __init__(self):
        pass

    def produce_initial(self):
        pass

    def generate_child_state(self, state):
        pass

    def is_finished(self):
        pass


class Nim(Game):
    def __init__(self, init_state):
        self.pieces_left = init_state


class OldGold(Game):
    def __init__(self, init_state):
        self.board = init_state
