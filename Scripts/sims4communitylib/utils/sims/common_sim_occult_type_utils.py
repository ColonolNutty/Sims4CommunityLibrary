"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator

from sims.sim_info import SimInfo
from sims4communitylib.enums.common_occult_type import CommonOccultType


class CommonSimOccultTypeUtils:
    """Utilities for determining the type of Occult a Sim is. i.e. Alien, Vampire, Ghost, etc.

    """
    @staticmethod
    def get_occult_types_for_all_occults_gen(sim_info: SimInfo) -> Iterator[CommonOccultType]:
        """get_occult_types_for_all_occults_gen(sim_info)

        Retrieve a generator of CommonOccultType for all Occults of a Sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult type will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: An iterable of Occult Types for all occults of the Sim.
        :rtype: Iterator[CommonOccultType]
        """
        if sim_info is None:
            return tuple()
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        for occult_sim_info in CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, tuple()):
            yield CommonSimOccultTypeUtils.determine_occult_type(occult_sim_info)

    @staticmethod
    def has_any_occult(sim_info: SimInfo) -> bool:
        """has_any_occult(sim_info)

        Determine if a Sim has any Occult Types.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: True, if the specified Sim has any Non-Human Occult Types. False, if not.
        :rtype: bool
        """
        for occult_type in CommonSimOccultTypeUtils.get_occult_types_for_all_occults_gen(sim_info):
            if occult_type in (CommonOccultType.NON_OCCULT, CommonOccultType.NONE):
                continue
            return True
        return False

    @staticmethod
    def determine_occult_type(sim_info: SimInfo) -> CommonOccultType:
        """determine_occult_type(sim_info)

        Determine the type of Occult a Sim is.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType that represents what a Sim is.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        if CommonOccultUtils.is_robot(sim_info):
            return CommonOccultType.ROBOT
        elif CommonOccultUtils.is_alien(sim_info):
            return CommonOccultType.ALIEN
        elif CommonOccultUtils.is_ghost(sim_info):
            return CommonOccultType.GHOST
        elif CommonOccultUtils.is_mermaid(sim_info):
            return CommonOccultType.MERMAID
        elif CommonOccultUtils.is_plant_sim(sim_info):
            return CommonOccultType.PLANT_SIM
        elif CommonOccultUtils.is_skeleton(sim_info):
            return CommonOccultType.SKELETON
        elif CommonOccultUtils.is_vampire(sim_info):
            return CommonOccultType.VAMPIRE
        elif CommonOccultUtils.is_witch(sim_info):
            return CommonOccultType.WITCH
        return CommonOccultType.NON_OCCULT

    @staticmethod
    def determine_current_occult_type(sim_info: SimInfo) -> CommonOccultType:
        """determine_current_occult_type(sim_info)

        Determine the type of Occult a Sim is currently appearing as.
        i.e. A mermaid with their tail out would currently be a MERMAID. But a Mermaid Sim with no tail out would currently be a CommonOccultType.NONE

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonOccultType the Sim is currently appearing as, or CommonOccultType.NONE if they are not appearing as any Occult or are appearing as their HUMAN disguise/occult.
        :rtype: CommonOccultType
        """
        from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        if CommonOccultUtils.is_currently_a_mermaid(sim_info) or CommonOccultUtils.is_mermaid_in_mermaid_form(sim_info):
            return CommonOccultType.MERMAID
        elif CommonOccultUtils.is_robot(sim_info):
            return CommonOccultType.ROBOT
        elif CommonOccultUtils.is_currently_a_vampire(sim_info):
            return CommonOccultType.VAMPIRE
        elif CommonOccultUtils.is_currently_a_witch(sim_info):
            return CommonOccultType.WITCH
        elif CommonOccultUtils.is_currently_an_alien(sim_info):
            return CommonOccultType.ALIEN
        elif CommonOccultUtils.is_plant_sim(sim_info):
            return CommonOccultType.PLANT_SIM
        elif CommonOccultUtils.is_ghost(sim_info):
            return CommonOccultType.GHOST
        elif CommonOccultUtils.is_skeleton(sim_info):
            return CommonOccultType.SKELETON
        return CommonOccultType.NON_OCCULT
