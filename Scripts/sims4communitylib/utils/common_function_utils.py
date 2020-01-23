"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Iterator

from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_log_registry import CommonLog


class CommonFunctionUtils:
    """Utilities for manipulating functions.

    """

    @staticmethod
    def noop(*_, **__) -> None:
        """An empty function that does nothing. Useful when you need something to do nothing.

        """
        pass

    @staticmethod
    def print_arguments(log: CommonLog, func_identifier: str='NO_IDENTIFIER_SPECIFIED') -> Callable[..., Any]:
        """Create a function that will log the arguments and keyword arguments it receives

        :param log: The log to print the arguments to.
        :param func_identifier: An identifier for the function to determine which function was invoked
        """

        def _print_arguments(*_, **__):
            log.enable()
            log.format_with_message('print_arguments invoked for identifier \'{}\':'.format(func_identifier), argles=_, kwargles=__)
            log.disable()

        return _print_arguments

    @staticmethod
    def safe_run(mod_identity: CommonModIdentity, primary_function: Callable[..., Any], fallback_function: Callable[..., Any], *args, **kwargs) -> Any:
        """Safely run a function, if the primary function throws an exception, the fallback function will be run instead.

        :param mod_identity: The identity of the mod running a function safely.
        :param primary_function: The primary function to safely run.
        :param fallback_function: A function called when the primary function throws an exception.
        :param args: Arguments to pass to both the primary function and fallback function.
        :param kwargs: Keyword Arguments to pass to both the primary function and fallback function.
        :return: The result of either the primary function or the fallback function if the primary threw an exception.
        """
        try:
            return primary_function(*args, **kwargs)
        except Exception as ex:
            # noinspection PyBroadException
            try:
                from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                CommonExceptionHandler.log_exception(mod_identity.name, 'Error occurred while running \'{}\''
                                                            .format(primary_function.__name__), exception=ex)
            except Exception:
                pass
            return fallback_function(*args, **kwargs)

    @staticmethod
    def run_predicates_as_one(predicate_functions: Iterator[Callable[..., bool]], all_must_pass: bool=True) -> Callable[..., bool]:
        """Wrap all specified predicate functions into a single predicate function. (See returned value for more information).

        :param predicate_functions: The predicate functions to run as one.
        :param all_must_pass: If True, all of the predicates must return a True value. If False, only some of the predicates must return a True value.
        :return: If all_must_pass is True a wrapped function that will return a value of:
          - True, if all predicates resulted in a True value.
          - False, if any predicates resulted in a False value.

          If all_must_pass is False a wrapped function that will return a value of:
          - True, if any predicates resulted in a True value.
          - False, if all predicates resulted in a False value.

        """
        def _wrapper(*_, **__):
            if all_must_pass:
                for primary_function in predicate_functions:
                    if not primary_function(*_, **__):
                        return False
                return True
            else:
                for primary_function in predicate_functions:
                    if primary_function(*_, **__):
                        return True
                return False
        return _wrapper

    @staticmethod
    def run_predicate_with_reversed_result(predicate_function: Callable[..., bool]) -> Callable[..., bool]:
        """Wrap the specified predicate function and reverse the result of it when the function is invoked.

        :param predicate_function: The predicate function to reverse the result of.
        :return: A wrapped function.
        """
        def _wrapper(*_, **__):
            return not predicate_function(*_, **__)
        return _wrapper

    @staticmethod
    def run_with_arguments(primary_function: Callable[..., Any], *args, **kwargs) -> Callable[..., Any]:
        """Wrap a function and run it with additional arguments when something invokes it.

        :param primary_function: The function that will be run.
        :return: A wrapped function.
        """
        def _wrapper(*_, **__):
            return primary_function(*_, *args, **__, **kwargs)
        return _wrapper
