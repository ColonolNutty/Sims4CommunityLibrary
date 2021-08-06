"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CommonRelationshipUtils:
    """Utilities for manipulating relationship bits, tracks, etc.

    """
    @staticmethod
    def has_met(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """has_met(sim_info, target_sim_info)

        Determine if a Sim has met the Target Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to check.
        :type target_sim_info: SimInfo
        :return: True, if both Sims have met each other. False, if not.
        :rtype: bool
        """
        return CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info, target_sim_info, CommonRelationshipBitId.HAS_MET)

    @staticmethod
    def are_blood_relatives(sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """are_blood_relatives(sim_info_a, sim_info_b)

        Determine if two Sims are blood relatives.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is blood relative of Sim B. False, if not.
        :rtype: bool
        """
        if sim_info_a is None or sim_info_b is None:
            return False
        return not sim_info_a.incest_prevention_test(sim_info_b)

    @staticmethod
    def is_romantically_committed_to_any_sims(sim_info: SimInfo) -> bool:
        """is_romantically_committed_to_any_sims(sim_info)

        Determine if the Sim is romantically committed to any Sims.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is romantically committed to any Sims. False, if not.
        :rtype: bool
        """
        return any(CommonRelationshipUtils.get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info))

    @staticmethod
    def is_romantically_committed_to(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """is_romantically_committed_to(sim_info, target_sim_info)

        Determine if a Sim is romantically committed to the Target Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to check.
        :type target_sim_info: SimInfo
        :return: True, if the Sim is romantically committed to the Target Sim. False, if not.
        :rtype: bool
        """
        return target_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info)

    @staticmethod
    def get_friendship_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """get_friendship_level(sim_info, target_sim_info)

        Retrieve the level of Friendship between two Sims.

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to use.
        :type target_sim_info: SimInfo
        :return: The current level of friendship between two Sims.
        :rtype: float
        """
        track_id = CommonRelationshipUtils._determine_friendship_track(sim_info, target_sim_info)
        if track_id == -1:
            return -1.0
        return CommonRelationshipUtils.get_relationship_level_of_sims(sim_info, target_sim_info, track_id)

    @staticmethod
    def get_romance_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """get_romance_level(sim_info, target_sim_info)

        Retrieve the level of Romance between two Sims.

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to use.
        :type target_sim_info: SimInfo
        :return: The current level of romance between two Sims.
        :rtype: float
        """
        track_id = CommonRelationshipUtils._determine_romance_track(sim_info, target_sim_info)
        if track_id == -1:
            return -1.0
        return CommonRelationshipUtils.get_relationship_level_of_sims(sim_info, target_sim_info, track_id)

    @staticmethod
    def calculate_average_relationship_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """calculate_average_relationship_level(sim_info, target_sim_info)

        Calculate an average level for Friendship and Romance between two Sims.

        .. note:: Math: (Friendship Level + Romance Level)/2

        .. note::

            Example Levels:
                Friendship Level: 10
                Romance Level: 20
                Average: 15

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to use.
        :type target_sim_info: SimInfo
        :return: The average level of friendship and romance between two Sims.
        :rtype: float
        """
        return (CommonRelationshipUtils.get_friendship_level(sim_info, target_sim_info) + CommonRelationshipUtils.get_romance_level(sim_info, target_sim_info)) / 2

    @staticmethod
    def has_relationship_bit_with_any_sims(sim_info: SimInfo, relationship_bit_id: Union[int, CommonRelationshipBitId], instanced_only: bool=True) -> bool:
        """has_relationship_bit_with_any_sims(sim_info, relationship_bit_id, instance_only=True)

        Determine if a Sim has the specified relationship bit with any Sims.

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param relationship_bit_id: The identifier of the Relationship Bit to check for.
        :type relationship_bit_id: Union[int, CommonRelationshipBitId]
        :param instanced_only: If True, only Sims that are currently loaded will be valid.
        :type instanced_only: bool, optional
        :return: True, if the Sim has the specified Relationship Bit with any Sims. False, if not.
        :rtype: bool
        """
        return any(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, relationship_bit_id, instanced_only=instanced_only))

    @staticmethod
    def has_relationship_bits_with_any_sims(sim_info: SimInfo, relationship_bit_ids: Iterator[int], instanced_only: bool=True) -> bool:
        """has_relationship_bits_with_any_sims(sim_info, relationship_bit_ids, instanced_only=True)

        Determine if a Sim has the specified relationship bits with any Sims.

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param relationship_bit_ids: A collection of identifier of Relationship Bits to check for.
        :type relationship_bit_ids: int
        :param instanced_only: If True, only Sims that are currently loaded will be valid.
        :type instanced_only: bool, optional
        :return: True, if the Sim has any of the specified Relationship Bits with any Sims. False, if not.
        :rtype: bool
        """
        return any(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, relationship_bit_ids, instanced_only=instanced_only))

    @staticmethod
    def has_relationship_bit_with_sim(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_id: Union[int, CommonRelationshipBitId],
    ) -> bool:
        """has_relationship_bit_with_sim(sim_info, target_sim_info, relationship_bit_id)

        Determine if two Sims have the specified relationship bit with each other.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim of the relationship bit (The target is especially important for Unidirectional/One Way Relationship Bits).
        :type target_sim_info: SimInfo
        :param relationship_bit_id: The identifier of the Relationship Bit to check for.
        :type relationship_bit_id: Union[int, CommonRelationshipBitId]
        :return: True, if the Sim has the specified Relationship Bit with the Target Sim. False, if not.
        :rtype: bool
        """
        return CommonRelationshipUtils.has_relationship_bits_with_sim(sim_info, target_sim_info, (relationship_bit_id,))

    @staticmethod
    def has_relationship_bits_with_sim(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_ids: Iterator[Union[int, CommonRelationshipBitId]],
    ) -> bool:
        """has_relationship_bits_with_sim(sim_info, target_sim_info, relationship_bit_ids)

        Determine if two sims have any of the specified relationship bits with each other.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim of the relationship bit (The target is especially important for Unidirectional/One Way Relationship Bits).
        :type target_sim_info: SimInfo
        :param relationship_bit_ids: A collection of identifier of Relationship Bits to check for.
        :type relationship_bit_ids: Iterator[Union[int, CommonRelationshipBitId]]
        :return: True, if the Sim has any of the specified Relationship Bits with the Target Sim. False, if not.
        :rtype: bool
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
        relationship_track_id: Union[int, CommonRelationshipTrackId]
    ) -> float:
        """get_relationship_level_of_sims(sim_info, target_sim_info, relationship_track_id)

        Retrieve the level of a relationship track between two sims.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim of the relationship track.
        :type target_sim_info: SimInfo
        :param relationship_track_id: An identifier for a Relationship Track to retrieve.
        :type relationship_track_id: Union[int, CommonRelationshipTrackId]
        :return: The current level between two Sims for the specified Relationship Track.
        :rtype: float
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
        relationship_track_id: Union[int, CommonRelationshipTrackId],
        level: float
    ) -> bool:
        """change_relationship_level_of_sims(sim_info, target_sim_info, relationship_track_id, level)

        Change the level of a relationship track between two Sims.

        :param sim_info: The sim that owns the relationship track.
        :type sim_info: SimInfo
        :param target_sim_info: The target of the relationship track.
        :type target_sim_info: SimInfo
        :param relationship_track_id: The identifier of the Relationship Track to change.
        :type relationship_track_id: : Union[int, CommonRelationshipTrackId]
        :param level: The amount to add to the relationship track (Can be positive or negative).
        :type level: float
        :return: True, if the relationship track was changed successfully. False, if not.
        :rtype: bool
        """
        relationship_track = CommonResourceUtils.load_instance(Types.STATISTIC, relationship_track_id)
        if relationship_track is None:
            return False
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        sim_info.relationship_tracker.add_relationship_score(target_sim_id, level, relationship_track)
        return True

    @staticmethod
    def set_relationship_level_of_sims(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_track_id: Union[int, CommonRelationshipTrackId],
        level: float
    ) -> bool:
        """set_relationship_level_of_sims(sim_info, target_sim_info, relationship_track_id, level)

        Set the level of a relationship track between two Sims.

        :param sim_info: The sim that owns the relationship track.
        :type sim_info: SimInfo
        :param target_sim_info: The target of the relationship track.
        :type target_sim_info: SimInfo
        :param relationship_track_id: The identifier of the Relationship Track to set.
        :type relationship_track_id: : Union[int, CommonRelationshipTrackId]
        :param level: The amount to set the relationship track to (Can be positive or negative).
        :type level: float
        :return: True, if the relationship track was set successfully. False, if not.
        :rtype: bool
        """
        relationship_track = CommonResourceUtils.load_instance(Types.STATISTIC, relationship_track_id)
        if relationship_track is None:
            return False
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        sim_info.relationship_tracker.set_relationship_score(target_sim_id, level, relationship_track)
        return True

    @staticmethod
    def add_relationship_bit(
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        relationship_bit_id: Union[int, CommonRelationshipBitId]
    ) -> bool:
        """add_relationship_bit(sim_info, target_sim_info, relationship_bit_id)

        Add a relationship bit between two sims.

        .. note::

            If the relationship bit is UNIDIRECTIONAL, it will only be added to sim_info in the direction of the Target.
            i.e. Sim will have relationship bit towards Target, but Target will not have relationship bit towards Sim.

            One example is the Caregiver relationship:

            - Sim is caregiver of Target.
            - Target is being cared for by Sim.

        :param sim_info: The source Sim of the Relationship Bit.
        :type sim_info: SimInfo
        :param target_sim_info: The target Sim of the Relationship Bit.
        :type target_sim_info: SimInfo
        :param relationship_bit_id: The identifier of the Relationship Bit to add.
        :type relationship_bit_id: Union[int, CommonRelationshipBitId]
        :return: True, if the relationship bit was added successfully. False, if not.
        :rtype: bool
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
        relationship_bit_id: Union[int, CommonRelationshipBitId]
    ) -> bool:
        """remove_relationship_bit(sim_info, target_sim_info, relationship_bit_id)

        Remove a relationship bit between two sims.

        .. note::

            If the relationship bit is UNIDIRECTIONAL, it will only be removed from sim_info in the direction of the Target.
            i.e. Sim will have no longer have relationship bit towards Target, but Target will still have relationship bit towards Sim.

            One example is the Caregiver relationship:

            - Sim is caregiver of Target.
            - Target is being cared for by Sim.

        :param sim_info: The source Sim of the Relationship Bit.
        :type sim_info: SimInfo
        :param target_sim_info: The target Sim of the Relationship Bit.
        :type target_sim_info: SimInfo
        :param relationship_bit_id: The identifier of the Relationship Bit to remove.
        :type relationship_bit_id: Union[int, CommonRelationshipBitId]
        :return: True, if the relationship bit was removed successfully. False, if not.
        :rtype: bool
        """
        relationship_bit_instance = CommonResourceUtils.load_instance(Types.RELATIONSHIP_BIT, relationship_bit_id)
        if relationship_bit_instance is None:
            return False
        target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
        sim_info.relationship_tracker.remove_relationship_bit(target_sim_id, relationship_bit_instance)
        return True

    @staticmethod
    def get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info: SimInfo, relationship_bit_id: Union[int, CommonRelationshipBitId], instanced_only: bool=True) -> Iterator[SimInfo]:
        """get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, relationship_bit_id, instanced_only=True)

        Retrieve an Iterator of SimInfo for all Sims that have the specified relationship bit with the specified Sim.

        .. note::

                For UNIDIRECTIONAL relationship bits, the direction is sim_info has relationship bit with target_sim_info

                Caregiver example:

                - The Caregiver has a relationship bit pointed at Toddler (The Caregiver would show "caregiving ward" when hovering over the Toddler in the relationships panel)
                - The Toddler would NOT have the relationship bit.
                - Sim is Caregiver of Toddler.

        :param sim_info: The Sim to locate the relationship bit on.
        :type sim_info: SimInfo
        :param relationship_bit_id: The identifier of the relationship bit to locate connections with.
        :type relationship_bit_id: Union[int, CommonRelationshipBitId]
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        :type instanced_only: bool, optional
        :return: An iterable of Sims that have the specified relationship bit with the specified Sim.
        :rtype: Iterator[SimInfo]
        """
        return CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, (relationship_bit_id, ), instanced_only=instanced_only)

    @staticmethod
    def get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info: SimInfo, relationship_bit_ids: Iterator[Union[int, CommonRelationshipBitId]], instanced_only: bool=True) -> Iterator[SimInfo]:
        """get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, relationship_bit_ids, instanced_only=True)

        Retrieve an Iterator of SimInfo for all Sims that have the specified relationship bits with the specified Sim.

        .. note::

            For UNIDIRECTIONAL relationship bits, the direction is sim_info has relationship bit with target_sim_info
            Caregiver example:

            - The Caregiver has a relationship bit pointed at Toddler (The Caregiver would show "caregiving ward" when hovering over the toddler in the relationships panel)
            - The toddler would NOT have the relationship bit.
            - Sim is Caregiver of Toddler.

        :param sim_info: The Sim to locate relationship bits on.
        :type sim_info: SimInfo
        :param relationship_bit_ids: A collection of identifiers for relationship bits to locate connections with.
        :type relationship_bit_ids: Iterator[Union[int, CommonRelationshipBitId]]
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        :type instanced_only: bool, optional
        :return: An iterable of Sims that have any of the specified relationship bits with the specified Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            return tuple()
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
        """has_positive_romantic_combo_relationship_bit_with(sim_info, target_sim_info)

        Determine if a Sim has a positive romantic combo with the Target Sim.

        .. note::

            Positive Romantic Combo Relationship Bits:

            - Soul Mates
            - Lovers
            - Sweethearts
            - Love Birds

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to check.
        :type target_sim_info: SimInfo
        :return: True, if the Sims have positive romantic combo relationship bits with each other. False, if not.
        :rtype: bool
        """
        return CommonRelationshipUtils.has_relationship_bits_with_sim(sim_info, target_sim_info, (
            CommonRelationshipBitId.ROMANTIC_COMBO_SOUL_MATES,
            CommonRelationshipBitId.ROMANTIC_COMBO_LOVERS,
            CommonRelationshipBitId.ROMANTIC_COMBO_SWEETHEARTS,
            CommonRelationshipBitId.ROMANTIC_COMBO_LOVEBIRDS
        ))

    @staticmethod
    def get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info: SimInfo, instanced_only: bool=True) -> Iterator[SimInfo]:
        """get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info, instanced_only=True)

        Retrieve a SimInfo object for all Sims romantically committed with the specified Sim.

        .. note::

            Romantic Commitments:

            - Married
            - Getting Married
            - Engaged
            - Significant Other


        :param sim_info: The Sim to locate romantically involved Sims with.
        :type sim_info: SimInfo
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        :type instanced_only: bool, optional
        :return: An iterable of Sims the specified Sim is romantically committed to.
        :rtype: Iterator[SimInfo]
        """
        romance_relationship_ids = (
            CommonRelationshipBitId.ROMANTIC_MARRIED,
            CommonRelationshipBitId.ROMANTIC_GETTING_MARRIED,
            CommonRelationshipBitId.ROMANTIC_ENGAGED,
            CommonRelationshipBitId.ROMANTIC_SIGNIFICANT_OTHER
        )
        for target_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, romance_relationship_ids, instanced_only=instanced_only):
            yield target_sim_info

    @staticmethod
    def _determine_friendship_track(sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        if CommonSpeciesUtils.is_human(sim_info_a):
            if CommonSpeciesUtils.is_animal(sim_info_b):
                return CommonRelationshipTrackId.SIM_TO_PET_FRIENDSHIP
            elif CommonSpeciesUtils.is_human(sim_info_b):
                return CommonRelationshipTrackId.FRIENDSHIP
        elif CommonSpeciesUtils.is_animal(sim_info_a):
            if CommonSpeciesUtils.is_animal(sim_info_b):
                return -1
            elif CommonSpeciesUtils.is_human(sim_info_b):
                return CommonRelationshipTrackId.SIM_TO_PET_FRIENDSHIP
        return -1

    @staticmethod
    def _determine_romance_track(sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        if CommonSpeciesUtils.is_human(sim_info_a) and CommonSpeciesUtils.is_human(sim_info_b):
            return CommonRelationshipTrackId.ROMANCE
        return -1
