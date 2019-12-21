"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from typing import Callable, Any


class CommonEventHandler:
    """ A handler of events. """
    def __init__(self, mod_name: str, event_function: Callable[..., Any]):
        if event_function is None:
            raise RuntimeError('Required parameter \'event_function\' required for event function from mod: {}'.format(mod_name))
        if not inspect.isfunction(event_function):
            raise TypeError('\'event_function\' with name \'{}\' was not a callable function. Mod Name: \'{}\''.format(event_function.__name__, mod_name))
        function_signature = inspect.signature(event_function)
        if function_signature.parameters is None or len(function_signature.parameters) == 0 or len(function_signature.parameters) > 1:
            raise AssertionError('Event Function has an incorrect number of parameters, Mod Name: \'{}\' Func Name: \'{}\''.format(mod_name, event_function.__name__))
        if 'event_data' not in function_signature.parameters:
            raise AssertionError('Event Function \'{}\' is missing the required argument with name \'event_data\'')
        if 'self' in function_signature.parameters or 'cls' in function_signature.parameters:
            raise AssertionError('Event functions must be static methods. Mod Name: \'{}\', Function: \'{}\''.format(mod_name, event_function.__name__))
        self._mod_name = mod_name
        self._event_function = event_function
        self._event_type = function_signature.parameters['event_data'].annotation

    @property
    def mod_name(self) -> str:
        """ The name of the mod this event handler was created for. """
        return self._mod_name

    @property
    def event_function(self) -> Callable[..., Any]:
        """ The action to take upon receiving an event. """
        return self._event_function

    @property
    def event_type(self):
        """ The class type of events this Event Handler will handle. """
        return self._event_type

    def can_handle_event(self, event) -> bool:
        """ Determine if this event handler can handle the type of the event. """
        return isinstance(event, self.event_type)

    def handle_event(self, event) -> bool:
        """
            Handle the event data.
        """
        return self.event_function(event)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'CommonEventHandler Mod Name: \'{}\' Function: \'{}\''.format(self.mod_name, self.event_function.__name__)
