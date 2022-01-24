"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_commands')
log.enable()


@Command('s4clib.the_mother_calls', command_type=CommandType.Live)
def _common_the_mother_calls(_connection: int=None):
    output = CheatOutput(_connection)
    try:
        output('She calls and you must listen! Who shall answer the call?')
        sim_count = 0
        # trait_Strangerville_Infected
        trait_id = 201407
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if CommonTraitUtils.has_trait(sim_info, trait_id):
                continue
            if CommonTraitUtils.add_trait(sim_info, trait_id):
                sim_count += 1
        output(f'{sim_count} Sim(s) have answered the call.')
    except Exception as ex:
        output('An error occurred while the mother was calling.')
        log.error('An error occurred while the mother was calling.', exception=ex)
    return False
