"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonObjectQuality(CommonInt):
    """Various types of object quality."""
    POOR: 'CommonObjectQuality' = ...
    NORMAL: 'CommonObjectQuality' = ...
    OUTSTANDING: 'CommonObjectQuality' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonObjectQuality'] = ()) -> Tuple['CommonObjectQuality']:
        """get_all(exclude_values=())

        Get a collection of all values.

        :param exclude_values: These values will be excluded. Default is an empty collection.
        :type exclude_values: Iterator[CommonObjectQuality], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonObjectQuality]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonObjectQuality, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonObjectQuality'] = ()) -> Tuple[str]:
        """get_all_names(exclude_values=())

        Retrieve a collection of the names of all values.

        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonObjectQuality'] = ()) -> str:
        """get_comma_separated_names_string(exclude_values=())

        Create a string containing all names of all values, separated by a comma.

        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))
