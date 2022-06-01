"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from sims4communitylib.enums.common_temperature import CommonTemperature
from sims4communitylib.enums.enumtypes.common_int import CommonInt

# noinspection PyBroadException
try:
    from weather.weather_enums import WeatherType
except:
    class WeatherType(CommonInt):
        """Mock class."""
        pass


class CommonWeatherType(CommonInt):
    """Identifiers for weather types."""
    FREEZING: 'CommonWeatherType' = CommonTemperature.FREEZING
    COLD: 'CommonWeatherType' = CommonTemperature.COLD
    COOL: 'CommonWeatherType' = CommonTemperature.COOL
    WARM: 'CommonWeatherType' = CommonTemperature.WARM
    HOT: 'CommonWeatherType' = CommonTemperature.HOT
    BURNING: 'CommonWeatherType' = CommonTemperature.BURNING
    UNDEFINED: 'CommonWeatherType' = 10
    ANY_SNOW: 'CommonWeatherType' = 11
    ANY_RAIN: 'CommonWeatherType' = 12
    MAX_SNOW_ACCUMULATION: 'CommonWeatherType' = 13
    MAX_RAIN_ACCUMULATION: 'CommonWeatherType' = 14
    ANY_LIGHTNING: 'CommonWeatherType' = 15
    STRUCK_BY_LIGHTNING: 'CommonWeatherType' = 16

    @classmethod
    def get_all(cls) -> Tuple['CommonWeatherType']:
        """get_all()

        Retrieve a collection of all CommonWeatherType, excluding UNDEFINED

        :return: A collection of all CommonWeatherType, without UNDEFINED
        :rtype: Tuple[CommonWeatherType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonWeatherType, ...] = tuple([value for value in cls.values if value != CommonWeatherType.UNDEFINED])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonWeatherType') -> Union[WeatherType, None]:
        """convert_to_vanilla(value)

        Convert a CommonWeatherType into WeatherType.

        :param value: An instance of CommonWeatherType
        :type value: CommonWeatherType
        :return: The specified CommonWeatherType translated to WeatherType, or None if the value could not be translated.
        :rtype: Union[WeatherType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), WeatherType, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: WeatherType) -> Union['CommonWeatherType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla WeatherType into CommonWeatherType.

        :param value: An instance of WeatherType
        :type value: WeatherType
        :return: The specified WeatherType translated to CommonWeatherType, or None if the value could not be translated.
        :rtype: Union[CommonWeatherType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonWeatherType, default_value=None)
