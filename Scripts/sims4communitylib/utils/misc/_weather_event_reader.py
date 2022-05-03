"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.resources import Types
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
        'WEATHER_CLOUDY_COLD': 'CLOUDY_COLD',
        'WEATHER_CLOUDY_COOL': 'CLOUDY_COOL',
        'WEATHER_CLOUDY_DRYLIGHTNING': 'CLOUDY_LIGHTNING',
        'WEATHER_CLOUDY_FREEZING': 'CLOUDY_FREEZING',
        'WEATHER_CLOUDY_HOT': 'CLOUDY_HOT',
        'WEATHER_CLOUDY_WARM': 'CLOUDY_WARM',
        'WEATHER_DEBUG_FASTRAIN': 'FAST_RAIN',
        'WEATHER_HEATWAVE': 'HEATWAVE',
        'WEATHER_MAGICREALM': 'MAGIC_REALM',
        'WEATHER_PARTLYCLOUDY_COLD': 'PARTLY_CLOUDY_COLD',
        'WEATHER_PARTLYCLOUDY_COOL': 'PARTLY_CLOUDY_COOL',
        'WEATHER_PARTLYCLOUDY_FREEZING': 'PARTLY_CLOUDY_FREEZING',
        'WEATHER_PARTLYCLOUDY_HOT': 'PARTLY_CLOUDY_HOT',
        'WEATHER_PARTLYCLOUDY_WARM': 'PARTLY_CLOUDY_WARM',
        'WEATHER_SUNSNOW_COLD': 'PARTLY_CLOUDY_SNOW_COLD',
        'WEATHER_SUNSNOW_COOL': 'PARTLY_CLOUDY_SNOW_COOL',
        'WEATHER_PARTLYCLOUDY_WARM_DEFAULT': 'PARTLY_CLOUDY_WARM_DEFAULT',
        'WEATHER_RAIN_HEAVY_COLD': 'RAIN_HEAVY_COLD',
        'WEATHER_RAIN_HEAVY_COOL': 'RAIN_HEAVY_COOL',
        'WEATHER_RAIN_HEAVY_WARM': 'RAIN_HEAVY_WARM',
        'WEATHER_RAIN_LIGHT_COLD': 'RAIN_LIGHT_COLD',
        'WEATHER_RAIN_LIGHT_COOL': 'RAIN_LIGHT_COOL',
        'WEATHER_RAIN_LIGHT_WARM': 'RAIN_LIGHT_WARM',
        'WEATHER_RAIN_STORM_COLD': 'RAINSTORM_COLD',
        'WEATHER_RAIN_STORM_COOL': 'RAINSTORM_COOL',
        'WEATHER_RAIN_STORM_WARM': 'RAINSTORM_WARM',
        'WEATHER_RAIN_STORM_WARM_MONSOONEP07': 'RAINSTORM_WARM_MONSOON',
        'WEATHER_SNOW_HEAVY_FREEZING': 'SNOW_HEAVY_FREEZING',
        'WEATHER_SNOW_LIGHT_FREEZING': 'SNOW_LIGHT_FREEZING',
        'WEATHER_SNOW_STORM': 'SNOWSTORM',
        'WEATHER_SNOW_TEST': 'SNOW_TEST',
        'WEATHER_SNOW_THUNDERSNOW': 'SNOW_THUNDERSTORM',
        'WEATHER_SUNNY_BURNING': 'CLEAR_BURNING',
        'WEATHER_SUNNY_COLD': 'CLEAR_COLD',
        'WEATHER_SUNNY_COOL': 'CLEAR_COOL',
        'WEATHER_SUNNY_FREEZING': 'CLEAR_FREEZING',
        'WEATHER_SUNNY_HOT': 'CLEAR_HOT',
        'WEATHER_SUNNY_WARM': 'CLEAR',
        'WEATHER_SUNSHOWER_COOL': 'CLEAR_SHOWER_COOL',
        'WEATHER_SUNSHOWER_HOT': 'CLEAR_SHOWER_HOT',
        'WEATHER_SUNSHOWER_WARM': 'CLEAR_SHOWER_WARM',
        'WEATHER_WINDY_BURNING': 'CLEAR_WINDY_BURNING',
        'WEATHER_WINDY_COLD': 'CLEAR_WINDY_COLD',
        'WEATHER_WINDY_COOL': 'CLEAR_WINDY_COOL',
        'WEATHER_WINDY_FREEZING': 'CLEAR_WINDY_FREEZING',
        'WEATHER_WINDY_HOT': 'CLEAR_WINDY_HOT',
        'WEATHER_WINDY_WARM': 'CLEAR_WINDY_WARM',
    }


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_dev.log_weather_events', 'Logs a list of weather events and weather event ids for easy transfer to CommonWeatherEventId', show_with_help_command=False)
def _common_log_weather_events_ready_for_update(output: CommonConsoleCommandOutput) -> None:
    output('Logging Weather Events')
    from sims4communitylib.utils.misc._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
    from sims4communitylib.enums.common_weather_event_ids import CommonWeatherEventId
    not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_instances(Types.WEATHER_EVENT, _S4CLReaderForUpdate.CONVERSIONS, CommonWeatherEventId, skip_not_found=True)
    output(f'Finished logging Weather Events. {len(not_found_values)} values were not found.')
