import yaml

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
    def __init__(self, cfg):
        self.state = cfg['nim']['n']
        self.k = cfg['nim']['k']
    

class OldGold(Game):
    def __init__(self, cfg):
        self.state = cfg['oldgold']['b_init']

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
og = OldGold(cfg)
