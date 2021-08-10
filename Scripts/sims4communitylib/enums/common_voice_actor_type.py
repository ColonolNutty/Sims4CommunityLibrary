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

    # Special
    KYLO_REN_1: 'CommonVoiceActorType' = 1719082469
    HONDO_OHNAKA_1: 'CommonVoiceActorType' = 1769415226
    REY_1: 'CommonVoiceActorType' = 1601639154

    # Human
    TODDLER_HUMAN_AMBIGUOUS_1: 'CommonVoiceActorType' = 1635194332

    CHILD_HUMAN_AMBIGUOUS_1: 'CommonVoiceActorType' = 1853303381
    CHILD_HUMAN_AMBIGUOUS_2: 'CommonVoiceActorType' = 1853303382

    ADULT_HUMAN_AMBIGUOUS_1: 'CommonVoiceActorType' = 1802970399

    ADULT_HUMAN_FEMININE_1: 'CommonVoiceActorType' = 1802970392
    ADULT_HUMAN_FEMININE_2: 'CommonVoiceActorType' = 1802970394

    ADULT_HUMAN_MASCULINE_1: 'CommonVoiceActorType' = 1685527060
    ADULT_HUMAN_MASCULINE_2: 'CommonVoiceActorType' = 1685527061
    ADULT_HUMAN_MASCULINE_3: 'CommonVoiceActorType' = 1685527063

    # Dog
    CHILD_DOG_AMBIGUOUS_1: 'CommonVoiceActorType' = 1786192777

    ADULT_DOG_AMBIGUOUS_1: 'CommonVoiceActorType' = 1836525760
    ADULT_DOG_AMBIGUOUS_2: 'CommonVoiceActorType' = 1836525762
    ADULT_DOG_AMBIGUOUS_3: 'CommonVoiceActorType' = 1836525763
    ADULT_DOG_AMBIGUOUS_4: 'CommonVoiceActorType' = 1836525765

    # Cat
    CHILD_CAT_AMBIGUOUS_1: 'CommonVoiceActorType' = 1719082493
    ADULT_CAT_AMBIGUOUS_1: 'CommonVoiceActorType' = 1702304872
    ADULT_CAT_AMBIGUOUS_2: 'CommonVoiceActorType' = 1702304875

    # Fox
    ADULT_FOX_AMBIGUOUS_1: 'CommonVoiceActorType' = 1886858530

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
