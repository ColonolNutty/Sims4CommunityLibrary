"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.enable_log',
    'Enable a log. Once enabled, any code that uses the functions of the log will starting logging their messages to "The Sims 4/mod_logs/modname_Messages.txt"',
    command_arguments=(
        CommonConsoleCommandArgument('log_name', 'Text', 'The name of a log to enable.'),
        CommonConsoleCommandArgument('mod_name', 'Text', 'The name of the mod to enable the log for. If a log is not available for a mod, but you know it exists, specify this argument to enable it without having to wait for the log itself to be used in the code first. If not specified, then the log will be enabled for all mods.', is_optional=True, default_value='All Mods'),
    ),
    command_aliases=(
        's4clib.enablelog',
    )
)
def _common_command_enable_log(output: CommonConsoleCommandOutput, log_name: str, mod_name: str=None):
    if log_name is None:
        output('ERROR: No log name specified (See all logs via "s4clib.logs" command)')
        return
    if mod_name is None:
        output(f'Attempting to enable log \'{log_name}\'.')
    else:
        output(f'Attempting to enable log \'{log_name}\' for mod \'{mod_name}\'.')
    if CommonLogRegistry.get().log_exists(log_name, mod_identifier=mod_name) or mod_name is not None:
        if CommonLogRegistry.get().enable_logs(log_name, mod_identifier=mod_name):
            if mod_name is None:
                output(f'SUCCESS: Log \'{log_name}\' was successfully enabled.')
            else:
                output(f'SUCCESS: Log \'{log_name}\' was successfully enabled for mod \'{mod_name}\'.')
        else:
            if mod_name is None:
                output(f'FAILED: Failed to enable log \'{log_name}\'. Do you need to specify a mod name?')
            else:
                output(f'FAILED: Failed to enable log \'{log_name}\' for mod \'{mod_name}\'.')
    else:
        if mod_name is None:
            output(f'ERROR: No log found with name \'{log_name}\'.')
        else:
            output(f'ERROR: No log found with name \'{log_name}\' for mod \'{mod_name}\'.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.disable_log',
    'Disable a log. Once disabled, any code that uses the functions of the log will stop logging their messages to "The Sims 4/mod_logs/modname_Messages.txt"',
    command_arguments=(
        CommonConsoleCommandArgument('log_name', 'Text', 'The name of a log to disable.'),
        CommonConsoleCommandArgument('mod_name', 'Text', 'The name of the mod to disable the log for. If not specified, then the log will be disabled for all mods.', is_optional=True, default_value='All Mods'),
    ),
    command_aliases=(
        's4clib.disablelog',
    )
)
def _common_command_disable_log(output: CommonConsoleCommandOutput, log_name: str, mod_name: str=None):
    if log_name is None:
        output('specify a log name (See all logs via "s4clib.logs" command)')
        return
    if mod_name is None:
        output(f'Attempting to disable log \'{log_name}\'.')
    else:
        output(f'Attempting to disable log \'{log_name}\' for mod \'{mod_name}\'.')
    if CommonLogRegistry().log_exists(log_name, mod_identifier=mod_name):
        if CommonLogRegistry().disable_logs(log_name, mod_identifier=mod_name):
            if mod_name is None:
                output(f'SUCCESS: Log \'{log_name}\' was successfully disabled.')
            else:
                output(f'SUCCESS: Log \'{log_name}\' was successfully disabled for mod \'{mod_name}\'.')
        else:
            if mod_name is None:
                output(f'Failed to disable log \'{log_name}\'. Do you need to specify a mod name?')
            else:
                output(f'Failed to disable log \'{log_name}\' for mod \'{mod_name}\'.')
    else:
        if mod_name is None:
            output(f'ERROR: Log \'{log_name}\' did not exist.')
        else:
            output(f'ERROR: Log \'{log_name}\' did not exist for mod \'{mod_name}\'.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.disable_all_logs',
    'Disable all logs.',
    command_arguments=(
        CommonConsoleCommandArgument('mod_name', 'Text', 'The name of the mod to disable logs for. If not specified, then logs will be disabled for all mods.', is_optional=True, default_value='All Mods'),
    ),
    command_aliases=(
        's4clib.disablealllogs',
    )
)
def _common_command_disable_all_logs(output: CommonConsoleCommandOutput, mod_name: str=None):
    if mod_name is None:
        output('Disabling all logs.')
    else:
        output(f'Disabling all logs for mod \'{mod_name}\'.')
    CommonLogRegistry.get().disable_all_logs(mod_identifier=mod_name)
    if mod_name is None:
        output(f'SUCCESS: All logs successfully disabled.')
    else:
        output(f'SUCCESS: All logs for mod \'{mod_name}\' successfully disabled.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.enablealllogs',
    'Enable all logs.',
    command_arguments=(
        CommonConsoleCommandArgument('mod_name', 'Text', 'The name of the mod to enable logs for. If not specified, then logs will be enabled for all mods.', is_optional=True, default_value='All Mods'),
    ),
    command_aliases=(
        's4clib.enablealllogs',
    )
)
def _common_command_enable_all_logs(output: CommonConsoleCommandOutput, mod_name: str=None):
    if mod_name is None:
        output(f'Attempting to enable all logs.')
    else:
        output(f'Attempting to enable log for mod \'{mod_name}\'.')
    CommonLogRegistry.get().enable_all_logs(mod_identifier=mod_name)
    if mod_name is None:
        output(f'SUCCESS: All logs successfully enabled.')
    else:
        output(f'SUCCESS: All logs for mod \'{mod_name}\' successfully enabled.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.logs',
    'Print a list of all available logs.',
    command_arguments=(
        CommonConsoleCommandArgument('mod_name', 'Text', 'If specified, all logs related to the specified mod will be listed. If not specified, all logs will be listed.', is_optional=True, default_value=None),
    )
)
def _common_command_show_all_logs(output: CommonConsoleCommandOutput, mod_name: str=None):
    log_names = CommonLogRegistry.get().get_registered_log_names(mod_identifier=mod_name)
    if log_names is None:
        return
    if not log_names:
        if mod_name is None:
            output(f'FAILED: No mods have registered any logs')
        else:
            output(f'FAILED: \'{mod_name} has not registered any logs')
        return
    for log_name in log_names:
        output(str(log_name))
