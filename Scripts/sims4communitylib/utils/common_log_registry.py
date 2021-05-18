"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
import sims4.commands
from typing import List, Dict, Any, Union, Tuple
from pprint import pformat

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.exceptions.common_stacktrace_utils import CommonStacktraceUtil
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_io_utils import CommonIOUtils
from sims4communitylib.utils.common_log_utils import CommonLogUtils


class CommonMessageType(CommonInt):
    """Message types for use when logging.

    """
    DEBUG: 'CommonMessageType' = 0
    ERROR: 'CommonMessageType' = 1
    INFO: 'CommonMessageType' = 2
    WARN: 'CommonMessageType' = 3


class CommonLog:
    """CommonLog(mod_identifier, log_name, custom_file_path=None)

    A class used to log messages.

    :param mod_identifier: The name or identity of the Mod that owns the log.
    :type mod_identifier: Union[str, CommonModIdentity]
    :param log_name: The name of the log, used when enabling/disabling logs via commands
    :type log_name: str
    :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
    :type custom_file_path: str, optional
    """
    def __init__(self, mod_identifier: Union[str, CommonModIdentity], log_name: str, custom_file_path: str=None):
        self._log_name = log_name
        self._mod_name = mod_identifier.name if isinstance(mod_identifier, CommonModIdentity) else mod_identifier
        self._custom_file_path = custom_file_path
        self._enabled_message_types = tuple()

    def debug(self, message: str):
        """debug(message)

        Log a message with message type DEBUG.

        :param message: The message to log.
        :type message: str
        """
        if self.is_enabled(CommonMessageType.DEBUG):
            self._log_message(CommonMessageType.DEBUG, message)

    def info(self, message: str):
        """info(message)

        Log a message with message type INFO.

        :param message: The message to log.
        :type message: str
        """
        if self.is_enabled(CommonMessageType.INFO):
            self._log_message(CommonMessageType.INFO, message)

    def format_info(self, *args: Any, update_tokens: bool=True, **kwargs: Any):
        """format_info(*args, update_tokens=True, **kwargs)

        Log a non-descriptive message containing pformatted arguments and keyword arguments with message type INFO.

        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format(*args, message_type=CommonMessageType.INFO, update_tokens=update_tokens, **kwargs)

    def format_info_with_message(self, message: str, *args, update_tokens: bool=True, **kwargs):
        """format_info_with_message(message, *args, update_tokens=True, **kwargs)

        Log a message containing pformatted arguments and keyword arguments with message type INFO.

        :param message: The message to log.
        :type message: str
        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format_with_message(message, *args, message_type=CommonMessageType.INFO, update_tokens=update_tokens, **kwargs)

    def format(self, *args, message_type: CommonMessageType=CommonMessageType.DEBUG, update_tokens: bool=True, **kwargs):
        """format(*args, message_type=CommonMessageType.DEBUG, update_tokens=True, **kwargs)

        Log a non-descriptive message containing pformatted arguments and keyword arguments with the specified message type.

        :param message_type: The MessageType of the logged message. Default is CommonMessageType.DEBUG.
        :type message_type: CommonMessageType, optional
        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if self.is_enabled(message_type):
            if update_tokens:
                args = self._update_args(*args)
                kwargs = self._update_kwargs(**kwargs)
            if args and kwargs:
                self._log_message(message_type, '{}, {}\n'.format(pformat(args), pformat(kwargs)))
            elif args:
                self._log_message(message_type, '{}\n'.format(pformat(args)))
            else:
                self._log_message(message_type, '{}\n'.format(pformat(kwargs)))

    def format_with_message(self, message: str, *args, message_type: CommonMessageType=CommonMessageType.DEBUG, update_tokens: bool=True, **kwargs):
        """format_with_message(message, *args, message_type=CommonMessageType.DEBUG, update_tokens=True, **kwargs)

        Log a message containing pformatted arguments and keyword arguments with the specified message type.

        :param message: The message to log.
        :type message: str
        :param message_type: The type of message being logged. Default is CommonMessageType.DEBUG.
        :type message_type: CommonMessageType, optional
        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if self.is_enabled(message_type):
            if update_tokens:
                args = self._update_args(*args)
                kwargs = self._update_kwargs(**kwargs)
            if args and kwargs:
                self._log_message(message_type, '{} {}, {}\n'.format(message, pformat(args), pformat(kwargs)))
            elif args:
                self._log_message(message_type, '{} {}\n'.format(message, pformat(args)))
            else:
                self._log_message(message_type, '{} {}\n'.format(message, pformat(kwargs)))

    def warn(self, message: str):
        """warn(message)

        Log a message with message type WARN.

        :param message: The message to log.
        :type message: str
        """
        if self.is_enabled(CommonMessageType.WARN):
            self._log_message(CommonMessageType.WARN, message)

    def format_warn(self, *args: Any, update_tokens: bool=True, **kwargs: Any):
        """format_warn(*args, update_tokens=True, **kwargs)

        Log a non-descriptive message containing pformatted arguments and keyword arguments with message type WARN.

        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format(*args, message_type=CommonMessageType.WARN, update_tokens=update_tokens, **kwargs)

    def format_warn_with_message(self, message: str, *args, update_tokens: bool=True, **kwargs):
        """format_warn_with_message(message, *args, update_tokens=True, **kwargs)

        Log a message containing pformatted arguments and keyword arguments with message type WARN.

        :param message: The message to log.
        :type message: str
        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        self.format_with_message(message, *args, message_type=CommonMessageType.WARN, update_tokens=update_tokens, **kwargs)

    def error(self, message: str, message_type: CommonMessageType=CommonMessageType.ERROR, exception: Exception=None, throw: bool=True, stack_trace: List[str]=None):
        """error(message, message_type=CommonMessageType.ERROR, exception=None, throw=True, stack_trace=None)

        Log an error message with the specified message type

        :param message: The message to log.
        :type message: str
        :param message_type: The message type of the error message. Default is CommonMessageType.ERROR.
        :type message_type: CommonMessageType, optional
        :param exception: The exception that occurred. Default is None.
        :type exception: Exception, optional
        :param stack_trace: The stack trace leading to the exception, if not supplied, a stack trace will be gathered for you. Default is None.
        :type stack_trace: List[str], optional
        :param throw: If set to True, the exception will be rethrown.
        :type throw: bool, optional
        """
        if throw:
            stack_trace = stack_trace or CommonStacktraceUtil.get_full_stack_trace()
            self._log_error(message, exception=exception, stack_trace=stack_trace)
        self._log_message(message_type, message)
        if exception is not None:
            self._log_message(message_type, pformat(exception))

    def format_error(self, *args, exception: Exception=None, throw: bool=True, update_tokens: bool=True, stack_trace: List[str]=None, **kwargs):
        """format_error(*args, exception=None, throw=True, update_tokens=True, stack_trace=None, **kwargs)

        Log a non-descriptive error message containing pformatted arguments and keyword arguments.

        :param exception: The exception that occurred.
        :type exception: Exception, optional
        :param throw: If set to True, the exception will be rethrown.
        :type throw: bool, optional
        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param stack_trace: The stack trace leading to the exception, if not supplied, a stack trace will be gathered for you. Default is None.
        :type stack_trace: List[str], optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if update_tokens:
            args = self._update_args(*args)
            kwargs = self._update_kwargs(**kwargs)
        stack_trace = stack_trace or CommonStacktraceUtil.get_full_stack_trace()
        if args and kwargs:
            self.error('{}, {}\n'.format(pformat(args), pformat(kwargs)), exception=exception, throw=throw, stack_trace=stack_trace)
        elif args:
            self.error('{}\n'.format(pformat(args)), exception=exception, throw=throw, stack_trace=stack_trace)
        else:
            self.error('{}\n'.format(pformat(kwargs)), exception=exception, throw=throw, stack_trace=stack_trace)

    def format_error_with_message(self, message: str, *args, exception: Exception=None, throw: bool=True, update_tokens: bool=True, stack_trace: List[str]=None, **kwargs):
        """format_error_with_message(message, *args, exception=None, throw=True, update_tokens=True, stack_trace=None, **kwargs)

        Log an error message containing pformatted arguments and keyword arguments.

        :param message: The message to log.
        :type message: str
        :param exception: The exception that occurred. Default is None.
        :type exception: Exception, None
        :param throw: If set to True, the exception will be rethrown. Default is True.
        :type throw: bool, optional
        :param update_tokens: If set to True, when an arg or kwarg value is a Sim or SimInfo, it will be converted to their name before format occurs. Default is True.
        :type update_tokens: bool, optional
        :param stack_trace: The stack trace leading to the exception, if not supplied, a stack trace will be gathered for you. Default is None.
        :type stack_trace: List[str], optional
        :param args: Arguments to format into the message.
        :type args: Any
        :param kwargs: Keyword Arguments to format into the message.
        :type kwargs: Any
        """
        if update_tokens:
            args = self._update_args(*args)
            kwargs = self._update_kwargs(**kwargs)
        stack_trace = stack_trace or CommonStacktraceUtil.get_full_stack_trace()
        if args and kwargs:
            self.error('{} {}, {}\n'.format(message, pformat(args), pformat(kwargs)), exception=exception, throw=throw, stack_trace=stack_trace)
        elif args:
            self.error('{} {}\n'.format(message, pformat(args)), exception=exception, throw=throw, stack_trace=stack_trace)
        else:
            self.error('{} {}\n'.format(message, pformat(kwargs)), exception=exception, throw=throw, stack_trace=stack_trace)

    def log_stack(self) -> None:
        """log_stack()

        Log the current stack trace and the calling frames

        .. note:: The best use for this is to find the path of invocation to the location this function is called at.

        """
        if not self.is_enabled(CommonMessageType.DEBUG):
            return
        import inspect
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        self.format(calling_frame)

    def enable(self, message_types: Tuple[CommonMessageType]=(CommonMessageType.WARN, CommonMessageType.DEBUG, CommonMessageType.INFO)) -> None:
        """enable(message_types=(CommonMessageType.WARN, CommonMessageType.DEBUG, CommonMessageType.INFO))

        Enable the log or specific types of logs.

        :param message_types: The types of messages to enable for logging. Default message types are Info, Debug, and Warn.
        :rtype message_types: Tuple[CommonMessageTypes], optional
        """
        self._enabled_message_types = message_types

    def disable(self) -> None:
        """disable()

        Disable the log

        """
        self._enabled_message_types = tuple()
    
    @property
    def enabled(self) -> bool:
        """Determine whether the log is enabled or not.

        .. note:: All logs are disabled by default.

        :return: True, if the log is enabled. False, if the log is disabled.
        :rtype: bool
        """
        return any(self._enabled_message_types)

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

    @property
    def messages_file_path(self) -> str:
        """The file path messages are logged to.

        :return: The file path messages are logged to.
        :rtype: str
        """
        return CommonLogUtils.get_message_file_path(self.mod_name, custom_file_path=self._custom_file_path)

    @property
    def exceptions_file_path(self) -> str:
        """The file path exceptions are logged to.

        :return: The file path exceptions are logged to.
        :rtype: str
        """
        return CommonLogUtils.get_exceptions_file_path(self.mod_name, custom_file_path=self._custom_file_path)

    def is_enabled(self, message_type: CommonMessageType) -> bool:
        """is_enabled(log_type)

        Determine if a specific message type is enabled in for logging.

        :param message_type: The type of messages to check for allowance.
        :type message_type: CommonMessageType
        :return: True, if the message type is enabled for logging. False, if not.
        :rtype: bool
        """
        return message_type in self._enabled_message_types

    def _log_message(self, message_type: CommonMessageType, message: str):
        from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
        from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
        current_date_time = CommonRealDateUtils.get_current_date_string()
        new_message = '{} {}: [{}]: {}\n'.format(current_date_time, message_type.name, self.name, message)
        try:
            from sims4communitylib.utils.common_io_utils import CommonIOUtils
            file_path = self.messages_file_path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            CommonIOUtils.write_to_file(file_path, new_message, ignore_errors=True)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_name, 'Error occurred while attempting to log message: {}'.format(pformat(message)), exception=ex, custom_file_path=self._custom_file_path)

    def _log_error(self, message: str, exception: Exception=None, stack_trace: List[str]=None):
        from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
        from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
        try:
            exceptions = stack_trace or CommonStacktraceUtil.get_full_stack_trace()
            if exception is not None:
                stack_trace_message = '{}{} -> {}: {}\n'.format(''.join(exceptions), message, type(exception).__name__, exception)
            else:
                stack_trace_message = '{}{}\n'.format(''.join(exceptions), message)
            file_path = self.exceptions_file_path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            exception_traceback_text = '[{}] {} {}\n'.format(self.mod_name, CommonRealDateUtils.get_current_date_string(), stack_trace_message)
            result = CommonIOUtils.write_to_file(file_path, exception_traceback_text, ignore_errors=True)
            if result:
                CommonExceptionHandler._notify_exception_occurred(file_path, mod_identifier=self.mod_name)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_name, 'Error occurred while attempting to log message: {}'.format(pformat(message)), exception=ex, custom_file_path=self._custom_file_path)

    def _update_args(self, *args: Any) -> Tuple[Any]:
        if not args:
            return args
        from sims4communitylib.utils.common_type_utils import CommonTypeUtils
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        new_args: List[Any] = list()
        for arg in args:
            if CommonTypeUtils.is_sim_or_sim_info(arg):
                sim_info = CommonSimUtils.get_sim_info(arg)
                if sim_info is None:
                    new_args.append(arg)
                else:
                    new_args.append('{} ({})'.format(CommonSimNameUtils.get_full_name(sim_info), str(CommonSimUtils.get_sim_id(sim_info))))
            else:
                new_args.append(arg)
        return tuple(new_args)

    def _update_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        if not kwargs:
            return kwargs
        new_kwargs: Dict[str, Any] = dict()
        from sims4communitylib.utils.common_type_utils import CommonTypeUtils
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        for (key, val) in kwargs.items():
            if CommonTypeUtils.is_sim_or_sim_info(val):
                sim_info = CommonSimUtils.get_sim_info(val)
                if sim_info is None:
                    new_kwargs[key] = val
                else:
                    new_kwargs[key] = '{} ({})'.format(CommonSimNameUtils.get_full_name(sim_info), str(CommonSimUtils.get_sim_id(sim_info)))
            else:
                new_kwargs[key] = val
        return new_kwargs


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
        self._delete_old_log_files()

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
        if mod_identifier is None:
            log_names = []
            for log_mod_name in self._registered_logs:
                for log_name in self._registered_logs[log_mod_name]:
                    log_names.append(log_name)
            return log_names
        else:
            mod_name = CommonModIdentity._get_mod_name(mod_identifier)
            mod_name = mod_name.lower()
            if mod_name not in self._registered_logs:
                return list()
            return list(self._registered_logs[mod_name].keys())

    def register_log(self, mod_identifier: Union[str, CommonModIdentity], log_name: str, custom_file_path: str=None) -> CommonLog:
        """register_log(mod_identifier, log_name, custom_file_path: str=None)

        Create and register a log with the specified name.

        .. note:: If `log_name` matches the name of a Log already registered, that log will be returned rather than creating a new Log.

        :param mod_identifier: The name or identifier of the mod the log is registered for.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param log_name: The name of the log.
        :type log_name: str
        :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type custom_file_path: str, optional
        :return: An object of type CommonLog
        :rtype: CommonLog
        """
        if self._registered_logs is None:
            self._registered_logs = dict()
        mod_name = CommonModIdentity._get_mod_name(mod_identifier)
        mod_name = mod_name.lower()
        # Dict[str, Dict[str, CommonLog]]
        if mod_name not in self._registered_logs:
            self._registered_logs[mod_name] = dict()
        # Dict[str, CommonLog]
        if log_name in self._registered_logs[mod_name]:
            return self._registered_logs[mod_name][log_name]
        log = CommonLog(mod_identifier, log_name, custom_file_path=custom_file_path)
        from sims4communitylib.s4cl_configuration import S4CLConfiguration
        if log_name in S4CLConfiguration().enable_logs:
            log.enable(message_types=S4CLConfiguration().enable_logs[log_name])
        self._registered_logs[mod_name][log_name] = log
        return log

    def _delete_old_log_files(self) -> None:
        from sims4communitylib.utils.common_io_utils import CommonIOUtils
        files_to_delete = (
            os.path.join(CommonLogUtils.get_sims_documents_location_path(), 'mod_logs'),
        )
        for file_to_delete in files_to_delete:
            # noinspection PyBroadException
            try:
                if os.path.isfile(file_to_delete):
                    CommonIOUtils.delete_file(file_to_delete, ignore_errors=True)
                else:
                    CommonIOUtils.delete_directory(file_to_delete, ignore_errors=True)
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
        if self._registered_logs is None:
            return False
        if mod_identifier is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                return True
        else:
            mod_name = CommonModIdentity._get_mod_name(mod_identifier)
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
        if mod_identifier is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                log = self._registered_logs[log_mod_name][log_name]
                log.enable()
        else:
            mod_name = CommonModIdentity._get_mod_name(mod_identifier)
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
        if mod_identifier is None:
            for log_mod_name in self._registered_logs:
                if log_name not in self._registered_logs[log_mod_name]:
                    continue
                log = self._registered_logs[log_mod_name][log_name]
                log.disable()
        else:
            mod_name = CommonModIdentity._get_mod_name(mod_identifier)
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
        if mod_identifier is None:
            for log_mod_name in self._registered_logs:
                for log_name in self._registered_logs[log_mod_name]:
                    self._registered_logs[log_mod_name][log_name].disable()
        else:
            mod_name = CommonModIdentity._get_mod_name(mod_identifier)
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
