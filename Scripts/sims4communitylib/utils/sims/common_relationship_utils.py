"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union, Tuple

from relationships.relationship import Relationship
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.relationship_tracks_enum import CommonRelationshipTrackId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
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
    def is_friendly_with(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """is_friendly_with(sim_info, target_sim_info)

        Determine if a Sim is friendly with a Target Sim.

        .. note:: By default, a Sim is friendly with another Sim when their Friendship relationship is at or above 30. If both Sims are Animals, they are friendly with each other if they have the Friendly relationship bit.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param target_sim_info: The info of a Sim.
        :type target_sim_info: SimInfo
        :return: True, if the Sim is friendly with the Target Sim. False, if not.
        :rtype: bool
        """
        if CommonSpeciesUtils.is_animal(sim_info) and CommonSpeciesUtils.is_animal(target_sim_info):
            return CommonRelationshipUtils.has_relationship_bit_with_sim(sim_info, target_sim_info, CommonRelationshipBitId.PET_TO_PET_FRIENDLY)\
                   or CommonRelationshipUtils.has_relationship_bit_with_sim(target_sim_info, sim_info, CommonRelationshipBitId.PET_TO_PET_FRIENDLY)
        return CommonRelationshipUtils.get_friendship_level(sim_info, target_sim_info) >= 30

    @classmethod
    def is_romantic_with(cls, sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """is_romantic_with(sim_info, target_sim_info)

        Determine if a Sim is romantic with a Target Sim.

        .. note:: By default, a Sim is romantic with another Sim when their Romance relationship is at or above 30.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param target_sim_info: The info of a Sim.
        :type target_sim_info: SimInfo
        :return: True, if the Sim is romantic with the Target Sim. False, if not.
        :rtype: bool
        """
        return cls.get_romance_level(sim_info, target_sim_info) >= 30

    @classmethod
    def get_romantically_committed_relationship_bits(cls) -> Tuple[CommonRelationshipBitId]:
        """get_romantically_committed_relationship_bits()

        Retrieve a collection of relationship bits that signify two Sims are in a committed relationship.

        :return: A collection of relationship bits.
        :rtype: Tuple[CommonRelationshipBitId]
        """
        result: Tuple[CommonRelationshipBitId, ...] = (
            CommonRelationshipBitId.ROMANTIC_ENGAGED,
            CommonRelationshipBitId.ROMANTIC_GETTING_MARRIED,
            CommonRelationshipBitId.ROMANTIC_MARRIED,
            CommonRelationshipBitId.ROMANTIC_PROMISED,
            CommonRelationshipBitId.ROMANTIC_SIGNIFICANT_OTHER,
            CommonRelationshipBitId.SEXUAL_ORIENTATION_WOOHOO_PARTNERS
        )
        return result

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

        .. note:: The return will be "0.0" if a friendship relationship track is not found.

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to use.
        :type target_sim_info: SimInfo
        :return: The current level of friendship between two Sims.
        :rtype: float
        """
        track_id = CommonRelationshipUtils.get_friendship_relationship_track(sim_info, target_sim_info)
        if track_id is None:
            return 0.0
        return CommonRelationshipUtils.get_relationship_level_of_sims(sim_info, target_sim_info, track_id)

    @staticmethod
    def get_romance_level(sim_info: SimInfo, target_sim_info: SimInfo) -> float:
        """get_romance_level(sim_info, target_sim_info)

        Retrieve the level of Romance between two Sims.

        .. note:: The return will be "0.0" if a romance relationship track is not found.

        :param sim_info: The Sim to use.
        :type sim_info: SimInfo
        :param target_sim_info: The Target Sim to use.
        :type target_sim_info: SimInfo
        :return: The current level of romance between two Sims.
        :rtype: float
        """
        track_id = CommonRelationshipUtils.get_romance_relationship_track(sim_info, target_sim_info)
        if track_id is None:
            return 0.0
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

    @classmethod
    def has_permission_for_romantic_relationships(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_permission_for_romantic_relationships(sim_info)

        Determine if a Sim has permission to have romantic relationships with other Sims.

        .. note:: In the vanilla game, only Teen, Adult, and Elder Sims have permission for romantic relationships.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if the test fails.
        :rtype: CommonTestResult
        """
        if not CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonTestResult(False, reason=f'{sim_info} does not have permission for romantic relationships. They are neither a Teen, Adult, nor Elder Sim.')
        return CommonTestResult(True, reason=f'{sim_info} has permission for romantic relationships.')

    @classmethod
    def has_permission_for_romantic_relationship_with(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        """Determine if two Sims are allowed to have a Romantic relationship together."""
        sim_a_permission_result = cls.has_permission_for_romantic_relationships(sim_info_a)
        if not sim_a_permission_result:
            return CommonTestResult(False, reason=f'{sim_info_a} does not have permission for a romantic relationship with {sim_info_b}. {sim_a_permission_result}')
        sim_b_permission_result = cls.has_permission_for_romantic_relationships(sim_info_b)
        if not sim_b_permission_result:
            return CommonTestResult(False, reason=f'{sim_info_a} does not have permission for a romantic relationship with {sim_info_b}. {sim_b_permission_result}')
        if CommonRelationshipUtils.are_blood_relatives(sim_info_a, sim_info_b):
            return CommonTestResult(False, reason=f'{sim_info_a} does not have permission for a romantic relationship with {sim_info_b}. {sim_info_a} is a blood relative of {sim_info_b}.')
        if not CommonSpeciesUtils.are_same_species(sim_info_a, sim_info_b):
            return CommonTestResult(False, reason=f'{sim_info_a} does not have permission for a romantic relationship with {sim_info_b}. {sim_info_a} and {sim_info_b} are not the same species.')
        if CommonAgeUtils.is_teen(sim_info_a) and CommonAgeUtils.is_teen(sim_info_b):
            return CommonTestResult(True, reason=f'{sim_info_a} has permission for a romantic relationship with {sim_info_b}.')
        if CommonAgeUtils.is_teen(sim_info_a):
            if not CommonAgeUtils.is_teen(sim_info_b):
                return CommonTestResult(False, reason=f'{sim_info_a} does not have permission for a romantic relationship with {sim_info_b}. {sim_info_a} is a Teen Sim and {sim_info_b} is an Adult or Elder Sim.')
        elif CommonAgeUtils.is_teen(sim_info_b):
            return CommonTestResult(False, reason=f'{sim_info_a} does not have permission for a romantic relationship with {sim_info_b}. {sim_info_a} is an Adult or Elder Sim and {sim_info_b} is a Teen Sim.')
        return CommonTestResult(True, reason=f'{sim_info_a} has permission for a romantic relationship with {sim_info_b}.')

    @classmethod
    def has_permission_to_be_blood_relative_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        """has_permission_to_be_blood_relative_of(sim_info_a, sim_info_b)

        Determine if Sim A has permission to be a Blood Relative of Sim B. (Such as Mother, Daughter, etc.)

        .. note:: In the vanilla game, only Sims of the same species have permission to be Blood Relatives.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: The result of the test. True, if the test passes. False, if the test fails.
        :rtype: CommonTestResult
        """
        if not CommonSpeciesUtils.are_same_species(sim_info_a, sim_info_b):
            return CommonTestResult(False, reason=f'{sim_info_a} has permission to be a Blood Relative of {sim_info_b}. {sim_info_a} and {sim_info_b} are not the same species.')
        return CommonTestResult(True, reason=f'{sim_info_a} has permission to be a Blood Relative of {sim_info_b}.')

    @staticmethod
    def has_relationship_bit_with_any_sims(sim_info: SimInfo, relationship_bit_id: Union[int, CommonRelationshipBitId], instanced_only: bool = True) -> bool:
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
    def has_relationship_bits_with_any_sims(sim_info: SimInfo, relationship_bit_ids: Iterator[int], instanced_only: bool = True) -> bool:
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
    def get_relationships_gen(sim_info: SimInfo) -> Iterator[Relationship]:
        """get_relationships_gen(sim_info)

        Retrieve all relationships a Sim has with other Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of Relationships a Sim has with other Sims.
        :rtype: Iterator[Relationship]
        """
        if not hasattr(sim_info, 'relationship_tracker') or not sim_info.relationship_tracker:
            return tuple()
        for relationship in sim_info.relationship_tracker:
            yield relationship

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
        relationship_tracker = sim_info.relationship_tracker
        if relationship_tracker is None:
            return False
        relationship_tracker.add_relationship_bit(target_sim_id, relationship_bit_instance)
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
        relationship_tracker = sim_info.relationship_tracker
        if relationship_tracker is None:
            return False
        relationship_tracker.remove_relationship_bit(target_sim_id, relationship_bit_instance)
        return True

    @staticmethod
    def remove_relationship_bit_from_all(
        sim_info: SimInfo,
        relationship_bit_id: Union[int, CommonRelationshipBitId]
    ) -> bool:
        """remove_relationship_bit_from_all(sim_info, relationship_bit_id)

        Remove a relationship bit between a Sim and all other Sims.

        .. note::

            If the relationship bit is UNIDIRECTIONAL, it will only be removed from sim_info in the direction of the Target.
            i.e. Sim will have no longer have relationship bit towards Target, but Target will still have relationship bit towards Sim.

            One example is the Caregiver relationship:

            - Sim is caregiver of Target.
            - Target is being cared for by Sim.

        :param sim_info: The source Sim of the Relationship Bit.
        :type sim_info: SimInfo
        :param relationship_bit_id: The identifier of the Relationship Bit to remove.
        :type relationship_bit_id: Union[int, CommonRelationshipBitId]
        :return: True, if the relationship bit was removed successfully. False, if not.
        :rtype: bool
        """
        relationship_bit_instance = CommonResourceUtils.load_instance(Types.RELATIONSHIP_BIT, relationship_bit_id)
        if relationship_bit_instance is None:
            return False
        sim_id_a = CommonSimUtils.get_sim_id(sim_info)
        for relationship in CommonRelationshipUtils.get_relationships_gen(sim_info):
            sim_id_b = relationship.get_other_sim_id(sim_id_a)
            if relationship.has_bit(sim_id_a, relationship_bit_instance):
                relationship.remove_bit(sim_id_a, sim_id_b, relationship_bit_instance)
        return True

    @staticmethod
    def get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info: SimInfo, relationship_bit_id: Union[int, CommonRelationshipBitId], instanced_only: bool = True) -> Iterator[SimInfo]:
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
    def get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info: SimInfo, relationship_bit_ids: Iterator[Union[int, CommonRelationshipBitId]], instanced_only: bool = True) -> Iterator[SimInfo]:
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

    @classmethod
    def get_sim_info_of_all_sims_romantically_committed_to_generator(cls, sim_info: SimInfo, instanced_only: bool = True) -> Iterator[SimInfo]:
        """get_sim_info_of_all_sims_romantically_committed_to_generator(sim_info, instanced_only=True)

        Retrieve a SimInfo object for all Sims romantically committed with the specified Sim.

        .. note::

            Romantic Commitments:

            - Married
            - Getting Married
            - Engaged
            - Significant Other
            - Promised


        :param sim_info: The Sim to locate romantically involved Sims with.
        :type sim_info: SimInfo
        :param instanced_only: If True, only Sims that are currently loaded will be returned.
        :type instanced_only: bool, optional
        :return: An iterable of Sims the specified Sim is romantically committed to.
        :rtype: Iterator[SimInfo]
        """
        romance_relationship_ids = cls.get_romantically_committed_relationship_bits()
        for target_sim_info in CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bits_generator(sim_info, romance_relationship_ids, instanced_only=instanced_only):
            yield target_sim_info

    @classmethod
    def get_friendship_relationship_track(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, None]:
        """get_friendship_relationship_track(sim_info_a, sim_info_b)

        Get an appropriate Friendship Relationship track between Sim A and Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: The decimal identifier of the Friendship Relationship Track appropriate for Sim A to have with Sim B or None if not found.
        :rtype: Union[CommonRelationshipTrackId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info_a):
            if CommonSpeciesUtils.is_animal(sim_info_b):
                return CommonRelationshipTrackId.SIM_TO_PET_FRIENDSHIP
            elif CommonSpeciesUtils.is_human(sim_info_b):
                return CommonRelationshipTrackId.FRIENDSHIP
        elif CommonSpeciesUtils.is_animal(sim_info_a):
            if CommonSpeciesUtils.is_animal(sim_info_b):
                return None
            elif CommonSpeciesUtils.is_human(sim_info_b):
                return CommonRelationshipTrackId.SIM_TO_PET_FRIENDSHIP
        return None

    @classmethod
    def get_romance_relationship_track(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, None]:
        """get_romance_relationship_track(sim_info_a, sim_info_b)

        Get an appropriate Romance Relationship track between Sim A and Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: The decimal identifier of the Romance Relationship Track appropriate for Sim A to have with Sim B or None if not found.
        :rtype: Union[CommonRelationshipTrackId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info_a) and CommonSpeciesUtils.is_human(sim_info_b):
            return CommonRelationshipTrackId.ROMANCE
        return None

    # These are here for backwards compatibility.
    @staticmethod
    def _determine_friendship_track(sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        result = CommonRelationshipUtils.get_friendship_relationship_track(sim_info_a, sim_info_b)
        if result is None:
            return -1
        return result

    @staticmethod
    def _determine_romance_track(sim_info_a: SimInfo, sim_info_b: SimInfo) -> Union[CommonRelationshipTrackId, int]:
        result = CommonRelationshipUtils.get_romance_relationship_track(sim_info_a, sim_info_b)
        if result is None:
            return -1
        return result


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'common_relationship_commands')
log.enable()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_relationship_bit',
    'Add a relationship bit between two Sims.',
    command_arguments=(
        CommonConsoleCommandArgument('relationship_bit', 'Relationship Bit Id or Tuning Name', 'The decimal identifier or Tuning Name of the Relationship Bit to add.'),
        CommonConsoleCommandArgument('target_sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to add the relationship bit to.'),
        CommonConsoleCommandArgument('source_sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to add the relationship bit from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.add_rel_bit',
    )
)
def _common_add_relationship_bit(
    output: CommonConsoleCommandOutput,
    relationship_bit: TunableInstanceParam(Types.RELATIONSHIP_BIT),
    target_sim_info: SimInfo,
    source_sim_info: SimInfo = None
):
    if isinstance(relationship_bit, str):
        output(f'ERROR: Invalid relationship bit specified \'{relationship_bit}\' or it was not found.')
        return False
    if target_sim_info is None:
        output('ERROR: No Target was specified!')
        return False
    if source_sim_info is target_sim_info:
        output('ERROR: Cannot add a relationship bit to the same Sim.')
        return False
    output(f'Attempting to add relationship bit {relationship_bit} between {source_sim_info} and {target_sim_info}')
    if not CommonRelationshipUtils.add_relationship_bit(source_sim_info, target_sim_info, relationship_bit):
        output(f'FAILURE: Failed to add relationship bit {relationship_bit} between {source_sim_info} and {target_sim_info}.')
        return False
    output(f'SUCCESS: Successfully added relationship bit {relationship_bit} between {source_sim_info} and {target_sim_info}.')
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_relationship_bit',
    'Remove a relationship bit from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('relationship_bit', 'Relationship Bit Id or Tuning Name', 'The decimal identifier or Tuning Name of the Relationship Bit to remove.'),
        CommonConsoleCommandArgument('source_sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to remove the relationship bit from as the source.', is_optional=True, default_value='Active Sim'),
        CommonConsoleCommandArgument('target_sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to remove the relationship bit from as the target of the relationship bit. If not specified, the relationship bit will be removed regardless of target.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.remove_rel_bit',
    )
)
def _common_remove_relationship_bit(
    output: CommonConsoleCommandOutput,
    relationship_bit: TunableInstanceParam(Types.RELATIONSHIP_BIT),
    source_sim_info: SimInfo = None,
    target_sim_info: SimInfo = None,
):
    if isinstance(relationship_bit, str):
        output(f'ERROR: Invalid relationship bit specified \'{relationship_bit}\' or it was not found.')
        return False
    if target_sim_info is None:
        output('ERROR: No Target was specified!')
        return False
    if source_sim_info is target_sim_info:
        output(f'Attempting to remove relationship bit {relationship_bit} between {source_sim_info} for all other Sims.')
        if not CommonRelationshipUtils.remove_relationship_bit_from_all(source_sim_info, relationship_bit):
            output(f'FAILURE: Failed to remove relationship bit {relationship_bit} between {source_sim_info} for all other Sims.')
            return False
    else:
        output(f'Attempting to remove relationship bit {relationship_bit} between {source_sim_info} and {target_sim_info}')
        if not CommonRelationshipUtils.add_relationship_bit(source_sim_info, target_sim_info, relationship_bit):
            output(f'FAILURE: Failed to remove relationship bit {relationship_bit} between {source_sim_info} and {target_sim_info}.')
            return False
    output(f'SUCCESS: Successfully removed relationship bit {relationship_bit} between {source_sim_info} and {target_sim_info}.')
    return True


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_relationship_bits',
    'Print a list of all relationship bits a Sim has with other Sims.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printrelationshipbits',
        's4clib_testing.print_rel_bits',
        's4clib_testing.printrelbits'
    )
)
def _common_print_relationship_bits(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Printing relationship bits of Sim {sim_info} with other Sims.')
    sim_id_a = CommonSimUtils.get_sim_id(sim_info)
    text = ''
    for relationship in sim_info.relationship_tracker:
        sim_info_b = relationship.get_other_sim_info(sim_id_a)
        try:
            bi_direction_bits = relationship._bi_directional_relationship_data._bits
            inner_text = f'\n---------------------Relationship ({sim_info} to {sim_info_b})---------------------'
            if bi_direction_bits:
                inner_text += '\n Bi-Directional Bits:'
                for (key, value) in bi_direction_bits.items():
                    bit_type = type(value)
                    inner_text += f'\n  - {key.__name__} ({bit_type.__mro__[1].__name__})'
                inner_text += '\n'

            sim_a_relationship_bits = relationship._sim_a_relationship_data._bits
            if sim_a_relationship_bits:
                inner_text += f'\n Unidirectional Bits Sim A (What {sim_info_b} is to {sim_info}):'
                for (key, value) in sim_a_relationship_bits.items():
                    bit_type = type(value)
                    inner_text += f'\n  - {key.__name__} ({bit_type.__mro__[1].__name__})'
                inner_text += '\n'

            sim_b_relationship_bits = relationship._sim_b_relationship_data._bits
            if sim_b_relationship_bits:
                inner_text += f'\n Unidirectional Bits Sim B (What {sim_info} is to {sim_info_b}):'
                for (key, value) in sim_b_relationship_bits.items():
                    bit_type = type(value)
                    inner_text += f'\n  - {key.__name__} ({bit_type.__mro__[1].__name__})'
                inner_text += '\n'
            output(inner_text)
            text += inner_text
        except Exception as ex:
            output(f'An error occurred when handling relationship bits for Sims {sim_info} to {sim_info_b} for relationship {relationship}: {ex}')
            log.format_error_with_message('Failed to print relationships', sim_info=sim_info, sim_info_b=sim_info_b, relationship=relationship, exception=ex)
    log.debug(text)
    output('Done')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.meet_everyone',
    'Add the Has Met Relationship Bit between all Sim.'
)
def _common_meet_everyone(output: CommonConsoleCommandOutput):
    output('Attempting to make everyone meet everyone.')
    sim_pair_count = 0
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        for target_sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if sim_info is target_sim_info:
                continue
            if CommonRelationshipUtils.has_met(sim_info, target_sim_info):
                continue
            sim_pair_count += 1
            CommonRelationshipUtils.add_relationship_bit(sim_info, target_sim_info, CommonRelationshipBitId.HAS_MET)
            CommonRelationshipUtils.add_relationship_bit(target_sim_info, sim_info, CommonRelationshipBitId.HAS_MET)
    output(f'Done adding the Has Met relationship bit to {sim_pair_count} Sim pair(s).')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.unmeet_everyone',
    'Remove the Has Met Relationship Bit between all Sims.',
)
def _common_meet_everyone(output: CommonConsoleCommandOutput):
    output('Attempting to make everyone unmeet everyone.')
    sim_pair_count = 0
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        for target_sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if sim_info is target_sim_info:
                continue
            if not CommonRelationshipUtils.has_met(sim_info, target_sim_info):
                continue
            sim_pair_count += 1
            CommonRelationshipUtils.remove_relationship_bit(sim_info, target_sim_info, CommonRelationshipBitId.HAS_MET)
            CommonRelationshipUtils.remove_relationship_bit(target_sim_info, sim_info, CommonRelationshipBitId.HAS_MET)
    output(f'Done removing the Has Met relationship from {sim_pair_count} Sim pair(s).')
