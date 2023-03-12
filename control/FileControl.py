from typing import List
from entity.UtilityAction import UtilityAction
from entity.Config import Config


class FileControl:

    # write all outputs to text file
    @staticmethod
    def write_to_text(config_info: str, is_value_iteration: bool,
                      scale_factor: int) -> None:
        try:
            file_name = f"results/all_value_iter_results_scale_{scale_factor}.txt" if is_value_iteration else f"results/all_policy_iter_results_scale_{scale_factor}.txt"
            FileControl.write_to_file_internal(config_info, file_name)
        except Exception as e:
            print(f"An error occurred while writing to file {file_name}: {e}")

    # write all utility values to csv file
    @staticmethod
    def write_to_csv(utility_list: List[List[List[UtilityAction]]],
                     scale_factor: int, is_value_iteration: bool) -> None:
        decimal_places = '{:.3f}'.format
        content = []
        file_name_scale_factor = f"results/value_iteration_utilities_scale_{scale_factor}.txt" if is_value_iteration else f"results/policy_iteration_utilities_scale_{scale_factor}.txt"

        for col in range(Config.COLUMN_NUM * scale_factor):
            for row in range(Config.ROW_NUM * scale_factor):

                iteration = iter(utility_list)
                while True:
                    try:
                        action_util = next(iteration)
                        content.append(
                            decimal_places(
                                action_util[col][row].get_utility())[
                                :6])
                        if next(iteration, None) is not None:
                            content.append(",")
                    except StopIteration:
                        break
                content.append("\n")

        FileControl.write_to_file_internal(
            ''.join(content).strip(),
            file_name_scale_factor + ".csv")

    # open file and write into it
    @staticmethod
    def write_to_file_internal(content: str, file_name: str) -> None:
        try:
            with open(file_name, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"An error occurred while writing to file {file_name}: {e}")
