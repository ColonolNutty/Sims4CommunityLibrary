"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonOccultType(CommonInt):
    """Custom Occult Types enum containing all occults. DLC not required.

    """
    NONE: 'CommonOccultType' = 0
    ALIEN: 'CommonOccultType' = 1
    GHOST: 'CommonOccultType' = 2
    NON_OCCULT: 'CommonOccultType' = 3
    MERMAID: 'CommonOccultType' = 4
    PLANT_SIM: 'CommonOccultType' = 5
    ROBOT: 'CommonOccultType' = 6
    SKELETON: 'CommonOccultType' = 7
    VAMPIRE: 'CommonOccultType' = 8
    WITCH: 'CommonOccultType' = 9

    @staticmethod
    def determine_occult_type(sim_info: SimInfo) -> 'CommonOccultType':
        """determine_occult_type(sim_info)

        Determine the type of Occult a Sim is.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType that represents what a Sim is.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        return CommonSimOccultTypeUtils.determine_occult_type(sim_info)

    @staticmethod
    def determine_current_occult_type(sim_info: SimInfo) -> 'CommonOccultType':
        """determine_current_occult_type(sim_info)

        Determine the type of Occult a Sim is currently appearing as.
        i.e. A mermaid with their tail out would currently be a MERMAID. But a Mermaid Sim with no tail out would currently be a CommonOccultType.NONE

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType the Sim is currently appearing as, or CommonOccultType.NONE if they are not appearing as any Occult or are appearing as their HUMAN disguise/occult.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        return CommonSimOccultTypeUtils.determine_current_occult_type(sim_info)
