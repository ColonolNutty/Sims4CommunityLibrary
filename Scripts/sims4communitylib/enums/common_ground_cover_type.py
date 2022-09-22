"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Iterator

from sims4communitylib.enums.enumtypes.common_int import CommonInt

# noinspection PyBroadException
try:
    from weather.weather_enums import GroundCoverType
except:
    class GroundCoverType(CommonInt):
        """Mock class."""
        RAIN_ACCUMULATION = 1002
        SNOW_ACCUMULATION = 1003


class CommonGroundCoverType(CommonInt):
    """Identifiers for ground cover types."""
    RAIN_ACCUMULATION: 'CommonGroundCoverType' = ...
    SNOW_ACCUMULATION: 'CommonGroundCoverType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonGroundCoverType'] = ()) -> Tuple['CommonGroundCoverType']:
        """get_all(exclude_values=())

        Get a collection of all values.

        :param exclude_values: These values will be excluded. Default is an empty collection.
        :type exclude_values: Iterator[CommonGroundCoverType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonGroundCoverType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonGroundCoverType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonGroundCoverType') -> Union[GroundCoverType, None]:
        """convert_to_vanilla(value)

        Convert a CommonGroundCoverType into the vanilla GroundCoverType enum.

        :param value: An instance of CommonGroundCoverType
        :type value: CommonGroundCoverType
        :return: The specified CommonGroundCoverType translated to GroundCoverType, or None if the value could not be translated.
        :rtype: Union[GroundCoverType, None]
        """
        if isinstance(value, GroundCoverType):
            return value
        mapping = {
            CommonGroundCoverType.RAIN_ACCUMULATION: GroundCoverType.RAIN_ACCUMULATION,
            CommonGroundCoverType.SNOW_ACCUMULATION: GroundCoverType.SNOW_ACCUMULATION
        }
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: GroundCoverType) -> Union['CommonGroundCoverType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla GroundCoverType into a CommonGroundCoverType enum.

        :param value: An instance of GroundCoverType
        :type value: GroundCoverType
        :return: The specified GroundCoverType translated to CommonGroundCoverType, or None if the value could not be translated.
        :rtype: Union[CommonGroundCoverType, None]
        """
        if isinstance(value, CommonGroundCoverType):
            return value
        mapping = {
            GroundCoverType.RAIN_ACCUMULATION: CommonGroundCoverType.RAIN_ACCUMULATION,
            GroundCoverType.SNOW_ACCUMULATION: CommonGroundCoverType.SNOW_ACCUMULATION
        }
        return mapping.get(value, None)
