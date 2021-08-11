"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CommonBodyFrame(CommonInt):
    """Custom Body Frames enum containing all body frames.

    """
    INVALID: 'CommonBodyFrame' = 0
    MASCULINE: 'CommonBodyFrame' = 1
    FEMININE: 'CommonBodyFrame' = 2

    @classmethod
    def get_all(cls) -> Tuple['CommonBodyFrame']:
        """get_all()

        Retrieve a collection of all CommonBodyFrame, excluding CommonBodyFrame.INVALID.

        :return: A collection of all CommonBodyFrame, without CommonBodyFrame.INVALID.
        :rtype: Tuple[CommonBodyFrame]
        """
        value_list: Tuple[CommonBodyFrame] = tuple([value for value in cls.values if value != cls.INVALID])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonBodyFrame, excluding CommonBodyFrame.INVALID.

        :return: A collection of the names of all CommonBodyFrame, without CommonBodyFrame.INVALID.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list

    @staticmethod
    def get_body_frame(sim_info: SimInfo) -> 'CommonBodyFrame':
        """get_body_frame(sim_info)

        Retrieve the CommonBodyFrame of a sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The body frame of the Sim or CommonBodyFrame.INVALID if their current body frame cannot be determined.
        :rtype: CommonBodyFrame
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        if CommonSpeciesUtils.is_animal(sim_info):
            if CommonGenderUtils.is_male(sim_info):
                return CommonBodyFrame.MASCULINE
            if CommonGenderUtils.is_female(sim_info):
                return CommonBodyFrame.FEMININE
            return CommonBodyFrame.INVALID

        if CommonSimGenderOptionUtils.has_masculine_frame(sim_info):
            return CommonBodyFrame.MASCULINE
        if CommonSimGenderOptionUtils.has_feminine_frame(sim_info):
            return CommonBodyFrame.FEMININE
        return CommonBodyFrame.INVALID
