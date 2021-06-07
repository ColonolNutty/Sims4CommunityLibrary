"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
import sims4.commands
from clock import ClockSpeedMode, GameClock, ClockSpeedMultiplierType
from date_and_time import DateAndTime
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from time_service import TimeService


class CommonTimeUtils:
    """Utilities for handling the in-game Time.

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

        Change the game time to Normal speed.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.NORMAL)

    @staticmethod
    def set_game_speed_to_speed_two() -> bool:
        """set_game_speed_to_speed_two()

        Change the game time to Speed Two.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SPEED2)

    @staticmethod
    def set_game_speed_to_speed_three() -> bool:
        """set_game_speed_to_speed_three()

        Change the game time to Speed Three.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SPEED3)

    @staticmethod
    def set_game_speed_to_interaction_startup_speed() -> bool:
        """set_game_speed_to_interaction_startup_speed()

        Change the game time to Interaction Startup Speed.

        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.INTERACTION_STARTUP_SPEED)

    @staticmethod
    def set_game_speed_to_super_speed_three() -> bool:
        """set_game_speed_to_super_speed_three()

        Change the game time to Super Speed Three.

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
    def advance_current_time(hours: int=0, minutes: int=0, seconds: int=0):
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
    def get_current_second(date_and_time: DateAndTime=None) -> int:
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
    def get_current_minute(date_and_time: DateAndTime=None) -> int:
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
    def get_current_hour(date_and_time: DateAndTime=None) -> int:
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
    def get_current_day(date_and_time: DateAndTime=None) -> int:
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
    def get_current_week(date_and_time: DateAndTime=None) -> int:
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
    def get_total_ticks(date_and_time: DateAndTime=None) -> int:
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
    def get_total_seconds(date_and_time: DateAndTime=None) -> float:
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
    def get_total_minutes(date_and_time: DateAndTime=None) -> float:
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
    def get_total_hours(date_and_time: DateAndTime=None) -> float:
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
    def get_total_days(date_and_time: DateAndTime=None) -> float:
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
    def get_total_weeks(date_and_time: DateAndTime=None) -> float:
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
    def get_day_of_week(date_and_time: DateAndTime=None) -> int:
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
    def is_sun_out() -> bool:
        """is_sun_out()

        Determine if the Sun is currently out.

        :return: True, if the sun is out. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.get_time_service().is_sun_out()

    @staticmethod
    def is_day_time() -> bool:
        """is_day_time()

        Determine if it is currently Day Time.

        :return: True, if it is day time. False, if not.
        :rtype: bool
        """
        return CommonTimeUtils.get_time_service().is_day_time()

    @staticmethod
    def is_night_time() -> bool:
        """is_night_time()

        Determine if it is currently Night Time.

        :return: True, if it is night time. False, if not.
        :rtype: bool
        """
        return not CommonTimeUtils.is_day_time()
    
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


@sims4.commands.Command('s4clib_testing.test_game_pause', command_type=sims4.commands.CommandType.Live)
def _s4clib_testing_test_game_pause(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Attempting to pause the game.')
    try:
        CommonTimeUtils.pause_the_game()
        output('Game paused successfully.')
    except Exception as ex:
        output('Failed to pause the game! See Exception log.')
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to pause the game!', exception=ex)
