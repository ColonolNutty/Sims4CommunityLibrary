"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import List, Dict, Any, Union
from pprint import pformat

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_utils import CommonLogUtils


class CommonMessageType(CommonInt):
    """Message types for use when logging.

    """
    DEBUG: 'CommonMessageType' = 0
    ERROR: 'CommonMessageType' = 1
    INFO: 'CommonMessageType' = 2
    WARN: 'CommonMessageType' = 3


class CommonLog:
    """CommonLog(mod_identifier, log_name)

    A class used to log messages.

    :param mod_identifier: The name or identity of the Mod that owns the log.
    :type mod_identifier: Union[str, CommonModIdentity]
    :param log_name: The name of the log, used when enabling/disabling logs via commands
    :type log_name: str
    """
    def __init__(self, mod_identifier: Union[str, CommonModIdentity], log_name: str):
        self._log_name = log_name
        self._mod_name = mod_identifier.name if isinstance(mod_identifier, CommonModIdentity) else mod_identifier
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

    def format_info(self, *args: Any, **kwargs: Any):
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

    def format(self, *args, message_type: CommonMessageType=CommonMessageType.DEBUG, **kwargs):
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

    def format_with_message(self, message: str, *args, message_type: CommonMessageType=CommonMessageType.DEBUG, **kwargs):
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

    def warn(self, message: str):
        """warn(message)

        Log a message with message type WARN.

        :param message: The message to log.
        :type message: str
        """
        if self.enabled:
            self._log_message(CommonMessageType.WARN, message)

    def format_warn(self, *args: Any, **kwargs: Any):
        """format_warn(*args, **kwargs)

        Log a non-descriptive message containing pformatted arguments and keyword arguments with message type WARN.

        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format(*args, message_type=CommonMessageType.WARN, **kwargs)

    def format_warn_with_message(self, message: str, *args, **kwargs):
        """format_warn_with_message(message, *args, **kwargs)

        Log a message containing pformatted arguments and keyword arguments with message type WARN.

        :param message: The message to log.
        :type message: str
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format_with_message(message, *args, message_type=CommonMessageType.WARN, **kwargs)

    def error(self, message: str, message_type: CommonMessageType=CommonMessageType.ERROR, exception: Exception=None, throw: bool=True):
        """error(message, message_type=CommonMessageType.ERROR, exception=None, throw=True)

        Log an error message with the specified message type

        :param message: The message to log.
        :type message: str
        :param message_type: The message type of the error message. Default is CommonMessageType.ERROR.
        :type message_type: CommonMessageType, optional
        :param exception: The exception that occurred.
        :param throw: If set to True, the exception will be rethrown.
        :type throw: bool, optional
        """
        if throw:
            CommonExceptionHandler.log_exception(self.mod_name, message, exception=exception)
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

    def log_stack(self) -> None:
        """log_stack()

        Log the current stack trace and the calling frames

        .. note:: The best use for this is to find the path of invocation to the location this function is called at.

        """
        if not self.enabled:
            return
        import inspect
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        self.format(calling_frame)

    def enable(self) -> None:
        """enable()

        Enable the log

        """
        self._enabled = True

    def disable(self) -> None:
        """disable()

        Disable the log

        """
        self._enabled = False
    
    @property
    def enabled(self) -> bool:
        """Determine whether the log is enabled or not.

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

    @property
    def mod_name(self) -> str:
        """The name of the mod that owns the log.

        :return: The name of the mod that owns the log
        :rtype: str
        """
        return self._mod_name

    def _log_message(self, message_type: CommonMessageType, message: str):
        from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
        from pprint import pformat
        from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
        current_date_time = CommonRealDateUtils.get_current_date_string()
        new_message = '{} {}: [{}]: {}\n'.format(current_date_time, message_type.name, self.name, message)
        try:
            from sims4communitylib.utils.common_io_utils import CommonIOUtils
            file_path = CommonLogUtils.get_message_file_path(self.mod_name)
            CommonIOUtils.write_to_file(file_path, new_message, ignore_errors=True)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_name, 'Error occurred while attempting to log message: {}'.format(pformat(message)), exception=ex)


class CommonLogRegistry(CommonService):
    """CommonLogRegistry()

    Used to register logs.

    .. note:: To register your own logs, please use :func:`~get` to create a CommonLogRegistry (CommonLogRegistry.get()).


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
    def __init__(self) -> None:
        self._registered_logs: Dict[str, Dict[str, CommonLog]] = dict()

    def get_registered_log_names(self, mod_identifier: Union[str, CommonModIdentity]=None) -> List[str]:
        """get_registered_log_names()

        Retrieve the names of all registered logs.

        :param mod_identifier: The name or identifier of the mod the log is registered for. Default is None.
        :type mod_identifier: Union[str, CommonModIdentity], optional
        :return: A collection of registered logs.
        :rtype: List[str]
        """
        if self._registered_logs is None:
            return list()
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            log_names = []
            for log_mod_name in self._registered_logs:
                for log_name in self._registered_logs[log_mod_name]:
                    log_names.append(log_name)
            return log_names
        else:
            mod_name = mod_name.lower()
            if mod_name not in self._registered_logs:
                return list()
            return list(self._registered_logs[mod_name].keys())

    def register_log(self, mod_identifier: Union[str, CommonModIdentity], log_name: str) -> CommonLog:
        """register_log(mod_identifier, log_name)

        Create and register a log with the specified name.

        .. note:: If `log_name` matches the name of a Log already registered, that log will be returned rather than creating a new Log.

        :param mod_identifier: The name or identifier of the mod the log is registered for.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param log_name: The name of the log.
        :type log_name: str
        :return: An object of type CommonLog
        :rtype: CommonLog
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            mod_name = 'Unknown_Mod_Name'
        mod_name = mod_name.lower()
        # Dict[str, Dict[str, CommonLog]]
        if mod_name not in self._registered_logs:
            self._registered_logs[mod_name] = dict()
            self._delete_old_log_files(mod_name)
        # Dict[str, CommonLog]
        if log_name in self._registered_logs[mod_name]:
            return self._registered_logs[mod_name][log_name]
        log = CommonLog(mod_identifier, log_name)
        self._registered_logs[mod_name][log_name] = log
        return log

    def _delete_old_log_files(self, mod_identifier: Union[str, CommonModIdentity]):
        from sims4communitylib.utils.common_io_utils import CommonIOUtils
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            mod_name = 'Unknown_Mod_Name'
        files_to_delete = (
            CommonLogUtils.get_message_file_path(mod_name),
            CommonLogUtils.get_exceptions_file_path(mod_name),
            CommonLogUtils.get_old_message_file_path(mod_name),
            CommonLogUtils.get_old_exceptions_file_path(mod_name)
        )
        for file_to_delete in files_to_delete:
            # noinspection PyBroadException
            try:
                CommonIOUtils.delete_file(file_to_delete, ignore_errors=True)
            except:
                continue

    # noinspection PyUnusedLocal
    def log_exists(self, log_name: str, mod_identifier: Union[str, CommonModIdentity]=None) -> bool:
        """log_exists(log_name, mod_identifier=None)

        Determine if logs exist with the specified name.

        :param log_name: The name of the log to locate.
        :type log_name: str
        :param mod_identifier: The name or identity of the mod the log belongs to. Default is None.
        :type mod_identifier: Union[str, CommonModIdentity], optional
        :return: True, if a handler exists with the specified name.
        :rtype: bool
        """
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                return True
        else:
            mod_name = mod_name.lower()
            return mod_name in self._registered_logs and log_name in self._registered_logs[mod_name]

    # noinspection PyUnusedLocal
    def enable_logs(self, log_name: str, mod_identifier: Union[str, CommonModIdentity]=None) -> bool:
        """enable_logs(log_name, mod_identifier=None)

        Enable all logs with the specified name.

        :param log_name: The name of the logs to enable.
        :type log_name: str
        :param mod_identifier: The name or identity of the mod the log belongs to. Default is None.
        :type mod_identifier: Union[str, CommonModIdentity], optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                log = self._registered_logs[log_mod_name][log_name]
                log.enable()
        else:
            mod_name = mod_name.lower()
            if log_name not in self._registered_logs[mod_name]:
                return False
            self._registered_logs[mod_name][log_name].enable()
        return True

    # noinspection PyUnusedLocal
    def disable_logs(self, log_name: str, mod_identifier: Union[str, CommonModIdentity]=None) -> bool:
        """disable_logs(log_name, mod_identifier=None)

        Disable all logs with the specified name.

        :param log_name: The name of the logs to disable.
        :type log_name: str
        :param mod_identifier: The name or identity of the mod to disable logs for. Default is None.
        :type mod_identifier: Union[str, CommonModIdentity], optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                log = self._registered_logs[log_mod_name][log_name]
                log.disable()
        else:
            mod_name = mod_name.lower()
            if log_name not in self._registered_logs[mod_name]:
                return False
            self._registered_logs[mod_name][log_name].disable()
        return True

    # noinspection PyUnusedLocal
    def disable_all_logs(self, mod_identifier: Union[str, CommonModIdentity]=None) -> bool:
        """disable_all_logs(mod_identifier=None)

        Disable all logs from logging

        :param mod_identifier: The name or identity of the mod to disable logs for. Default is None.
        :type mod_identifier: Union[str, CommonModIdentity], optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        if mod_name is None:
            for log_mod_name in self._registered_logs:
                for log_name in self._registered_logs[log_mod_name]:
                    self._registered_logs[log_mod_name][log_name].disable()
        else:
            mod_name = mod_name.lower()
            for log_name in self._registered_logs.get(mod_name, dict()):
                self._registered_logs[mod_name][log_name].disable()
        return True


@sims4.commands.Command('s4clib.enable_log', 's4clib.enablelog', command_type=sims4.commands.CommandType.Live)
def _common_command_enable_log(log_name: str=None, mod_name: str=None, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        if log_name is None:
            output('specify a log name (See all logs via "s4clib.logs" command)')
            return
        output('Attempting to enable log with name \'{}\''.format(log_name))
        if CommonLogRegistry.get().log_exists(log_name, mod_identifier=mod_name):
            if CommonLogRegistry.get().enable_logs(log_name, mod_identifier=mod_name):
                output('Log enabled: {}'.format(log_name))
            else:
                if mod_name is None:
                    output('Failed to enable log with name \'{}\', did you forget to specify a mod name?'.format(log_name))
                else:
                    output('Failed to enable log with name \'{}\' for mod \'{}\''.format(log_name, mod_name))
        else:
            if mod_name is None:
                output('No log found with name \'{}\''.format(log_name))
            else:
                output('No log found with name \'{}\' for mod \'{}\''.format(log_name, mod_name))
    except Exception as ex:
        output('Failed to enable log: {}'.format(pformat(ex)))


@sims4.commands.Command('s4clib.disable_log', 's4clib.disablelog', command_type=sims4.commands.CommandType.Live)
def _common_command_disable_log(log_name: str=None, mod_name: str=None, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        if log_name is None:
            output('specify a log name (See all logs via "s4clib.logs" command)')
            return
        output('Attempting to disable log with name \'{}\''.format(log_name))
        if CommonLogRegistry.get().log_exists(log_name, mod_identifier=mod_name):
            if CommonLogRegistry.get().disable_logs(log_name, mod_identifier=mod_name):
                output('Log disabled: {}'.format(log_name))
            else:
                if mod_name is None:
                    output('Failed to disable log with name \'{}\', did you forget to specify a mod name?'.format(log_name))
                else:
                    output('Failed to disable log with name \'{}\' for mod \'{}\''.format(log_name, mod_name))
        else:
            if mod_name is None:
                output('No log found with name \'{}\''.format(log_name))
            else:
                output('No log found with name \'{}\' for mod \'{}\''.format(log_name, mod_name))
    except Exception as ex:
        output('Failed to disable log: {}'.format(pformat(ex)))


@sims4.commands.Command('s4clib.disable_all_logs', 's4clib.disablealllogs', command_type=sims4.commands.CommandType.Live)
def _common_command_disable_all_logs(mod_name: str=None, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Disabling all logs')
    try:
        CommonLogRegistry.get().disable_all_logs(mod_identifier=mod_name)
    except Exception as ex:
        output('Failed to disable all logs: {}'.format(pformat(ex)))
    output('All logs disabled')


@sims4.commands.Command('s4clib.logs', command_type=sims4.commands.CommandType.Live)
def _common_command_show_all_logs(mod_identifier: str=None, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        log_names = CommonLogRegistry.get().get_registered_log_names(mod_identifier=mod_identifier)
        if log_names is None or output is None:
            return
        if len(log_names) == 0:
            output('No registered logs found')
            return
        for log_name in log_names:
            output('' + str(log_name))
    except Exception as ex:
        output('Failed to show logs: {}'.format(pformat(ex)))
