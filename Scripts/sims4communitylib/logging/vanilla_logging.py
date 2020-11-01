"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4.commands import Command, CommandType, CheatOutput
from sims4.log import Logger
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog


class _CommonVanillaLogOverride(CommonService):
    def __init__(self) -> None:
        self.logs_enabled = False
        self.logs = list()

    def get_log(self, log_name: str) -> CommonLog:
        """ Get a log for a log name. """
        _log = CommonLogRegistry().register_log('{}_S4CLVanillaLog'.format(log_name), 'log', 'vanilla_logs')
        _log.enable()
        self.logs.append(_log)
        return _log

    def _format_message(self, message, *args, owner=None, **__) -> str:
        to_log_message = message
        if args:
            to_log_message = to_log_message.format(*args)
        if owner:
            to_log_message = '[{owner}] {}'.format(to_log_message, owner=owner)
        return to_log_message

    def enable_logs(self) -> None:
        """ Enable logs. """
        self.logs_enabled = True

    def disable_logs(self) -> None:
        """ Disable logs. """
        self.logs_enabled = False

    def _log(self, log_name: str, message: str, *args, level, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug('{}: {}'.format(level, to_log_message))

    def _debug(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.debug(to_log_message)

    def _info(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.info(to_log_message)

    def _warn(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.warn(to_log_message)

    def _error(self, log_name: str, message: str, *args, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.error(to_log_message, throw=False)

    def _exception(self, log_name: str, message: str, *args, exc: Exception=None, owner=None, **kwargs) -> Any:
        if not self.logs_enabled:
            return
        _log = _CommonVanillaLogOverride().get_log(log_name)
        to_log_message = _CommonVanillaLogOverride()._format_message(message, *args, owner=owner, **kwargs)
        _log.error(to_log_message, exception=exc, throw=True)


@Command('s4clib.enable_vanilla_logs', command_type=CommandType.Live)
def _common_enable_vanilla_logs(_connection: int=None):
    output = CheatOutput(_connection)
    output('Enabling vanilla logs.')
    _CommonVanillaLogOverride().enable_logs()
    output('Done')


@Command('s4clib.disable_vanilla_logs', command_type=CommandType.Live)
def _common_disable_vanilla_logs(_connection: int=None):
    output = CheatOutput(_connection)
    output('Disabling vanilla logs.')
    _CommonVanillaLogOverride().disable_logs()
    output('Done')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, Logger.log.__name__, handle_exceptions=False)
def _common_logger_log(original, self, message, *args, level, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._log(log_name, message, *args, level, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, level, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, Logger.debug.__name__, handle_exceptions=False)
def _common_logger_debug(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._debug(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, Logger.info.__name__, handle_exceptions=False)
def _common_logger_info(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._info(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, Logger.warn.__name__, handle_exceptions=False)
def _common_logger_warn(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._warn(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, Logger.error.__name__, handle_exceptions=False)
def _common_logger_error(original, self, message, *args, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._error(log_name, message, *args, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, owner=owner, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Logger, Logger.exception.__name__, handle_exceptions=False)
def _common_logger_exception(original, self, message, *args, exc=None, owner=None, **kwargs) -> Any:
    log_name = self.group
    _CommonVanillaLogOverride()._exception(log_name, message, *args, exc=exc, owner=owner or self.default_owner, **kwargs)
    return original(self, message, *args, exc=exc, owner=owner, **kwargs)
