"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator

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

    INFANT_HUMAN_AMBIGUOUS_1: 'CommonVoiceActorType' = 1752637603

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

    # Horse
    ADULT_HORSE_AMBIGUOUS_1: 'CommonVoiceActorType' = 1886858546
    CHILD_HORSE_AMBIGUOUS_1: 'CommonVoiceActorType' = 1853303388

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonVoiceActorType'] = None) -> Tuple['CommonVoiceActorType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, UNKNOWN will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonVoiceActorType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonVoiceActorType]
        """
        if exclude_values is None:
            exclude_values = (cls.UNKNOWN,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonVoiceActorType] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonVoiceActorType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, UNKNOWN will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonVoiceActorType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonVoiceActorType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, UNKNOWN will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonVoiceActorType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))
