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
    from weather.weather_enums import Temperature
except:
    class Temperature(CommonInt):
        """Mock class."""
        FREEZING = -3
        COLD = -2
        COOL = -1
        WARM = 0
        HOT = 1
        BURNING = 2


class CommonTemperature(CommonInt):
    """Identifiers for temperatures."""
    FREEZING: 'CommonTemperature' = ...
    COLD: 'CommonTemperature' = ...
    COOL: 'CommonTemperature' = ...
    WARM: 'CommonTemperature' = ...
    HOT: 'CommonTemperature' = ...
    BURNING: 'CommonTemperature' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonTemperature'] = ()) -> Tuple['CommonTemperature']:
        """get_all(exclude_values=())

        Get a collection of all values.

        :param exclude_values: These values will be excluded. Default is an empty collection.
        :type exclude_values: Iterator[CommonTemperature], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonTemperature]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonTemperature, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonTemperature') -> Union[Temperature, None]:
        """convert_to_vanilla(value)

        Convert a value into Temperature.

        :param value: An instance of CommonTemperature
        :type value: CommonTemperature
        :return: The specified value translated to Temperature, or None if the value could not be translated.
        :rtype: Union[Temperature, None]
        """
        if value is None:
            return None
        if isinstance(value, Temperature):
            return value
        mapping = {
            CommonTemperature.FREEZING: Temperature.FREEZING,
            CommonTemperature.COLD: Temperature.COLD,
            CommonTemperature.COOL: Temperature.COOL,
            CommonTemperature.WARM: Temperature.WARM,
            CommonTemperature.HOT: Temperature.HOT,
            CommonTemperature.BURNING: Temperature.BURNING,
        }
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: Temperature) -> Union['CommonTemperature', None]:
        """convert_from_vanilla(value)

        Convert a value into CommonTemperature.

        :param value: An instance of Temperature
        :type value: Temperature
        :return: The specified value translated to CommonTemperature, or None if the value could not be translated.
        :rtype: Union[CommonTemperature, None]
        """
        if value is None:
            return None
        if isinstance(value, CommonTemperature):
            return value
        mapping = {
            Temperature.FREEZING: CommonTemperature.FREEZING,
            Temperature.COLD: CommonTemperature.COLD,
            Temperature.COOL: CommonTemperature.COOL,
            Temperature.WARM: CommonTemperature.WARM,
            Temperature.HOT: CommonTemperature.HOT,
            Temperature.BURNING: CommonTemperature.BURNING,
        }
        return mapping.get(value, None)
