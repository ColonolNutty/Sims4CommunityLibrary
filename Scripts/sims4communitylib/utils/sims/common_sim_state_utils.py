"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimStateUtils:
    """Utilities for checking the state of a sim.

    """
    @staticmethod
    def is_dying(sim_info: SimInfo) -> CommonTestResult:
        """is_dying(sim_info)

        Determine if a Sim is currently dying.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is dying. False, if the Sim is not dying.
        :rtype: CommonTestResult
        """
        return CommonBuffUtils.has_buff(sim_info, CommonBuffId.SIM_IS_DYING)

    @staticmethod
    def is_wearing_towel(sim_info: SimInfo) -> CommonTestResult:
        """is_wearing_towel(sim_info)

        Determine if a Sim is wearing a towel.

        ..warning:: Obsolete: Use :func:`~is_wearing_towel` in :class:`.CommonOutfitUtils` instead.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the sim is wearing a towel. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        return CommonOutfitUtils.is_wearing_towel(sim_info)

    @staticmethod
    def is_in_sunlight(sim_info: SimInfo) -> bool:
        """is_in_sunlight(sim_info)

        Determine if a Sim is in sunlight.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is in sunlight. False, if the Sim is not in sunlight.
        :rtype: bool
        """
        from sims4communitylib.utils.common_time_utils import CommonTimeUtils
        sim = CommonSimUtils.get_sim_instance(sim_info)
        return CommonTimeUtils.get_time_service().is_in_sunlight(sim)

    @staticmethod
    def is_leaving_zone(sim_info: SimInfo) -> bool:
        """is_leaving_zone(sim_info)

        Determine if a Sim is currently leaving the zone.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is leaving the zone. False, if the Sim is not leaving the zone.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        return sim is not None and services.sim_spawner_service().sim_is_leaving(sim)

    @staticmethod
    def is_hidden(sim_info: SimInfo) -> bool:
        """is_hidden(sim_info)

        Determine if a Sim is hidden.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is hidden. False, if the Sim is not hidden.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        return sim_id is None or sim is None or services.hidden_sim_service().is_hidden(sim_id) or sim.is_hidden() or sim.opacity == 0

    @staticmethod
    def is_visible(sim_info: SimInfo) -> bool:
        """is_visible(sim_info)

        Determine if a Sim is visible.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is visible. False, if the Sim is not visible.
        :rtype: bool
        """
        return not CommonSimStateUtils.is_hidden(sim_info)
