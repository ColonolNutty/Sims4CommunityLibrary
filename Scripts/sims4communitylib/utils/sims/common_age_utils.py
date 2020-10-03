"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonAgeUtils:
    """Utilities for manipulating Ages of Sims.

    """
    @staticmethod
    def get_age(sim_info: SimInfo) -> Union[Age, None]:
        """get_age(sim_info)

        Retrieve the Age of a Sim.

        :param sim_info: The Sim to get the Age of.
        :type sim_info: SimInfo
        :return: The Age of the Sim or None if a problem occurs.
        :rtype: Union[Age, None]
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, '_base') and hasattr(sim_info._base, 'age'):
            return sim_info._base.age
        if hasattr(sim_info, 'age'):
            # noinspection PyPropertyAccess
            return sim_info.age
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age'):
            return sim_info.sim_info._base.age
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'age'):
            return sim_info.sim_info.age
        return None

    @staticmethod
    def set_age(sim_info: SimInfo, age: Union[Age, int]) -> bool:
        """set_age(sim_info, age)

        Set the Age of a Sim.

        :param sim_info: The Sim to set the Age of.
        :type sim_info: SimInfo
        :param age: The Age to set the Sim to.
        :type age: Union[Age, int]
        :return: True, if the Age was set successfully. False, if not.
        :rtype: bool
        """
        try:
            sim_info.apply_age(age)
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to set age of sim {} to {}.'.format(pformat(sim_info), age), exception=ex)
            return False

    @staticmethod
    def are_same_age(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_age(sim_info, other_sim_info)

        Determine if two Sims are the same Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The other Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Age.
        :rtype: bool
        """
        return CommonAgeUtils.get_age(sim_info) == CommonAgeUtils.get_age(other_sim_info)

    @staticmethod
    def is_younger_than(sim_info: SimInfo, age: Union[Age, int], or_equal: bool=False) -> bool:
        """is_younger_than(sim_info, age, or_equal=False)

        Determine if a Sim is younger than the specified Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param age: The age to check with.
        :type age: Union[Age, int]
        :param or_equal: If True, the age check will be younger than or equal to. If False, the age check will be younger than.
        :type or_equal: bool
        :return: True, if the Sim is younger than the specified Age or equal to the specified age if `or_equal` is True. False, if not.
        :rtype: bool
        """
        sim_age = CommonAgeUtils.get_age(sim_info)
        if or_equal:
            return sim_age <= age
        return sim_age < age

    @staticmethod
    def is_older_than(sim_info: SimInfo, age: Union[Age, int], or_equal: bool=False) -> bool:
        """is_older_than(sim_info, age, or_equal=False)

        Determine if a Sim is older than the specified Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param age: The age to check with.
        :type age: Union[Age, int]
        :param or_equal: If True, the age check will be older than or equal to. If False, the Age check will be older than.
        :type or_equal: bool
        :return: True, if the Sim is older than the specified Age or equal to the specified Age if `or_equal` is True. False, if not.
        :rtype: bool
        """
        sim_age = CommonAgeUtils.get_age(sim_info)
        if or_equal:
            return sim_age >= age
        return sim_age > age

    @staticmethod
    def is_baby_age(age: Union[Age, int]) -> bool:
        """is_baby_age(age)

        Determine if an Age is a Baby.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.BABY

    @staticmethod
    def is_toddler_age(age: Union[Age, int]) -> bool:
        """is_toddler_age(age)

        Determine if an Age is a Toddler.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.TODDLER

    @staticmethod
    def is_child_age(age: Union[Age, int]) -> bool:
        """is_child_age(age)

        Determine if an Age is a Child.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.CHILD

    @staticmethod
    def is_teen_age(age: Union[Age, int]) -> bool:
        """is_teen_age(age)

        Determine if an Age is a Teen.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.TEEN

    @staticmethod
    def is_adult_age(age: Union[Age, int]) -> bool:
        """is_adult_age(age)

        Determine if an Age is a Young Adult or an Adult.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_young_adult_age(age) or CommonAgeUtils.is_mature_adult_age(age)

    @staticmethod
    def is_young_adult_age(age: Union[Age, int]) -> bool:
        """is_young_adult_age(age)

        Determine if an Age is a Young Adult.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.YOUNGADULT

    @staticmethod
    def is_mature_adult_age(age: Union[Age, int]) -> bool:
        """is_mature_adult_age(age)

        Determine if an Age is an Adult.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.ADULT

    @staticmethod
    def is_elder_age(age: Union[Age, int]) -> bool:
        """is_elder_age(age)

        Determine if an Age is an Elder.

        :param age: The age to check.
        :type age: Union[Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return age == Age.ELDER

    @staticmethod
    def is_baby_or_toddler_age(age: Age) -> bool:
        """is_baby_or_toddler_age(age)

        Determine if an age is Baby or Toddler.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_age(age) or CommonAgeUtils.is_toddler_age(age)

    @staticmethod
    def is_baby_toddler_or_child_age(age: Age) -> bool:
        """is_baby_toddler_or_child_age(age)

        Determine if an age is Baby, Toddler, or Child.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_age(age) or CommonAgeUtils.is_toddler_age(age) or CommonAgeUtils.is_child_age(age)

    @staticmethod
    def is_toddler_or_child_age(age: Age) -> bool:
        """is_toddler_or_child_age(age)

        Determine if an age is Toddler or Child.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_age(age) or CommonAgeUtils.is_child_age(age)

    @staticmethod
    def is_child_or_teen_age(age: Age) -> bool:
        """is_child_or_teen_age(age)

        Determine if an age is Child or Teen.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_age(age) or CommonAgeUtils.is_teen_age(age)

    @staticmethod
    def is_teen_or_young_adult_age(age: Age) -> bool:
        """is_teen_or_young_adult_age(age)

        Determine if an age is Teen or Young Adult.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(age) or CommonAgeUtils.is_young_adult_age(age)

    @staticmethod
    def is_teen_or_adult_age(age: Age) -> bool:
        """is_teen_or_adult_age(age)

        Determine if an age is Teen, Young Adult, or Adult.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(age) or CommonAgeUtils.is_adult_age(age)

    @staticmethod
    def is_teen_adult_or_elder_age(age: Age) -> bool:
        """is_teen_adult_or_elder_age(age)

        Determine if an age is Teen, Young Adult, Adult, or Elder.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(age) or CommonAgeUtils.is_adult_age(age) or CommonAgeUtils.is_elder_age(age)

    @staticmethod
    def is_adult_or_elder_age(age: Age) -> bool:
        """is_adult_or_elder_age(age)

        Determine if an age is Young Adult, Adult, or Elder.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_age(age) or CommonAgeUtils.is_elder_age(age)

    @staticmethod
    def is_mature_adult_or_elder_age(age: Age) -> bool:
        """is_mature_adult_or_elder_age(age)

        Determine if an age is Adult or Elder.

        :param age: The age to check.
        :type age: Age
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_age(age) or CommonAgeUtils.is_elder_age(age)

    @staticmethod
    def is_baby(sim_info: SimInfo) -> bool:
        """is_baby(sim_info)

        Determine if a sim is a Baby.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_toddler(sim_info: SimInfo) -> bool:
        """is_toddler(sim_info)

        Determine if a sim is a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_child(sim_info: SimInfo) -> bool:
        """is_child(sim_info)

        Determine if a sim is a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen(sim_info: SimInfo) -> bool:
        """is_teen(sim_info)

        Determine if a sim is a Teen.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_young_adult(sim_info: SimInfo) -> bool:
        """is_young_adult(sim_info)

        Determine if a sim is an Young Adult.

        .. note:: This function does not determine whether they are an Adult or not. Use "is_adult" to check for both.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_young_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_mature_adult(sim_info: SimInfo) -> bool:
        """is_mature_adult(sim_info)

        Determine if a sim is an Adult.

        .. note:: This function does not determine whether they are a Young Adult or not. Use 'is_adult' to check for both.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_elder(sim_info: SimInfo) -> bool:
        """is_elder(sim_info)

        Determine if a sim is an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_adult(sim_info: SimInfo) -> bool:
        """is_adult(sim_info)

        Determine if a sim is either a Young Adult or an Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_baby_or_toddler(sim_info: SimInfo) -> bool:
        """is_baby_or_toddler(sim_info)

        Determine if a sim is a Baby or a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_or_toddler_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_toddler_or_child(sim_info: SimInfo) -> bool:
        """is_toddler_or_child(sim_info)

        Determine if a sim is a Toddler or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_or_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_baby_toddler_or_child(sim_info: SimInfo) -> bool:
        """is_baby_toddler_or_child(sim_info)

        Determine if a sim is a Baby, a Toddler, or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_toddler_or_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_child_or_teen(sim_info: SimInfo) -> bool:
        """is_child_or_teen(sim_info)

        Determine if a sim is a Child or a Teen.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_or_teen_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen_or_young_adult(sim_info: SimInfo) -> bool:
        """is_teen_or_young_adult(sim_info)

        Determine if a sim is a Teen or a Young Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_or_young_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen_or_adult(sim_info: SimInfo) -> bool:
        """is_teen_or_adult(sim_info)

        Determine if a sim is a Teen, a Young Adult, or an Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_or_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen_adult_or_elder(sim_info: SimInfo) -> bool:
        """is_teen_adult_or_elder(sim_info)

        Determine if a sim is a Teen, a Young Adult, an Adult, or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_adult_or_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_adult_or_elder(sim_info: SimInfo) -> bool:
        """is_adult_or_elder(sim_info)

        Determine if a sim is a Young Adult, an Adult, or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_or_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_mature_adult_or_elder(sim_info: SimInfo) -> bool:
        """is_mature_adult_or_elder(sim_info)

        Determine if a sim is an Adult or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_or_elder_age(CommonAgeUtils.get_age(sim_info))

    # Obsolete Functionality

    @staticmethod
    def is_baby_child_or_toddler(sim_info: SimInfo) -> bool:
        """is_baby_child_or_toddler(sim_info)

        .. warning:: Obsolete: Don't use this function. Use the :func:'~is_baby_toddler_or_child' function instead.

        """
        return CommonAgeUtils.is_baby(sim_info) or CommonAgeUtils.is_toddler(sim_info) or CommonAgeUtils.is_child(sim_info)
