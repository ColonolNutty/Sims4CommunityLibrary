"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator

import services
from weather.weather_enums import Temperature, WeatherEffectType, CloudType
from weather.weather_service import WeatherService


class CommonWeatherUtils:
    """Utilities for manipulating the weather.

    """

    @staticmethod
    def weather_effect_is_active(weather_effect_type: WeatherEffectType) -> bool:
        """weather_effect_is_active(weather_effect_type)

        Determine if the specified weather effect is currently active.

        :param weather_effect_type: The weather effect to check for.
        :type weather_effect_type: WeatherEffectType
        :return: True, if the weather is active. False, if it is not.
        :rtype: bool
        """
        return CommonWeatherUtils.weather_effects_are_active((weather_effect_type,))

    @staticmethod
    def weather_effects_are_active(weather_effect_types: Iterator[WeatherEffectType]) -> bool:
        """weather_effects_are_active(weather_effect_types)

        Determine if any of the specified weather effects are currently active.

        :param weather_effect_types: An iterable of weather effects to check for.
        :type weather_effect_types: Iterator[WeatherEffectType]
        :return: True, if any of the weathers is active. False, if none of the weathers are active.
        :rtype: bool
        """
        if not hasattr(services, 'weather_service'):
            return False
        weather_service: WeatherService = services.weather_service()
        if weather_service is None:
            return False
        for weather_effect_type in weather_effect_types:
            if not bool(weather_service.get_weather_element_value(weather_effect_type, default=0.0)):
                continue
            return True
        return False

    @staticmethod
    def current_temperature_is_cold_or_freezing() -> bool:
        """current_temperature_is_cold_or_freezing()

        Determine if the current temperature is cold or freezing.

        :return: True, if the current temperature contains cold or freezing. False, if not.
        :rtype: bool
        """
        current_temperature = CommonWeatherUtils.get_current_temperature()
        return current_temperature == Temperature.COLD or current_temperature == Temperature.FREEZING

    @staticmethod
    def current_weather_contains_thunder_or_lightning() -> bool:
        """current_weather_contains_thunder_or_lightning()

        Determine if the current weather contains lightning or thunder.

        :return: True, if the current weather contains thunder or lightning. False, if not.
        :rtype: bool
        """
        return CommonWeatherUtils.weather_effects_are_active((WeatherEffectType.LIGHTNING, WeatherEffectType.THUNDER))

    @staticmethod
    def get_current_temperature() -> Temperature:
        """get_current_temperature()

        Retrieve the current temperature.

        :return: The current temperature.
        :rtype: Temperature
        """
        from weather.weather_enums import WeatherEffectType, Temperature
        weather_service = services.weather_service()
        if weather_service is not None:
            return Temperature(weather_service.get_weather_element_value(WeatherEffectType.TEMPERATURE, default=Temperature.WARM))
        return Temperature.WARM

    @staticmethod
    def get_weather_cloud_type() -> CloudType:
        """get_weather_cloud_type()

        Retrieve the current cloud type.

        :return: The current cloud type.
        :rtype: CloudType
        """
        weather_service = services.weather_service()
        if weather_service is None:
            return CloudType.CLEAR
        for cloud_type in CloudType.values:
            if not weather_service.get_weather_element_value(cloud_type, default=0.0):
                continue
            return cloud_type
        return CloudType.CLEAR
