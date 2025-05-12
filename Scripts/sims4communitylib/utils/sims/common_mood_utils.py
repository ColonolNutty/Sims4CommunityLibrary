"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from statistics.mood import Mood
from sims4communitylib.enums.moods_enum import CommonMoodId


class CommonMoodUtils:
    """Utilities for manipulating Sim moods.

    """
    @staticmethod
    def is_angry(sim_info: SimInfo) -> bool:
        """is_angry(sim_info)

        Determine if a Sim is angry.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.ANGRY)

    @staticmethod
    def is_bored(sim_info: SimInfo) -> bool:
        """is_bored(sim_info)

        Determine if a Sim is bored.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.BORED)

    @staticmethod
    def is_confident(sim_info: SimInfo) -> bool:
        """is_confident(sim_info)

        Determine if a Sim is confident.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.CONFIDENT)

    @staticmethod
    def is_dazed(sim_info: SimInfo) -> bool:
        """is_dazed(sim_info)

        Determine if a Sim is dazed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.DAZED)

    @staticmethod
    def is_embarrassed(sim_info: SimInfo) -> bool:
        """is_embarrassed(sim_info)

        Determine if a Sim is embarrassed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.EMBARRASSED)

    @staticmethod
    def is_energized(sim_info: SimInfo) -> bool:
        """is_energized(sim_info)

        Determine if a Sim is energized.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.ENERGIZED)

    @staticmethod
    def is_fine(sim_info: SimInfo) -> bool:
        """is_fine(sim_info)

        Determine if a Sim is fine.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.FINE)

    @staticmethod
    def is_flirty(sim_info: SimInfo) -> bool:
        """is_flirty(sim_info)

        Determine if a Sim is flirty.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.FLIRTY)

    @staticmethod
    def is_focused(sim_info: SimInfo) -> bool:
        """is_focused(sim_info)

        Determine if a Sim is focused.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.FOCUSED)

    @staticmethod
    def is_happy(sim_info: SimInfo) -> bool:
        """is_happy(sim_info)

        Determine if a Sim is happy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.HAPPY)

    @staticmethod
    def is_inspired(sim_info: SimInfo) -> bool:
        """is_inspired(sim_info)

        Determine if a Sim is inspired.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.INSPIRED)

    @staticmethod
    def is_playful(sim_info: SimInfo) -> bool:
        """is_playful(sim_info)

        Determine if a Sim is playful.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.PLAYFUL)

    @staticmethod
    def is_sad(sim_info: SimInfo) -> bool:
        """is_sad(sim_info)

        Determine if a Sim is sad.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.SAD)

    @staticmethod
    def is_stressed(sim_info: SimInfo) -> bool:
        """is_stressed(sim_info)

        Determine if a Sim is stressed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.STRESSED)

    @staticmethod
    def is_uncomfortable(sim_info: SimInfo) -> bool:
        """is_uncomfortable(sim_info)

        Determine if a Sim is uncomfortable.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.UNCOMFORTABLE)

    @staticmethod
    def is_possessed(sim_info: SimInfo) -> bool:
        """is_possessed(sim_info)

        Determine if a Sim is possessed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.POSSESSED)

    @staticmethod
    def is_sleeping(sim_info: SimInfo) -> bool:
        """is_sleeping(sim_info)

        Determine if a Sim is sleeping.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is the Mood. False, if the Sim is not.
        :rtype: bool
        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.SLEEPING)

    @staticmethod
    def has_mood(sim_info: SimInfo, mood_id: CommonMoodId) -> bool:
        """has_mood(sim_info, mood_id)

        Determine if a Sim has the specified mood.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param mood_id: The identifier of the Mood to check for.
        :type mood_id: CommonMoodId
        :return: True, if the Sim has the specified Mood. False, if the Sim does not.
        :rtype: bool
        """
        if not hasattr(sim_info, 'get_mood'):
            return False
        try:
            current_mood_id = CommonMoodUtils.get_current_mood_id(sim_info)
            if current_mood_id == -1:
                return False
            return current_mood_id == mood_id
        except AttributeError:
            return False

    @staticmethod
    def get_current_mood(sim_info: SimInfo) -> Union[Mood, None]:
        """get_current_mood(sim_info)

        Retrieve the current mood for the specified Sim.

        :param sim_info: The Sim to retrieve the mood of.
        :type sim_info: SimInfo
        :return: The current Mood of the Sim.
        :rtype: Mood
        """
        if not hasattr(sim_info, 'get_mood'):
            return None
        try:
            return sim_info.get_mood()
        except AttributeError:
            return None

    @staticmethod
    def get_current_mood_id(sim_info: SimInfo) -> int:
        """get_current_mood_id(sim_info)

        Retrieve an identifier of the current mood for the specified Sim.

        :param sim_info: The Sim to retrieve the mood identifier of.
        :type sim_info: SimInfo
        :return: The identifier of the current Mood of the Sim.
        :rtype: int
        """
        if not hasattr(sim_info, 'get_mood'):
            return -1
        current_mood = CommonMoodUtils.get_current_mood(sim_info)
        if current_mood is None:
            return -1
        return getattr(current_mood, 'guid64', -1)
