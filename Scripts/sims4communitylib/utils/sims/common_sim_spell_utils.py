"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple

from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from spells.spells import Spell


class CommonSimSpellUtils:
    """Utilities for unlocking and locking things, usually learned things such as Spells. """
    @classmethod
    def add_spell(cls, sim_info: SimInfo, spell: Union[int, Spell], mark_as_new: bool = True) -> CommonExecutionResult:
        """add_spell(sim_info, spell, mark_as_new=True)

        Make a Sim learn a Spell.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param spell: The spell to add.
        :type spell: Union[int, Spell]
        :param mark_as_new: Set True to mark the Spell as being new. Set False to refrain from marking the spell as new. Default is True.
        :type mark_as_new: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.add_spells(sim_info, (spell,), mark_as_new=mark_as_new)

    @classmethod
    def add_spells(cls, sim_info: SimInfo, spells: Tuple[Union[int, Spell]], mark_as_new: bool = True) -> CommonExecutionResult:
        """add_spells(sim_info, spells, mark_as_new=True)

        Make a Sim learn Spells.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param spells: A collection of spells to add.
        :type spells: Tuple[Union[int, Spell]]
        :param mark_as_new: Set True to mark the Spells as being new. Set False to refrain from marking the spells as new. Default is True.
        :type mark_as_new: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_sim_unlock_utils import CommonSimUnlockUtils
        unlock_tracker = CommonSimUnlockUtils.get_unlock_tracker(sim_info)
        if unlock_tracker is None:
            return CommonExecutionResult(False, reason=f'Failed to locate the unlock tracker for {sim_info}', hide_tooltip=True)
        for spell in spells:
            spell_id = spell
            spell = cls.load_spell_by_id(spell)
            if spell is None:
                return CommonExecutionResult(False, reason=f'Spell not found by id {spell_id}.', hide_tooltip=True)
            unlock_tracker.add_unlock(spell, None, mark_as_new=mark_as_new)
        return CommonExecutionResult.TRUE

    @classmethod
    def add_all_spells(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_all_spells(sim_info)

        Make a Sim learn all Spells.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_sim_unlock_utils import CommonSimUnlockUtils
        unlock_tracker = CommonSimUnlockUtils.get_unlock_tracker(sim_info)
        if unlock_tracker is None:
            return CommonExecutionResult(False, reason=f'Failed to locate the unlock tracker for {sim_info}', hide_tooltip=True)
        spells: Tuple[Spell] = tuple(CommonResourceUtils.load_all_instance_values(Types.SPELL, return_type=Spell))
        return cls.add_spells(sim_info, spells)

    @classmethod
    def remove_spell(cls, sim_info: SimInfo, spell: Union[int, Spell]) -> CommonExecutionResult:
        """remove_spell(sim_info, spell)

        Make a Sim unlearn a Spell.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param spell: The spell to remove.
        :type spell: Union[int, Spell]
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.remove_spells(sim_info, (spell,))

    @classmethod
    def remove_spells(cls, sim_info: SimInfo, spells: Tuple[Union[int, Spell]]) -> CommonExecutionResult:
        """remove_spells(sim_info, spells)

        Make a Sim unlearn Spells.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param spells: A collection of spells to remove.
        :type spells: Tuple[Union[int, Spell]]
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_sim_unlock_utils import CommonSimUnlockUtils
        unlock_tracker = CommonSimUnlockUtils.get_unlock_tracker(sim_info)
        if unlock_tracker is None:
            return CommonExecutionResult(False, reason=f'Failed to locate the unlock tracker for {sim_info}', hide_tooltip=True)
        for spell in spells:
            spell_id = spell
            spell = cls.load_spell_by_id(spell)
            if spell is None:
                return CommonExecutionResult(False, reason=f'Spell not found by id {spell_id}.', hide_tooltip=True)
            found_unlock = None
            for unlock in unlock_tracker._unlocks:
                if unlock.tuning_class == spell:
                    found_unlock = unlock
                    break
            if not found_unlock:
                return CommonExecutionResult(False, reason=f'{sim_info} did not have spell {spell} unlocked.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_KNOW_SPELL, tooltip_tokens=(sim_info, str(spell)))
            unlock_tracker._unlocks.remove(found_unlock)
            if spell in unlock_tracker._marked_new_unlocks:
                unlock_tracker._marked_new_unlocks.remove(spell)
            (provided_super_affordances, provided_target_affordances) = unlock_tracker._get_provided_super_affordances_from_unlock(spell)
            if provided_super_affordances:
                if unlock_tracker._super_affordances_cache is not None:
                    for provided_super_affordance in provided_super_affordances:
                        if provided_super_affordance in unlock_tracker._super_affordances_cache:
                            unlock_tracker._super_affordances_cache.remove(provided_super_affordance)
            if provided_target_affordances:
                if unlock_tracker._target_provided_affordances_cache is not None:
                    for provided_target_affordance in provided_target_affordances:
                        if provided_target_affordance in unlock_tracker._target_provided_affordances_cache:
                            unlock_tracker._target_provided_affordances_cache.remove(provided_target_affordance)
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_all_spells(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_all_spells(sim_info)

        Make a Sim unlearn all Spells.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_sim_unlock_utils import CommonSimUnlockUtils
        unlock_tracker = CommonSimUnlockUtils.get_unlock_tracker(sim_info)
        if unlock_tracker is None:
            return CommonExecutionResult(False, reason=f'Failed to locate the unlock tracker for {sim_info}', hide_tooltip=True)
        spells: Tuple[Spell] = tuple(CommonResourceUtils.load_all_instance_values(Types.SPELL, return_type=Spell))
        return cls.remove_spells(sim_info, spells)

    @classmethod
    def load_spell_by_id(cls, spell: Union[int, Spell]) -> Union[Spell, None]:
        """load_spell_by_id(spell)

        Load an instance of a Spell by its decimal identifier.

        :param spell: The identifier of a Spell.
        :type spell: Union[int, CommonSpellId, Spell]
        :return: An instance of a Spell matching the decimal identifier or None if not found.
        :rtype: Union[Spell, None]
        """
        if isinstance(spell, Spell):
            return spell
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            spell_instance = spell()
            if isinstance(spell_instance, Spell):
                # noinspection PyTypeChecker
                return spell
        except:
            pass
        # noinspection PyBroadException
        try:
            spell: int = int(spell)
        except:
            # noinspection PyTypeChecker
            spell: Spell = spell
            return spell

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.SPELL, spell)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_spell',
    'Add a Spell to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('spell', 'Spell Id or Tuning Name', 'The decimal identifier or name of a spell to add.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.unlock_spell',
        's4clib.learn_spell',
    )
)
def _common_add_spell(
    output: CommonConsoleCommandOutput,
    spell: TunableInstanceParam(Types.SPELL),
    sim_info: SimInfo = None
):
    output(f'Adding spell {spell} to Sim {sim_info}')
    result = CommonSimSpellUtils.add_spell(sim_info, spell)
    if result:
        output(f'Successfully added spell {spell} to Sim {sim_info}')
    else:
        output(f'Failed to add spell {spell} to Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_spell',
    'Remove a Spell from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('spell', 'Spell Id or Tuning Name', 'The decimal identifier or name of a spell to remove.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.lock_spell',
        's4clib.unlearn_spell',
    )
)
def _common_add_spell(
    output: CommonConsoleCommandOutput,
    spell: TunableInstanceParam(Types.SPELL),
    sim_info: SimInfo = None
):
    output(f'Removing spell {spell} from Sim {sim_info}')
    result = CommonSimSpellUtils.remove_spell(sim_info, spell)
    if result:
        output(f'Successfully removed spell {spell} from Sim {sim_info}')
    else:
        output(f'Failed to remove spell {spell} from Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_all_spells',
    'Add all Spells to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.add_spells',
        's4clib.unlock_all_spells',
        's4clib.learn_spells',
    )
)
def _common_add_all_spells(
    output: CommonConsoleCommandOutput,
    sim_info: SimInfo = None
):
    output(f'Removing all spells to Sim {sim_info}')
    result = CommonSimSpellUtils.add_all_spells(sim_info)
    if result:
        output(f'Successfully added all spells to Sim {sim_info}')
    else:
        output(f'Failed to add all spells to Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_all_spells',
    'Remove all Spells from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.remove_spells',
        's4clib.lock_all_spells',
        's4clib.unlearn_all_spells',
    )
)
def _common_remove_all_spells(
    output: CommonConsoleCommandOutput,
    sim_info: SimInfo = None
):
    output(f'Removing all spells from Sim {sim_info}')
    result = CommonSimSpellUtils.remove_all_spells(sim_info)
    if result:
        output(f'Successfully removed all spells from Sim {sim_info}')
    else:
        output(f'Failed to remove all spells from Sim {sim_info}. Reason: {result.reason}')
