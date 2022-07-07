"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.resources import Types
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
    }


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_dev.log_object_state_values', 'Logs a list of Object State Values and Object State Value ids for easy transfer to CommonObjectStateValueId', show_with_help_command=False)
def _common_log_object_state_values_ready_for_update(output: CommonConsoleCommandOutput) -> None:
    output('Logging Object State Values')
    from sims4communitylib_development._development._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
    from sims4communitylib.enums.common_object_state_value_ids import CommonObjectStateValueId
    not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_instances(Types.OBJECT_STATE, _S4CLReaderForUpdate.CONVERSIONS, CommonObjectStateValueId, skip_not_found=True)
    output(f'Finished logging Object State Values. {len(not_found_values)} values were not found.')
