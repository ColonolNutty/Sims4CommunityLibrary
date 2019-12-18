"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from sims.sim_info import SimInfo
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimStateUtils:
    """ Utilities for handling the state of a sim. """
    @staticmethod
    def is_dying(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is currently dying.
        """
        return CommonBuffUtils.has_buff(sim_info, CommonBuffId.SIM_IS_DYING)

    @staticmethod
    def is_wearing_towel(sim_info: SimInfo) -> bool:
        """ Obsolete: Please use CommonOutfitUtils.is_wearing_towel """
        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        return CommonOutfitUtils.is_wearing_towel(sim_info)

    @staticmethod
    def is_in_sunlight(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is in sunlight.
        """
        from sims4communitylib.utils.common_time_utils import CommonTimeUtils
        sim = CommonSimUtils.get_sim_instance(sim_info)
        return CommonTimeUtils.get_time_service().is_in_sunlight(sim)

    @staticmethod
    def is_leaving_zone(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is currently leaving the zone.
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        return sim is not None and services.sim_spawner_service().sim_is_leaving(sim)

    @staticmethod
    def is_hidden(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is hidden.
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        return sim_id is None or sim is None or services.hidden_sim_service().is_hidden(sim_id) or sim.is_hidden() or sim.opacity == 0

    @staticmethod
    def is_visible(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is visible.
        """
        return not CommonSimStateUtils.is_hidden(sim_info)
