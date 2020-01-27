"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonGenderUtils:
    """Utilities for manipulating Genders of Sims.

    """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def get_gender(sim_info: SimInfo) -> Union[Gender, None]:
        """get_gender(sim_info)

        Retrieve the Gender of a Sim.

        :param sim_info: The Sim to retrieve the gender of.
        :type sim_info: SimInfo
        :return: The Gender of the Sim or None if a problem occurs.
        :rtype: Union[Gender, None]
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
        """set_gender(sim_info, gender)

        Set the Gender of a Sim.

        :param sim_info: The Sim to set the Gender of.
        :type sim_info: SimInfo
        :param gender: The Gender to set the Sim to.
        :type gender: Union[int, Gender]
        :return: True, if the Gender of the Sim was set successfully. False, if not.
        :rtype: bool
        """
        try:
            sim_info.gender = gender
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Failed to set gender of Sim {} to {}.'.format(pformat(sim_info), gender), exception=ex)
            return False

    @staticmethod
    def are_same_gender(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_gender(sim_info, other_sim_info)

        Determine if two Sims are the same Gender.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Gender. False, if not.
        :rtype: bool
        """
        return CommonGenderUtils.get_gender(sim_info) == CommonGenderUtils.get_gender(other_sim_info)

    @staticmethod
    def is_female_gender(gender: Gender) -> bool:
        """is_female_gender(gender)

        Determine if a Gender is Female.

        :param gender: The gender to check.
        :type gender: Gender
        :return: True, if the gender is female. False, if the gender is not female.
        :rtype: bool
        """
        return gender == Gender.FEMALE

    @staticmethod
    def is_male_gender(gender: Gender) -> bool:
        """is_male_gender(gender)

        Determine if a Gender is Male.

        :param gender: The gender to check.
        :type gender: Gender
        :return: True, if the gender is male. False, if the gender is not male.
        :rtype: bool
        """
        return gender == Gender.MALE

    @staticmethod
    def is_female(sim_info: SimInfo) -> bool:
        """is_female(sim_info)

        Determine if a Sim is Female.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is female. False, if the Sim is not female.
        :rtype: bool
        """
        return CommonGenderUtils.is_female_gender(CommonGenderUtils.get_gender(sim_info))

    @staticmethod
    def is_male(sim_info: SimInfo) -> bool:
        """is_male(sim_info)

        Determine if a Sim is Male.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is male. False, if the Sim is not male.
        :rtype: bool
        """
        return CommonGenderUtils.is_male_gender(CommonGenderUtils.get_gender(sim_info))
