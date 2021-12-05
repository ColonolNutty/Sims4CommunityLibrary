"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, List, Union
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_update.events.zone_update_event import S4CLZoneUpdateEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService


class CommonIntervalDispatcher:
    """CommonIntervalDispatcher(mod_identifier, milliseconds, listening_func, run_once=False)

    A dispatcher that invokes a callback based on the amount of time passed.

    .. note:: The dispatcher will only keep track of the amount of time passed while the game was not paused.\
        It will never dispatch while the game is paused.

    :param mod_identifier: The name or identity of the mod the dispatcher belongs to.
    :type mod_identifier: Union[str, CommonModIdentity]
    :param milliseconds: The number of milliseconds that need to pass before `listening_func` will be invoked.
    :type milliseconds: int
    :param listening_func: A callback invoked after an amount of time has passed.
    :type listening_func: Callable[..., Any]
    :param run_once: If set to True, the dispatcher will only invoke `listening_func` once before it stops listening.\
    If set to False, the dispatcher will invoke `listening_func` every time the specified number of milliseconds has passed.
    :type run_once: bool
    """
    def __init__(self, mod_identifier: Union[str, CommonModIdentity], milliseconds: int, listening_func: Callable[..., Any], run_once: bool=False):
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        self._mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier)
        self._minimum_milliseconds_to_dispatch = milliseconds
        self._listening_func = listening_func
        self.total_milliseconds_passed = 0.0
        self._run_once = run_once

    @property
    def total_milliseconds_passed(self) -> float:
        """The amount of time in milliseconds that has passed since the dispatcher started keeping track.

        :return: The amount of time in milliseconds that has passed since the dispatcher started keeping track.
        :rtype: float
        """
        return self._total_milliseconds_passed

    @total_milliseconds_passed.setter
    def total_milliseconds_passed(self, milliseconds: float):
        self._total_milliseconds_passed = milliseconds

    @property
    def minimum_milliseconds_to_dispatch(self) -> int:
        """The minimum amount of time in milliseconds that must pass before `listening_func` will be run.

        :return: The minimum amount of time in milliseconds that must pass before `listening_func` will be run.
        :rtype: int
        """
        return self._minimum_milliseconds_to_dispatch

    @minimum_milliseconds_to_dispatch.setter
    def minimum_milliseconds_to_dispatch(self, val: int):
        self._minimum_milliseconds_to_dispatch = val

    @property
    def mod_name(self) -> str:
        """The name of the mod the dispatcher belongs to.

        :return: The name of the mod the dispatcher belongs to.
        :rtype: str
        """
        return self._mod_name

    @property
    def listening_func_name(self) -> str:
        """The name of the function waiting for invocation.

        :return: The name of the function waiting for invocation.
        :rtype: str
        """
        return self._listening_func.__name__

    @property
    def run_once(self) -> bool:
        """Determine if the dispatch will run only once.

        :return: True, if the dispatcher will only run once. False, if the dispatcher runs more than once.
        :rtype: bool
        """
        return self._run_once

    def try_dispatch(self, milliseconds_since_last_update: int) -> bool:
        """Attempt to run the dispatcher.

        :param milliseconds_since_last_update: The amount of time in milliseconds that has passed since the last update.
        :type milliseconds_since_last_update: int
        :return: True, if the event was run. False, if the event was not run or not enough time has passed.
        :rtype: bool
        """
        self.total_milliseconds_passed += milliseconds_since_last_update
        if self.total_milliseconds_passed < self.minimum_milliseconds_to_dispatch:
            return False
        self.total_milliseconds_passed = max(0.0, self.total_milliseconds_passed - self.minimum_milliseconds_to_dispatch)
        self._listening_func()
        return True


class CommonIntervalEventRegistry(CommonService):
    """A registry that will run functions based on an amount of time.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        # This is an example showing how you may register your functions to run on intervals.
        class ExampleIntervalListener:
            # This function will run only once, after 200 milliseconds have passed. It will then stop listening.
            @staticmethod
            @CommonIntervalEventRegistry.run_once(ModInfo.get_identity().name, milliseconds=200)
            def _example_run_once():
                pass

            # This function will run every 500 milliseconds. It will continue listening until the game is closed or until it is manually unregistered.
            @staticmethod
            @CommonIntervalEventRegistry.run_every(ModInfo.get_identity().name, milliseconds=500)
            def _example_run_every():
                pass

    """

    def __init__(self) -> None:
        self._registered_interval_trackers: List[CommonIntervalDispatcher] = []

    @staticmethod
    def run_every(mod_identifier: Union[str, CommonModIdentity], milliseconds: int=1500) -> Callable[..., Callable[..., Any]]:
        """run_every(mod_identifier, milliseconds=1500)

        Register a function to run in intervals of the specified time.

        .. note:: The function will run in intervals every time the amount of time has occurred.

        :param mod_identifier: The name or identity of the mod registering the listener.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param milliseconds: The amount of time in milliseconds that must pass before the decorated function will be run.
        :type milliseconds: int
        :return: A callable function wrapped that runs in intervals.
        :rtype: Callable[..., Callable[..., Any]]
        """
        def _wrapper(listening_func) -> Callable[..., Any]:
            CommonIntervalEventRegistry.get()._add_tracker(mod_identifier, milliseconds, listening_func)
            return listening_func
        return _wrapper

    @staticmethod
    def run_once(mod_identifier: Union[str, CommonModIdentity], milliseconds: int=1500) -> Callable[..., Callable[..., Any]]:
        """run_once(mod_identifier, milliseconds=1500)

        Register a function to run a single time after a certain amount of time.

        .. note:: A function decorated with this decorator will only run once.

        :param mod_identifier: The name or identity of the mod registering the listener.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param milliseconds: The amount of time in milliseconds that must pass before the decorated function will be run.
        :type milliseconds: int
        :return: A callable function wrapped to run once.
        :rtype: Callable[..., Callable[..., Any]]
        """

        def _wrapper(listening_func) -> Any:
            CommonIntervalEventRegistry.get()._add_tracker(mod_identifier, milliseconds, listening_func, run_once=True)
            return listening_func
        return _wrapper

    def register_dispatcher(self, mod_identity: CommonModIdentity, milliseconds: int, listening_func: Callable[..., Any], run_once: bool=False) -> Union[CommonIntervalDispatcher, None]:
        """register_dispatcher(mod_identity, milliseconds, listening_func, run_once=False)

        Manually register a new dispatcher to the registry.

        :param mod_identity: The identity of the mod that owns the interval dispatcher.
        :type mod_identity: CommonModIdentity
        :param milliseconds: How much time before the dispatcher runs the first time as well as how much time before it runs again.
        :type milliseconds: int
        :param listening_func: The function to invoke after the set amount of time.
        :type listening_func: Callable[..., Any]
        :param run_once: If True, the dispatcher will run a single time, then be removed from the registry. If False, the dispatcher will continue running after the specified milliseconds and will repeat. Default is False.
        :type run_once: bool, optional
        :return: A dispatcher that will trigger after a set amount of time or None if an error occurs while registering a dispatcher.
        :rtype: Union[CommonIntervalDispatcher, None]
        """
        if milliseconds <= 0:
            CommonExceptionHandler.log_exception(mod_identity, 'Failed to registry an interval dispatcher. The specified milliseconds must be above zero.')
            return None
        return self._add_tracker(mod_identity, milliseconds, listening_func, run_once=run_once)

    def _add_tracker(self, mod_identifier: Union[str, CommonModIdentity], milliseconds: int, listening_func: Callable[..., Any], run_once: bool=False) -> CommonIntervalDispatcher:
        dispatcher = CommonIntervalDispatcher(mod_identifier, milliseconds, listening_func, run_once=run_once)
        self._registered_interval_trackers.append(dispatcher)
        return dispatcher

    def _attempt_to_dispatch(self, milliseconds_since_last_update: int):
        interval_trackers = list(self._registered_interval_trackers)
        for interval_tracker in interval_trackers:
            try:
                interval_tracker.try_dispatch(milliseconds_since_last_update)
            except Exception as ex:
                CommonExceptionHandler.log_exception(interval_tracker.mod_name, 'Error occurred when attempting to dispatch listener \'{}\''.format(interval_tracker.listening_func_name), exception=ex)
            try:
                if interval_tracker.run_once:
                    self._registered_interval_trackers.remove(interval_tracker)
            except Exception as ex:
                CommonExceptionHandler.log_exception(interval_tracker.mod_name, 'Error occurred when attempting to unregister listener \'{}\''.format(interval_tracker.listening_func_name), exception=ex)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _update_game_tick_on_zone_update(event_data: S4CLZoneUpdateEvent) -> bool:
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if event_data.is_paused or CommonZoneSpinEventDispatcher().game_loading:
            return False
        CommonIntervalEventRegistry.get()._attempt_to_dispatch(event_data.ticks_since_last_update)
        return True


# noinspection PyMissingOrEmptyDocstring
class ExampleIntervalListener:
    # This function will run once after 200 milliseconds have passed. Then it stops listening.
    @staticmethod
    # @CommonIntervalEventRegistry.run_once(ModInfo.get_identity().name, milliseconds=200)
    def _example_run_once() -> None:
        pass

    # This function will run every 500 milliseconds. It will continue listening until the game is closed or until it is manually unregistered.
    @staticmethod
    # @CommonIntervalEventRegistry.run_every(ModInfo.get_identity().name, milliseconds=500)
    def _example_run_every() -> None:
        pass
