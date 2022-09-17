"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSide(CommonInt):
    """A side of an object."""
    NONE: 'CommonSide' = ...
    LEFT: 'CommonSide' = ...
    RIGHT: 'CommonSide' = ...
    FRONT: 'CommonSide' = ...
    BACK: 'CommonSide' = ...
    TOP: 'CommonSide' = ...
    BOTTOM: 'CommonSide' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonSide'] = None) -> Tuple['CommonSide']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSide], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonSide]
        """
        if exclude_values is None:
            exclude_values = (cls.NONE,)
        # noinspection PyTypeChecker
        result: Tuple[CommonSide, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return result

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonSide'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will not be returned. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSide], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonSide'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will not be returned. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSide], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @classmethod
    def convert_to_opposite(cls, value: 'CommonSide') -> 'CommonSide':
        """convert_to_opposite(value)

        Convert a value to its opposite.

        :param value: An instance of a value
        :type value: CommonSide
        :return: The specified value converted to its opposite or the value itself if it could not be converted.
        :rtype: CommonSide
        """
        mapping = {
            CommonSide.LEFT: CommonSide.RIGHT,
            CommonSide.RIGHT: CommonSide.LEFT,
            CommonSide.FRONT: CommonSide.BACK,
            CommonSide.BACK: CommonSide.FRONT,
            CommonSide.TOP: CommonSide.BOTTOM,
            CommonSide.BOTTOM: CommonSide.TOP,
        }
        return mapping.get(value, value)

    @classmethod
    def convert_to_localized_string_id(cls, value: Union[int, 'CommonSide']) -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a value into a Localized String identifier.

        :param value: An instance of a value
        :type value: CommonSide
        :return: The specified value translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        mapping = {
            CommonSide.LEFT: CommonStringId.S4CL_LEFT,
            CommonSide.RIGHT: CommonStringId.S4CL_RIGHT,
            CommonSide.FRONT: CommonStringId.S4CL_FRONT,
            CommonSide.BACK: CommonStringId.S4CL_BACK,
            CommonSide.TOP: CommonStringId.S4CL_TOP,
            CommonSide.BOTTOM: CommonStringId.S4CL_BOTTOM,
        }
        return mapping.get(value, value.name if hasattr(value, 'name') else str(value))
