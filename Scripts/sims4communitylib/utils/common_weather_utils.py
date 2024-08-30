"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union

from objects.game_object import GameObject
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.common_cloud_type import CommonCloudType
from sims4communitylib.enums.common_temperature import CommonTemperature
from sims4communitylib.enums.common_weather_effect_type import CommonWeatherEffectType
from sims4communitylib.enums.common_weather_event_ids import CommonWeatherEventId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from weather.weather_enums import PrecipitationType, WeatherEffectType
from weather.weather_event import WeatherEvent
from weather.weather_service import WeatherService


class CommonWeatherUtils:
    """Utilities for manipulating the weather.

    """

    @classmethod
    def weather_effect_is_active(cls, weather_effect_type: CommonWeatherEffectType) -> bool:
        """weather_effect_is_active(weather_effect_type)

        Determine if the specified weather effect is currently active.

        :param weather_effect_type: The weather effect to check for.
        :type weather_effect_type: CommonWeatherEffectType
        :return: True, if the weather is active. False, if it is not.
        :rtype: bool
        """
        return cls.weather_effects_are_active((weather_effect_type,))

    @classmethod
    def weather_effects_are_active(cls, weather_effect_types: Iterator[CommonWeatherEffectType]) -> bool:
        """weather_effects_are_active(weather_effect_types)

        Determine if any of the specified weather effects are currently active.

        :param weather_effect_types: An iterator of weather effects to check for.
        :type weather_effect_types: Iterator[CommonWeatherEffectType]
        :return: True, if any of the weathers is active. False, if none of the weathers are active.
        :rtype: bool
        """
        weather_service: WeatherService = cls.get_weather_service()
        if weather_service is None:
            return False
        for weather_effect_type in weather_effect_types:
            if not bool(weather_service.get_weather_element_value(weather_effect_type, default=0.0)):
                continue
            return True
        return False

    @classmethod
    def current_temperature_is_cold_or_freezing(cls) -> bool:
        """current_temperature_is_cold_or_freezing()

        Determine if the current temperature is cold or freezing.

        :return: True, if the current temperature contains cold or freezing. False, if not.
        :rtype: bool
        """
        current_temperature = cls.get_current_temperature()
        return current_temperature == CommonTemperature.COLD or current_temperature == CommonTemperature.FREEZING

    @classmethod
    def current_weather_contains_thunder_or_lightning(cls) -> bool:
        """current_weather_contains_thunder_or_lightning()

        Determine if the current weather contains lightning or thunder.

        :return: True, if the current weather contains thunder or lightning. False, if not.
        :rtype: bool
        """
        return cls.weather_effects_are_active((CommonWeatherEffectType.LIGHTNING, CommonWeatherEffectType.THUNDER))

    @classmethod
    def get_current_temperature(cls) -> CommonTemperature:
        """get_current_temperature()

        Retrieve the current temperature.

        :return: The current temperature.
        :rtype: CommonTemperature
        """
        weather_service = cls.get_weather_service()
        if weather_service is not None:
            return CommonTemperature.convert_from_vanilla(weather_service.get_weather_element_value(CommonWeatherEffectType.TEMPERATURE, default=CommonTemperature.WARM))
        return CommonTemperature.WARM

    @classmethod
    def get_current_wind_speed(cls) -> int:
        """get_current_wind_speed()

        Retrieve the current wind speed.

        :return: The current speed of the wind.
        :rtype: int
        """
        weather_service = cls.get_weather_service()
        if weather_service is None:
            return 0
        return weather_service.get_weather_element_value(WeatherEffectType.WIND, time=CommonTimeUtils.get_current_date_and_time())

    @classmethod
    def get_current_precipitation_level(cls, precipitation_type: PrecipitationType) -> int:
        """get_current_precipitation_level(precipitation_type)

        Retrieve the current precipitation level.

        :param precipitation_type: The type of precipitation to get.
        :type precipitation_type: PrecipitationType
        :return: The current precipitation level.
        :rtype: int
        """
        weather_service = cls.get_weather_service()
        if weather_service is None:
            return 0
        return weather_service.get_weather_element_value(precipitation_type, time=CommonTimeUtils.get_current_date_and_time())

    @classmethod
    def get_current_lightning_level(cls) -> int:
        """get_current_lightning_level()

        Retrieve the current lightning level.

        :return: The current lightning level.
        :rtype: int
        """
        weather_service = cls.get_weather_service()
        if weather_service is None:
            return 0
        return weather_service.get_weather_element_value(WeatherEffectType.LIGHTNING, time=CommonTimeUtils.get_current_date_and_time())

    @classmethod
    def get_weather_cloud_type(cls) -> CommonCloudType:
        """get_weather_cloud_type()

        Retrieve the current cloud type.

        :return: The current cloud type or CLEAR if weather is not available.
        :rtype: CommonCloudType
        """
        weather_service = cls.get_weather_service()
        if weather_service is None:
            return CommonCloudType.CLEAR
        for cloud_type in CommonCloudType.get_all():
            vanilla_cloud_type = CommonCloudType.convert_to_vanilla(cloud_type)
            if not weather_service.get_weather_element_value(vanilla_cloud_type, default=0.0):
                continue
            return cloud_type
        return CommonCloudType.CLEAR

    @classmethod
    def start_weather_event(cls, weather_event: Union[int, CommonWeatherEventId, WeatherEvent], duration_in_hours: int) -> None:
        """start_weather_event(weather_event, duration_in_hours)

        Start a weather event. Essentially changing the current weather.

        :param weather_event: The identifier of the weather event to start.
        :type weather_event: Union[int, CommonWeatherEventId, WeatherEvent]
        :param duration_in_hours: The number of Sim hours to run the weather event for.
        :type duration_in_hours: int
        """
        weather_service = cls.get_weather_service()
        if weather_service is None:
            return
        weather_event = cls.load_weather_event_by_id(weather_event)
        weather_service.start_weather_event(weather_event, duration_in_hours)

    @classmethod
    def get_weather_service(cls) -> Union[WeatherService, None]:
        """get_weather_service()
        
        Retrieve the service that handles the weather.
        
        :return: An instance of the service for handling weather or None if there is no weather service.
        :rtype: Union[WeatherService, None]
        """
        import services
        if not hasattr(services, 'weather_service'):
            return None
        return services.weather_service()

    @classmethod
    def load_weather_event_by_id(cls, weather_event: Union[int, CommonWeatherEventId, WeatherEvent]) -> Union[WeatherEvent, None]:
        """load_weather_event_by_id(weather_event)

        Load an instance of a Weather Event by its identifier.

        :param weather_event: The identifier of a Weather Event.
        :type weather_event: Union[int, CommonWeatherEventId, WeatherEvent]
        :return: An instance of a WeatherEvent matching the decimal identifier or None if not found.
        :rtype: Union[WeatherEvent, None]
        """
        if isinstance(weather_event, WeatherEvent):
            return weather_event
        # noinspection PyBroadException
        try:
            weather_event: int = int(weather_event)
        except:
            # noinspection PyTypeChecker
            weather_event: WeatherEvent = weather_event
            return weather_event

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.WEATHER_EVENT, weather_event)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.clear_weather',
    'Change the weather to clear, with sunny skies!',
    command_arguments=(
        CommonConsoleCommandArgument('duration_in_hours', 'Number', 'The number of Sim hours the weather should last.', is_optional=True, default_value='6 Hours'),
    )
)
def _common_set_weather(output: CommonConsoleCommandOutput, duration_in_hours: int=6):
    output(f'Changing the weather to clear')
    CommonWeatherUtils.start_weather_event(CommonWeatherEventId.CLEAR, duration_in_hours)
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.change_weather',
    'Set the weather',
    command_arguments=(
        CommonConsoleCommandArgument('weather', 'Weather Id or Tuning Name', 'The decimal identifier or Tuning Name of the Weather to add.'),
        CommonConsoleCommandArgument('duration_in_hours', 'Number', 'The number of Sim hours the weather should last.', is_optional=True, default_value='6 Hours'),
    )
)
def _common_set_weather(output: CommonConsoleCommandOutput, weather: TunableInstanceParam(Types.WEATHER_EVENT), duration_in_hours: int=6):
    if not weather or isinstance(weather, int) or isinstance(weather, float) or isinstance(weather, str):
        output(f'Weather \'{weather}\' was not found.')
        return False
    output(f'Changing the weather to {weather}')
    CommonWeatherUtils.start_weather_event(weather, duration_in_hours)
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.smite_sim',
    'A Sim will be struck by the power of Zeus.',
    command_aliases=(
      's4clib.smite_me',
    ),
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to smite.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_smite_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    sim = CommonSimUtils.get_sim_instance(sim_info)
    if sim is None:
        output(f'Sim was not found nearby. {sim_info}')
        return
    output(f'Smiting Sim {sim_info} with the power of Zeus.')
    from weather.lightning import LightningStrike
    LightningStrike.strike_sim(sim_to_strike=sim)
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.smite_object',
    'An object will be struck by the power of Zeus.',
    command_aliases=(
      's4clib.smite_it',
    ),
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Object Id or Name', 'The instance id or name of an Object to smite.'),
    )
)
def _common_smite_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    output(f'Smiting Object {game_object} with the power of Zeus.')
    from weather.lightning import LightningStrike
    LightningStrike.strike_object(obj_to_strike=game_object)
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.angry_zeus',
    'Zeus be Angry.'
)
def _common_smite_object(output: CommonConsoleCommandOutput, zeus_fury_count: int=100):
    output(f'Zeus be angry, I hope your Sims are indoors!')
    from weather.lightning import LightningStrike
    count = 0
    while count <= zeus_fury_count:
        LightningStrike.perform_active_lightning_strike()
        count += 1
    return True
