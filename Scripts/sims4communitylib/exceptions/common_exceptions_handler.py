"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from functools import wraps
from typing import Any, Callable, Union
from sims4communitylib.exceptions.common_stacktrace_utils import CommonStacktraceUtil
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonExceptionHandler:
    """A class for catching and logging exceptions to a file on the system.

    """

    @staticmethod
    def log_exception(mod_identifier: Union[str, CommonModIdentity], exception_message: str, exception: Exception=None) -> bool:
        """log_exception(mod_identifier, exception_message, exception=None)

        Manually log an exception with a custom message.

        :param mod_identifier: The name or identity of the mod logging the exception.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param exception_message: A message to provide more information about the exception.
        :type exception_message: str
        :param exception: The exception being logged. Default is None.
        :type exception: Exception, optional
        :return: True, if the message was successfully logged. False, if the message was not successfully logged.
        :rtype: bool
        """
        exceptions = CommonStacktraceUtil.get_full_stack_trace()
        stack_trace = '{}{} -> {}: {}\n'.format(''.join(exceptions), exception_message, type(exception).__name__, exception)
        from sims4communitylib.utils.common_log_registry import CommonLogUtils
        file_path = CommonLogUtils.get_exceptions_file_path(mod_identifier)
        result = CommonExceptionHandler._log_stacktrace(mod_identifier, stack_trace, file_path)
        if result:
            CommonExceptionHandler._notify_exception_occurred(file_path, mod_identifier=mod_identifier)
        return result

    @staticmethod
    def catch_exceptions(mod_identifier: Union[str, CommonModIdentity], fallback_return: Any=None) -> Callable[..., Any]:
        """catch_exceptions(mod_identifier, fallback_return=None)

        Automatically catch exceptions thrown by the decorated function, log them to a file, and notify the player about the exception.

        .. note:: Decorate functions with this decorator to catch and log exceptions

        :param mod_identifier: The name or identity of the mod catching exceptions.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param fallback_return: A value to return upon an exception being caught. Default is None.
        :type fallback_return: Any, optional
        :return: A function wrapped to catch and log exceptions.
        :rtype: Callable[..., Any]
        """
        if isinstance(mod_identifier, CommonModIdentity):
            mod_identifier = mod_identifier.name

        def _catch_exception(exception_function: Callable[..., Any]):
            @wraps(exception_function)
            def _wrapper(*args, **kwargs) -> Any:
                try:
                    return exception_function(*args, **kwargs)
                except Exception as ex:
                    CommonExceptionHandler.log_exception(mod_identifier, 'Exception caught while invoking: {}'.format(exception_function.__name__), exception=ex)
                return fallback_return
            return _wrapper
        return _catch_exception

    @staticmethod
    def _log_stacktrace(mod_identifier: Union[str, CommonModIdentity], _traceback: str, file_path: str) -> bool:
        if isinstance(mod_identifier, CommonModIdentity):
            mod_identifier = mod_identifier.name
        exception_traceback_text = '[{}] {} {}\n'.format(mod_identifier, CommonRealDateUtils.get_current_date_string(), _traceback)
        return CommonIOUtils.write_to_file(file_path, exception_traceback_text, ignore_errors=True)

    @staticmethod
    def _notify_exception_occurred(file_path: str, mod_identifier: Union[str, CommonModIdentity]=None):
        from ui.ui_dialog_notification import UiDialogNotification
        from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
        from sims4communitylib.enums.strings_enum import CommonStringId
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if not CommonZoneSpinEventDispatcher.get().game_loaded:
            return
        if mod_identifier is None or not mod_identifier:
            mod_identifier = ModInfo.get_identity().name
        if isinstance(mod_identifier, CommonModIdentity):
            mod_identifier = mod_identifier.name
        basic_notification = CommonBasicNotification(
            CommonStringId.EXCEPTION_OCCURRED_TITLE_FOR_MOD,
            CommonStringId.EXCEPTION_OCCURRED_TEXT,
            title_tokens=(mod_identifier,),
            description_tokens=(file_path,),
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        basic_notification.show()
