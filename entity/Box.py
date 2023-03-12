class Box:
    # initialize
    def __init__(self, reward):
        self.reward = reward
        self.has_wall = False

    # return the reward
    def get_reward(self):
        return self.reward

    # set the reward
    def set_reward(self, reward):
        self.reward = reward

    # return boolean depending on if its a wall or not
    def is_wall(self):
        return self.has_wall

    # set param as wall
    def set_wall(self, has_wall):
        self.has_wall = has_wall
