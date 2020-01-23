"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from statistics.mood import Mood
from sims4communitylib.enums.moods_enum import CommonMoodId


class CommonMoodUtils:
    """Utilities for manipulating Sim moods.

    """
    @staticmethod
    def is_angry(sim_info: SimInfo) -> bool:
        """Determine if a Sim is angry.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.ANGRY)

    @staticmethod
    def is_bored(sim_info: SimInfo) -> bool:
        """Determine if a Sim is bored.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.BORED)

    @staticmethod
    def is_confident(sim_info: SimInfo) -> bool:
        """Determine if a Sim is confident.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.CONFIDENT)

    @staticmethod
    def is_dazed(sim_info: SimInfo) -> bool:
        """Determine if a Sim is dazed.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.DAZED)

    @staticmethod
    def is_embarrassed(sim_info: SimInfo) -> bool:
        """Determine if a Sim is embarrassed.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.EMBARRASSED)

    @staticmethod
    def is_energized(sim_info: SimInfo) -> bool:
        """Determine if a Sim is energized.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.ENERGIZED)

    @staticmethod
    def is_fine(sim_info: SimInfo) -> bool:
        """Determine if a Sim is fine.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.FINE)

    @staticmethod
    def is_flirty(sim_info: SimInfo) -> bool:
        """Determine if a Sim is flirty.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.FLIRTY)

    @staticmethod
    def is_focused(sim_info: SimInfo) -> bool:
        """Determine if a Sim is focused.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.FOCUSED)

    @staticmethod
    def is_happy(sim_info: SimInfo) -> bool:
        """Determine if a Sim is happy.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.HAPPY)

    @staticmethod
    def is_inspired(sim_info: SimInfo) -> bool:
        """Determine if a Sim is inspired.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.INSPIRED)

    @staticmethod
    def is_playful(sim_info: SimInfo) -> bool:
        """Determine if a Sim is playful.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.PLAYFUL)

    @staticmethod
    def is_sad(sim_info: SimInfo) -> bool:
        """Determine if a Sim is sad.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.SAD)

    @staticmethod
    def is_stressed(sim_info: SimInfo) -> bool:
        """Determine if a Sim is stressed.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.STRESSED)

    @staticmethod
    def is_uncomfortable(sim_info: SimInfo) -> bool:
        """Determine if a Sim is uncomfortable.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.UNCOMFORTABLE)

    @staticmethod
    def is_possessed(sim_info: SimInfo) -> bool:
        """Determine if a Sim is possessed.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.POSSESSED)

    @staticmethod
    def is_sleeping(sim_info: SimInfo) -> bool:
        """Determine if a Sim is sleeping.

        """
        return CommonMoodUtils.has_mood(sim_info, CommonMoodId.SLEEPING)

    @staticmethod
    def has_mood(sim_info: SimInfo, mood_id: int) -> bool:
        """Determine if a Sim has the specified mood.

        """
        return CommonMoodUtils.get_current_mood_id(sim_info) == mood_id

    @staticmethod
    def get_current_mood(sim_info: SimInfo) -> Mood:
        """Retrieve the current mood for the specified Sim.

        """
        return sim_info.get_mood()

    @staticmethod
    def get_current_mood_id(sim_info: SimInfo) -> int:
        """Retrieve an identifier of the current mood for the specified Sim.

        """
        return getattr(CommonMoodUtils.get_current_mood(sim_info), 'guid64', -1)
