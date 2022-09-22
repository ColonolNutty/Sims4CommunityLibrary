"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Iterator

from sims4communitylib.enums.common_temperature import Temperature
from sims4communitylib.enums.enumtypes.common_int import CommonInt

# noinspection PyBroadException
try:
    from weather.weather_enums import WeatherType
except:
    class WeatherType(CommonInt):
        """Mock class."""
        Freezing = Temperature.FREEZING
        Cold = Temperature.COLD
        Cool = Temperature.COOL
        Warm = Temperature.WARM
        Hot = Temperature.HOT
        Burning = Temperature.BURNING
        UNDEFINED = 10
        AnySnow = 11
        AnyRain = 12
        Max_Snow_Accumulation = 13
        Max_Rain_Accumulation = 14
        AnyLightning = 15
        StruckByLightning = 16


class CommonWeatherType(CommonInt):
    """Identifiers for weather types."""
    UNDEFINED: 'CommonWeatherType' = ...
    FREEZING: 'CommonWeatherType' = ...
    COLD: 'CommonWeatherType' = ...
    COOL: 'CommonWeatherType' = ...
    WARM: 'CommonWeatherType' = ...
    HOT: 'CommonWeatherType' = ...
    BURNING: 'CommonWeatherType' = ...
    ANY_SNOW: 'CommonWeatherType' = ...
    ANY_RAIN: 'CommonWeatherType' = ...
    MAX_SNOW_ACCUMULATION: 'CommonWeatherType' = ...
    MAX_RAIN_ACCUMULATION: 'CommonWeatherType' = ...
    ANY_LIGHTNING: 'CommonWeatherType' = ...
    STRUCK_BY_LIGHTNING: 'CommonWeatherType' = ...
    RAIN_LIGHT: 'CommonWeatherType' = ...
    RAIN_HEAVY: 'CommonWeatherType' = ...
    RAIN_STORM: 'CommonWeatherType' = ...
    SNOW_LIGHT: 'CommonWeatherType' = ...
    SNOW_HEAVY: 'CommonWeatherType' = ...
    SNOW_STORM: 'CommonWeatherType' = ...
    CLOUDY_PARTIAL: 'CommonWeatherType' = ...
    CLOUDY_FULL: 'CommonWeatherType' = ...
    WINDY: 'CommonWeatherType' = ...
    SUN_SHOWER: 'CommonWeatherType' = ...
    SUNNY: 'CommonWeatherType' = ...
    HEATWAVE: 'CommonWeatherType' = ...
    THUNDER: 'CommonWeatherType' = ...
    MIN_SNOW_ACCUMULATION: 'CommonWeatherType' = ...
    MED_SNOW_ACCUMULATION: 'CommonWeatherType' = ...
    HIGH_SNOW_ACCUMULATION: 'CommonWeatherType' = ...
    VAMPIRE_SAFE_CLOUD_LEVEL: 'CommonWeatherType' = ...
    CLEAR_SKIES: 'CommonWeatherType' = ...
    THUNDER_SNOW: 'CommonWeatherType' = ...
    SUNSNOW: 'CommonWeatherType' = ...
    DRY_LIGHTNING: 'CommonWeatherType' = ...
    WINDY_HOT: 'CommonWeatherType' = ...
    CLOUDY_WARM: 'CommonWeatherType' = ...
    STRANGE_WEATHER: 'CommonWeatherType' = ...
    SUNBATHING_WEATHER: 'CommonWeatherType' = ...
    ICY: 'CommonWeatherType' = ...
    FROZEN_WATER: 'CommonWeatherType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonWeatherType'] = None) -> Tuple['CommonWeatherType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, UNDEFINED will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonWeatherType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonWeatherType]
        """
        if exclude_values is None:
            exclude_values = (cls.UNDEFINED,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonWeatherType, ...] = tuple([value for value in cls.values if value not in exclude_values])
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
        mapping = dict()
        if hasattr(WeatherType, 'Freezing'):
            mapping[CommonWeatherType.FREEZING] = WeatherType.Freezing
        if hasattr(WeatherType, 'Cold'):
            mapping[CommonWeatherType.COLD] = WeatherType.Cold
        if hasattr(WeatherType, 'Cool'):
            mapping[CommonWeatherType.COOL] = WeatherType.Cool
        if hasattr(WeatherType, 'Warm'):
            mapping[CommonWeatherType.WARM] = WeatherType.Warm
        if hasattr(WeatherType, 'Hot'):
            mapping[CommonWeatherType.HOT] = WeatherType.Hot
        if hasattr(WeatherType, 'Burning'):
            mapping[CommonWeatherType.BURNING] = WeatherType.Burning
        if hasattr(WeatherType, 'UNDEFINED'):
            mapping[CommonWeatherType.UNDEFINED] = WeatherType.UNDEFINED
        if hasattr(WeatherType, 'AnySnow'):
            mapping[CommonWeatherType.ANY_SNOW] = WeatherType.AnySnow
        if hasattr(WeatherType, 'AnyRain'):
            mapping[CommonWeatherType.ANY_RAIN] = WeatherType.AnyRain
        if hasattr(WeatherType, 'Max_Snow_Accumulation'):
            mapping[CommonWeatherType.MAX_SNOW_ACCUMULATION] = WeatherType.Max_Snow_Accumulation
        if hasattr(WeatherType, 'Max_Rain_Accumulation'):
            mapping[CommonWeatherType.MAX_RAIN_ACCUMULATION] = WeatherType.Max_Rain_Accumulation
        if hasattr(WeatherType, 'AnyLightning'):
            mapping[CommonWeatherType.ANY_LIGHTNING] = WeatherType.AnyLightning
        if hasattr(WeatherType, 'StruckByLightning'):
            mapping[CommonWeatherType.STRUCK_BY_LIGHTNING] = WeatherType.StruckByLightning
        if hasattr(WeatherType, 'Rain_Light'):
            mapping[CommonWeatherType.RAIN_LIGHT] = WeatherType.Rain_Light
        if hasattr(WeatherType, 'Rain_Heavy'):
            mapping[CommonWeatherType.RAIN_HEAVY] = WeatherType.Rain_Heavy
        if hasattr(WeatherType, 'Rain_Storm'):
            mapping[CommonWeatherType.RAIN_STORM] = WeatherType.Rain_Storm
        if hasattr(WeatherType, 'Snow_Light'):
            mapping[CommonWeatherType.SNOW_LIGHT] = WeatherType.Snow_Light
        if hasattr(WeatherType, 'Snow_Heavy'):
            mapping[CommonWeatherType.SNOW_HEAVY] = WeatherType.Snow_Heavy
        if hasattr(WeatherType, 'Snow_Storm'):
            mapping[CommonWeatherType.SNOW_STORM] = WeatherType.Snow_Storm
        if hasattr(WeatherType, 'Cloudy_Partial'):
            mapping[CommonWeatherType.CLOUDY_PARTIAL] = WeatherType.Cloudy_Partial
        if hasattr(WeatherType, 'Cloudy_Full'):
            mapping[CommonWeatherType.CLOUDY_FULL] = WeatherType.Cloudy_Full
        if hasattr(WeatherType, 'Windy'):
            mapping[CommonWeatherType.WINDY] = WeatherType.Windy
        if hasattr(WeatherType, 'Sun_Shower'):
            mapping[CommonWeatherType.SUN_SHOWER] = WeatherType.Sun_Shower
        if hasattr(WeatherType, 'Sunny'):
            mapping[CommonWeatherType.SUNNY] = WeatherType.Sunny
        if hasattr(WeatherType, 'Heatwave'):
            mapping[CommonWeatherType.HEATWAVE] = WeatherType.Heatwave
        if hasattr(WeatherType, 'Thunder'):
            mapping[CommonWeatherType.THUNDER] = WeatherType.Thunder
        if hasattr(WeatherType, 'Min_Snow_Accumulation'):
            mapping[CommonWeatherType.MIN_SNOW_ACCUMULATION] = WeatherType.Min_Snow_Accumulation
        if hasattr(WeatherType, 'Med_Snow_Accumulation'):
            mapping[CommonWeatherType.MED_SNOW_ACCUMULATION] = WeatherType.Med_Snow_Accumulation
        if hasattr(WeatherType, 'High_Snow_Accumulation'):
            mapping[CommonWeatherType.HIGH_SNOW_ACCUMULATION] = WeatherType.High_Snow_Accumulation
        if hasattr(WeatherType, 'Vampire_Safe_CloudLevel'):
            mapping[CommonWeatherType.VAMPIRE_SAFE_CLOUD_LEVEL] = WeatherType.Vampire_Safe_CloudLevel
        if hasattr(WeatherType, 'Clear_Skies'):
            mapping[CommonWeatherType.CLEAR_SKIES] = WeatherType.Clear_Skies
        if hasattr(WeatherType, 'Thundersnow'):
            mapping[CommonWeatherType.THUNDER_SNOW] = WeatherType.Thundersnow
        if hasattr(WeatherType, 'Sunsnow'):
            mapping[CommonWeatherType.SUNSNOW] = WeatherType.Sunsnow
        if hasattr(WeatherType, 'Dry_Lightning'):
            mapping[CommonWeatherType.DRY_LIGHTNING] = WeatherType.Dry_Lightning
        if hasattr(WeatherType, 'Windy_Hot'):
            mapping[CommonWeatherType.WINDY_HOT] = WeatherType.Windy_Hot
        if hasattr(WeatherType, 'Cloudy_Warm'):
            mapping[CommonWeatherType.CLOUDY_WARM] = WeatherType.Cloudy_Warm
        if hasattr(WeatherType, 'StrangeWeather'):
            mapping[CommonWeatherType.STRANGE_WEATHER] = WeatherType.StrangeWeather
        if hasattr(WeatherType, 'Sunbathing_Weather'):
            mapping[CommonWeatherType.SUNBATHING_WEATHER] = WeatherType.Sunbathing_Weather
        if hasattr(WeatherType, 'Icy'):
            mapping[CommonWeatherType.ICY] = WeatherType.Icy
        if hasattr(WeatherType, 'Frozen_Water'):
            mapping[CommonWeatherType.FROZEN_WATER] = WeatherType.Frozen_Water
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: WeatherType) -> Union['CommonWeatherType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla WeatherType into CommonWeatherType.

        :param value: An instance of WeatherType
        :type value: WeatherType
        :return: The specified WeatherType translated to CommonWeatherType, or None if the value could not be translated.
        :rtype: Union[CommonWeatherType, None]
        """
        mapping = dict()
        if hasattr(WeatherType, 'Freezing'):
            mapping[WeatherType.Freezing] = CommonWeatherType.FREEZING
        if hasattr(WeatherType, 'Cold'):
            mapping[WeatherType.Cold] = CommonWeatherType.COLD
        if hasattr(WeatherType, 'Cool'):
            mapping[WeatherType.Cool] = CommonWeatherType.COOL
        if hasattr(WeatherType, 'Warm'):
            mapping[WeatherType.Warm] = CommonWeatherType.WARM
        if hasattr(WeatherType, 'Hot'):
            mapping[WeatherType.Hot] = CommonWeatherType.HOT
        if hasattr(WeatherType, 'Burning'):
            mapping[WeatherType.Burning] = CommonWeatherType.BURNING
        if hasattr(WeatherType, 'UNDEFINED'):
            mapping[WeatherType.UNDEFINED] = CommonWeatherType.UNDEFINED
        if hasattr(WeatherType, 'AnySnow'):
            mapping[WeatherType.AnySnow] = CommonWeatherType.ANY_SNOW
        if hasattr(WeatherType, 'AnyRain'):
            mapping[WeatherType.AnyRain] = CommonWeatherType.ANY_RAIN
        if hasattr(WeatherType, 'Max_Snow_Accumulation'):
            mapping[WeatherType.Max_Snow_Accumulation] = CommonWeatherType.MAX_SNOW_ACCUMULATION
        if hasattr(WeatherType, 'Max_Rain_Accumulation'):
            mapping[WeatherType.Max_Rain_Accumulation] = CommonWeatherType.MAX_RAIN_ACCUMULATION
        if hasattr(WeatherType, 'AnyLightning'):
            mapping[WeatherType.AnyLightning] = CommonWeatherType.ANY_LIGHTNING
        if hasattr(WeatherType, 'StruckByLightning'):
            mapping[WeatherType.StruckByLightning] = CommonWeatherType.STRUCK_BY_LIGHTNING
        if hasattr(WeatherType, 'Rain_Light'):
            mapping[WeatherType.Rain_Light] = CommonWeatherType.RAIN_LIGHT
        if hasattr(WeatherType, 'Rain_Heavy'):
            mapping[WeatherType.Rain_Heavy] = CommonWeatherType.RAIN_HEAVY
        if hasattr(WeatherType, 'Rain_Storm'):
            mapping[WeatherType.Rain_Storm] = CommonWeatherType.RAIN_STORM
        if hasattr(WeatherType, 'Snow_Light'):
            mapping[WeatherType.Snow_Light] = CommonWeatherType.SNOW_LIGHT
        if hasattr(WeatherType, 'Snow_Heavy'):
            mapping[WeatherType.Snow_Heavy] = CommonWeatherType.SNOW_HEAVY
        if hasattr(WeatherType, 'Snow_Storm'):
            mapping[WeatherType.Snow_Storm] = CommonWeatherType.SNOW_STORM
        if hasattr(WeatherType, 'Cloudy_Partial'):
            mapping[WeatherType.Cloudy_Partial] = CommonWeatherType.CLOUDY_PARTIAL
        if hasattr(WeatherType, 'Cloudy_Full'):
            mapping[WeatherType.Cloudy_Full] = CommonWeatherType.CLOUDY_FULL
        if hasattr(WeatherType, 'Windy'):
            mapping[WeatherType.Windy] = CommonWeatherType.WINDY
        if hasattr(WeatherType, 'Sun_Shower'):
            mapping[WeatherType.Sun_Shower] = CommonWeatherType.SUN_SHOWER
        if hasattr(WeatherType, 'Sunny'):
            mapping[WeatherType.Sunny] = CommonWeatherType.SUNNY
        if hasattr(WeatherType, 'Heatwave'):
            mapping[WeatherType.Heatwave] = CommonWeatherType.HEATWAVE
        if hasattr(WeatherType, 'Thunder'):
            mapping[WeatherType.Thunder] = CommonWeatherType.THUNDER
        if hasattr(WeatherType, 'Min_Snow_Accumulation'):
            mapping[WeatherType.Min_Snow_Accumulation] = CommonWeatherType.MIN_SNOW_ACCUMULATION
        if hasattr(WeatherType, 'Med_Snow_Accumulation'):
            mapping[WeatherType.Med_Snow_Accumulation] = CommonWeatherType.MED_SNOW_ACCUMULATION
        if hasattr(WeatherType, 'High_Snow_Accumulation'):
            mapping[WeatherType.High_Snow_Accumulation] = CommonWeatherType.HIGH_SNOW_ACCUMULATION
        if hasattr(WeatherType, 'Vampire_Safe_CloudLevel'):
            mapping[WeatherType.Vampire_Safe_CloudLevel] = CommonWeatherType.VAMPIRE_SAFE_CLOUD_LEVEL
        if hasattr(WeatherType, 'Clear_Skies'):
            mapping[WeatherType.Clear_Skies] = CommonWeatherType.CLEAR_SKIES
        if hasattr(WeatherType, 'Thundersnow'):
            mapping[WeatherType.Thundersnow] = CommonWeatherType.THUNDER_SNOW
        if hasattr(WeatherType, 'Sunsnow'):
            mapping[WeatherType.Sunsnow] = CommonWeatherType.SUNSNOW
        if hasattr(WeatherType, 'Dry_Lightning'):
            mapping[WeatherType.Dry_Lightning] = CommonWeatherType.DRY_LIGHTNING
        if hasattr(WeatherType, 'Windy_Hot'):
            mapping[WeatherType.Windy_Hot] = CommonWeatherType.WINDY_HOT
        if hasattr(WeatherType, 'Cloudy_Warm'):
            mapping[WeatherType.Cloudy_Warm] = CommonWeatherType.CLOUDY_WARM
        if hasattr(WeatherType, 'StrangeWeather'):
            mapping[WeatherType.StrangeWeather] = CommonWeatherType.STRANGE_WEATHER
        if hasattr(WeatherType, 'Sunbathing_Weather'):
            mapping[WeatherType.Sunbathing_Weather] = CommonWeatherType.SUNBATHING_WEATHER
        if hasattr(WeatherType, 'Icy'):
            mapping[WeatherType.Icy] = CommonWeatherType.ICY
        if hasattr(WeatherType, 'Frozen_Water'):
            mapping[WeatherType.Frozen_Water] = CommonWeatherType.FROZEN_WATER
        return mapping.get(value, None)
