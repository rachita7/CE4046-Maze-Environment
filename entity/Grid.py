from entity.Box import Box
from entity.Config import Config


class Grid:
    # initialise grid
    def __init__(self, scale_factor: int = 1):
        self.grid = None
        # scale_factor will be 1 for the main assignment question
        if scale_factor == 1:
            self.grid = [[Box(Config.REWARD_WHITE) for _ in range(
                Config.COLUMN_NUM)] for _ in range(Config.ROW_NUM)]
            self.build_grid()

        # scale_factor will be say 3 for the bonus part
        else:
            self.grid = [[Box(Config.REWARD_WHITE) for _ in range(
                Config.COLUMN_NUM * scale_factor)] for _ in range(Config.ROW_NUM * scale_factor)]
            self.build_grid(scale_factor)

    # build the grid with the reward values as given
    def build_grid(self, scale_factor=1):
        # initialise the values of all squares as the reward for white -0.4
        for row in range(Config.ROW_NUM):
            for column in range(Config.COLUMN_NUM):
                self.grid[row][column] = Box(Config.REWARD_WHITE)

        # initialise values for all wall squares as 0
        # set the set_wall() property of these squares such that the agent does
        # not traverse to them
        for wall_square in Config.SQ_WALL.split(Config.GRID_BREAK):
            wall_square = wall_square.strip()
            grid_column, grid_row = map(
                int, wall_square.split(
                    Config.ROW_COL_BREAK))
            # for main assignment
            if scale_factor == 1:
                self.grid[grid_row][grid_column].set_reward(Config.REWARD_WALL)
                self.grid[grid_row][grid_column].set_wall(True)
            # for bonus
            else:
                for i in range(grid_row * scale_factor,
                               (grid_row + 1) * scale_factor):
                    for j in range(grid_column * scale_factor,
                                   (grid_column + 1) * scale_factor):
                        self.grid[i][j].set_reward(Config.REWARD_WALL)
                        self.grid[i][j].set_wall(True)

        # initialise values for all green squares as +1
        for green_sq in Config.SQ_GREEN.split(Config.GRID_BREAK):
            green_sq = green_sq.strip()
            grid_column, grid_row = map(
                int, green_sq.split(
                    Config.ROW_COL_BREAK))
            # for main assignment
            if scale_factor == 1:
                self.grid[grid_row][grid_column].set_reward(
                    Config.REWARD_GREEN)
            # for bonus
            else:
                for i in range(grid_row * scale_factor,
                               (grid_row + 1) * scale_factor):
                    for j in range(grid_column * scale_factor,
                                   (grid_column + 1) * scale_factor):
                        self.grid[i][j].set_reward(Config.REWARD_GREEN)

        # initialise values for all brown squares as -1
        for brown_sq in Config.SQ_BROWN.split(Config.GRID_BREAK):
            brown_sq = brown_sq.strip()
            grid_column, grid_row = map(
                int, brown_sq.split(
                    Config.ROW_COL_BREAK))
            # for main assignment
            if scale_factor == 1:
                self.grid[grid_row][grid_column].set_reward(
                    Config.REWARD_BROWN)
            # for bonus
            else:
                for i in range(grid_row * scale_factor,
                               (grid_row + 1) * scale_factor):
                    for j in range(grid_column * scale_factor,
                                   (grid_column + 1) * scale_factor):
                        self.grid[i][j].set_reward(Config.REWARD_BROWN)
