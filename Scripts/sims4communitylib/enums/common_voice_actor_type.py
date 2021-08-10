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
    TODDLER_HUMAN_1: 'CommonVoiceActorType' = 1635194332

    CHILD_HUMAN_1: 'CommonVoiceActorType' = 1853303381
    CHILD_HUMAN_2: 'CommonVoiceActorType' = 1853303382

    ADULT_HUMAN_1: 'CommonVoiceActorType' = 1802970399

    TODDLER_HUMAN_FEMALE_1: 'CommonVoiceActorType' = TODDLER_HUMAN_1
    CHILD_HUMAN_FEMALE_1: 'CommonVoiceActorType' = CHILD_HUMAN_1
    CHILD_HUMAN_FEMALE_2: 'CommonVoiceActorType' = CHILD_HUMAN_2
    ADULT_HUMAN_FEMALE_1: 'CommonVoiceActorType' = 1802970392
    ADULT_HUMAN_FEMALE_2: 'CommonVoiceActorType' = 1802970394
    ADULT_HUMAN_FEMALE_3: 'CommonVoiceActorType' = ADULT_HUMAN_1

    TODDLER_HUMAN_MALE_1: 'CommonVoiceActorType' = TODDLER_HUMAN_1
    CHILD_HUMAN_MALE_1: 'CommonVoiceActorType' = CHILD_HUMAN_1
    CHILD_HUMAN_MALE_2: 'CommonVoiceActorType' = CHILD_HUMAN_2
    ADULT_HUMAN_MALE_1: 'CommonVoiceActorType' = 1685527060
    ADULT_HUMAN_MALE_2: 'CommonVoiceActorType' = 1685527061
    ADULT_HUMAN_MALE_3: 'CommonVoiceActorType' = 1685527063
    ADULT_HUMAN_MALE_4: 'CommonVoiceActorType' = ADULT_HUMAN_1

    # Dog
    CHILD_DOG_1: 'CommonVoiceActorType' = 1786192777

    ADULT_DOG_1: 'CommonVoiceActorType' = 1836525760
    ADULT_DOG_2: 'CommonVoiceActorType' = 1836525762
    ADULT_DOG_3: 'CommonVoiceActorType' = 1836525763
    ADULT_DOG_4: 'CommonVoiceActorType' = 1836525765

    # Large Dog
    ADULT_LARGE_DOG_1: 'CommonVoiceActorType' = ADULT_DOG_1
    ADULT_LARGE_DOG_2: 'CommonVoiceActorType' = ADULT_DOG_2
    ADULT_LARGE_DOG_3: 'CommonVoiceActorType' = ADULT_DOG_3
    ADULT_LARGE_DOG_4: 'CommonVoiceActorType' = ADULT_DOG_4

    CHILD_LARGE_DOG_FEMALE_1: 'CommonVoiceActorType' = CHILD_DOG_1
    ADULT_LARGE_DOG_FEMALE_1: 'CommonVoiceActorType' = ADULT_LARGE_DOG_1
    ADULT_LARGE_DOG_FEMALE_2: 'CommonVoiceActorType' = ADULT_LARGE_DOG_2
    ADULT_LARGE_DOG_FEMALE_3: 'CommonVoiceActorType' = ADULT_LARGE_DOG_3
    ADULT_LARGE_DOG_FEMALE_4: 'CommonVoiceActorType' = ADULT_LARGE_DOG_4

    CHILD_LARGE_DOG_MALE_1: 'CommonVoiceActorType' = CHILD_DOG_1
    ADULT_LARGE_DOG_MALE_1: 'CommonVoiceActorType' = ADULT_LARGE_DOG_1
    ADULT_LARGE_DOG_MALE_2: 'CommonVoiceActorType' = ADULT_LARGE_DOG_2
    ADULT_LARGE_DOG_MALE_3: 'CommonVoiceActorType' = ADULT_LARGE_DOG_3
    ADULT_LARGE_DOG_MALE_4: 'CommonVoiceActorType' = ADULT_LARGE_DOG_4

    # Small Dog
    ADULT_SMALL_DOG_1: 'CommonVoiceActorType' = ADULT_DOG_1
    ADULT_SMALL_DOG_2: 'CommonVoiceActorType' = ADULT_DOG_2
    ADULT_SMALL_DOG_3: 'CommonVoiceActorType' = ADULT_DOG_3
    ADULT_SMALL_DOG_4: 'CommonVoiceActorType' = ADULT_DOG_4

    CHILD_SMALL_DOG_FEMALE_1: 'CommonVoiceActorType' = CHILD_DOG_1
    ADULT_SMALL_DOG_FEMALE_1: 'CommonVoiceActorType' = ADULT_SMALL_DOG_1
    ADULT_SMALL_DOG_FEMALE_2: 'CommonVoiceActorType' = ADULT_SMALL_DOG_2
    ADULT_SMALL_DOG_FEMALE_3: 'CommonVoiceActorType' = ADULT_SMALL_DOG_3
    ADULT_SMALL_DOG_FEMALE_4: 'CommonVoiceActorType' = ADULT_SMALL_DOG_4

    CHILD_SMALL_DOG_MALE_1: 'CommonVoiceActorType' = CHILD_DOG_1
    ADULT_SMALL_DOG_MALE_1: 'CommonVoiceActorType' = ADULT_SMALL_DOG_1
    ADULT_SMALL_DOG_MALE_2: 'CommonVoiceActorType' = ADULT_SMALL_DOG_2
    ADULT_SMALL_DOG_MALE_3: 'CommonVoiceActorType' = ADULT_SMALL_DOG_3
    ADULT_SMALL_DOG_MALE_4: 'CommonVoiceActorType' = ADULT_SMALL_DOG_4

    # Cat
    CHILD_CAT_1: 'CommonVoiceActorType' = 1719082493
    ADULT_CAT_1: 'CommonVoiceActorType' = 1702304872
    ADULT_CAT_2: 'CommonVoiceActorType' = 1702304875

    CHILD_CAT_FEMALE_1: 'CommonVoiceActorType' = CHILD_CAT_1
    ADULT_CAT_FEMALE_1: 'CommonVoiceActorType' = ADULT_CAT_1
    ADULT_CAT_FEMALE_2: 'CommonVoiceActorType' = ADULT_CAT_2

    CHILD_CAT_MALE_1: 'CommonVoiceActorType' = CHILD_CAT_1
    ADULT_CAT_MALE_1: 'CommonVoiceActorType' = ADULT_CAT_1
    ADULT_CAT_MALE_2: 'CommonVoiceActorType' = ADULT_CAT_2

    # Fox
    ADULT_FOX_1: 'CommonVoiceActorType' = 1886858530

    ADULT_FOX_FEMALE_1: 'CommonVoiceActorType' = ADULT_FOX_1
    ADULT_FOX_MALE_1: 'CommonVoiceActorType' = ADULT_FOX_1

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
