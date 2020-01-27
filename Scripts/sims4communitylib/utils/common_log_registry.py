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
    """CommonLog(mod_name, log_name)

    A class used to log messages.

    :param mod_name: The name of the Mod that owns the log.
    :type mod_name: str
    :param log_name: The name of the log, used when enabling/disabling logs via commands
    :type log_name: str
    """
    def __init__(self, mod_name: str, log_name: str):
        self._log_name = log_name
        self._mod_name = mod_name
        self._enabled = False

    def debug(self, message: str):
        """debug(message)

        Log a message with message type DEBUG.

        :param message: The message to log.
        :type message: str
        """
        if self.enabled:
            self._log_message(CommonMessageType.DEBUG, message)

    def info(self, message: str):
        """info(message)

        Log a message with message type INFO.

        :param message: The message to log.
        :type message: str
        """
        if self.enabled:
            self._log_message(CommonMessageType.INFO, message)

    def format_info(self, *args, **kwargs):
        """format_info(*args, **kwargs)

        Log a non-descriptive message containing pformatted arguments and keyword arguments with message type INFO.

        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format(*args, message_type=CommonMessageType.INFO, **kwargs)

    def format_info_with_message(self, message: str, *args, **kwargs):
        """format_info_with_message(message, *args, **kwargs)

        Log a message containing pformatted arguments and keyword arguments with message type INFO.

        :param message: The message to log.
        :type message: str
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format_with_message(message, *args, message_type=CommonMessageType.INFO, **kwargs)

    def format(self, *args, message_type: str=CommonMessageType.DEBUG, **kwargs):
        """format(*args, message_type=CommonMessageType.DEBUG, **kwargs)

        Log a non-descriptive message containing pformatted arguments and keyword arguments with the specified message type.

        :param message_type: The MessageType of the logged message.
        :type message_type: CommonMessageType, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if self.enabled:
            self._log_message(message_type, '{}, {}\n'.format(pformat(args), pformat(kwargs)))

    def format_with_message(self, message: str, *args, message_type: str=CommonMessageType.DEBUG, **kwargs):
        """format_with_message(message, *args, message_type=CommonMessageType.DEBUG, **kwargs)

        Log a message containing pformatted arguments and keyword arguments with the specified message type.

        :param message: The message to log.
        :type message: str
        :param message_type: The type of message being logged.
        :type message_type: CommonMessageType, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if self.enabled:
            self._log_message(message_type, '{} {}, {}\n'.format(message, pformat(args), pformat(kwargs)))

    def error(self, message: str, message_type: str=CommonMessageType.ERROR, exception: Exception=None, throw: bool=True):
        """error(message, message_type=CommonMessageType.ERROR, exception=None, throw=True)

        Log an error message with the specified message type

        :param message: The message to log.
        :type message: str
        :param message_type: The message type of the error message.
        :type message_type: CommonMessageType, optional
        :param exception: The exception that occurred.
        :param throw: If set to True, the exception will be rethrown.
        :type throw: bool, optional
        """
        if throw:
            CommonExceptionHandler.log_exception(self._mod_name, message, exception=exception)
        self._log_message(message_type, message)
        if exception is not None:
            self._log_message(message_type, pformat(exception))

    def format_error(self, *args, exception: Exception=None, throw: bool=True, **kwargs):
        """format_error(*args, exception=None, throw=True, **kwargs)

        Log a non-descriptive error message containing pformatted arguments and keyword arguments.

        :param exception: The exception that occurred.
        :type exception: Exception, optional
        :param throw: If set to True, the exception will be rethrown.
        :type throw: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.error('{}, {}\n'.format(pformat(args), pformat(kwargs)), exception=exception, throw=throw)

    def format_error_with_message(self, message: str, *args, exception: Exception=None, throw: bool=True, **kwargs):
        """format_error_with_message(message, *args, exception=None, throw=True, **kwargs)

        Log an error message containing pformatted arguments and keyword arguments.

        :param message: The message to log.
        :type message: str
        :param exception: The exception that occurred.
        :type exception: Exception, None
        :param throw: If set to True, the exception will be rethrown.
        :type throw: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.error('{} {}, {}\n'.format(message, pformat(args), pformat(kwargs)), exception=exception, throw=throw)

    def log_stack(self):
        """Log the current stack trace and the calling frames

        .. note:: The best use for this is to find the path of invocation to the location this function is called at.

        """
        if not self.enabled:
            return
        import inspect
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        self.format(calling_frame)

    def enable(self):
        """Enable the log

        """
        self._enabled = True

    def disable(self):
        """Disable the log

        """
        self._enabled = False
    
    @property
    def enabled(self) -> bool:
        """Determine if the log is enabled or not.

        .. note:: All logs are disabled by default.

        :return: True, if the log is enabled. False, if the log is disabled.
        :rtype: bool
        """
        return self._enabled

    @property
    def name(self) -> str:
        """The identifier of this log.

        :return: A string identifier.
        :rtype: str
        """
        return self._log_name

    def _log_message(self, message_type: str, message: str):
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


    :Example Usage:

    .. highlight:: python
    .. code-block:: python

        # Register the log, Logs will appear in a file titled "MOD_NAME_Messages.txt" and messages logged using this log will be prefixed with "s4cl_log_name"
        log = CommonLogRegistry.get().register_log('MOD_NAME', 's4cl_log_name')
        # Enable the log, if not enabled, messages will not be logged.
        log.enable()
        # Log a message
        log.debug('Printing a message to the log.')
        # Disable the log
        log.disable()

        # The MOD_NAME_Messages.txt file will contain the "Printing a message to the log." message.

    .. note::

        Available Commands:

        - `s4clib.enable_log` or `s4clib.enablelog`
        - `s4clib.disable_log` or `s4clib.disablelog`
        - `s4clib.disable_all_logs` or `s4clib.disablealllogs`
        - `s4clib.logs`

    """
    def __init__(self):
        self._registered_logs: Dict[str, List[CommonLog]] = dict()

    def get_registered_log_names(self) -> List[str]:
        """get_registered_log_names()

        Retrieve the names of all registered logs.

        :return: A collection of registered logs.
        :rtype: List[str]
        """
        if self._registered_logs is None:
            return []
        log_names = []
        for log_name in self._registered_logs:
            log_names.append(log_name)
        return log_names

    def register_log(self, mod_name: str, log_name: str) -> CommonLog:
        """register_log(mod_name, log_name)

        Create and register a log with the specified name.

        .. note:: If `log_name` matches the name of a Log already registered, that log will be returned rather than creating a new Log.

        :param mod_name: The name of the mod the log is registered for.
        :type mod_name: str
        :param log_name: The name of the log.
        :type log_name: str
        :return: An object of type CommonLog
        :rtype: CommonLog
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
        """log_exists(log_name)

        Determine if logs exist with the specified name.

        :param log_name: The name of the logs
        :type log_name: str
        :return: True, if a handler exists with the specified name.
        :rtype: bool
        """
        return log_name in self._registered_logs

    def enable_logs(self, log_name: str) -> bool:
        """enable_logs(log_name)

        Enables all logs with the specified name to begin logging.

        :param log_name: The name of the logs to enable.
        :type log_name: str
        :return: True, if successful
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        for log in self._registered_logs.get(log_name, list()):
            log.enable()
        return True

    def disable_logs(self, log_name: str) -> bool:
        """disable_logs(log_name)

        Disable all logs with the specified name from logging.

        :param log_name: The name of the logs to disable.
        :type log_name: str
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        for log in self._registered_logs.get(log_name, list()):
            log.disable()
        return True

    def disable_all_logs(self) -> bool:
        """disable_all_logs()

        Disable all logs from logging

        :return: True, if successful. False, if not.
        :rtype: bool
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
