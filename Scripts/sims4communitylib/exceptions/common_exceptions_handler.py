"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from functools import wraps
from typing import Any

from sims4communitylib.exceptions.common_stacktrace_utils import CommonStacktraceUtil
from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonExceptionHandler:
    """
        A class for handling and logging custom exceptions to a file on the system.
    """

    @staticmethod
    def log_exception(mod_name: str, exception_message: str, exception: Exception=None) -> bool:
        """
            Log an exception with a custom message
        :param mod_name: The name of the mod logging the exception.
        :param exception_message: A message to log
        :param exception: The exception that was thrown.
        :return: True if successfully logged.
        """
        exceptions = CommonStacktraceUtil.get_full_stack_trace()
        stack_trace = '{}{} -> {}: {}\n'.format(''.join(exceptions), exception_message, type(exception).__name__, exception)
        from sims4communitylib.utils.common_log_registry import CommonLogUtils
        file_path = CommonLogUtils.get_exceptions_file_path(mod_name)
        return CommonExceptionHandler._log_stacktrace(mod_name, stack_trace, file_path)

    @staticmethod
    def _log_stacktrace(mod_name: str, _traceback, file_path: str) -> bool:
        exception_traceback_text = '[{}] {} {}\n'.format(mod_name, CommonRealDateUtils.get_current_date_string(), _traceback)
        return CommonIOUtils.write_to_file(file_path, exception_traceback_text)

    @staticmethod
    def catch_exceptions(mod_name: str, fallback_return: Any=None):
        """
            A decorator for catching exceptions thrown by functions.
        :param mod_name: An identifier to indicate which mod it occurs in.
        :param fallback_return: A value to return upon an exception being thrown.
        :return: A wrapped function.
        """

        # noinspection PyMissingOrEmptyDocstring
        def catch_exception(exception_function):
            # noinspection PyBroadException,PyMissingOrEmptyDocstring
            @wraps(exception_function)
            def wrapper(*args, **kwargs):
                try:
                    return exception_function(*args, **kwargs)
                except Exception as ex:
                    CommonExceptionHandler.log_exception(mod_name, 'Exception caught while invoking: {}'.format(exception_function.__name__), exception=ex)
                return fallback_return
            return wrapper
        return catch_exception
