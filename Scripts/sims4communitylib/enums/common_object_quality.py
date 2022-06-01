"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonObjectQuality(CommonInt):
    """Various types of object quality."""
    POOR: 'CommonObjectQuality' = ...
    NORMAL: 'CommonObjectQuality' = ...
    OUTSTANDING: 'CommonObjectQuality' = ...

    @classmethod
    def get_all(cls) -> Tuple['CommonObjectQuality']:
        """get_all()

        Retrieve a collection of all CommonObjectQuality.

        :return: A collection of all CommonObjectQuality.
        :rtype: Tuple[CommonObjectQuality]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonObjectQuality, ...] = tuple([value for value in cls.values])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonObjectQuality.

        :return: A collection of the names of all CommonObjectQuality.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls) -> str:
        """get_comma_separated_names_string()

        Create a string containing all names of all CommonObjectQuality values, separated by a comma.

        :return: A string containing all names of all CommonObjectQuality values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names())
