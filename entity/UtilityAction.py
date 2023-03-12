from typing import Optional

from entity.Action import Action

# define utility class


class UtilityAction:
    def __init__(self, action: Optional[Action] = None, utility: float = 0.0):
        self.utility = utility
        self.action = action

    # get the utility value
    def get_utility(self) -> float:
        return self.utility

    # return the action
    def get_action(self) -> Optional[Action]:
        return self.action

    # set the action
    def set_action(self, action: Optional[Action]):
        self.action = action

    # return string action if not wall, else return 'Wall'
    def get_action_str(self) -> str:
        return str(self.action) if self.action is not None else " Wall"

    # defines 'less than'
    # helps us to get the descending order based on utility values
    def __lt__(self, other: 'UtilityAction') -> bool:
        return other.get_utility().__lt__(self.get_utility())

    # defines 'equal to'
    # helps us to compare equality of two utility values
    def __eq__(self, other: 'UtilityAction') -> bool:
        return self.get_utility() == other.get_utility()
