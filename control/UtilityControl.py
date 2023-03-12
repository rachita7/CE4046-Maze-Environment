from entity.Action import Action
from entity.Box import Box
from entity.UtilityAction import UtilityAction
from entity.Config import Config
from control.MoveControl import MoveControl
from typing import List


class UtilityControl:
    # calculates utility for all actions
    # returns action with maximal utility
    @staticmethod
    def get_best_utility(
            column: int, row: int, curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> UtilityAction:
        utilities = sorted([
            UtilityAction(
                Action.UP,
                UtilityControl.get_up_utility(
                    column,
                    row,
                    curr_util_arr,
                    grid,
                    scale_factor)),
            UtilityAction(
                Action.DOWN,
                UtilityControl.get_down_utility(
                    column,
                    row,
                    curr_util_arr,
                    grid,
                    scale_factor)),
            UtilityAction(
                Action.LEFT,
                UtilityControl.get_left_utility(
                    column,
                    row,
                    curr_util_arr,
                    grid,
                    scale_factor)),
            UtilityAction(
                Action.RIGHT,
                UtilityControl.get_right_utility(
                    column,
                    row,
                    curr_util_arr,
                    grid,
                    scale_factor))
        ])
        return utilities[0]

    # utility for a given action
    @staticmethod
    def get_fixed_utility(action: Action, column: int, row: int,
                          action_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> UtilityAction:
        return {
            Action.UP: UtilityAction(Action.UP, UtilityControl.get_up_utility(column, row, action_util_arr, grid, scale_factor)),
            Action.DOWN: UtilityAction(Action.DOWN, UtilityControl.get_down_utility(column, row, action_util_arr, grid, scale_factor)),
            Action.LEFT: UtilityAction(Action.LEFT, UtilityControl.get_left_utility(column, row, action_util_arr, grid, scale_factor)),
            Action.RIGHT: UtilityAction(
                Action.RIGHT, UtilityControl.get_right_utility(
                    column, row, action_util_arr, grid, scale_factor))
        }[action]

    # Bellman update function to estimate next utilities
    @staticmethod
    def estimate_next_utilities(
            util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> List[List[UtilityAction]]:
        # create empty utility array
        curr_util_arr = [[UtilityAction() for row in range(Config.ROW_NUM * scale_factor)]
                         for column in range(Config.COLUMN_NUM * scale_factor)]
        new_util_arr = [[UtilityAction() for row in range(Config.ROW_NUM * scale_factor)]
                        for column in range(Config.COLUMN_NUM * scale_factor)]

        # save the current utility array to a new utility array
        for row in range(Config.ROW_NUM * scale_factor):
            for column in range(Config.COLUMN_NUM * scale_factor):
                new_util_arr[column][row] = UtilityAction(
                    util_arr[column][row].action, util_arr[column][row].utility)

        for k in range(Config.K):
            # copy  new utility array into current utility array
            for i in range(len(new_util_arr)):
                curr_util_arr[i] = new_util_arr[i][:]

            # update the utility for each state
            for row in range(Config.ROW_NUM * scale_factor):
                for column in range(Config.COLUMN_NUM * scale_factor):
                    if not grid[column][row].is_wall():
                        action = curr_util_arr[column][row].action
                        new_util_arr[column][row] = UtilityControl.get_fixed_utility(
                            action, column, row, curr_util_arr, grid, scale_factor)

        return new_util_arr

    # overall utility for wishing to go up
    @staticmethod
    def get_up_utility(column: int, row: int,
                       curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> float:
        # initialise
        action_up_utility = 0.000

        # utility to go up, move right and left
        action_up_utility += Config.MAIN_PROB * \
            MoveControl.agent_move_up(column, row, curr_util_arr, grid)
        action_up_utility += Config.RIGHT_PROB * \
            MoveControl.agent_move_right(
                column, row, curr_util_arr, grid, scale_factor)
        action_up_utility += Config.LEFT_PROB * \
            MoveControl.agent_move_left(column, row, curr_util_arr, grid)

        # final utility calculated
        action_up_utility = grid[column][row].get_reward(
        ) + Config.DISCOUNT_FACTOR * action_up_utility

        return action_up_utility

    # overall utility for wishing to go down
    @staticmethod
    def get_down_utility(
            column: int, row: int, curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> float:
        # initialise
        action_down_utility = 0.000

        # utility to go down, move left and right
        action_down_utility += Config.MAIN_PROB * \
            MoveControl.agent_move_down(
                column, row, curr_util_arr, grid, scale_factor)
        action_down_utility += Config.LEFT_PROB * \
            MoveControl.agent_move_left(column, row, curr_util_arr, grid)
        action_down_utility += Config.RIGHT_PROB * \
            MoveControl.agent_move_right(
                column, row, curr_util_arr, grid, scale_factor)

        # final utility calculated
        action_down_utility = grid[column][row].get_reward(
        ) + Config.DISCOUNT_FACTOR * action_down_utility

        return action_down_utility

    # overall utility for wishing to go left
    @staticmethod
    def get_left_utility(
            column: int, row: int, curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> float:
        # initialise
        action_left_utility = 0.000

        # utility to go left, move up and down
        action_left_utility += Config.MAIN_PROB * \
            MoveControl.agent_move_left(column, row, curr_util_arr, grid)
        action_left_utility += Config.RIGHT_PROB * \
            MoveControl.agent_move_up(column, row, curr_util_arr, grid)
        action_left_utility += Config.LEFT_PROB * \
            MoveControl.agent_move_down(
                column, row, curr_util_arr, grid, scale_factor)

        # final utility calculated
        action_left_utility = grid[column][row].get_reward(
        ) + Config.DISCOUNT_FACTOR * action_left_utility

        return action_left_utility

    # overall utility for wishing to go right
    @staticmethod
    def get_right_utility(
            column: int, row: int, curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> float:
        # initialise
        action_right_utility = 0.000

        # utility to go right, move down and up
        action_right_utility += Config.MAIN_PROB * \
            MoveControl.agent_move_right(
                column, row, curr_util_arr, grid, scale_factor)
        action_right_utility += Config.RIGHT_PROB * \
            MoveControl.agent_move_down(
                column, row, curr_util_arr, grid, scale_factor)
        action_right_utility += Config.LEFT_PROB * \
            MoveControl.agent_move_up(column, row, curr_util_arr, grid)

        # final utility calculated
        action_right_utility = grid[column][row].get_reward(
        ) + Config.DISCOUNT_FACTOR * action_right_utility

        return action_right_utility
