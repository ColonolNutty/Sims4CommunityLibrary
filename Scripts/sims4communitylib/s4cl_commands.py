"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from services.fire_service import FireService
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_commands')
log.enable()


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.the_mother_calls', 'Invokes the mothers call.', show_with_help_command=False)
def _common_the_mother_calls(output: CommonConsoleCommandOutput):
    output('She calls and you must listen! Who shall answer the call?')
    sim_count = 0
    # trait_Strangerville_Infected
    trait_id = 201407
    output(f'The call has begun, who shall answer it?')
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        if CommonTraitUtils.has_trait(sim_info, trait_id):
            continue
        if CommonTraitUtils.add_trait(sim_info, trait_id):
            sim_count += 1
    output(f'{sim_count} Sim(s) have answered the call.')


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.come_to_me_now', 'Formally request all objects in the area to come to the active Sim.', show_with_help_command=False)
def _common_come_to_me_now(output: CommonConsoleCommandOutput):
    sim_info = CommonSimUtils.get_active_sim_info()
    new_location = CommonSimLocationUtils.get_location(sim_info)
    object_count = 0
    output(f'Attempting to request all objects to come to {sim_info}.')
    for game_object in CommonObjectUtils.get_instance_for_all_game_objects_generator():
        # noinspection PyBroadException
        try:
            CommonObjectLocationUtils.set_location(game_object, new_location)
            object_count += 1
        except:
            continue
    output(f'{object_count} Object(s) came to {sim_info}.')


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.burn_it_all', 'Some Sims just want to see the world burn.', show_with_help_command=False)
def _common_burn_it_all(output: CommonConsoleCommandOutput):
    object_count = 0
    output(f'Do you smell smoke?')
    for game_object in CommonObjectUtils.get_instance_for_all_game_objects_generator():
        # noinspection PyBroadException
        try:
            fire_service: FireService = services.get_fire_service()
            fire_service.spawn_fire_at_object(game_object)
            object_count += 1
        except:
            continue
    output(f'{object_count} Object(s) have been set ablaze. You might want to run now.')
