"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, List
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_update.events.zone_update_event import S4CLZoneUpdateEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService


class CommonIntervalDispatcher:
    """ Keeps track of the amount of time that has passed for listeners to trigger. """
    def __init__(self, mod_name: str, milliseconds: int, listening_func: Callable[..., Any], run_once: bool=False):
        self._mod_name = mod_name
        self._minimum_milliseconds_to_dispatch = milliseconds
        self._listening_func = listening_func
        self.total_milliseconds_passed = 0.0
        self._run_once = run_once

    @property
    def total_milliseconds_passed(self) -> float:
        """
            The total amount of milliseconds this dispatcher has known to have passed.
        """
        return self._total_milliseconds_passed

    @total_milliseconds_passed.setter
    def total_milliseconds_passed(self, milliseconds: float):
        self._total_milliseconds_passed = milliseconds

    @property
    def minimum_milliseconds_to_dispatch(self) -> int:
        """
            The minimum amount of milliseconds that must pass before this dispatcher will dispatch.
        """
        return self._minimum_milliseconds_to_dispatch

    @minimum_milliseconds_to_dispatch.setter
    def minimum_milliseconds_to_dispatch(self, val: int):
        """
            The minimum amount of milliseconds that must pass before this dispatcher will dispatch.
        """
        self._minimum_milliseconds_to_dispatch = val

    @property
    def mod_name(self) -> str:
        """ The name of the mod that is listening for events. """
        return self._mod_name

    @property
    def listening_func_name(self) -> str:
        """ The name of the function listening for events. """
        return self._listening_func.__name__

    @property
    def run_once(self) -> bool:
        """ Determine if this tracker only runs once. """
        return self._run_once

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def try_dispatch(self, milliseconds_since_last_update: int):
        """ Attempt to trigger the listener based on the amount of time passed. """
        self.total_milliseconds_passed += milliseconds_since_last_update
        if self.total_milliseconds_passed < self.minimum_milliseconds_to_dispatch:
            return False
        self.total_milliseconds_passed = max(0.0, self.total_milliseconds_passed - self.minimum_milliseconds_to_dispatch)
        self._listening_func()
        return True


class CommonIntervalEventRegistry(CommonService):
    """ Register functions to run in intervals. """

    def __init__(self):
        self._registered_interval_trackers: List[CommonIntervalDispatcher] = []

    def _add_tracker(self, mod_name: str, milliseconds: int, listening_func: Callable[..., Any], run_once: bool=False) -> CommonIntervalDispatcher:
        dispatcher = CommonIntervalDispatcher(mod_name, milliseconds, listening_func, run_once=run_once)
        self._registered_interval_trackers.append(dispatcher)
        return dispatcher

    @staticmethod
    def run_every(mod_name: str, milliseconds: int=1500) -> Callable[..., Any]:
        """
            Register a function to run in intervals of the specified time.

            Note: The function will run in intervals every time the amount of time has occurred.
        :param mod_name: The name of the mod registering this listener.
        :param milliseconds: The amount of time in milliseconds that needs to pass until this function will be run again.
        """
        def _wrapper(listening_func):
            CommonIntervalEventRegistry.get()._add_tracker(mod_name, milliseconds, listening_func)
            return listening_func
        return _wrapper

    @staticmethod
    def run_once(mod_name: str, milliseconds: int=1500) -> Callable[..., Any]:
        """
            Register a function to run once after the specified milliseconds.

            Note: The function will only run once.
        :param mod_name: The name of the mod registering this listener.
        :param milliseconds: The amount of time in milliseconds that needs to pass until this function is run.
        """

        def _wrapper(listening_func):
            CommonIntervalEventRegistry.get()._add_tracker(mod_name, milliseconds, listening_func, run_once=True)
            return listening_func
        return _wrapper

    def _attempt_to_dispatch(self, milliseconds_since_last_update: int):
        interval_trackers = list(self._registered_interval_trackers)
        for interval_tracker in interval_trackers:
            try:
                if interval_tracker.try_dispatch(milliseconds_since_last_update):
                    if interval_tracker.run_once:
                        self._registered_interval_trackers.remove(interval_tracker)
            except Exception as ex:
                CommonExceptionHandler.log_exception(interval_tracker.mod_name, 'Error occurred when attempting to dispatch listener \'{}\''.format(interval_tracker.listening_func_name), exception=ex)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def _update_game_tick_on_zone_update(event_data: S4CLZoneUpdateEvent):
        if event_data.is_paused:
            return
        CommonIntervalEventRegistry.get()._attempt_to_dispatch(event_data.ticks_since_last_update)
