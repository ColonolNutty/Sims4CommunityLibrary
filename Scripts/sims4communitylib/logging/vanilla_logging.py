"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4.log import Logger
from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.s4cl_configuration import S4CLConfiguration
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from sims4communitylib.utils.misc.common_text_utils import CommonTextUtils


class _CommonVanillaLogOverride(CommonService):
    def __init__(self) -> None:
        self.logs_enabled = S4CLConfiguration().enable_vanilla_logging
        self.logs = list()
        self.stop_watches = dict()
        self.last_time = dict()

    def get_log(self, log_name: str) -> CommonLog:
        """ Get a log for a log name. """
        _log = CommonLogRegistry().register_log(f'{log_name}_S4CLVanillaLog', 'log', 'vanilla_logs')
        _log.enable()
        self.logs.append(_log)
        return _log

    def _format_message(self, message, *args, owner=None, **__) -> str:
        to_log_message = message
        if args:
            to_log_message = to_log_message.format(*args)
        if owner:
            to_log_message = f'[{owner}] {to_log_message}'
        return to_log_message

    def enable_logs(self) -> None:
        """ Enable logs. """
        self.logs_enabled = True

    def disable_logs(self) -> None:
        """ Disable logs. """
        self.logs_enabled = False

    def _log(self, log_name: str, message: str, *args, level=None, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        message = self._append_time(log_name, message)
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(f'{level}: {to_log_message}')

    def _debug(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        message = self._append_time(log_name, message)
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(to_log_message)

    def _info(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        message = self._append_time(log_name, message)
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.info(to_log_message)

    def _warn(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        message = self._append_time(log_name, message)
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.warn(to_log_message)

    def _error(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        message = self._append_time(log_name, message)
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.error(to_log_message + ' (This exception is not caused by S4CL, but rather caught)')

    def _exception(self, log_name: str, message: str, *args, exc: Exception = None, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        message = self._append_time(log_name, message)
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.error(to_log_message + ' (This exception is not caused by S4CL, but rather caught)', exception=exc, throw=True)

    def _append_time(self, log_name: str, message: str) -> str:
        stop_watch = self._get_stop_watch(log_name)
        interval = stop_watch.interval_milliseconds()
        if log_name not in self.last_time:
            self.last_time[log_name] = interval
            compare_time = 0
        else:
            last_time = self.last_time[log_name]
            compare_time = interval - last_time
            self.last_time[log_name] = interval
        interval_str = CommonTextUtils.to_truncated_decimal(interval)
        compare_time_str = CommonTextUtils.to_truncated_decimal(compare_time)
        return f'{interval_str}ms +{compare_time_str}ms {message}'

    def _get_stop_watch(self, log_name: str) -> CommonStopWatch:
        if log_name not in self.stop_watches:
            stop_watch = CommonStopWatch()
            stop_watch.start()
            self.stop_watches[log_name] = stop_watch
        return self.stop_watches[log_name]

    def _clear_log_times(self) -> None:
        stop_watches = list(self.stop_watches.values())
        self.stop_watches.clear()
        self.stop_watches.clear()
        self.last_time.clear()
        for stop_watch in stop_watches:
            stop_watch.stop()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.enable_vanilla_logs',
    'Enable the Vanilla Logs. Vanilla Logs are useful for discovering previously unknown exceptions and messages being logged by the game itself. Vanilla logs appear under "The Sims 4/mod_logs/vanilla_logs"',
    command_aliases=(
        's4clib.enablevanillalogs',
    )
)
def _common_enable_vanilla_logs(output: CommonConsoleCommandOutput):
    output('Enabling the Vanilla Logs.')
    if _CommonVanillaLogOverride().logs_enabled:
        output('The Vanilla Logs are already enabled.')
        return
    _CommonVanillaLogOverride()._clear_log_times()
    _CommonVanillaLogOverride().enable_logs()
    output('Vanilla Logs are now enabled.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.disable_vanilla_logs',
    'Disable the Vanilla Logs.',
    command_aliases=(
        's4clib.disablevanillalogs',
    )
)
def _common_disable_vanilla_logs(output: CommonConsoleCommandOutput):
    output('Disabling the Vanilla Logs.')
    if not _CommonVanillaLogOverride().logs_enabled:
        output('The Vanilla Logs are already disabled.')
        return
    _CommonVanillaLogOverride().disable_logs()
    _CommonVanillaLogOverride()._clear_log_times()
    output('Vanilla Logs are now disabled.')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, 'log', handle_exceptions=False)
def _common_logger_log(original, self, message, *args, level=None, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._log(log_name, message, *args, level=level, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, level=level, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, 'debug', handle_exceptions=False)
def _common_logger_debug(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._debug(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, 'info', handle_exceptions=False)
def _common_logger_info(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._info(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, 'warn', handle_exceptions=False)
def _common_logger_warn(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._warn(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, 'error', handle_exceptions=False)
def _common_logger_error(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._error(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, 'exception', handle_exceptions=False)
def _common_logger_exception(original, self, message, *args, exc=None, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._exception(log_name, message, *args, exc=exc, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, exc=exc, owner=owner, **kwargs)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.clear_log_times', 'Clear the stop watches for the vanilla logs', show_with_help_command=False)
def _common_clear_log_times(output: CommonConsoleCommandOutput):
    output('Clearing Vanilla Logs log times.')
    _CommonVanillaLogOverride()._clear_log_times()
