"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
    }


# noinspection PyMissingOrEmptyDocstring
class CommonInstanceId(CommonInt):
    """A Fake enum used when displaying values using `s4clib_dev.log_instances`"""
    pass


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_type_printer')
log.enable()


@Command('s4clib_dev.log_instances', command_type=CommandType.Live)
def _common_log_instances_ready_for_update(type_str: str=None, _connection: int=None) -> None:
    try:
        output = CheatOutput(_connection)
        output(f'Logging {type_str}')
        if type_str is None:
            output('ERROR: No Type was specified!')
            return
        instance_type = CommonResourceUtils.get_enum_by_name(type_str.upper(), Types, default_value=None)
        if instance_type is None:
            output(f'ERROR: {type_str} is not a valid type.')
            return
        from sims4communitylib.utils.misc._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
        not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_instances(instance_type, _S4CLReaderForUpdate.CONVERSIONS, CommonInstanceId, skip_not_found=True)
        output(f'Finished logging {type_str}. {len(not_found_values)} values were not found.')
    except Exception as ex:
        log.error(f'Error when logging {type_str}.', exception=ex)
