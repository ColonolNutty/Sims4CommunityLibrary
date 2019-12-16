"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonGenderUtils:
    """ Utilities for handling sim genders. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def get_gender(sim_info: SimInfo) -> Union[Gender, None]:
        """
            Retrieve the Gender of a sim.
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, 'gender'):
            # noinspection PyPropertyAccess
            return sim_info.gender
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'gender'):
            return sim_info.siminfo.gender
        return None

    @staticmethod
    def set_gender(sim_info: SimInfo, gender: Union[int, Gender]) -> bool:
        """
            Set the Gender of a sim.
        """
        try:
            sim_info.gender = gender
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Failed to set gender of sim {} to {}.'.format(pformat(sim_info), gender), exception=ex)
            return False

    @staticmethod
    def are_same_gender(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """
            Determine if two sims are the same Gender.
        """
        return CommonGenderUtils.get_gender(sim_info) == CommonGenderUtils.get_gender(other_sim_info)

    @staticmethod
    def is_female_gender(gender: Gender) -> bool:
        """
            Determine if a Gender is Female.
        """
        return gender == Gender.FEMALE

    @staticmethod
    def is_male_gender(gender: Gender) -> bool:
        """
            Determine if a Gender is Male.
        """
        return gender == Gender.MALE

    @staticmethod
    def is_female(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Female.
        """
        return CommonGenderUtils.is_female_gender(CommonGenderUtils.get_gender(sim_info))

    @staticmethod
    def is_male(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Male.
        """
        return CommonGenderUtils.is_male_gender(CommonGenderUtils.get_gender(sim_info))
