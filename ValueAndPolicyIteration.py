from typing import List, Tuple
import numpy as np

from entity.UtilityAction import UtilityAction
from entity.Config import Config
from entity.Grid import Grid
from entity.Box import Box
from entity.Action import Action

from control.DisplayControl import DisplayControl
from control.FileControl import FileControl
from control.UtilityControl import UtilityControl


def value_iteration(grid: List[List[Box]]) -> Tuple[List[UtilityAction], int]:
    """
    Value Iteration algorithm is applied to the given grid environment to compute the optimal plot as well as the optimal utility of each state.

    Args:
        grid (List[List[Box]]): grid representing the set-up environment.

    Returns:
        A Tuple containing:
        - List of UtilityAction: list containing the utilities at each iteration.
        - int: number of iterations performed before convergence.
    """

    # initializing variables
    utility_list = []
    curr_util_arr = np.zeros(
        (Config.COLUMN_NUM *
         Config.SCALE_FACTOR,
         Config.ROW_NUM *
         Config.SCALE_FACTOR),
        dtype=UtilityAction)
    new_util_arr = np.zeros(
        (Config.COLUMN_NUM *
         Config.SCALE_FACTOR,
         Config.ROW_NUM *
         Config.SCALE_FACTOR),
        dtype=UtilityAction)

    # initializing new utility array keeping the UtilityAction values
    for column in range(Config.COLUMN_NUM * Config.SCALE_FACTOR):
        for row in range(Config.ROW_NUM * Config.SCALE_FACTOR):
            new_util_arr[column][row] = UtilityAction()

    # iteration variables
    delta = np.inf
    iterations = 0

    # iterating until convergence is reached
    while delta >= Config.CONV_THRESHOLD:
        iterations += 1

        # resetting delta
        delta = np.finfo(float).min

        # storing a copy of current utilities
        curr_util_arr = new_util_arr.copy()
        utility_list.append(curr_util_arr.copy())

        # updating utility value of each state
        for row in range(Config.ROW_NUM * Config.SCALE_FACTOR):
            for column in range(Config.COLUMN_NUM * Config.SCALE_FACTOR):
                if not grid[column][row].is_wall():
                    new_util_arr[column][row] = UtilityControl.get_best_utility(
                        column, row, curr_util_arr, grid, Config.SCALE_FACTOR)

                    updated_util = new_util_arr[column][row].get_utility()
                    current_util = curr_util_arr[column][row].get_utility()

                    # calculating delta for this state
                    updated_delta = abs(updated_util - current_util)

                    delta = max(delta, updated_delta)

    return utility_list, iterations

def policy_iteration(grid: List[List[Box]]) -> Tuple[List[UtilityAction], int]:
    """
    Policy Iteration algorithm is applied to the given grid environment to compute the optimal plot as well as the optimal utility of each state.

    Args:
        grid (List[List[Box]]): grid representing the set-up environment.

    Returns:
        A Tuple containing:
        - List of UtilityAction: list containing the utilities at each iteration.
        - int: number of iterations performed before convergence.
    """

    # initializing variables
    utility_list = []
    curr_util_arr = np.zeros(
        (Config.COLUMN_NUM * Config.SCALE_FACTOR, Config.ROW_NUM * Config.SCALE_FACTOR), dtype=UtilityAction
    )
    new_util_arr = np.zeros(
        (Config.COLUMN_NUM * Config.SCALE_FACTOR, Config.ROW_NUM * Config.SCALE_FACTOR), dtype=UtilityAction
    )

    # randomly initialize utility values and actions for all non-wall boxes
    for column in range(Config.COLUMN_NUM*Config.SCALE_FACTOR):
        for row in range(Config.ROW_NUM*Config.SCALE_FACTOR):
            new_util_arr[column][row] = UtilityAction()
            if not grid[column][row].is_wall():
                random_action = Action.get_random_action()
                new_util_arr[column][row].set_action(random_action)

    # iterating until convergence is reached
    unchanged = False
    iterations = 0
    while not unchanged:
        # storing a copy of current utilities
        curr_util_arr = new_util_arr.copy()
        utility_list.append(curr_util_arr.copy())

        # computing  next utilities based on the current policy
        new_util_arr = UtilityControl.estimate_next_utilities(curr_util_arr, grid, Config.SCALE_FACTOR)

        # updating policy if a better action is found
        unchanged = True
        for row in range(Config.ROW_NUM*Config.SCALE_FACTOR):
            for column in range(Config.COLUMN_NUM*Config.SCALE_FACTOR):
                if not grid[column][row].is_wall():
                    # checking if a better action is available
                    best_action_util = UtilityControl.get_best_utility(column, row, new_util_arr, grid, Config.SCALE_FACTOR)
                    policy_action = new_util_arr[column][row].get_action()
                    policy_action_util = None
                    if policy_action == Action.UP:
                        policy_action_util = UtilityAction(Action.UP, UtilityControl.get_up_utility(column, row, new_util_arr, grid, Config.SCALE_FACTOR))
                    elif policy_action == Action.DOWN:
                        policy_action_util = UtilityAction(Action.DOWN, UtilityControl.get_down_utility(column, row, new_util_arr, grid, Config.SCALE_FACTOR))
                    elif policy_action == Action.LEFT:
                        policy_action_util = UtilityAction(Action.LEFT, UtilityControl.get_left_utility(column, row, new_util_arr, grid, Config.SCALE_FACTOR))
                    elif policy_action == Action.RIGHT:
                        policy_action_util = UtilityAction(Action.RIGHT, UtilityControl.get_right_utility(column, row, new_util_arr, grid, Config.SCALE_FACTOR))

                    # update policy if a better action is found
                    if best_action_util.get_utility() > policy_action_util.get_utility():
                        new_util_arr[column][row].set_action(best_action_util.get_action())
                        unchanged = False
        iterations += 1

    return utility_list, iterations


def display_results(
        grid: List[List[Box]], optimal_policy: np.ndarray, iterations: int, is_value_iteration: bool) -> str:
    """
    Returns a string containing the various outputs such as optimal policy and final utilities.
    
    Args:
    - grid (List[List[Box]]): 2D list of Box objects representing the environment.
    - optimal_policy (np.ndarray): numpy array representing the optimal policy path in the grid.
    - iterations (int): total number of iterations in which convergence occurs.
    - is_value_iteration (bool): to represent if its value iteration (True) or policy iteration (False).
    Returns:
    - str: string containing the results of various display controls.
    """
    # create a list of outputs to be displayed
    content = [
        # display the config values
        DisplayControl.experiment_setup(is_value_iteration, Config.CONV_THRESHOLD),
        # display the grid environment- walls, +1 and -1
        DisplayControl.environment_grid(grid, Config.SCALE_FACTOR),
        # display optimal policy path in grid
        DisplayControl.optimal_policy(optimal_policy, Config.SCALE_FACTOR),
        # display final utilites of the grid elements
        DisplayControl.final_utilities(
            grid, optimal_policy, Config.SCALE_FACTOR),
        # display final utilites of the grid elements (grid format)
        DisplayControl.final_utilities_grid(
            optimal_policy, Config.SCALE_FACTOR),
        # display total iterations in which convergence occurs
        DisplayControl.total_iterations(iterations)
    ]
    # concatenate all display controls and return as string
    return ''.join(content)


if __name__ == '__main__':

    while True:
        grid_environment = Grid(Config.SCALE_FACTOR)
        grid = grid_environment.grid
        
        print("# ------ CZ/CE4046 Intelligent Agents | Assignment 1 ------ #")
        print("")
        print("# ------------------------- MENU -------------------------- #")
        print("")
        print("Please select an option:")
        print("     1.   Value Iteration")
        print("     2.   Policy Iteration")
        print("     3.   Bonus Question")
        print("     4.   Exit")
        
        option = input()
        
        if option == "1":
            # Perform value iteration
            print("Performing value iteration...")
            is_value_iteration = True
            utility_list, iterations = value_iteration(grid)
            optimal_policy = utility_list[-1]
            config_info = display_results(grid, optimal_policy, iterations, is_value_iteration)

            # Save the output
            FileControl.write_to_text(
                config_info,
                is_value_iteration,
                Config.SCALE_FACTOR) # Config.SCALE_FACTOR is set to 1
            FileControl.write_to_csv(utility_list, Config.SCALE_FACTOR, is_value_iteration)
            
        elif option == "2":
            # Perform policy iteration
            print("Performing policy iteration...")
            is_value_iteration = False
            utility_list, iterations = policy_iteration(grid)
            optimal_policy = utility_list[-1]
            config_info = display_results(grid, optimal_policy, iterations, is_value_iteration)

            # Save the output
            FileControl.write_to_text(
                config_info,
                is_value_iteration,
                Config.SCALE_FACTOR) # Config.SCALE_FACTOR is set to 1
            FileControl.write_to_csv(utility_list, Config.SCALE_FACTOR, is_value_iteration)
            
        elif option == "3":
            # Ask the user to input scale factor
            scale = input("Please enter the scale factor (3 or 6): ")
            
            if scale not in ["3", "6"]:
                print("Invalid scale factor entered. Please try again.")
                continue
            
            # Perform both value and policy iteration suing the inputted scale factor
            print("Performing both value and policy iteration with scale factor =", scale)

            scale = int(scale)
            # Config.SCALE_FACTOR = scale
            print("")
            print("Performing value iteration...")
            is_value_iteration = True
            utility_list, iterations = value_iteration(grid)
            optimal_policy = utility_list[-1]
            config_info = display_results(grid, optimal_policy, iterations, is_value_iteration)

            # Save the output
            FileControl.write_to_text(
                config_info,
                is_value_iteration,
                Config.SCALE_FACTOR)
            FileControl.write_to_csv(utility_list, Config.SCALE_FACTOR, is_value_iteration)

            print("")
            print("Performing policy iteration...")
            is_value_iteration = False
            utility_list, iterations = policy_iteration(grid)
            optimal_policy = utility_list[-1]
            config_info = display_results(grid, optimal_policy, iterations, is_value_iteration)

            # Save the output
            FileControl.write_to_text(
                config_info,
                is_value_iteration,
                Config.SCALE_FACTOR)
            FileControl.write_to_csv(utility_list, Config.SCALE_FACTOR, is_value_iteration)
            
        elif option == "4":
            # Exit the program
            print("Exiting program...")
            break
            
        else:
            # Invalid option selected
            print("Invalid option selected. Please try again.")
