"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
    }


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_trait_printer')
log.enable()


@Command('s4clib_dev.log_traits', command_type=CommandType.Live)
def _common_log_traits_ready_for_update(_connection: int=None) -> None:
    try:
        output = CheatOutput(_connection)
        output('Logging Traits')
        from sims4communitylib.utils.misc._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_instances(Types.TRAIT, _S4CLReaderForUpdate.CONVERSIONS, CommonTraitId, skip_not_found=True)
        output(f'Finished logging Traits. {len(not_found_values)} values were not found.')
    except Exception as ex:
        log.error('Error when logging Traits.', exception=ex)
