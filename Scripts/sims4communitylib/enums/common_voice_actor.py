"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonVoiceActor(CommonInt):
    """Various Voice Actor values."""
    INVALID: 'CommonVoiceActor' = 0
    MUTE: 'CommonVoiceActor' = 1
    FEMALE_1: 'CommonVoiceActor' = 1802970392
    FEMALE_2: 'CommonVoiceActor' = 1802970394

    MALE_1: 'CommonVoiceActor' = 1685527060
    MALE_2: 'CommonVoiceActor' = 1685527061

    @classmethod
    def get_all(cls) -> Tuple['CommonVoiceActor']:
        """get_all()

        Retrieve a collection of all CommonVoiceActor, excluding CommonVoiceActor.INVALID.

        :return: A collection of all CommonVoiceActor, without CommonVoiceActor.INVALID.
        :rtype: Tuple[CommonVoiceActor]
        """
        value_list: Tuple[CommonVoiceActor] = tuple([value for value in cls.values if value != cls.INVALID])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonVoiceActor, excluding CommonVoiceActor.INVALID.

        :return: A collection of the names of all CommonVoiceActor, without CommonVoiceActor.INVALID.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list
