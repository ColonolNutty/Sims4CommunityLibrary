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
    from weather.weather_enums import PrecipitationType
except:
    class PrecipitationType(CommonInt):
        """Mock class."""
        RAIN = 1000
        SNOW = 1001


class CommonPrecipitationType(CommonInt):
    """Identifiers for precipitation types."""
    RAIN: 'CommonPrecipitationType' = ...
    SNOW: 'CommonPrecipitationType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonPrecipitationType'] = ()) -> Tuple['CommonPrecipitationType']:
        """get_all(exclude_values=())

        Get a collection of all values.

        :param exclude_values: These values will be excluded. Default is an empty collection.
        :type exclude_values: Iterator[CommonPrecipitationType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonPrecipitationType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonPrecipitationType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonPrecipitationType') -> PrecipitationType:
        """convert_to_vanilla(value)

        Convert a CommonPrecipitationType into PrecipitationType.

        :param value: An instance of CommonPrecipitationType
        :type value: CommonPrecipitationType
        :return: The specified CommonPrecipitationType translated to PrecipitationType, or the value itself if the value could not be translated.
        :rtype: PrecipitationType
        """
        if isinstance(value, PrecipitationType):
            return value
        mapping = {
            CommonPrecipitationType.RAIN: PrecipitationType.RAIN,
            CommonPrecipitationType.SNOW: PrecipitationType.SNOW
        }
        return mapping.get(value, value)

    @staticmethod
    def convert_from_vanilla(value: PrecipitationType) -> Union['CommonPrecipitationType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla PrecipitationType into CommonPrecipitationType.

        :param value: An instance of PrecipitationType
        :type value: PrecipitationType
        :return: The specified PrecipitationType translated to CommonPrecipitationType, or the value itself if the value could not be translated.
        :rtype: CommonPrecipitationType
        """
        if isinstance(value, CommonPrecipitationType):
            return value
        mapping = {
            PrecipitationType.RAIN: CommonPrecipitationType.RAIN,
            PrecipitationType.SNOW: CommonPrecipitationType.SNOW
        }
        return mapping.get(value, value)
