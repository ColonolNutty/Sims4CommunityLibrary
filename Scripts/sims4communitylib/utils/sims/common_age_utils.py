"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonAgeUtils:
    """ Utilities for handling sim ages. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def get_age(sim_info: SimInfo) -> Union[Age, None]:
        """
            Retrieve the Age of a sim.
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
        """
            Set the Age of a sim.
        """
        try:
            sim_info.apply_age(age)
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'Failed to set age of sim {} to {}.'.format(pformat(sim_info), age), exception=ex)
            return False

    @staticmethod
    def are_same_age(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """
            Determine if two sims are the same Age.
        """
        return CommonAgeUtils.get_age(sim_info) == CommonAgeUtils.get_age(other_sim_info)

    @staticmethod
    def is_younger_than(sim_info: SimInfo, age: Union[Age, int], or_equal: bool=False) -> bool:
        """
            Determine if a sim is younger than the specified age.
        :param sim_info: The sim to check.
        :param age: The age to check with.
        :param or_equal: If True, the age check will be younger than or equal to. If False, the age check will be younger than.
        """
        sim_age = CommonAgeUtils.get_age(sim_info)
        if or_equal:
            return sim_age <= age
        return sim_age < age

    @staticmethod
    def is_older_than(sim_info: SimInfo, age: Union[Age, int], or_equal: bool=False) -> bool:
        """
            Determine if a sim is older than the specified age.
        :param sim_info: The sim to check.
        :param age: The age to check with.
        :param or_equal: If True, the age check will be older than or equal to. If False, the age check will be older than.
        """
        sim_age = CommonAgeUtils.get_age(sim_info)
        if or_equal:
            return sim_age >= age
        return sim_age > age

    @staticmethod
    def is_baby_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is a Baby.
        """
        return age == Age.BABY

    @staticmethod
    def is_toddler_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is a Toddler.
        """
        return age == Age.TODDLER

    @staticmethod
    def is_child_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is a Child.
        """
        return age == Age.CHILD

    @staticmethod
    def is_teen_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is a Teen.
        """
        return age == Age.TEEN

    @staticmethod
    def is_adult_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is a Young Adult or an Adult.
        """
        return CommonAgeUtils.is_young_adult_age(age) or CommonAgeUtils.is_mature_adult_age(age)

    @staticmethod
    def is_young_adult_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is a Young Adult.
        """
        return age == Age.YOUNGADULT

    @staticmethod
    def is_mature_adult_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is an Adult.
        """
        return age == Age.ADULT

    @staticmethod
    def is_elder_age(age: Union[Age, int]) -> bool:
        """
            Determine if an Age is an Elder.
        """
        return age == Age.ELDER

    @staticmethod
    def is_baby(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Baby.
        """
        return CommonAgeUtils.is_baby_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_toddler(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Toddler.
        """
        return CommonAgeUtils.is_toddler_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_child(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Child.
        """
        return CommonAgeUtils.is_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Teen.
        """
        return CommonAgeUtils.is_teen_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_young_adult(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is an Young Adult.

            Note: Does not determine whether they are an Adult or not. Use "is_adult" to check for both.
        """
        return CommonAgeUtils.is_young_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_mature_adult(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is an Adult.

            Note: Does not determine whether they are a Young Adult or not. Use 'is_adult' to check for both.
        """
        return CommonAgeUtils.is_mature_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_elder(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is an Elder.
        """
        return CommonAgeUtils.is_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_adult(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is either a Young Adult or an Adult.
        """
        return CommonAgeUtils.is_young_adult(sim_info) or CommonAgeUtils.is_mature_adult(sim_info)
