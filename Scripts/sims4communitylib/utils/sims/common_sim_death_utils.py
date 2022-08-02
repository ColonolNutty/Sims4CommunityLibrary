"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from interactions.utils.death import DeathType, DeathTracker
from sims.ghost import Ghost
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimDeathUtils:
    """Utilities for manipulating the body of Sims.

    """
    @classmethod
    def kill_sim(cls, sim_info: SimInfo, death_type: Union[CommonDeathType, DeathType], is_off_lot_death: bool = False) -> CommonExecutionResult:
        """kill_sim(sim_info, death_type, is_off_lot_death=False)

        Kill a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param death_type: The type of death to invoke upon the Sim.
        :type death_type: Union[CommonDeathType, DeathType]
        :param is_off_lot_death: Set True to indicate the death is happening off lot. Set False to indicate the death is happening on lot. Default is False.
        :type is_off_lot_death: bool, optional
        :return:
        """
        death_tracker = cls.get_death_tracker(sim_info)
        if death_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} did not have a death tracker.')
        if death_tracker.death_type is not None:
            return CommonExecutionResult(True, reason=f'{sim_info} is already dead.')
        if death_tracker.is_ghost:
            return CommonExecutionResult(False, reason=f'{sim_info} is already a ghost.')
        death_tracker.set_death_type(death_type, is_off_lot_death=is_off_lot_death)
        Ghost.make_ghost_if_needed(sim_info)
        return CommonExecutionResult.TRUE

    @classmethod
    def revive_sim(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """revive_sim(sim_info)

        Revive a Dead Sim.

        :param sim_info:
        :return:
        """
        death_tracker = cls.get_death_tracker(sim_info)
        if death_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} did not have a death tracker.')
        if death_tracker.death_type is None:
            return CommonExecutionResult(True, reason=f'{sim_info} is not dead.')
        urn_object_id = Ghost.get_urnstone_for_sim_id(CommonSimUtils.get_sim_id(sim_info))
        death_tracker.clear_death_type()
        Ghost.remove_ghost_from_sim(sim_info)
        game_object = CommonObjectUtils.get_game_object(urn_object_id)
        CommonObjectSpawnUtils.schedule_object_for_destroy(game_object)
        return CommonExecutionResult.TRUE

    @classmethod
    def get_death_tracker(cls, sim_info: SimInfo) -> Union[DeathTracker, None]:
        """get_death_tracker(sim_info)

        Retrieve the death tracker for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The death tracker for the Sim or None if not found.
        :rtype: Union[DeathTracker, None]
        """
        if sim_info is None:
            return None
        return sim_info.death_tracker


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.kill_sim',
    'Kill a Sim with a random death.',
    command_arguments=(
        CommonConsoleCommandArgument('death_type', 'Name of Death Type', 'The type of death to bring upon a Sim.', is_optional=True, default_value='Random'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_kill_sim(output: CommonConsoleCommandOutput, death_type: CommonDeathType = CommonDeathType.NONE, sim_info: SimInfo = None):
    if death_type == CommonDeathType.NONE:
        death_type = CommonDeathType.convert_from_vanilla(DeathType.get_random_death_type())
    output(f'Killing Sim {sim_info} with death {death_type.name}.')
    result = CommonSimDeathUtils.kill_sim(sim_info, death_type)
    if result:
        output(f'Successfully killed {sim_info} with death {death_type.name}.')
    else:
        output(f'Failed to kill {sim_info} with death {death_type.name}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.kill_sim',
    'Kill a Sim with a random death.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_kill_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    death_type = CommonDeathType.convert_from_vanilla(DeathType.get_random_death_type())
    output(f'Killing Sim {sim_info} with death {death_type.name}.')
    result = CommonSimDeathUtils.kill_sim(sim_info, death_type)
    if result:
        output(f'Successfully killed {sim_info} with death {death_type.name}.')
    else:
        output(f'Failed to kill {sim_info} with death {death_type.name}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.revive_sim',
    'Revive a Sim and stop them being a ghost.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_revive_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output(f'Reviving Sim {sim_info}.')
    result = CommonSimDeathUtils.revive_sim(sim_info)
    if result:
        output(f'Successfully revived {sim_info}.')
    else:
        output(f'Failed to revive {sim_info}.')
