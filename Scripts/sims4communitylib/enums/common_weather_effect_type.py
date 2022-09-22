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
    from weather.weather_enums import WeatherEffectType
except:
    class WeatherEffectType(CommonInt):
        """Mock class."""
        WINDOW_FROST = 1004
        WATER_FROZEN = 1005
        WIND = 1006
        TEMPERATURE = 1007
        THUNDER = 1008
        LIGHTNING = 1009
        SNOW_FRESHNESS = 1010
        STRANGERVILLE_ACT = 1011
        ECO_FOOTPRINT = 1012
        ACID_RAIN = 1013
        # noinspection SpellCheckingInspection
        STARWARS_RESISTANCE = 1014
        # noinspection SpellCheckingInspection
        STARWARS_FIRST_ORDER = 1015
        SNOW_ICINESS = 1016


class CommonWeatherEffectType(CommonInt):
    """Identifiers for weather effects types."""
    WINDOW_FROST: 'CommonWeatherEffectType' = ...
    WATER_FROZEN: 'CommonWeatherEffectType' = ...
    WIND: 'CommonWeatherEffectType' = ...
    TEMPERATURE: 'CommonWeatherEffectType' = ...
    THUNDER: 'CommonWeatherEffectType' = ...
    LIGHTNING: 'CommonWeatherEffectType' = ...
    SNOW_FRESHNESS: 'CommonWeatherEffectType' = ...
    STRANGERVILLE_ACT: 'CommonWeatherEffectType' = ...
    ECO_FOOTPRINT: 'CommonWeatherEffectType' = ...
    ACID_RAIN: 'CommonWeatherEffectType' = ...
    STAR_WARS_RESISTANCE: 'CommonWeatherEffectType' = ...
    STAR_WARS_FIRST_ORDER: 'CommonWeatherEffectType' = ...
    SNOW_ICINESS: 'CommonWeatherEffectType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonWeatherEffectType'] = ()) -> Tuple['CommonWeatherEffectType']:
        """get_all(exclude_values=())

        Get a collection of all values.

        :param exclude_values: These values will be excluded. Default is an empty collection.
        :type exclude_values: Iterator[CommonWeatherEffectType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonWeatherEffectType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonWeatherEffectType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonWeatherEffectType') -> Union[WeatherEffectType, None]:
        """convert_to_vanilla(value)

        Convert a CommonWeatherEffectType into WeatherEffectType.

        :param value: An instance of CommonWeatherEffectType
        :type value: CommonWeatherEffectType
        :return: The specified CommonWeatherEffectType translated to WeatherEffectType, or None if the value could not be translated.
        :rtype: Union[WeatherEffectType, None]
        """
        if isinstance(value, WeatherEffectType):
            return value
        mapping = {
            CommonWeatherEffectType.WINDOW_FROST: WeatherEffectType.WINDOW_FROST,
            CommonWeatherEffectType.WATER_FROZEN: WeatherEffectType.WATER_FROZEN,
            CommonWeatherEffectType.WIND: WeatherEffectType.WIND,
            CommonWeatherEffectType.TEMPERATURE: WeatherEffectType.TEMPERATURE,
            CommonWeatherEffectType.THUNDER: WeatherEffectType.THUNDER,
            CommonWeatherEffectType.LIGHTNING: WeatherEffectType.LIGHTNING,
            CommonWeatherEffectType.SNOW_FRESHNESS: WeatherEffectType.SNOW_FRESHNESS,
            CommonWeatherEffectType.STRANGERVILLE_ACT: WeatherEffectType.STRANGERVILLE_ACT,
            CommonWeatherEffectType.ECO_FOOTPRINT: WeatherEffectType.ECO_FOOTPRINT,
            CommonWeatherEffectType.ACID_RAIN: WeatherEffectType.ACID_RAIN,
            CommonWeatherEffectType.STAR_WARS_RESISTANCE: WeatherEffectType.STARWARS_RESISTANCE,
            CommonWeatherEffectType.STAR_WARS_FIRST_ORDER: WeatherEffectType.STARWARS_FIRST_ORDER,
            CommonWeatherEffectType.SNOW_ICINESS: WeatherEffectType.SNOW_ICINESS,
        }
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: WeatherEffectType) -> Union['CommonWeatherEffectType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla WeatherEffectType into CommonWeatherEffectType.

        :param value: An instance of WeatherEffectType
        :type value: WeatherEffectType
        :return: The specified WeatherEffectType translated to CommonWeatherEffectType, or None if the value could not be translated.
        :rtype: Union[CommonWeatherEffectType, None]
        """
        if isinstance(value, CommonWeatherEffectType):
            return value
        mapping = {
            WeatherEffectType.WINDOW_FROST: CommonWeatherEffectType.WINDOW_FROST,
            WeatherEffectType.WATER_FROZEN: CommonWeatherEffectType.WATER_FROZEN,
            WeatherEffectType.WIND: CommonWeatherEffectType.WIND,
            WeatherEffectType.TEMPERATURE: CommonWeatherEffectType.TEMPERATURE,
            WeatherEffectType.THUNDER: CommonWeatherEffectType.THUNDER,
            WeatherEffectType.LIGHTNING: CommonWeatherEffectType.LIGHTNING,
            WeatherEffectType.SNOW_FRESHNESS: CommonWeatherEffectType.SNOW_FRESHNESS,
            WeatherEffectType.STRANGERVILLE_ACT: CommonWeatherEffectType.STRANGERVILLE_ACT,
            WeatherEffectType.ECO_FOOTPRINT: CommonWeatherEffectType.ECO_FOOTPRINT,
            WeatherEffectType.ACID_RAIN: CommonWeatherEffectType.ACID_RAIN,
            WeatherEffectType.STARWARS_RESISTANCE: CommonWeatherEffectType.STAR_WARS_RESISTANCE,
            WeatherEffectType.STARWARS_FIRST_ORDER: CommonWeatherEffectType.STAR_WARS_FIRST_ORDER,
            WeatherEffectType.SNOW_ICINESS: CommonWeatherEffectType.SNOW_ICINESS,
        }
        return mapping.get(value, None)
