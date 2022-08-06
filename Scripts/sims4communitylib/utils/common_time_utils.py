"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

import clock
import services
from clock import ClockSpeedMode, GameClock, ClockSpeedMultiplierType
from date_and_time import DateAndTime, TimeSpan
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from time_service import TimeService


class CommonTimeUtils:
    """Utilities for handling the in-game Time, also known as Sim Time.

    """
    @staticmethod
    def pause_the_game() -> bool:
        """pause_the_game()

        Pause the game.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.PAUSED)

    @staticmethod
    def game_is_paused() -> bool:
        """game_is_paused()

        Determine if the game is paused.

        :return: True, if the game is paused. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.game_is_running_at_speed(ClockSpeedMode.PAUSED)

    @staticmethod
    def game_is_running_at_speed(clock_speed: ClockSpeedMode) -> bool:
        """game_is_running_at_speed(clock_speed)

        Determine if the game is running at the specified speed.

        :param clock_speed: The speed to change the game time to.
        :type clock_speed: ClockSpeedMode
        :return: True, if the game is running at the specified speed. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.get_clock_speed() == clock_speed

    @staticmethod
    def set_game_speed_normal() -> bool:
        """set_game_speed_normal()

        Change the speed of the game clock to Normal speed.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.NORMAL)

    @staticmethod
    def set_game_speed_to_speed_two() -> bool:
        """set_game_speed_to_speed_two()

        Change the speed of the game clock to Speed Two.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SPEED2)

    @staticmethod
    def set_game_speed_to_speed_three() -> bool:
        """set_game_speed_to_speed_three()

        Change the speed of the game clock to Speed Three.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SPEED3)

    @staticmethod
    def set_game_speed_to_interaction_startup_speed() -> bool:
        """set_game_speed_to_interaction_startup_speed()

        Change the speed of the game clock to Interaction Startup Speed.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.INTERACTION_STARTUP_SPEED)

    @staticmethod
    def set_game_speed_to_super_speed_three() -> bool:
        """set_game_speed_to_super_speed_three()

        Change the speed of the game clock to Super Speed Three.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SUPER_SPEED3)

    @staticmethod
    def get_clock_speed() -> ClockSpeedMode:
        """get_clock_speed()

        Retrieve the current clock speed.

        :return: The current speed of the game clock.
        :rtype: ClockSpeedMode
        """
        return CommonTimeUtils.get_game_clock().clock_speed

    @staticmethod
    def get_clock_speed_scale() -> ClockSpeedMultiplierType:
        """get_clock_speed_scale()

        Retrieve the current clock speed multiplier.

        :return: The current speed multiplier of the game clock.
        :rtype: ClockSpeedMultiplierType
        """
        return CommonTimeUtils.get_game_clock().current_clock_speed_scale()

    @staticmethod
    def set_clock_speed(clock_speed: ClockSpeedMode) -> bool:
        """set_clock_speed(clock_speed)

        Set the clock speed.

        :param clock_speed: The speed to set the game clock to.
        :type clock_speed: ClockSpeedMode
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.get_game_clock().set_clock_speed(clock_speed)

    @staticmethod
    def set_current_time(hours: int, minutes: int, seconds: int):
        """set_current_time(hours, minutes, seconds)

        Set the current time.

        :param hours: The hour of the day to set the time to.
        :type hours: int
        :param minutes: The minute of the hour to set the time to.
        :type minutes: int
        :param seconds: The second of the minute to set the time to.
        :type seconds: int
        """
        CommonTimeUtils.get_game_clock().set_game_time(hours, minutes, seconds)

    @staticmethod
    def advance_current_time(hours: int = 0, minutes: int = 0, seconds: int = 0):
        """advance_current_time(hours=0, minutes=0, seconds=0)

        Advance the current time by the specified amounts.

        :param hours: The number of hours to advance.
        :type hours: int, optional
        :param minutes: The number of minutes to advance.
        :type minutes: int, optional
        :param seconds: The number of seconds to advance.
        :type seconds: int, optional
        """
        CommonTimeUtils.get_game_clock().advance_game_time(hours=hours, minutes=minutes, seconds=seconds)
    
    @staticmethod
    def get_current_date_and_time() -> DateAndTime:
        """get_current_date_and_time()

        Retrieve the current date and time.

        :return: The current date and time.
        :rtype: DateAndTime
        """
        return services.time_service().sim_now
    
    @staticmethod
    def get_current_second(date_and_time: DateAndTime = None) -> int:
        """get_current_second(date_and_time)

        Retrieve the current Sim second of the minute.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The current Sim second of the minute.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.second())
    
    @staticmethod
    def get_current_minute(date_and_time: DateAndTime = None) -> int:
        """get_current_minute(date_and_time)

        Retrieve the current Sim minute of the hour.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The current Sim minute of the hour.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.minute())
    
    @staticmethod
    def get_current_hour(date_and_time: DateAndTime = None) -> int:
        """get_current_hour(date_and_time)

        Retrieve the current Sim hour of the day in military time.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The current Sim hour of the day in military time.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.hour())

    @staticmethod
    def get_current_day(date_and_time: DateAndTime = None) -> int:
        """get_current_day(date_and_time)

        Retrieve the current Sim day of the month.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The current Sim day of the month.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.day())

    @staticmethod
    def get_current_week(date_and_time: DateAndTime = None) -> int:
        """get_current_week(date_and_time)

        Retrieve the current Sim week of the month.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The current Sim week of the month.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.week())
    
    @staticmethod
    def get_total_ticks(date_and_time: DateAndTime = None) -> int:
        """get_total_ticks(date_and_time)

        Retrieve the total Sim ticks since the start of the day.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The total number of Sim ticks in milliseconds since the start of the day.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.absolute_ticks())

    @staticmethod
    def get_total_seconds(date_and_time: DateAndTime = None) -> float:
        """get_total_seconds(date_and_time)

        Retrieve the total Sim seconds since the start of the day.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The total number of Sim seconds since the start of the day.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.absolute_seconds())

    @staticmethod
    def get_total_minutes(date_and_time: DateAndTime = None) -> float:
        """get_total_minutes(date_and_time)

        Retrieve the total Sim minutes since the start of the day.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The total number of Sim minutes since the start of the day.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.absolute_minutes())

    @staticmethod
    def get_total_hours(date_and_time: DateAndTime = None) -> float:
        """get_total_hours(date_and_time)

        Retrieve the total Sim hours since the start of the day in military time.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The total number of Sim hours since the start of the day in military time.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.absolute_hours())

    @staticmethod
    def get_total_days(date_and_time: DateAndTime = None) -> float:
        """get_total_days(date_and_time)

        Retrieve the total Sim days since the start of the season.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The total number of Sim days since the start of the season.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.absolute_days())

    @staticmethod
    def get_total_weeks(date_and_time: DateAndTime = None) -> float:
        """get_total_weeks(date_and_time)

        Retrieve the total Sim weeks since the start of the season.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The total number of Sim weeks since the start of the season.
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.absolute_weeks())

    @staticmethod
    def get_day_of_week(date_and_time: DateAndTime = None) -> int:
        """get_day_of_week(date_and_time)

        Retrieve the current day of the week.

        :param date_and_time: The date and time to retrieve the value from. If not specified, the current date and time will be used. Default is None.
        :type date_and_time: DateAndTime, optional
        :return: The current day of the week. 0-6
        :rtype: int
        """
        if date_and_time is None:
            date_and_time = CommonTimeUtils.get_current_date_and_time()
        return int(date_and_time.day())

    @staticmethod
    def create_interval_from_sim_seconds(seconds: int) -> TimeSpan:
        """create_interval_from_sim_seconds(seconds)

        Create a time span interval that spans from the current Sim time to a number of Sim seconds in the future.

        :param seconds: A number of Sim seconds in the future the time span will indicate.
        :type seconds: int
        :return: A time span that will occur a number of Sim seconds in the future.
        :rtype: TimeSpan
        """
        return clock.interval_in_sim_seconds(seconds)

    @staticmethod
    def create_interval_from_sim_minutes(minutes: int) -> TimeSpan:
        """create_interval_from_sim_minutes(minutes)

        Create a time span interval that spans from the current Sim time to a number of Sim minutes in the future.

        :param minutes: A number of Sim minutes in the future the time span will indicate.
        :type minutes: int
        :return: A time span that will occur a number of Sim minutes in the future.
        :rtype: TimeSpan
        """
        return clock.interval_in_sim_minutes(minutes)

    @staticmethod
    def create_interval_from_sim_hours(hours: int) -> TimeSpan:
        """create_interval_from_sim_hours(hours)

        Create a time span interval that spans from the current Sim time to a number of Sim hours in the future.

        :param hours: A number of Sim hours in the future the time span will indicate.
        :type hours: int
        :return: A time span that will occur a number of Sim hours in the future.
        :rtype: TimeSpan
        """
        return clock.interval_in_sim_hours(hours)

    @staticmethod
    def interval_in_sim_days(days: int) -> TimeSpan:
        """interval_in_sim_days(days)

        Create a time span interval that spans from the current Sim time to a number of Sim days in the future.

        :param days: A number of Sim days in the future the time span will indicate.
        :type days: int
        :return: A time span that will occur a number of Sim days in the future.
        :rtype: TimeSpan
        """
        return clock.interval_in_sim_days(days)

    @staticmethod
    def interval_in_sim_weeks(weeks: int) -> TimeSpan:
        """interval_in_sim_weeks(weeks)

        Create a time span interval that spans from the current Sim time to a number of Sim weeks in the future.

        :param weeks: A number of Sim weeks in the future the time span will indicate.
        :type weeks: int
        :return: A time span that will occur a number of Sim weeks in the future.
        :rtype: TimeSpan
        """
        return clock.interval_in_sim_weeks(weeks)

    @staticmethod
    def create_time_span(minutes: int = 0, hours: int = 0, days: int = 0) -> TimeSpan:
        """create_time_span(minutes=0, hours=0, days=0)

        Create a time span that spans from the current Sim time to a number of Sim minutes, hours, or days in the future.

        :param minutes: A number of Sim minutes in the future the time span will indicate. Default is 0 Sim minutes.
        :type minutes: int, optional
        :param hours: A number of Sim hours in the future the time span will indicate. Default is 0 Sim hours.
        :type hours: int, optional
        :param days: A number of Sim days in the future the time span will indicate. Default is 0 Sim days.
        :type days: int, optional
        :return: A time span that will occur a number of Sim minutes, hours, or days in the future.
        :rtype: TimeSpan
        """
        from date_and_time import create_time_span
        return create_time_span(days=days, hours=hours, minutes=minutes)

    @staticmethod
    def create_date_and_time(minutes: int = 0, hours: int = 0, days: int = 0) -> DateAndTime:
        """create_date_and_time(minutes=0, hours=0, days=0)

        Create a date and time that takes place a number of Sim minutes, hours, or days in the future.

        :param minutes: A number of Sim minutes in the future the date and time will be set at. Default is 0 Sim minutes.
        :type minutes: int, optional
        :param hours: A number of Sim hours in the future the date and time will be set at. Default is 0 Sim hours.
        :type hours: int, optional
        :param days: A number of Sim days in the future the date and time will be set at. Default is 0 Sim days.
        :type days: int, optional
        :return: A date and time that will occur a number of Sim minutes, hours, or days in the future.
        :rtype: DateAndTime
        """
        from date_and_time import create_date_and_time
        return create_date_and_time(days=days, hours=hours, minutes=minutes)

    @staticmethod
    def convert_milliseconds_to_seconds(milliseconds: float) -> float:
        """convert_milliseconds_to_seconds(milliseconds)

        Convert Milliseconds to Seconds.

        :param milliseconds: The value to convert.
        :type milliseconds: float
        :return: The converted value in seconds.
        :rtype: float
        """
        from date_and_time import MILLISECONDS_PER_SECOND
        if MILLISECONDS_PER_SECOND <= 0:
            return milliseconds/1000
        return milliseconds/MILLISECONDS_PER_SECOND

    @staticmethod
    def convert_seconds_to_milliseconds(seconds: float) -> float:
        """convert_seconds_to_milliseconds(milliseconds)

        Convert Seconds to Milliseconds.

        :param seconds: The value to convert.
        :type seconds: float
        :return: The converted value in milliseconds.
        :rtype: float
        """
        from date_and_time import MILLISECONDS_PER_SECOND
        if MILLISECONDS_PER_SECOND <= 0:
            return seconds * 1000
        return seconds * MILLISECONDS_PER_SECOND

    @staticmethod
    def is_sun_out() -> bool:
        """is_sun_out()

        Determine if the Sun is currently out.

        :return: True, if the sun is out. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.get_time_service().is_sun_out()

    @staticmethod
    def is_day_time(date_and_time: DateAndTime = None) -> bool:
        """is_day_time(date_and_time=None)

        Determine if it is currently Day Time.

        :param date_and_time: A date and time to check. If not specified, the current time will be used instead. Default is unspecified.
        :type date_and_time: DateAndTime, optional
        :return: True, if it is day time. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.get_time_service().is_day_time(time=date_and_time)

    @staticmethod
    def is_night_time(date_and_time: DateAndTime = None) -> bool:
        """is_night_time(date_and_time=None)

        Determine if it is currently Night Time.

        :param date_and_time: A date and time to check. If not specified, the current time will be used instead. Default is unspecified.
        :type date_and_time: DateAndTime, optional
        :return: True, if it is night time. False, if not.
        :rtype: bool
        """
        return not CommonTimeUtils.is_day_time(date_and_time=date_and_time)
    
    @staticmethod
    def get_time_service() -> TimeService:
        """get_time_service()

        Get an instance of the TimeService.

        :return: An instance of the Time Service.
        :rtype: TimeService
        """
        return services.time_service()
    
    @staticmethod
    def get_game_clock() -> GameClock:
        """get_game_clock()

        Get an instance of the GameClock.

        :return: An instance of the game clock.
        :rtype: GameClock
        """
        return services.game_clock_service()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.pause_game',
    'Pause the game.'
)
def _s4clib_pause_game(output: CommonConsoleCommandOutput):
    output('Attempting to pause the game.')
    CommonTimeUtils.pause_the_game()
    output('Game paused successfully.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.advance_time',
    'Advance the time in-game.',
    command_arguments=(
        CommonConsoleCommandArgument('seconds', 'Positive Number', 'The number of seconds to advance time by. Default is 0.', is_optional=True, default_value=0),
        CommonConsoleCommandArgument('minutes', 'Positive Number', 'The number of minutes to advance time by. Default is 0.', is_optional=True, default_value=0),
        CommonConsoleCommandArgument('hours', 'Positive Number', 'The number of hours to advance time by. Default is 0.', is_optional=True, default_value=0),
    )
)
def _s4clib_advance_time(
    output: CommonConsoleCommandOutput,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0
):
    output(f'Attempting to advance time by {hours}h {minutes}m {seconds}s')
    CommonTimeUtils.advance_current_time(hours=hours, minutes=minutes, seconds=seconds)
    output('Finished advancing time.')
