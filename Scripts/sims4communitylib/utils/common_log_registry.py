"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import List, Dict
from pprint import pformat

from sims4communitylib.enums.enumtypes.string_enum import CommonEnumStringBase
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_utils import CommonLogUtils


class CommonMessageType(CommonEnumStringBase):
    """Message types for use when logging.

    """
    DEBUG = 'DEBUG'
    ERROR = 'ERROR'
    INFO = 'INFO'


class CommonLog:
    """A logging class used to log messages.

    """
    def __init__(self, mod_name: str, log_name: str):
        self._log_name = log_name
        self._mod_name = mod_name
        self._enabled = False

    def debug(self, message: str):
        """Log a message with message type DEBUG.

        :param message: The message to log.
        """
        if self.enabled:
            self._log_message(CommonMessageType.DEBUG, message)

    def info(self, message: str):
        """Log a message with message type INFO.

        :param message: The message to log.
        """
        if self.enabled:
            self._log_message(CommonMessageType.INFO, message)

    def format_info(self, *args, **kwargs):
        """Log a non-descriptive message containing pformatted arguments and keyword arguments with message type INFO.

        """
        self.format(*args, message_type=CommonMessageType.INFO, **kwargs)

    def format_info_with_message(self, message: str, *args, **kwargs):
        """Log a message containing pformatted arguments and keyword arguments with message type INFO.

        :param message: The message to log.
        """
        self.format_with_message(message, *args, message_type=CommonMessageType.INFO, **kwargs)

    def format(self, *args, message_type: str=CommonMessageType.DEBUG, **kwargs):
        """Log a non-descriptive message containing pformatted arguments and keyword arguments with the specified message type.

        :param message_type: The MessageType of the logged message.
        """
        if self.enabled:
            self._log_message(message_type, '{}, {}\n'.format(pformat(args), pformat(kwargs)))

    def format_with_message(self, message: str, *args, message_type: str=CommonMessageType.DEBUG, **kwargs):
        """Log a message containing pformatted arguments and keyword arguments with the specified message type.

        :param message: The message to log.
        :param message_type: The type of message being logged.
        """
        if self.enabled:
            self._log_message(message_type, '{} {}, {}\n'.format(message, pformat(args), pformat(kwargs)))

    def error(self, message: str, message_type: str=CommonMessageType.ERROR, exception: Exception=None, throw: bool=True):
        """Log an error message with the specified message type

        :param message: The message to log.
        :param message_type: The message type of the error message.
        :param exception: The exception that occurred.
        :param throw: If set to True, the exception will be rethrown.
        """
        if throw:
            CommonExceptionHandler.log_exception(self._mod_name, message, exception=exception)
        self._log_message(message_type, message)
        if exception is not None:
            self._log_message(message_type, pformat(exception))

    def format_error(self, *args, exception: Exception=None, throw: bool=True, **kwargs):
        """Log a non-descriptive error message containing pformatted arguments and keyword arguments.

        :param exception: The exception that occurred.
        :param throw: If set to True, the exception will be rethrown.
        """
        self.error('{}, {}\n'.format(pformat(args), pformat(kwargs)), exception=exception, throw=throw)

    def format_error_with_message(self, message: str, *args, exception: Exception=None, throw: bool=True, **kwargs):
        """Log an error message containing pformatted arguments and keyword arguments.

        :param message: The message to log.
        :param exception: The exception that occurred.
        :param throw: If set to True, the exception will be rethrown.
        """
        self.error('{} {}, {}\n'.format(message, pformat(args), pformat(kwargs)), exception=exception, throw=throw)

    def log_stack(self):
        """Log the current stack trace and the calling frames

        """
        if not self.enabled:
            return
        import inspect
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        self.format(calling_frame)

    def enable(self):
        """Enable this log for logging.

        """
        self._enabled = True

    def disable(self):
        """Disable this log from logging

        """
        self._enabled = False
    
    @property
    def enabled(self) -> bool:
        """Determine if the log is enabled or not.

        :return: True if the log is enabled.
        """
        return self._enabled

    @property
    def name(self) -> str:
        """The identifier of this log.

        :return: A string identifier.
        """
        return self._log_name

    def _log_message(self, message_type: str, message: str):
        """Log a message with message type.

        :param message_type: The type of message being logged.
        :param message: The message being logged.
        """
        from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
        from pprint import pformat
        from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
        current_date_time = CommonRealDateUtils.get_current_date_string()
        new_message = '{} [{}] {}: [{}]: {}\n'.format(current_date_time, self._mod_name, str(message_type), self.name, message)
        try:
            from sims4communitylib.utils.common_io_utils import CommonIOUtils
            file_path = CommonLogUtils.get_message_file_path(self._mod_name)
            CommonIOUtils.write_to_file(file_path, new_message, ignore_errors=True)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self._mod_name, 'Error occurred while attempting to log message: {}'.format(pformat(message)), exception=ex)


class CommonLogRegistry(CommonService):
    """A registry for log handlers.
    To register your own logs, please use CommonLogRegistry.get() to create a CommonLogRegistry.

    """
    def __init__(self):
        self._registered_logs: Dict[str, List[CommonLog]] = dict()

    def get_registered_log_names(self) -> List[str]:
        """Retrieve the names of all registered logs.

        :return: A collection of type str
        """
        if self._registered_logs is None:
            return []
        log_names = []
        for log_name in self._registered_logs:
            log_names.append(log_name)
        return log_names

    def register_log(self, mod_name: str, log_name: str) -> CommonLog:
        """Create and register a log with the specified name.

        :param mod_name: The name of the mod the log is registered for.
        :param log_name: The name of the log.
        :return: An object of type CommonLog
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        logs = list()
        if log_name in self._registered_logs:
            logs = self._registered_logs[log_name]
        log = CommonLog(mod_name, log_name)
        logs.append(log)
        self._registered_logs[log_name] = logs
        return log

    def log_exists(self, log_name: str) -> bool:
        """Determine if logs exist with the specified name.

        :param log_name: The name of the logs
        :return: True if a handler exists with the specified name.
        """
        return log_name in self._registered_logs

    def enable_logs(self, log_name: str) -> bool:
        """Enables all logs with the specified name to begin logging.

        :param log_name: The name of the logs to enable.
        :return: True if successful
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        for log in self._registered_logs.get(log_name, list()):
            log.enable()
        return True

    def disable_logs(self, log_name: str) -> bool:
        """Disable all logs with the specified name from logging.

        :param log_name: The name of the logs to disable.
        :return: True if successful
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        for log in self._registered_logs.get(log_name, list()):
            log.disable()
        return True

    def disable_all_logs(self) -> bool:
        """Disable all logs from logging

        :return: True if successful
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        for log_name in self._registered_logs:
            for log in self._registered_logs.get(log_name):
                log.disable()
        return True


@sims4.commands.Command('s4clib.enable_log', 's4clib.enablelog', command_type=sims4.commands.CommandType.Live)
def _common_command_enable_log(*args, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    if len(args) == 0 or args[0] is None:
        output('specify a log name (See all logs via "s4clib.logs" command)')
        return
    if CommonLogRegistry.get().log_exists(args[0]) and CommonLogRegistry.get().enable_logs(args[0]):
        output('Log enabled: ' + str(args[0]))
    else:
        output('No log found: ' + str(args[0]))


@sims4.commands.Command('s4clib.disable_log', 's4clib.disablelog', command_type=sims4.commands.CommandType.Live)
def _common_command_disable_log(*args, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    if len(args) == 0 or args[0] is None:
        output('specify a log name (See all logs via "s4clib.logs" command)')
        return
    if CommonLogRegistry.get().log_exists(args[0]) and CommonLogRegistry.get().disable_logs(args[0]):
        output('Log disabled: ' + str(args[0]))
    else:
        output('No log found: ' + str(args[0]))


@sims4.commands.Command('s4clib.disable_all_logs', 's4clib.disablealllogs', command_type=sims4.commands.CommandType.Live)
def _common_command_disable_all_logs(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Disabling all logs')
    CommonLogRegistry.get().disable_all_logs()
    output('All logs disabled')


@sims4.commands.Command('s4clib.logs', command_type=sims4.commands.CommandType.Live)
def _common_command_show_all_logs(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    log_names = CommonLogRegistry.get().get_registered_log_names()
    if log_names is None or output is None:
        return
    if len(log_names) == 0:
        output('No registered logs found')
        return
    for log_name in log_names:
        output('' + str(log_name))
