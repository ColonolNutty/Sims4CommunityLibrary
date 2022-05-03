"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from sims4communitylib.enums.enumtypes.common_int import CommonInt

# noinspection PyBroadException
try:
    from weather.weather_enums import WeatherEffectType
except:
    class WeatherEffectType(CommonInt):
        """Mock class."""
        pass


class CommonWeatherEffectType(CommonInt):
    """Identifiers for weather effects types."""
    WINDOW_FROST: 'CommonWeatherEffectType' = 1004
    WATER_FROZEN: 'CommonWeatherEffectType' = 1005
    WIND: 'CommonWeatherEffectType' = 1006
    TEMPERATURE: 'CommonWeatherEffectType' = 1007
    THUNDER: 'CommonWeatherEffectType' = 1008
    LIGHTNING: 'CommonWeatherEffectType' = 1009
    SNOW_FRESHNESS: 'CommonWeatherEffectType' = 1010
    STRANGERVILLE_ACT: 'CommonWeatherEffectType' = 1011
    ECO_FOOTPRINT: 'CommonWeatherEffectType' = 1012
    ACID_RAIN: 'CommonWeatherEffectType' = 1013
    STAR_WARS_RESISTANCE: 'CommonWeatherEffectType' = 1014
    STAR_WARS_FIRST_ORDER: 'CommonWeatherEffectType' = 1015
    SNOW_ICINESS: 'CommonWeatherEffectType' = 1016

    @classmethod
    def get_all(cls) -> Tuple['CommonWeatherEffectType']:
        """get_all()

        Retrieve a collection of all CommonWeatherEffectType

        :return: A collection of all CommonWeatherEffectType
        :rtype: Tuple[CommonWeatherEffectType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonWeatherEffectType, ...] = tuple([value for value in cls.values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonWeatherEffectType') -> Union[WeatherEffectType, None]:
        """convert_to_vanilla(value)

        Convert a CommonWeatherEffectType into the vanilla WeatherEffectType enum.

        :param value: An instance of a CommonWeatherEffectType
        :type value: CommonWeatherEffectType
        :return: The specified CommonWeatherEffectType translated to a WeatherEffectType or None if a vanilla WeatherEffectType is not found.
        :rtype: Union[WeatherEffectType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), WeatherEffectType, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: WeatherEffectType) -> Union['CommonWeatherEffectType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla WeatherEffectType into a CommonWeatherEffectType enum.

        :param value: An instance of a CommonWeatherEffectType
        :type value: CommonWeatherEffectType
        :return: The specified WeatherEffectType translated to a WeatherEffectType or None if a CommonWeatherEffectType is not found.
        :rtype: Union[WeatherEffectType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonWeatherEffectType, default_value=None)
