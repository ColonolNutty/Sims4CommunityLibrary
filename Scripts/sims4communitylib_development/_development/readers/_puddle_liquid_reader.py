"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.puddles import PuddleLiquid
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
        'GREENGOO': 'GREEN_GOO',
        'DARK MATTER': 'DARK_MATTER'
    }


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_dev.log_puddle_liquids', 'Logs a list of puddle liquids for easy transfer to CommonPuddleLiquid', show_with_help_command=False)
def _common_log_ready_for_update(output: CommonConsoleCommandOutput) -> None:
    output('Logging Puddle Liquids to Messages.txt')
    from sims4communitylib_development._development._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
    from sims4communitylib.enums.common_puddle_liquid import CommonPuddleLiquid
    not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_enum(PuddleLiquid, _S4CLReaderForUpdate.CONVERSIONS, CommonPuddleLiquid)
    output(f'Finished logging Puddle Liquids. {len(not_found_values)} values were not found.')
