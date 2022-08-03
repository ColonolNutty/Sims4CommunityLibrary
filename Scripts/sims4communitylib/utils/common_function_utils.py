"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Iterator, Union

from sims4communitylib.classes.testing.common_enqueue_result import CommonEnqueueResult
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_log_registry import CommonLog


class CommonFunctionUtils:
    """Utilities for manipulating functions.

    """

    @staticmethod
    def noop(*_, **__) -> None:
        """noop(*_, **__)

        An empty function that does nothing. Useful when you need something to do nothing.

        .. note:: Use this when you want something to do nothing.

        """
        pass

    @staticmethod
    def noop_execution_result(*_, **__) -> CommonExecutionResult:
        """noop_execution_result(*_, **__)

        An empty function that does nothing but return :func:`CommonExecutionResult.NONE`. Useful when you need something to simply return CommonExecutionResult.NONE.

        .. note:: Use this when you want something to simply return CommonExecutionResult.NONE.

        :return: Returns CommonExecutionResult.NONE.
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.NONE

    @staticmethod
    def noop_test_result(*_, **__) -> CommonTestResult:
        """noop_test_result(*_, **__)

        An empty function that does nothing but return :func:`CommonTestResult.NONE`. Useful when you need something to simply return CommonTestResult.NONE.

        .. note:: Use this when you want something to simply return CommonTestResult.NONE.

        :return: Returns CommonTestResult.NONE.
        :rtype: CommonTestResult
        """
        return CommonTestResult.NONE

    @staticmethod
    def noop_enqueue(*_, **__) -> CommonEnqueueResult:
        """noop_enqueue(*_, **__)

        An empty function that does nothing but return :func:`CommonEnqueueResult.NONE`. Useful when you need something to simply return CommonEnqueueResult.NONE.

        .. note:: Use this when you want something to simply return CommonEnqueueResult.NONE.

        :return: Returns CommonEnqueueResult.NONE.
        :rtype: CommonEnqueueResult
        """
        return CommonEnqueueResult.NONE

    @staticmethod
    def noop_true(*_, **__) -> bool:
        """noop_true(*_, **__)

        An empty function that does nothing but return True. Useful when you need something to simply return True.

        .. note:: Use this when you want something to simply return True.

        :return: Returns True.
        :rtype: bool
        """
        return True

    @staticmethod
    def noop_false(*_, **__) -> bool:
        """noop_false(*_, **__)

        An empty function that does nothing but return False. Useful when you need something to simply return False.

        .. note:: Use this when you want something to simply return False.

        :return: Returns False.
        :rtype: bool
        """
        return False

    @staticmethod
    def print_arguments(log: CommonLog, func_identifier: str = 'NO_IDENTIFIER_SPECIFIED') -> Callable[..., Any]:
        """print_arguments(log, func_identifier='NO_IDENTIFIER_SPECIFIED')

        Create a function that will log the arguments and keyword arguments it receives

        :param log: The log to print the arguments to.
        :type log: CommonLog
        :param func_identifier: An identifier for the function to determine which function was invoked
        :type func_identifier: str
        :return: A function that will print the arguments sent to it when the original function is invoked.
        :rtype: Callable[..., Any]
        """

        def _print_arguments(*_: Any, **__: Any):
            log.enable()
            log.format_with_message(f'print_arguments invoked for identifier \'{func_identifier}\':', argles=_, kwargles=__)
            log.disable()

        return _print_arguments

    @staticmethod
    def safe_run(mod_identity: CommonModIdentity, primary_function: Callable[..., Any], fallback_function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """safe_run(mod_identity, primary_function, fallback_function, *args, **kwargs)

        Safely run a function, if the primary function throws an exception, the fallback function will be run instead.

        :param mod_identity: The identity of the mod running a function safely.
        :type mod_identity: CommonModIdentity
        :param primary_function: The primary function to safely run.
        :type primary_function: Callable[..., Any]
        :param fallback_function: A function called when the primary function throws an exception.
        :type fallback_function: Callable[..., Any]
        :param args: Arguments to pass to both the primary function and fallback function.
        :type args: Any
        :param kwargs: Keyword Arguments to pass to both the primary function and fallback function.
        :type kwargs: Any
        :return: The result of either the primary function or the fallback function if the primary threw an exception.
        :rtype: Any
        """
        try:
            if primary_function is None:
                if fallback_function is None:
                    return
                return fallback_function(*args, **kwargs)
            return primary_function(*args, **kwargs)
        except Exception as ex:
            # noinspection PyBroadException
            try:
                from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                CommonExceptionHandler.log_exception(
                    mod_identity,
                    f'Error occurred while running \'{primary_function.__name__}\'',
                    exception=ex
                )
            except Exception:
                pass
            # noinspection PyBroadException
            try:
                if fallback_function is None:
                    return
                return fallback_function(*args, **kwargs)
            except:
                pass

    @staticmethod
    def run_predicates_as_one(predicate_functions: Iterator[Callable[..., Union[bool, CommonExecutionResult, CommonTestResult]]], all_must_pass: bool = True) -> Callable[..., Union[bool, CommonExecutionResult, CommonTestResult]]:
        """run_predicates_as_one(predicate_functions, all_must_pass=True)

        Wrap all predicate functions into a single predicate function. (See returned value for more information).

        .. note::

            If `all_must_pass` is True a wrapped function that will return a value of:

            - True, if all predicates resulted in a True value.
            - False, if any predicates resulted in a False value.

            If `all_must_pass` is False a wrapped function that will return a value of:

            - True, if any predicates resulted in a True value.
            - False, if all predicates resulted in a False value.

        :param predicate_functions: The predicate functions to run as one.
        :type predicate_functions: Iterator[Callable[..., bool]]
        :param all_must_pass: If True, all the predicates must return a True value. If False, any of the predicates must return a True value.
        :type all_must_pass: bool, optional
        :return: The result of running all functions.
        :rtype: bool
        """
        def _wrapper(*_: Any, **__: Any):
            if all_must_pass:
                for primary_function in predicate_functions:
                    if primary_function is None:
                        continue
                    if not primary_function(*_, **__):
                        return False
                return True
            else:
                for primary_function in predicate_functions:
                    if primary_function is None:
                        continue
                    if primary_function(*_, **__):
                        return True
                return False
        _wrapper.__name__ = ', '.join([func.__name__ for func in predicate_functions if func is not None])
        return _wrapper

    @staticmethod
    def run_predicate_with_reversed_result(predicate_function: Callable[..., Union[bool, CommonExecutionResult, CommonTestResult]]) -> Callable[..., Union[bool, CommonExecutionResult, CommonTestResult]]:
        """run_predicate_with_reversed_result(predicate_function)

        Wrap the specified predicate function and reverse the result of it when the function is invoked.

        :param predicate_function: The predicate function to reverse the result of.
        :type predicate_function: Callable[..., bool]
        :return: A function that will reverse the result of `predicate_function` upon invocation.
        :rtype: Callable[..., bool]
        """
        def _wrapper(*_: Any, **__: Any) -> Any:
            if predicate_function is None:
                return False
            result = predicate_function(*_, **__)
            if isinstance(result, CommonExecutionResult) or isinstance(result, CommonTestResult):
                return result.reverse_result()
            return not result
        if predicate_function is not None:
            _wrapper.__name__ = predicate_function.__name__
        return _wrapper

    @staticmethod
    def run_with_arguments(primary_function: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """run_with_arguments(primary_function, *args, **kwargs)

        Wrap a function and run it with additional arguments when something invokes it.

        :param primary_function: The function that will be run.
        :type primary_function: Callable[..., Any]
        :return: A function that will send extra arguments upon invocation.
        :rtype: Callable[..., Any]
        """
        def _wrapper(*_: Any, **__: Any) -> Any:
            if primary_function is None:
                return False
            return primary_function(*_, *args, **__, **kwargs)
        if primary_function is not None:
            _wrapper.__name__ = primary_function.__name__
        return _wrapper
