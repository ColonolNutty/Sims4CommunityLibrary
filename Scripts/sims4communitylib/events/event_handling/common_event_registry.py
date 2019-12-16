"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Callable, Any
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.events.event_handling.common_event_handler import CommonEventHandler
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService


class CommonEventRegistry(CommonService):
    """ Register event handlers and dispatch events. """

    def __init__(self):
        self._event_handlers: List[CommonEventHandler] = []

    @staticmethod
    def handle_events(mod_name: str):
        """
            Decorate functions with this static method to register that function to handle an event.

            Note: Event functions MUST be decorated with staticmethod and must only have a single argument with the name 'event_data' (Errors will be thrown upon loading the game otherwise)
        :param mod_name: The name of the mod the class is being registered for.
        """
        def _wrapper(event_function):
            CommonEventRegistry.get()._register_event_handler(mod_name, event_function)
            return event_function
        return _wrapper

    def _register_event_handler(self, mod_name: str, event_function: Callable[..., Any]):
        event_handler = CommonEventHandler(mod_name, event_function)
        self._event_handlers.append(event_handler)

    def dispatch(self, event: CommonEvent) -> bool:
        """ Dispatch an event to any event handlers listening for it. """
        event_handlers = list(self._event_handlers)
        try:
            for event_handler in event_handlers:
                if not event_handler.can_handle_event(event):
                    continue
                try:
                    event_handler.handle_event(event)
                except Exception as ex:
                    CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred when attempting to handle event type \'{}\' via event handler \'{}\''.format(type(event), str(event_handler)), exception=ex)
                    continue
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Failed to dispatch event \'{}\''.format(event), exception=ex)
            return False
        return True
