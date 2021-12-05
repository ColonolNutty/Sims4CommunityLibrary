"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from typing import Callable, Any, Union

from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonEventHandler:
    """CommonEventHandler(mod_identifier, event_function)

    Handles events.

    :param mod_identifier: The name or identity of the mod handling events.
    :type mod_identifier: Union[str, CommonModIdentity]
    :param event_function: The function this handler invokes.
    :type event_function: Callable[[CommonEvent], Any]
    :exception RuntimeError: When event_function is None.
    :exception TypeError: When event_function is not a callable function.
    :exception AssertionError: When the event_function is missing the event_data argument, when the event_function contains a self or cls argument, or when more than one argument is found.
    """
    def __init__(self, mod_identifier: Union[str, CommonModIdentity], event_function: Callable[[CommonEvent], Any]):
        if event_function is None:
            raise RuntimeError('Required parameter \'event_function\' required for event function from mod: {}'.format(repr(mod_identifier)))
        if not inspect.isfunction(event_function):
            raise TypeError('\'event_function\' with name \'{}\' was not a callable function. Mod Name: \'{}\''.format(event_function.__name__, repr(mod_identifier)))
        function_signature = inspect.signature(event_function)
        if function_signature.parameters is None or len(function_signature.parameters) == 0 or len(function_signature.parameters) > 1:
            raise AssertionError('Event Function has an incorrect number of parameters, Mod Name: \'{}\' Func Name: \'{}\''.format(repr(mod_identifier), event_function.__name__))
        if 'event_data' not in function_signature.parameters:
            raise AssertionError('Event Function \'{}\' is missing the required argument with name \'event_data\'')
        if 'self' in function_signature.parameters or 'cls' in function_signature.parameters:
            raise AssertionError('Event functions must be static methods. Mod Name: \'{}\', Function: \'{}\''.format(repr(mod_identifier), event_function.__name__))
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        self._mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier)
        self._event_function = event_function
        self._event_type = function_signature.parameters['event_data'].annotation

    @property
    def mod_name(self) -> str:
        """The name of the mod this event handler was created for.

        :return: The name of the Mod that owns this handler.
        :rtype: str
        """
        return self._mod_name

    @property
    def event_function(self) -> Callable[[CommonEvent], Any]:
        """The action to take upon receiving an event.

        :return: The function that handles events.
        :rtype: Callable[[CommonEvent], Any]
        """
        return self._event_function

    @property
    def event_type(self) -> type:
        """The class type of events this Event Handler will handle.

        :return: The types of events the handler handles.
        :rtype: type
        """
        return self._event_type

    def can_handle_event(self, event: CommonEvent) -> bool:
        """can_handle_event(event)

        Determine if this event handler can handle the type of the event.

        :param event: The event to check.
        :type event: CommonEvent
        :return: True, if this handler can handle the event. False, if not.
        :rtype: bool
        """
        return isinstance(event, self.event_type)

    def handle_event(self, event: CommonEvent) -> bool:
        """handle_event(event)

        Handle the event data.

        :param event: The event to handle.
        :type event: CommonEvent
        :return: True, if the event was successful. False, if not.
        :rtype: bool
        """
        return self.event_function(event)

    def __repr__(self) -> str:
        return 'mod_name_{}_function_{}_event_type_{}'.format(self.mod_name, self.event_function.__name__, self.event_type.__name__)

    def __str__(self) -> str:
        return 'CommonEventHandler Mod Name: \'{}\' Function: \'{}\' Event Type: \'{}\''.format(self.mod_name, self.event_function.__name__, self.event_type.__name__)
