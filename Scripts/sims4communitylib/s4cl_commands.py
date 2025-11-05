"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from aspirations.aspiration_tuning import AspirationBasic
from aspirations.aspiration_types import AspriationType
from event_testing.resolver import DataResolver
from objects.game_object import GameObject
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.misc.common_fire_utils import CommonFireUtils
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
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
            if CommonFireUtils.spawn_fires_on_object(game_object):
                object_count += 1
        except:
            continue
    output(f'{object_count} Object(s) have been set ablaze. You might want to run now.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.burn_it',
    'Some Sims just want to see the world burn.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Decimal ID', 'The Decimal Identifier of the object to spawn a fire at.'),
    ),
    show_with_help_command=False
)
def _common_burn_it(output: CommonConsoleCommandOutput, game_object: GameObject):
    output(f'Do you smell smoke?')
    if not CommonFireUtils.is_fire_allowed_at_location(CommonObjectLocationUtils.get_location(game_object)):
        output(f'Fires are not allowed on the object. {game_object}.')
        return
    if CommonFireUtils.spawn_fires_on_object(game_object):
        output(f'{game_object} has been set ablaze. You might want to run now.')
    else:
        output(f'For some reason {game_object} failed to catch fire.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.trigger_burglar',
    'The time to steal is now.',
    show_with_help_command=False
)
def _common_burgle_it(output: CommonConsoleCommandOutput):
    output(f'Do you smell valuables?')
    sim_info = CommonSimUtils.get_active_sim_info()
    burglar_loot = 8288151420394453877  # S4CL_Loot_Situation_Burglar
    CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(burglar_loot, sim_info)
    output('Done, burglar will show at midnight.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_rig',
    'Print rig information for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim to attach the buff to.', is_optional=True, default_value='Active Sim'),
    ),
    show_with_help_command=False
)
def _common_burgle_it(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output(f'Printing Rig for {sim_info}')
    sim = CommonSimUtils.get_sim_instance(sim_info)
    rig_hash64 = sim.rig.hash64
    rig_instance = sim.rig.instance
    current_sim_info = sim.sim_info
    log.format_with_message('All things on rig', rig_dir=dir(sim.rig), rig64=rig_hash64, rig_instance=rig_instance, rig_key=sim_info.rig_key, current_rig_key=current_sim_info.rig_key)
    output(f'Rig Hash 64: {rig_hash64}')
    output(f'Rig Instance: {rig_instance}')
    output(f'Rig Key: {sim_info.rig_key}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.complete_objective',
    'Complete an objective for an aspiration.',
    command_arguments=(
        CommonConsoleCommandArgument('objective', 'Objective Id or Name', 'The name or instance id of a Sim to attach the buff to.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim to complete the objective for.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_complete_objective(output: CommonConsoleCommandOutput, objective: TunableInstanceParam(Types.OBJECTIVE), sim_info: SimInfo = None):
    if sim_info is None:
        output('No Sim specified')
        return
    if objective is None:
        output('No objective specified.')
        return
    output(f'Completing objective {objective} for Sim {sim_info}')
    aspiration_tracker = sim_info.aspiration_tracker
    for (key, aspiration) in CommonResourceUtils.load_all_instances(Types.ASPIRATION, return_type=AspirationBasic):
        aspiration: AspirationBasic = aspiration
        log.format_with_message(f'Checking Aspiration {aspiration}')
        # noinspection PyUnresolvedReferences
        if aspiration.aspiration_type == AspriationType.FULL_ASPIRATION and aspiration.do_not_register_events_on_load and not aspiration_tracker.aspiration_in_sequence(aspiration):
            continue
            # log.format_with_message(f'Not a full aspiration {aspiration} do not register {aspiration.do_not_register_events_on_load} ')
        else:
            for asp_objective in aspiration_tracker.get_objectives(aspiration):
                if asp_objective == objective:
                    log.format_with_message(f'Found the objective {asp_objective} on {aspiration}.')
                    aspiration_tracker.handle_event(aspiration, None, DataResolver(sim_info), debug_objectives_to_force_complete=[objective])
                # else:
                #     log.format_with_message(f'Objective not a match {asp_objective}')
    log.format_with_message('Done')
    output(f'Completed {objective} on {sim_info}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_fame_level',
    'Set the fame level of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('fame_level', 'Value 0 through 5', 'The level of fame to set the Sim to.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim to set the fame level of.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_set_fame_level(output: CommonConsoleCommandOutput, fame_level: int, sim_info: SimInfo = None):
    if not (0 <= fame_level <= 5):
        output('Fame Level must be between 0 and 5.')
        return
    output(f'Setting the fame level of {sim_info} to star level {fame_level}')
    fame_level_mapping = {
        0: 0,  # level starts at 0
        1: 462,  # level starts at 162
        2: 1037,  # level starts at 837
        3: 2117,  # level starts at 1917
        4: 3534,  # level starts at 3334
        5: 5321  # level starts at 5021
    }

    fame_level_value = fame_level_mapping.get(fame_level)
    CommonSimStatisticUtils.set_statistic_value(sim_info, CommonStatisticId.RANKED_FAME, fame_level_value)
    output('Done')
