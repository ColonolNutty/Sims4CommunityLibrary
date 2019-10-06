"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils


class CommonSimStateUtils:
    """ Utilities for handling the state of a sim. """
    @classmethod
    def is_dying(cls, sim_info: SimInfo) -> bool:
        """
            Determine if a sim is currently dying.
        """
        return CommonBuffUtils.has_buff(sim_info, CommonBuffId.SIM_IS_DYING)

    @classmethod
    def is_wearing_towel(cls, sim_info: SimInfo) -> bool:
        """
            Determine if a sim is currently wearing a towel.
        """
        return CommonBuffUtils.has_buff(sim_info, CommonBuffId.IS_WEARING_TOWEL)
