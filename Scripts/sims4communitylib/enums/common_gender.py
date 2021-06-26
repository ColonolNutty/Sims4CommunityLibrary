"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonGender(CommonInt):
    """Custom Gender enum containing all genders.

    """
    INVALID: 'CommonGender' = 0
    MALE: 'CommonGender' = 4096
    FEMALE: 'CommonGender' = 8192

    @staticmethod
    def get_gender(sim_info: SimInfo) -> 'CommonGender':
        """get_gender(sim_info)

        Retrieve the CommonGender of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonGender that represents what gender a Sim is or CommonGender.INVALID if their gender cannot be determined.
        :rtype: CommonGender
        """
        from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
        if CommonGenderUtils.is_male(sim_info):
            return CommonGender.MALE
        elif CommonGenderUtils.is_female(sim_info):
            return CommonGender.FEMALE
        return CommonGender.INVALID

    @staticmethod
    def convert_to_vanilla(gender: 'CommonGender') -> Union[Gender, None]:
        """convert_to_gender(gender)

        Convert a CommonGender into the vanilla Gender enum.

        :param gender: An instance of a CommonGender
        :type gender: CommonGender
        :return: The specified CommonGender translated to a Gender or None if the CommonGender could not be translated.
        :rtype: Union[Gender, None]
        """
        if gender == CommonGender.INVALID:
            return None
        if isinstance(gender, Gender):
            return gender
        conversion_mapping: Dict[CommonGender, Gender] = {
            CommonGender.MALE: Gender.MALE,
            CommonGender.FEMALE: Gender.FEMALE
        }
        if gender not in conversion_mapping:
            return None
        return conversion_mapping[gender]

    @staticmethod
    def convert_from_vanilla(gender: Gender) -> 'CommonGender':
        """convert_from_vanilla(gender)

        Convert a vanilla Gender into a CommonGender enum.

        :param gender: An instance of a Gender
        :type gender: Gender
        :return: The specified Gender translated to a CommonGender or CommonGender.INVALID if the Gender could not be translated.
        :rtype: Union[Gender, None]
        """
        if gender is None:
            return CommonGender.INVALID
        if isinstance(gender, CommonGender):
            return gender
        conversion_mapping: Dict[int, CommonGender] = {
            int(Gender.MALE): CommonGender.MALE,
            int(Gender.FEMALE): CommonGender.FEMALE
        }
        gender = int(gender)
        if gender not in conversion_mapping:
            return CommonGender.INVALID
        return conversion_mapping[gender]
