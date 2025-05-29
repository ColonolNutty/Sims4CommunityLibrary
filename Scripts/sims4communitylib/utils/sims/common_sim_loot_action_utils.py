"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from event_testing.resolver import SingleSimResolver, DoubleSimResolver
from interactions.utils.loot import LootActions
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.resources.common_loot_action_utils import CommonLootActionUtils


class CommonSimLootActionUtils:
    """Utilities for manipulating Loot Actions for Sims."""
    @staticmethod
    def apply_loot_actions_to_sim(loot_actions: LootActions, sim_info: SimInfo) -> bool:
        """apply_loot_actions_to_sim(loot_actions, sim_info)

        Apply loot actions to a Sim.

        :param loot_actions: The loot actions to apply.
        :type loot_actions: LootActions
        :param sim_info: The Sim to apply the loot actions to.
        :type sim_info: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return CommonLootActionUtils.apply_loot_actions_using_resolver(loot_actions, SingleSimResolver(sim_info))

    @staticmethod
    def apply_loot_actions_by_id_to_sim(loot_actions_id: int, sim_info: SimInfo) -> bool:
        """apply_loot_actions_by_id_to_sim(loot_actions_id, sim_info)

        Apply loot actions to a Sim.

        :param loot_actions_id: The decimal identifier of a loot actions instance to apply.
        :type loot_actions_id: int
        :param sim_info: The Sim to apply the loot actions to.
        :type sim_info: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return CommonLootActionUtils.apply_loot_actions_by_id_using_resolver(loot_actions_id, SingleSimResolver(sim_info))

    @staticmethod
    def apply_loot_actions_by_ids_to_sim(loot_actions_ids: Tuple[int], sim_info: SimInfo) -> bool:
        """apply_loot_actions_by_ids_to_sim(loot_actions_ids, sim_info)

        Apply loot actions to a Sim.

        :param loot_actions_ids: The decimal identifiers of the loot actions to apply.
        :type loot_actions_ids: Tuple[int]
        :param sim_info: The Sim to apply the loot actions to.
        :type sim_info: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        return CommonLootActionUtils.apply_loot_actions_by_ids_using_resolver(loot_actions_ids, SingleSimResolver(sim_info))

    @staticmethod
    def apply_loot_actions_to_duo_sims(loot_actions: LootActions, sim_info_actor: SimInfo, sim_info_target: SimInfo) -> bool:
        """apply_loot_actions_to_duo_sims(loot_actions, sim_info_actor, sim_info_target)

        Apply loot actions to two Sims at once.

        :param loot_actions: The loot actions to apply.
        :type loot_actions: LootActions
        :param sim_info_actor: The Actor Sim to apply the loot actions to.
        :type sim_info_actor: SimInfo
        :param sim_info_target: The Target Sim to apply the loot actions to.
        :type sim_info_target: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if sim_info_actor is None or sim_info_target is None:
            return False
        return CommonLootActionUtils.apply_loot_actions_using_resolver(loot_actions, DoubleSimResolver(sim_info_actor, sim_info_target))

    @staticmethod
    def apply_loot_actions_by_id_to_duo_sims(loot_actions_id: int, sim_info_actor: SimInfo, sim_info_target: SimInfo) -> bool:
        """apply_loot_actions_by_id_to_duo_sims(loot_actions_id, sim_info_actor, sim_info_target)

        Apply loot actions by decimal identifier to two Sims at once.

        :param loot_actions_id: The decimal identifier of a loot actions instance to apply.
        :type loot_actions_id: int
        :param sim_info_actor: The Actor Sim to apply the loot actions to.
        :type sim_info_actor: SimInfo
        :param sim_info_target: The Target Sim to apply the loot actions to.
        :type sim_info_target: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if sim_info_actor is None or sim_info_target is None:
            return False
        return CommonLootActionUtils.apply_loot_actions_by_id_using_resolver(loot_actions_id, DoubleSimResolver(sim_info_actor, sim_info_target))

    @staticmethod
    def apply_loot_actions_by_ids_to_duo_sims(loot_actions_ids: Tuple[int], sim_info_actor: SimInfo, sim_info_target: SimInfo) -> bool:
        """apply_loot_actions_by_id_to_duo_sims(loot_actions_ids, sim_info_actor, sim_info_target)

        Apply loot actions by decimal identifiers to two Sims at once.

        :param loot_actions_ids: The decimal identifiers of the loot actions to apply.
        :type loot_actions_ids: Tuple[int]
        :param sim_info_actor: The Actor Sim to apply the loot actions to.
        :type sim_info_actor: SimInfo
        :param sim_info_target: The Target Sim to apply the loot actions to.
        :type sim_info_target: SimInfo
        :return: True, if the loot actions applied successfully. False, if not.
        :rtype: bool
        """
        if sim_info_actor is None or sim_info_target is None:
            return False
        return CommonLootActionUtils.apply_loot_actions_by_ids_using_resolver(loot_actions_ids, DoubleSimResolver(sim_info_actor, sim_info_target))


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.apply_loot_action',
    'Apply a loot action to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('loot_action_id', 'Loot Action Id', 'The Id of the Loot Action to apply to a Sim.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to apply the Loot Action to.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_apply_loot_action_to_sim(output: CommonConsoleCommandOutput, loot_action_id: int, sim_info: SimInfo = None):
    if loot_action_id is None or not isinstance(loot_action_id, int):
        output(f'Invalid loot_action_id specified. You specified "{loot_action_id}".')
        return
    output(f'Applying Loot Action {loot_action_id} to Sim {sim_info}')
    result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(loot_action_id, sim_info)
    if result:
        output('Success')
    else:
        loot_actions = CommonLootActionUtils.load_loot_actions_by_id(loot_action_id)
        if loot_actions is None:
            output(f'Failed, no loot action found with id {loot_action_id}')
            return
        output('Failed')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.apply_duo_loot_action',
    'Apply a loot action that uses two Sims.',
    command_arguments=(
        CommonConsoleCommandArgument('loot_action_id', 'Loot Action Id', 'The Id of the Loot Action to apply to a Sim.'),
        CommonConsoleCommandArgument('target_sim_info', 'Sim Id or Name', 'The Sim to apply the Loot Action to.'),
        CommonConsoleCommandArgument('source_sim_info', 'Sim Id or Name', 'The Sim to apply the Loot Action to.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_apply_loot_action_to_sim(output: CommonConsoleCommandOutput, loot_action_id: int, target_sim_info: SimInfo, source_sim_info: SimInfo = None):
    if loot_action_id is None or not isinstance(loot_action_id, int):
        output(f'Invalid loot_action_id specified. You specified "{loot_action_id}".')
        return
    output(f'Applying Loot Action {loot_action_id} to Sim {source_sim_info} toward {target_sim_info}')
    result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_duo_sims(loot_action_id, source_sim_info, target_sim_info)
    if result:
        output('Success')
    else:
        loot_actions = CommonLootActionUtils.load_loot_actions_by_id(loot_action_id)
        if loot_actions is None:
            output(f'Failed, no loot action found with id {loot_action_id}')
            return
        output('Failed')
