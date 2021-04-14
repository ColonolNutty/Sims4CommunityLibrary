"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
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
        if CommonSpeciesUtils.is_pet(sim_info):
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
