"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonVoiceActorType(CommonInt):
    """Various Voice Actor types."""
    UNKNOWN: 'CommonVoiceActorType' = 0
    MUTE: 'CommonVoiceActorType' = 1
    ADULT_HUMAN_FEMALE_1: 'CommonVoiceActorType' = 1802970392
    ADULT_HUMAN_FEMALE_2: 'CommonVoiceActorType' = 1802970394

    ADULT_HUMAN_MALE_1: 'CommonVoiceActorType' = 1685527060
    ADULT_HUMAN_MALE_2: 'CommonVoiceActorType' = 1685527061

    @classmethod
    def get_all(cls) -> Tuple['CommonVoiceActorType']:
        """get_all()

        Retrieve a collection of all CommonVoiceActor, excluding CommonVoiceActor.INVALID.

        :return: A collection of all CommonVoiceActor, without CommonVoiceActor.INVALID.
        :rtype: Tuple[CommonVoiceActorType]
        """
        value_list: Tuple[CommonVoiceActorType] = tuple([value for value in cls.values if value != cls.UNKNOWN])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonVoiceActorType, excluding CommonVoiceActorType.INVALID.

        :return: A collection of the names of all CommonVoiceActorType, without CommonVoiceActorType.INVALID.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list
