"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from sims4communitylib.utils.common_log_registry import CommonLog


class CommonFunctionUtils:
    """ Utilities for manipulating functions. """

    @staticmethod
    def noop(*_, **__) -> None:
        """ An empty function that does nothing. """
        pass

    @staticmethod
    def print_arguments(log: CommonLog, func_identifier: str='NO_IDENTIFIER_SPECIFIED') -> Callable[..., Any]:
        """
            Create a function that will log the arguments and keyword arguments it receives.
        :param log: The log to print the arguments to.
        :param func_identifier: An identifier for the function to determine which function was invoked
        """

        def _print_arguments(*_, **__):
            log.enable()
            log.format_with_message('print_arguments invoked for identifier \'{}\':'.format(func_identifier), argles=_, kwargles=__)
            log.disable()

        return _print_arguments
