"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator
from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
try:
    from traits.trait_type import TraitType
except ModuleNotFoundError:
    from traits.traits import TraitType


class CommonOccultUtils:
    """Utilities for manipulating the Occults of Sims.

    """

    @staticmethod
    def get_sim_info_of_all_occults_gen(sim_info: SimInfo, *exclude_occult_types: OccultType) -> Iterator[SimInfo]:
        """get_sim_info_of_all_occults_gen(sim_info, *exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult sim info will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: OccultType
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            return tuple()
        yield sim_info
        for occult in OccultType.values:
            if occult in exclude_occult_types:
                continue
            # noinspection PyPropertyAccess
            if occult == sim_info.current_occult_types:
                continue
            if not sim_info.occult_tracker.has_occult_type(occult):
                continue
            occult_sim_info: SimInfo = sim_info.occult_tracker.get_occult_sim_info(occult)
            if occult_sim_info is None:
                continue
            yield occult_sim_info

    @staticmethod
    def is_vampire(sim_info: SimInfo) -> bool:
        """is_vampire(sim_info)

        Determine if a sim is a Vampire.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE)

    @staticmethod
    def is_alien(sim_info: SimInfo) -> bool:
        """is_alien(sim_info)

        Determine if a sim is an Alien.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_ALIEN)

    @staticmethod
    def is_plant_sim(sim_info: SimInfo) -> bool:
        """is_plant_sim(sim_info)

        Determine if a sim is a Plant Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PLANT_SIM)

    @staticmethod
    def is_ghost(sim_info: SimInfo) -> bool:
        """is_ghost(sim_info)

        Determine if a sim is a Ghost.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            is_ghost_trait = getattr(trait, 'is_ghost_trait', None)
            if is_ghost_trait:
                return True
        return False

    @staticmethod
    def is_robot(sim_info: SimInfo) -> bool:
        """is_robot(sim_info)

        Determine if a sim is a Robot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        if not hasattr(TraitType, 'ROBOT'):
            return False
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            trait_type = getattr(trait, 'trait_type', -1)
            if trait_type == TraitType.ROBOT:
                return True
        return False

    @staticmethod
    def is_witch(sim_info: SimInfo) -> bool:
        """is_witch(sim_info)

        Determine if a sim is a Mermaid

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_WITCH)

    @staticmethod
    def is_mermaid(sim_info: SimInfo) -> bool:
        """is_mermaid(sim_info)

        Determine if a sim is a Mermaid

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Occult. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID)

    @staticmethod
    def is_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_in_mermaid_form(sim_info)

        Determine if a sim is in Mermaid Form (The Sim has a visible Tail).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has their mermaid tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID_MERMAID_FORM)

    @staticmethod
    def is_mermaid_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_mermaid_in_mermaid_form(sim_info)

        Determine if a sim is a Mermaid and is in Mermaid Form (Their Tail is visible).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid with their tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_mermaid(sim_info) and CommonOccultUtils.is_in_mermaid_form(sim_info)

    @staticmethod
    def is_currently_human(sim_info: SimInfo) -> bool:
        """is_currently_human(sim_info)

        Determine if a sim is currently Human (Not an Occult)

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently the Occult. False, if not.
        :rtype: bool
        """
        if not hasattr(OccultType, 'HUMAN'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.HUMAN

    @staticmethod
    def is_currently_a_mermaid(sim_info: SimInfo) -> bool:
        """is_currently_a_mermaid(sim_info)

        Determine if a sim is currently a Mermaid

        .. note:: This only checks their occult status, it does not check for a visible Tail.\
            Use :func:`~is_in_mermaid_form` to check for a visible Tail.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently the Occult. False, if not.
        :rtype: bool
        """
        if not hasattr(OccultType, 'MERMAID'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.MERMAID

    @staticmethod
    def is_currently_a_vampire(sim_info: SimInfo) -> bool:
        """is_currently_a_vampire(sim_info)

        Determine if a sim is currently a Vampire

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently the Occult. False, if not.
        :rtype: bool
        """
        if not hasattr(OccultType, 'VAMPIRE'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.VAMPIRE

    @staticmethod
    def is_currently_an_alien(sim_info: SimInfo) -> bool:
        """is_currently_an_alien(sim_info)

        Determine if a sim is currently an Alien

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently the Occult. False, if not.
        :rtype: bool
        """
        if not hasattr(OccultType, 'ALIEN'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.ALIEN

    @staticmethod
    def is_currently_a_witch(sim_info: SimInfo) -> bool:
        """is_currently_a_witch(sim_info)

        Determine if a sim is currently a Witch

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently the Occult. False, if not.
        :rtype: bool
        """
        if not hasattr(OccultType, 'WITCH'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.WITCH

    @staticmethod
    def _has_occult_trait(sim_info: SimInfo, trait: int) -> bool:
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for sim_trait in equipped_sim_traits:
            sim_trait_id = getattr(sim_trait, 'guid64', None)
            if sim_trait_id == trait:
                return True
        return False

    @staticmethod
    def _get_current_occult_type(sim_info: SimInfo) -> OccultType:
        # noinspection PyPropertyAccess
        return sim_info.current_occult_types
