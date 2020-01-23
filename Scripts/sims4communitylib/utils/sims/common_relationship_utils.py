"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonRelationshipUtils:
    """Utilities for managing relationship bits, tracks, etc.

    """
    @staticmethod
    def has_met(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """Determine if a Sim has met the Target Sim.

        """
        return CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info, target_sim_info, CommonRelationshipBitId.HAS_MET)

    @staticmethod
    def is_romantically_committed_to_any_sims(sim_info: SimInfo) -> bool:
        """Determine if the Sim is romantically committed to any Sims.

        """
        return any(CommonRelationshipUtils.get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info))

    @staticmethod
    def is_romantically_committed_to(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """Determine if a Sim is romantically committed to the Target Sim.

        """
        return target_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info)

    @staticmethod
    def get_friendship_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """Retrieve the level of Friendship between two Sims.

        """
        return CommonRelationshipUtils.get_relationship_level_of_sims(sim_info, target_sim_info, CommonRelationshipTrackId.FRIENDSHIP)

    @staticmethod
    def get_romance_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """Retrieve the level of Romance between two Sims.

        """
        return CommonRelationshipUtils.get_relationship_level_of_sims(sim_info, target_sim_info, CommonRelationshipTrackId.ROMANCE)

    @staticmethod
    def calculate_average_relationship_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """Calculate an average level for Friendship and Romance between two Sims.

        Math: (Friendship Level + Romance Level)/2

        Example:
        Friendship Level: 10
        Romance Level: 20
        Average: 15

        """
        return (CommonRelationshipUtils.get_friendship_level(sim_info, target_sim_info) + CommonRelationshipUtils.get_romance_level(sim_info, target_sim_info)) / 2

    @staticmethod
    def has_relationship_bit_with_any_sims(sim_info: SimInfo, relationship_bit_id: int, instanced_only: bool=True) -> bool:
        """Determine if a Sim has the specified relationship bit with any Sims.

        """
        return any(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, relationship_bit_id, instanced_only=instanced_only))

    @staticmethod
    def has_relationship_bits_with_any_sims(sim_info: SimInfo, relationship_bit_ids: Iterator[int], instanced_only: bool=True) -> bool:
        """Determine if a Sim has the specified relationship bits with any Sims.

        """
        return any(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, relationship_bit_ids, instanced_only=instanced_only))

    @staticmethod
    def has_relationship_bit_with_sim(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_id: int,
    ) -> bool:
        """Determine if two sims have the specified relationship bit with each other.

        """
        return CommonRelationshipUtils.has_relationship_bits_with_sim(sim_info, target_sim_info, (relationship_bit_id,))

    @staticmethod
    def has_relationship_bits_with_sim(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_ids: Iterator[int],
    ) -> bool:
        """Determine if two sims have any of the specified relationship bits with each other.

        """
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        relationship_bits = sim_info.relationship_tracker.get_all_bits(target_sim_id)
        for relationship_bit in relationship_bits:
            relationship_bit_id = getattr(relationship_bit, 'guid64', None)
            if relationship_bit_id in relationship_bit_ids:
                return True
        return False

    @staticmethod
    def get_relationship_level_of_sims(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_track_id: int
    ) -> float:
        """Retrieve the level of a relationship track between two sims.

        """
        relationship_track = CommonResourceUtils.load_instance(Types.STATISTIC, relationship_track_id)
        if relationship_track is None:
            return 0.0
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        return sim_info.relationship_tracker.get_relationship_score(target_sim_id, relationship_track)

    @staticmethod
    def change_relationship_level_of_sims(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_track_id: int,
        level: float
    ) -> bool:
        """Change a relationship track level between two sims.

        :param sim_info: The sim that owns the relationship track.
        :param target_sim_info: The target of the relationship track.
        :param relationship_track_id: The relationship track to change.
        :param level: The amount to add to the relationship track (Can be positive or negative).
        :return: True if the relationship track was changed successfully.
        """
        relationship_track = CommonResourceUtils.load_instance(Types.STATISTIC, relationship_track_id)
        if relationship_track is None:
            return False
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        sim_info.relationship_tracker.add_relationship_score(target_sim_id, level, relationship_track)
        return True

    @staticmethod
    def add_relationship_bit(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_id: int
    ) -> bool:
        """Add a relationship bit between two sims.
        note:: If the relationship bit is UNIDIRECTIONAL, it will only be added to sim_info in the direction of the Target.
        i.e. Sim will have relationship bit towards Target, but Target will not have relationship bit towards Sim.
        One example is the Caregiver relationship:
        - Sim is caregiver of Target.
        - Target is being cared for by Sim.

        """
        relationship_bit_instance = CommonResourceUtils.load_instance(Types.RELATIONSHIP_BIT, relationship_bit_id)
        if relationship_bit_instance is None:
            return False
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        sim_info.relationship_tracker.add_relationship_bit(target_sim_id, relationship_bit_instance)
        return True

    @staticmethod
    def remove_relationship_bit(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_id: int
    ) -> bool:
        """Remove a relationship bit between two sims.

        note:: If the relationship bit is UNIDIRECTIONAL, it will only be removed from sim_info in the direction of the Target.

        i.e. Sim will have no longer have relationship bit towards Target, but Target will still have relationship bit towards Sim.
        One example is the Caregiver relationship:
        - Sim is caregiver of Target.
        - Target is being cared for by Sim.

        """
        relationship_bit_instance = CommonResourceUtils.load_instance(Types.RELATIONSHIP_BIT, relationship_bit_id)
        if relationship_bit_instance is None:
            return False
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        sim_info.relationship_tracker.remove_relationship_bit(target_sim_id, relationship_bit_instance)
        return True

    @staticmethod
    def get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info: SimInfo, relationship_bit_id: int, instanced_only: bool=True) -> Iterator[SimInfo]:
        """Retrieve an Iterator of SimInfo for all Sims that have the specified relationship bit with the specified Sim.

        note:: For UNIDIRECTIONAL relationship bits, the direction is sim_info has relationship bit with target_sim_info
        Caregiver example:
        The Caregiver has a relationship bit pointed at Toddler (The Caregiver would show "caregiving ward" when hovering over the Toddler in the relationships panel)
        The Toddler would NOT have the relationship bit.
        Sim is Caregiver of Toddler.

        :param sim_info: The Sim to locate relationship bits on.
        :param relationship_bit_id: The identifier of the relationship bit to locate connections with.
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        """
        return CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, (relationship_bit_id, ), instanced_only=instanced_only)

    @staticmethod
    def get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info: SimInfo, relationship_bit_ids: Iterator[int], instanced_only: bool=True) -> Iterator[SimInfo]:
        """Retrieve an Iterator of SimInfo for all Sims that have the specified relationship bits with the specified Sim.

        note:: For UNIDIRECTIONAL relationship bits, the direction is sim_info has relationship bit with target_sim_info
         Caregiver example:
         The Caregiver has a relationship bit pointed at Toddler (The Caregiver would show "caregiving ward" when hovering over the toddler in the relationships panel)
         The toddler would NOT have the relationship bit.
         Sim is Caregiver of Toddler.

        :param sim_info: The Sim to locate relationship bits on.
        :param relationship_bit_ids: A collection of identifiers for relationship bits to locate connections with.
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        """
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        for relationship in sim_info.relationship_tracker:
            if relationship.sim_id_a != sim_id:
                target_sim_id = relationship.sim_id_a
            else:
                target_sim_id = relationship.sim_id_b
            target_sim_info = CommonSimUtils.get_sim_info(target_sim_id)
            if target_sim_info is None:
                continue
            if instanced_only and CommonSimUtils.get_sim_instance(target_sim_info) is None:
                continue
            for relationship_bit_id in relationship_bit_ids:
                relationship_bit_instance = CommonResourceUtils.load_instance(Types.RELATIONSHIP_BIT, relationship_bit_id)
                if relationship_bit_instance is None:
                    continue
                if relationship.has_bit(sim_id, relationship_bit_instance):
                    yield target_sim_info
                    break

    @staticmethod
    def has_positive_romantic_combo_relationship_bit_with(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """Determine if a Sim has a positive romantic combo with the Target Sim.

        """
        return CommonRelationshipUtils.has_relationship_bits_with_sim(sim_info, target_sim_info, (
            CommonRelationshipBitId.ROMANTIC_COMBO_SOUL_MATES,
            CommonRelationshipBitId.ROMANTIC_COMBO_LOVERS,
            CommonRelationshipBitId.ROMANTIC_COMBO_SWEETHEARTS,
            CommonRelationshipBitId.ROMANTIC_COMBO_LOVEBIRDS
        ))

    @staticmethod
    def get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info: SimInfo, instanced_only: bool=True) -> Iterator[SimInfo]:
        """Retrieve a SimInfo object for all Sims romantically committed with the specified Sim.

        :param sim_info: The Sim to locate romantically involved Sims with.
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        """
        romance_relationship_ids = (
            CommonRelationshipBitId.ROMANTIC_MARRIED,
            CommonRelationshipBitId.ROMANTIC_GETTING_MARRIED,
            CommonRelationshipBitId.ROMANTIC_ENGAGED,
            CommonRelationshipBitId.ROMANTIC_SIGNIFICANT_OTHER
        )
        for target_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, romance_relationship_ids, instanced_only=instanced_only):
            yield target_sim_info
