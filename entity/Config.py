class Config:
    # Grid world dimensions
    COLUMN_NUM = 6
    ROW_NUM = 6

    # Starting position of agent
    START_COL = 2
    START_ROW = 3

    # Reward function values
    REWARD_WHITE = -0.040
    REWARD_GREEN = +1.000
    REWARD_BROWN = -1.000
    REWARD_WALL = 0.000

    # Probabilities for transition model
    MAIN_PROB = 0.800
    LEFT_PROB = 0.100
    RIGHT_PROB = 0.100

    # Breaks for the grid and row, column
    GRID_BREAK = ";"
    ROW_COL_BREAK = ","

    # row, column information for the grid world
    SQ_GREEN = "0,0; 0,2; 0,5; 1,3; 2,4; 3,5"
    SQ_BROWN = "1,1; 1,5; 2,2; 3,3; 4,4"
    SQ_WALL = "0,1; 1,4; 4,1; 4,2; 4,3"

    # Variables
    DISCOUNT_FACTOR = 0.990
    R_MAX = 1.000
    C = 0.1  # constant which adjusts maximum error allowed
    EPSILON_VALUE = C * R_MAX
    UTILITY_UP_BOUND = R_MAX / (1 - DISCOUNT_FACTOR)
    CONV_THRESHOLD = EPSILON_VALUE * \
        ((1.000 - DISCOUNT_FACTOR) / DISCOUNT_FACTOR)
    K = 50  # times we apply the Bellman update to produce next utility estimate

    # For BONUS section use values such as 3,6 etc in MENU
    SCALE_FACTOR = 3
