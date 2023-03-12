import random


class Action:

    # Movement ALL_ACTIONS
    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"

    # get random
    RAND = random.Random()
    # define list of all possible actions
    ALL_ACTIONS = [UP, DOWN, LEFT, RIGHT]
    # total number of actions
    SIZE = len(ALL_ACTIONS)

    # initialise
    def __init__(self, temp):
        self.temp = temp

    def __str__(self):
        return self.temp

    # get any of the 4 actions at random
    @staticmethod
    def get_random_action():
        return Action.ALL_ACTIONS[Action.RAND.randint(0, Action.SIZE - 1)]
