"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator

import services
from weather.weather_enums import Temperature, WeatherEffectType, CloudType


class CommonWeatherUtils:
    """ Utilities for manipulating the weather. """

    @staticmethod
    def weather_effect_is_active(weather_effect_type: WeatherEffectType) -> bool:
        """ Determine if the specified weather effect is currently active. """
        return CommonWeatherUtils.weather_effects_are_active((weather_effect_type,))

    @staticmethod
    def weather_effects_are_active(weather_effect_types: Iterator[WeatherEffectType]) -> bool:
        """ Determine if any of the specified weather effects are currently active. """
        if not hasattr(services, 'weather_service'):
            return False
        weather_service = services.weather_service()
        if weather_service is None:
            return False
        for weather_effect_type in weather_effect_types:
            if not bool(weather_service.get_weather_element_value(weather_effect_type, default=0.0)):
                continue
            return True
        return False

    @staticmethod
    def current_temperature_is_cold_or_freezing() -> bool:
        """ Determine if the current temperature is cold or freezing. """
        current_temperature = CommonWeatherUtils.get_current_temperature()
        return current_temperature == Temperature.COLD or current_temperature == Temperature.FREEZING

    @staticmethod
    def current_weather_contains_thunder_or_lightning() -> bool:
        """ Determine if the current weather contains lightning or thunder. """
        return CommonWeatherUtils.weather_effects_are_active((WeatherEffectType.LIGHTNING, WeatherEffectType.THUNDER))

    @staticmethod
    def get_current_temperature() -> Temperature:
        """ Retrieve the current temperature. """
        from weather.weather_enums import WeatherEffectType, Temperature
        weather_service = services.weather_service()
        if weather_service is not None:
            return Temperature(weather_service.get_weather_element_value(WeatherEffectType.TEMPERATURE, default=Temperature.WARM))
        return Temperature.WARM

    @staticmethod
    def get_weather_cloud_type() -> CloudType:
        """ Retrieve the current cloud type. """
        weather_service = services.weather_service()
        if weather_service is None:
            return CloudType.CLEAR
        for cloud_type in CloudType.values:
            if not weather_service.get_weather_element_value(cloud_type, default=0.0):
                continue
            return cloud_type
        return CloudType.CLEAR
