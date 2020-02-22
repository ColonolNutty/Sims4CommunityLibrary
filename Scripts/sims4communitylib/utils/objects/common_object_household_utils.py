"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject


class CommonObjectHouseholdUtils:
    """Utilities for manipulating Household ownership of Objects.

    """

    @staticmethod
    def set_owning_household_id(game_object: GameObject, household_id: int) -> bool:
        """set_owning_household_id(game_object, household_id)

        Set the Household that owns the Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param household_id: The decimal identifier of a Household.
        :type household_id: int
        :return: True, if the Household was successfully set as the owner. False, if not.
        :rtype: bool
        """
        if game_object is None or household_id == -1:
            return False
        game_object.set_household_owner_id(household_id)
        return True

    @staticmethod
    def get_owning_household_id(game_object: GameObject) -> int:
        """get_owning_household_id(game_object)

        Retrieve the decimal identifier of the Household that owns the Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The decimal identifier of the Household that owns the object.
        :rtype: int
        """
        if game_object is None:
            return -1
        return game_object.get_household_owner_id()
