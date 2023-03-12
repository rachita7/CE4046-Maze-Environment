from entity.Box import Box
from entity.UtilityAction import UtilityAction
from entity.Config import Config
from typing import List


class MoveControl:
    # agent moves upwards
    @staticmethod
    def agent_move_up(column: int, row: int,
                      curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]]) -> float:
        if row - 1 >= 0 and not grid[column][row - 1].is_wall():
            return curr_util_arr[column][row - 1].get_utility()
        else:
            return curr_util_arr[column][row].get_utility()

    # agent moves downwards
    @staticmethod
    def agent_move_down(column: int, row: int,
                        curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> float:
        if row + 1 < Config.ROW_NUM * \
                scale_factor and not grid[column][row + 1].is_wall():
            return curr_util_arr[column][row + 1].get_utility()
        else:
            return curr_util_arr[column][row].get_utility()

    # agent moves left
    @staticmethod
    def agent_move_left(column: int, row: int,
                        curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]]) -> float:
        if column - 1 >= 0 and not grid[column - 1][row].is_wall():
            return curr_util_arr[column - 1][row].get_utility()
        else:
            return curr_util_arr[column][row].get_utility()

    # agent moves right
    @staticmethod
    def agent_move_right(
            column: int, row: int, curr_util_arr: List[List[UtilityAction]], grid: List[List[Box]], scale_factor: int) -> float:
        if column + 1 < Config.COLUMN_NUM * \
                scale_factor and not grid[column + 1][row].is_wall():
            return curr_util_arr[column + 1][row].get_utility()
        else:
            return curr_util_arr[column][row].get_utility()
