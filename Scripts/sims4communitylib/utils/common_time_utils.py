"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

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
    """ Utilities for handling the game clock. """
    @staticmethod
    def pause_the_game() -> bool:
        """
            Pause the game.
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.PAUSED)

    @staticmethod
    def game_is_paused() -> bool:
        """
            Determine if the game is paused.
        """
        return CommonTimeUtils.game_is_running_at_speed(ClockSpeedMode.PAUSED)

    @staticmethod
    def game_is_running_at_speed(clock_speed: ClockSpeedMode) -> bool:
        """
            Determine if the game is running at the specified speed.
        """
        return CommonTimeUtils.get_clock_speed() == clock_speed

    @staticmethod
    def set_game_speed_normal() -> bool:
        """
            Change the game time to Normal speed.
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.NORMAL)

    @staticmethod
    def set_game_speed_to_speed_two() -> bool:
        """
            Change the game time to Speed Two.
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SPEED2)

    @staticmethod
    def set_game_speed_to_speed_three() -> bool:
        """
            Change the game time to Speed Three.
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SPEED3)

    @staticmethod
    def set_game_speed_to_interaction_startup_speed() -> bool:
        """
            Change the game time to Interaction Startup Speed.
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.INTERACTION_STARTUP_SPEED)

    @staticmethod
    def set_game_speed_to_super_speed_three() -> bool:
        """
            Change the game time to Super Speed Three.
        """
        return CommonTimeUtils.set_clock_speed(ClockSpeedMode.SUPER_SPEED3)

    @staticmethod
    def get_clock_speed() -> ClockSpeedMode:
        """
            Retrieve the current clock speed.
        """
        return CommonTimeUtils.get_game_clock().clock_speed

    @staticmethod
    def get_clock_speed_scale() -> ClockSpeedMultiplierType:
        """
            Retrieve the current clock speed multiplier.
        """
        return CommonTimeUtils.get_game_clock().current_clock_speed_scale()

    @staticmethod
    def set_clock_speed(clock_speed: ClockSpeedMode) -> bool:
        """
            Set the clock speed.
        """
        return CommonTimeUtils.get_game_clock().set_clock_speed(clock_speed)

    @staticmethod
    def set_current_time(hours: int, minutes: int, seconds: int):
        """
            Set the current time.
        """
        CommonTimeUtils.get_game_clock().set_game_time(hours, minutes, seconds)

    @staticmethod
    def advance_current_time(hours: int=0, minutes: int=0, seconds: int=0):
        """
            Advance the current time by the specified amounts.
        """
        CommonTimeUtils.get_game_clock().advance_game_time(hours=hours, minutes=minutes, seconds=seconds)
    
    @staticmethod
    def get_current_date_and_time() -> DateAndTime:
        """
            Retrieve the current date and time.
        """
        return services.time_service().sim_now
    
    @staticmethod
    def get_current_second() -> int:
        """
            Retrieve the current sim second.
        """
        return int(CommonTimeUtils.get_current_date_and_time().second())
    
    @staticmethod
    def get_current_minute() -> int:
        """
            Retrieve the current sim minute.
        """
        return int(CommonTimeUtils.get_current_date_and_time().minute())
    
    @staticmethod
    def get_current_hour() -> int:
        """
            Retrieve the current sim hour.
        """
        return int(CommonTimeUtils.get_current_date_and_time().hour())
    
    @staticmethod
    def get_total_ticks() -> int:
        """
            Retrieve the total sim ticks since the start of the game.
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_ticks())

    @staticmethod
    def get_total_hours() -> int:
        """
            Retrieve the total sim hours since the start of the game.
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_hours())

    @staticmethod
    def get_total_days() -> int:
        """
            Retrieve the total sim days since the start of the game.
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_days())

    @staticmethod
    def get_total_weeks() -> int:
        """
            Retrieve the total sim weeks since the start of the game.
        """
        return int(CommonTimeUtils.get_current_date_and_time().absolute_weeks())

    @staticmethod
    def get_day_of_week() -> int:
        """
            Retrieve the current day of the week.
        """
        return int(CommonTimeUtils.get_current_date_and_time().day())

    @staticmethod
    def is_sun_out() -> bool:
        """
            Determine if the Sun is currently out.
        """
        return CommonTimeUtils.get_time_service().is_sun_out()

    @staticmethod
    def is_day_time() -> bool:
        """
            Determine if it is currently Day Time.
        """
        return CommonTimeUtils.get_time_service().is_day_time()

    @staticmethod
    def is_night_time() -> bool:
        """
            Determine if it is currently Night Time.
        """
        return not CommonTimeUtils.is_day_time()
    
    @staticmethod
    def get_time_service() -> TimeService:
        """
            Get an instance of the TimeService.
        """
        return services.time_service()
    
    @staticmethod
    def get_game_clock() -> GameClock:
        """
            Get an instance of the GameClock.
        """
        return services.game_clock_service()


@sims4.commands.Command('s4clib_testing.test_game_pause', command_type=sims4.commands.CommandType.Live)
def _s4clib_testing_test_game_pause(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Attempting to pause the game.')
    try:
        CommonTimeUtils.pause_the_game()
        output('Game paused successfully.')
    except Exception as ex:
        output('Failed to pause the game! See Exception log.')
        CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'Failed to pause the game!', exception=ex)
