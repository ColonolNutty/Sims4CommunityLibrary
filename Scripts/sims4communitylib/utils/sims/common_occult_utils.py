"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple
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
    def get_sim_info_for_all_occults_gen(sim_info: SimInfo, exclude_occult_types: Iterator[OccultType]) -> Iterator[SimInfo]:
        """get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult Sim info will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: Iterator[OccultType]
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            return tuple()
        exclude_occult_types: Tuple[OccultType] = tuple(exclude_occult_types)
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

        Determine if a Sim is a Vampire.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Vampire. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE)

    @staticmethod
    def is_alien(sim_info: SimInfo) -> bool:
        """is_alien(sim_info)

        Determine if a Sim is an Alien.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Alien. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_ALIEN)

    @staticmethod
    def is_plant_sim(sim_info: SimInfo) -> bool:
        """is_plant_sim(sim_info)

        Determine if a Sim is a Plant Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Plant Sim. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PLANT_SIM)

    @staticmethod
    def is_ghost(sim_info: SimInfo) -> bool:
        """is_ghost(sim_info)

        Determine if a Sim is a Ghost.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Ghost. False, if not.
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

        Determine if a Sim is a Robot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Robot. False, if not.
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
    def is_skeleton(sim_info: SimInfo) -> bool:
        """is_skeleton(sim_info)

        Determine if a Sim is a Skeleton.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is the a Skeleton. False, if not.
        :rtype: bool
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        skeleton_trait_ids = {
            CommonTraitId.HIDDEN_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_SERVICE_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_TEMPLE_SKELETON
        }
        for trait in equipped_sim_traits:
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id in skeleton_trait_ids:
                return True
        return False

    @staticmethod
    def is_witch(sim_info: SimInfo) -> bool:
        """is_witch(sim_info)

        Determine if a Sim is a Witch

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Witch. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_WITCH)

    @staticmethod
    def is_mermaid(sim_info: SimInfo) -> bool:
        """is_mermaid(sim_info)

        Determine if a Sim is a Mermaid

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID)

    @staticmethod
    def is_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_in_mermaid_form(sim_info)

        Determine if a Sim is in Mermaid Form (The Sim has a visible Tail).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has their Mermaid tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID_MERMAID_FORM)

    @staticmethod
    def is_mermaid_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_mermaid_in_mermaid_form(sim_info)

        Determine if a Sim is a Mermaid and is in Mermaid Form (Their Tail is visible).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid with their tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_mermaid(sim_info) and CommonOccultUtils.is_in_mermaid_form(sim_info)

    @staticmethod
    def is_currently_human(sim_info: SimInfo) -> bool:
        """is_currently_human(sim_info)

        Determine if a Sim is currently in their Human form (regardless of their Occult type).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently a Human. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'HUMAN'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.HUMAN

    @staticmethod
    def is_currently_a_mermaid(sim_info: SimInfo) -> bool:
        """is_currently_a_mermaid(sim_info)

        Determine if a Sim is currently in their Mermaid form. (Not disguised)

        .. note:: This only checks their current occult status, it does not check for a visible Tail.\
            Use :func:`~is_in_mermaid_form` to check for a visible Tail.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Mermaid form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'MERMAID'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.MERMAID

    @staticmethod
    def is_currently_a_vampire(sim_info: SimInfo) -> bool:
        """is_currently_a_vampire(sim_info)

        Determine if a Sim is currently in their Vampire form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Vampire form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'VAMPIRE'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.VAMPIRE

    @staticmethod
    def is_currently_an_alien(sim_info: SimInfo) -> bool:
        """is_currently_an_alien(sim_info)

        Determine if a Sim is currently in their Alien form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Alien form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'ALIEN'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.ALIEN

    @staticmethod
    def is_currently_a_witch(sim_info: SimInfo) -> bool:
        """is_currently_a_witch(sim_info)

        Determine if a Sim is currently in their Witch form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Witch form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'WITCH'):
            return False
        return CommonOccultUtils._get_current_occult_type(sim_info) == OccultType.WITCH

    @staticmethod
    def get_sim_info_of_all_occults_gen(sim_info: SimInfo, *exclude_occult_types: OccultType) -> Iterator[SimInfo]:
        """get_sim_info_of_all_occults_gen(sim_info, *exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. warning:: Obsolete, please use :func:`~get_sim_info_for_all_occults_gen` instead.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: OccultType
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        return CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

    @staticmethod
    def _has_occult_trait(sim_info: SimInfo, trait_id: int) -> bool:
        return CommonOccultUtils._has_occult_traits(sim_info, (trait_id,))

    @staticmethod
    def _has_occult_traits(sim_info: SimInfo, trait_ids: Iterator[int]) -> bool:
        if sim_info is None:
            return False
        equipped_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for equipped_trait in equipped_traits:
            trait_id = CommonTraitUtils.get_trait_id(equipped_trait)
            if trait_id in trait_ids:
                return True
        return False

    @staticmethod
    def _get_current_occult_type(sim_info: SimInfo) -> OccultType:
        if sim_info is None:
            return OccultType.HUMAN
        # noinspection PyPropertyAccess
        return sim_info.current_occult_types
