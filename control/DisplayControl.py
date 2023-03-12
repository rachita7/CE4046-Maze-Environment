from entity.Config import Config
from entity.Box import Box
from entity.UtilityAction import UtilityAction
from typing import List

# display the results


class DisplayControl:

    # display all configuration reuslts based on if it is value or policy
    # iteration
    @staticmethod
    def experiment_setup(is_value_iteration: bool,
                         converge_threshold: float) -> str:
        # create the initial content string
        content = DisplayControl.frame_title("Configuration Values")

        # add configuration values based on the is_value_iteration parameter
        if is_value_iteration:
            content += f"Discount Factor 'Discount' \t\t\t\t:\t{Config.DISCOUNT_FACTOR}\n"
            content += f"Constant 'c'\t\t\t\t\t\t:\t{Config.C}\n"
            content += f"Max Reward 'Rmax'\t\t\t\t\t:\t{Config.R_MAX}\n"
            content += f"Epsilon Value 'e' (c * Rmax) \t\t\t\t:\t{Config.EPSILON_VALUE}\n"
            content += f"Utility Upper Bound (Rmax / (1 - Discount))\t\t:\t{Config.UTILITY_UP_BOUND:.5g}\n"
            content += f"Convergence Threshold (e * ((1 - Discount) / Discount))\t:\t{converge_threshold:.5f}\n\n"
        else:
            content += f"Discount Factor 'Discount'\t:\t{Config.DISCOUNT_FACTOR}\n"
            content += f"Constant 'k'\t\t\t:\t{Config.K}\n\n"

        # print and return the content string
        print(content)
        return content

    # display the environment grid which is given to us in the question
    @staticmethod
    def environment_grid(grid: List[List[Box]], scale_factor: int) -> str:
        # create the initial content string
        content = DisplayControl.frame_title("Grid Environment")
        # start grid lines
        content += "|" + "----------|" * \
            (Config.COLUMN_NUM * scale_factor) + "\n"

        for row in range(Config.ROW_NUM * scale_factor):
            content += "|" + "          |" * \
                (Config.COLUMN_NUM * scale_factor) + "\n"
            content += "|"

            for column in range(Config.COLUMN_NUM * scale_factor):
                state = grid[column][row]

                # for starting point
                if column == Config.START_COL * \
                        scale_factor and row == Config.START_ROW * scale_factor:
                    temp = " Start"
                # for all walls
                elif state.is_wall():
                    temp = "Wall"
                # for green or brown squares
                elif state.get_reward() != Config.REWARD_WHITE:
                    temp = str(state.get_reward())
                    if temp[0] != '-':
                        temp = " " + temp
                else:
                    temp = "{:>4}".format("")

                # formatting the blank spaces to form the grid correctly
                n = (10 - len(temp)) // 2
                str_new = "{:<{}}".format("", n)
                content += str_new + temp + str_new + "|"

            # end the grid diagram
            content += "\n|" + "          |" * \
                (Config.COLUMN_NUM * scale_factor) + "\n"
            content += "|" + "----------|" * \
                (Config.COLUMN_NUM * scale_factor) + "\n"

        # print and return content string
        print(content)
        return content

    # display the optimal policy at each grid box

    @staticmethod
    def optimal_policy(
            utility_array: List[List[UtilityAction]], scale_factor: int) -> str:
        # create the initial content string
        content = DisplayControl.frame_title("Optimal Policy Plot")

        # loop through each row and column of utility array
        for row in range(Config.ROW_NUM * scale_factor):
            content += "\n"

            for column in range(Config.COLUMN_NUM * scale_factor):
                # get the action string for the current utility
                utility = utility_array[column][row].get_action_str()

                # calculate padding for the action string
                n = (9 - len(utility)) // 2
                str1 = "{:<{}}".format("", n - 1)

                # add action string with appropriate padding to the content
                # string
                content += "{:<{}}".format("", n) + utility + str1

        content += "\n"

        # print and return the content string
        print(content)
        return content

    # display the utilities of all non-wall states

    @staticmethod
    def final_utilities(
            grid: List[List[Box]], utility_array: List[List[UtilityAction]], scale_factor: int) -> str:
        # create the initial content string
        content = DisplayControl.frame_title(
            "Final Utilitites of All Non-Wall States")

        # loop through each state in the grid
        for column in range(Config.COLUMN_NUM * scale_factor):
            for row in range(Config.ROW_NUM * scale_factor):
                # if the state is not a wall
                if not grid[column][row].is_wall():
                    # get the utility value for the state
                    utility = "{:.8g}".format(
                        utility_array[column][row].get_utility())
                    # add the state's row and column coordinate and utility
                    # value
                    content += "({}, {}): {}\n".format(column, row, utility)

        content += "\n"

        # print and return the content string
        print(content)
        return content

    # display the utilities of all states in a grid

    @staticmethod
    def final_utilities_grid(
            utility_array: List[List[UtilityAction]], scale_factor: int) -> str:
        # create a title for the output content
        content = DisplayControl.frame_title(
            "Final Utilitites of All States (grid)")
        content += "\n"
        decimal_format = "{:.3f}".format

        # loop through each row and add a new line
        for row in range(Config.ROW_NUM * scale_factor):
            content += "\n"
            for column in range(Config.COLUMN_NUM * scale_factor):
                content += f" {decimal_format(utility_array[column][row].get_utility()):6}  "
            content += "\n"

        # print and return the content string
        print(content)
        return content

    # display the total number of iterations required

    @staticmethod
    def total_iterations(num: int) -> str:
        # create the initial content string
        content = DisplayControl.frame_title("Total Iteration Count")

        # add number of iterations to the content string
        content += f"Iterations: {num}\n"

        # print and return the content string
        print(content)
        return content

    @staticmethod
    def frame_title(str: str) -> str:
        return f"\n########## {str} ##########\n\n"
