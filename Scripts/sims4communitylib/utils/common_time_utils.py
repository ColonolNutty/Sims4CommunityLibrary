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
    def get_current_second() -> int:
        """get_current_second()

        Retrieve the current sim second.

        :return: The current second of the minute.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().second())
    
    @staticmethod
    def get_current_minute() -> int:
        """get_current_minute()

        Retrieve the current sim minute.

        :return: The current minute of the hour.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().minute())
    
    @staticmethod
    def get_current_hour() -> int:
        """get_current_hour()

        Retrieve the current sim hour.

        :return: The current hour of the day.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().hour())
    
    @staticmethod
    def get_total_ticks() -> int:
        """get_total_ticks()

        Retrieve the total sim ticks since the start of the game.

        :return: The total number of ticks in milliseconds since the start of the game.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_ticks())

    @staticmethod
    def get_total_hours() -> int:
        """get_total_hours()

        Retrieve the total sim hours since the start of the game.

        :return: The total number of hours since the start of the game.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_hours())

    @staticmethod
    def get_total_days() -> int:
        """get_total_days()

        Retrieve the total sim days since the start of the game.

        :return: The total number of days since the start of the game.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_days())

    @staticmethod
    def get_total_weeks() -> int:
        """get_total_weeks()

        Retrieve the total sim weeks since the start of the game.

        :return: The total number of weeks since the start of the game.
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_weeks())

    @staticmethod
    def get_day_of_week() -> int:
        """get_day_of_week()

        Retrieve the current day of the week.

        :return: The current day of the week. 0-6
        :rtype: int
        """
        return int(CommonTimeUtils.get_current_date_and_time().day())

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
