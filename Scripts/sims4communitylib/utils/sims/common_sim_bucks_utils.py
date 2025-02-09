"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

from bucks.bucks_enums import BucksType
from bucks.bucks_perk import BucksPerk
from bucks.bucks_tracker import BucksTrackerBase
from bucks.bucks_utils import BucksUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_bucks_types import CommonBucksType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimBucksUtils:
    """Utilities for bucks. """
    @classmethod
    def add_all_perks(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType], no_cost: bool = True, **__) -> CommonExecutionResult:
        """remove_all_perks(sim_info, bucks_type, refund_cost=True, **__)

        Add all Perks of a specified Bucks type to a Sim.

        .. note:: A Sim needs to be spawned before their perks can be added.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perks being added.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :param no_cost: Set True to unlock the perk without spending perk points. Set False to spend perk points to unlock the perk.. Default is False
        :type no_cost: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before all of their perks can be locked.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        for perk in cls.get_locked_perks_gen(sim_info, bucks_type):
            if cls.has_perk_unlocked(sim_info, perk):
                return CommonExecutionResult(True, reason=f'Perk {perk} is already unlocked.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERK_UNLOCKED, tooltip_tokens=(sim_info, str(perk)))
            perk = cls.load_perk_by_guid(perk)
            if perk is None:
                return CommonExecutionResult(False, reason=f'Failed to locate perk by id {perk}', hide_tooltip=True)
            modified_for_cost = False
            if no_cost:
                if not cls.can_afford_perk(sim_info, perk):
                    unlock_cost = cls.get_perk_unlock_cost(perk)
                    modify_result = cls.modify_bucks(sim_info, bucks_type, unlock_cost, reason='Perk being unlocked at no cost.')
                    if not modify_result:
                        return modify_result
                    modified_for_cost = True
            elif not cls.can_afford_perk(sim_info, perk):
                continue
            if bucks_tracker.pay_for_and_unlock_perk(perk):
                if not modified_for_cost:
                    unlock_cost = cls.get_perk_unlock_cost(perk)
                    modify_result = cls.modify_bucks(sim_info, bucks_type, unlock_cost, reason='Perk being unlocked at no cost.')
                    if not modify_result:
                        return modify_result
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_all_perks(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType], refund_cost: bool = True, reason: str = None, remove_perk_points: bool = False, **__) -> CommonExecutionResult:
        """remove_all_perks(sim_info, bucks_type, refund_cost=True, reason=None, remove_perk_points=False, **__)

        Remove all Perks of a specified Bucks type from a Sim.

        .. note:: A Sim needs to be spawned before their perks can be removed.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perks being removed.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :param refund_cost: Set True to refund the cost of all unlocked perks. Set False to give no perk points back. Default is True
        :type refund_cost: bool, optional
        :param reason: The reason the perks are being removed. Default is None.
        :type reason: str, optional
        :param remove_perk_points: Set True to remove all perk points in addition to all the perks. Set False to remove only the perks. If this is True, refund_cost will be ignored. Default is False.
        :type remove_perk_points: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before all of their perks can be removed.', hide_tooltip=True)
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return CommonExecutionResult(False, reason=f'Bucks Type {bucks_type} was not valid.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=False)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        bucks_tracker.lock_all_perks(vanilla_bucks_type, refund_cost=refund_cost or remove_perk_points)
        if remove_perk_points:
            cls.set_bucks(sim_info, bucks_type, 0, reason=reason, **__)
        return CommonExecutionResult.TRUE

    @classmethod
    def lock_all_perks(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType], refund_cost: bool = True) -> CommonExecutionResult:
        """lock_all_perks(sim_info, bucks_type, refund_cost=True)

        Lock all perks of a specific Bucks type for a Sim.

        .. note:: A Sim needs to be spawned before their perks can be locked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perks being locked.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :param refund_cost: Set True to refund the cost of all unlocked perks. Set False to give no perk points back. Default is True
        :type refund_cost: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before all of their perks can be locked.', hide_tooltip=True)
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return CommonExecutionResult(False, reason=f'Bucks Type {bucks_type} was not valid.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        bucks_tracker.lock_all_perks(vanilla_bucks_type, refund_cost=refund_cost)
        return CommonExecutionResult.TRUE

    @classmethod
    def has_perk_unlocked(cls, sim_info: SimInfo, perk: Union[BucksPerk, int]) -> CommonTestResult:
        """has_perk_unlocked(sim_info, perk)

        Determine if a Sim has a perk unlocked.

        .. note:: A Sim needs to be spawned to check this.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param perk: The perk to lock.
        :type perk: Union[BucksPerk, int]
        :return: The result of the test. True, if the test passed. False, if the test failed.
        :rtype: CommonTestResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonTestResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before any of their perks can be unlocked.', hide_tooltip=True)
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return CommonTestResult(False, reason=f'Failed to locate perk by id {perk}', hide_tooltip=True)
        bucks_type = cls.get_perk_bucks_type(perk)
        if bucks_type is None:
            return CommonTestResult(False, reason=f'Perk {perk} had no Bucks Type specified.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonTestResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        if bucks_tracker.is_perk_unlocked(perk):
            return CommonTestResult(True, reason=f'{sim_info} has perk {perk} unlocked.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERK_UNLOCKED, tooltip_tokens=(sim_info, str(perk)))
        return CommonTestResult(False, reason=f'{sim_info} does not have perk {perk} unlocked.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERK_UNLOCKED, tooltip_tokens=(sim_info, str(perk)))

    @classmethod
    def has_perk_locked(cls, sim_info: SimInfo, perk: Union[BucksPerk, int]) -> CommonTestResult:
        """has_perk_locked(sim_info, perk)

        Determine if a Sim has a perk locked.

        .. note:: The Sim being checked needs to be spawned.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param perk: The perk to check.
        :type perk: Union[BucksPerk, int]
        :return: The result of the test. True, if the test passed. False, if the test failed.
        :rtype: CommonTestResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonTestResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before any of their perks can be locked.', hide_tooltip=True)
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return CommonTestResult(False, reason=f'Failed to locate perk by id {perk}', hide_tooltip=True)
        bucks_type = cls.get_perk_bucks_type(perk)
        if bucks_type is None:
            return CommonTestResult(False, reason=f'Perk {perk} had no Bucks Type specified.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonTestResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        if not bucks_tracker.is_perk_unlocked(perk):
            return CommonTestResult(True, reason=f'{sim_info} has perk {perk} locked.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERK_LOCKED, tooltip_tokens=(sim_info, str(perk)))
        return CommonTestResult(False, reason=f'{sim_info} does not have perk {perk} locked.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERK_LOCKED, tooltip_tokens=(sim_info, str(perk)))

    @classmethod
    def lock_perk(cls, sim_info: SimInfo, perk: Union[BucksPerk, int], refund_cost: bool = True) -> CommonExecutionResult:
        """lock_perk(sim_info, perk, refund_cost=True)

        Lock a perk for a Sim.

        .. note:: A Sim needs to be spawned before their perks can be locked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param perk: The perk to lock.
        :type perk: Union[BucksPerk, int]
        :param refund_cost: Set True to refund the cost of the perk. Set False to give no perk points back. Default is True
        :type refund_cost: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before all of their perks can be locked.', hide_tooltip=True)
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return CommonExecutionResult(False, reason=f'Failed to locate perk by id {perk}', hide_tooltip=True)
        bucks_type = cls.get_perk_bucks_type(perk)
        if bucks_type is None:
            return CommonExecutionResult(False, reason=f'Perk {perk} had no Bucks Type specified.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        bucks_tracker.lock_perk(perk, refund_cost=refund_cost)
        return CommonExecutionResult.TRUE

    @classmethod
    def unlock_perk(cls, sim_info: SimInfo, perk: Union[BucksPerk, int], no_cost: bool = False) -> CommonExecutionResult:
        """unlock_perk(sim_info, perk, no_cost=True)

        Unlock a perk.

        .. note:: A Sim needs to be spawned before their perks can be unlocked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param perk: The perk to lock.
        :type perk: Union[BucksPerk, int]
        :param no_cost: Set True to unlock the perk without spending perk points. Set False to spend perk points to unlock the perk.. Default is False
        :type no_cost: bool, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if cls.has_perk_unlocked(sim_info, perk):
            return CommonExecutionResult(True, reason=f'Perk {perk} is already unlocked.', hide_tooltip=True)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before all of their perks can be locked.', hide_tooltip=True)
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return CommonExecutionResult(False, reason=f'Failed to locate perk by id {perk}', hide_tooltip=True)
        bucks_type = cls.get_perk_bucks_type(perk)
        if bucks_type is None:
            return CommonExecutionResult(False, reason=f'Perk {perk} had no Bucks Type specified.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        if cls.has_perk_unlocked(sim_info, perk):
            return CommonExecutionResult(True, reason=f'Perk {perk} is already unlocked.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERK_UNLOCKED, tooltip_tokens=(sim_info, str(perk)))
        modified_for_cost = False
        if no_cost:
            if not cls.can_afford_perk(sim_info, perk):
                unlock_cost = cls.get_perk_unlock_cost(perk)
                modify_result = cls.modify_bucks(sim_info, bucks_type, unlock_cost, reason='Perk being unlocked at no cost.')
                if not modify_result:
                    return modify_result
                modified_for_cost = True
        elif not cls.can_afford_perk(sim_info, perk):
            return CommonExecutionResult(False, reason=f'{sim_info} cannot afford perk {perk}.', tooltip_text=CommonStringId.S4CL_SIM_CANNOT_AFFORD_PERK, tooltip_tokens=(sim_info, str(perk)))
        if bucks_tracker.pay_for_and_unlock_perk(perk):
            if not modified_for_cost:
                unlock_cost = cls.get_perk_unlock_cost(perk)
                modify_result = cls.modify_bucks(sim_info, bucks_type, unlock_cost, reason='Perk being unlocked at no cost.')
                if not modify_result:
                    return modify_result
        return CommonExecutionResult.TRUE

    @classmethod
    def can_afford_perk(cls, sim_info: SimInfo, perk: Union[BucksPerk, int]) -> CommonTestResult:
        """can_afford_perk(sim_info, perk)

        Determine if a Sim can afford to purchase a perk.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param perk: The perk to check.
        :type perk: Union[BucksPerk, int]
        :return: The result of the test. True, if the perk can be afforded by the Sim. False, if not.
        :rtype: CommonTestResult
        """
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return CommonTestResult(False, reason=f'Failed to locate perk by id {perk}', hide_tooltip=True)
        bucks_type = cls.get_perk_bucks_type(perk)
        if bucks_type == CommonBucksType.INVALID:
            return CommonTestResult(False, reason=f'Perk {perk} had no Bucks Type specified.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=False)
        if bucks_tracker is None:
            return CommonTestResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        bucks_amount = cls.get_bucks_amount(sim_info, bucks_type)
        perk_cost = cls.get_perk_unlock_cost(perk)
        if bucks_amount < perk_cost:
            return CommonTestResult(False, reason=f'{sim_info} cannot afford perk {perk}.', tooltip_text=CommonStringId.S4CL_SIM_CANNOT_AFFORD_PERK, tooltip_tokens=(sim_info, str(perk)))
        return CommonTestResult(True, reason=f'{sim_info} can afford perk {perk}.', tooltip_text=CommonStringId.S4CL_SIM_CAN_AFFORD_PERK, tooltip_tokens=(sim_info, str(perk)))

    @classmethod
    def get_available_perks_gen(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType]) -> Iterator[BucksPerk]:
        """get_available_perks_gen(sim_info, bucks_type)

        Retrieve all available Perks for the specified Bucks Type and Sim.

        .. note:: A Sim needs to be spawned before perks can be checked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perks being returned.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :return: An iterator of Bucks Perks available to a Sim, regardless of locked status.
        :rtype: Iterator[BucksPerk]
        """
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return tuple()
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return tuple()
        yield from bucks_tracker.all_perks_of_type_gen(vanilla_bucks_type)

    @classmethod
    def get_locked_perks_gen(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType]) -> Iterator[BucksPerk]:
        """get_locked_perks_gen(sim_info, bucks_type)

        Retrieve all Perks for the specified Bucks Type a Sim has locked.

        .. note:: A Sim needs to be spawned before perks can be checked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perks being returned.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :return: An iterator of Bucks Perks that are locked for a Sim.
        :rtype: Iterator[BucksPerk]
        """
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return tuple()
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return tuple()
        yield from bucks_tracker.all_perks_of_type_with_lock_state_gen(vanilla_bucks_type, True)

    @classmethod
    def get_unlocked_perks_gen(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType]) -> Iterator[BucksPerk]:
        """get_unlocked_perks_gen(sim_info, bucks_type)

        Retrieve all Perks for the specified Bucks Type a Sim has unlocked.

        .. note:: A Sim needs to be spawned before perks can be checked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perks being returned.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :return: An iterator of Bucks Perks that are unlocked for a Sim.
        :rtype: Iterator[BucksPerk]
        """
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return tuple()
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return tuple()
        yield from bucks_tracker.all_perks_of_type_with_lock_state_gen(vanilla_bucks_type, False)

    @classmethod
    def get_bucks_amount(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType]) -> int:
        """get_bucks_amount(sim_info, bucks_type)

        Retrieve the number of available bucks to a Sim.

        .. note:: A Sim needs to be spawned before bucks can be checked.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the amount to return.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :return: The number of available bucks to a Sim for the specified Bucks Type or 0 if the Sim is not spawned, the bucks type does not exist, or a bucks tracker is not found.
        :rtype: int
        """
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return 0
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=False)
        if bucks_tracker is None:
            return 0
        return bucks_tracker.get_bucks_amount_for_type(vanilla_bucks_type)

    @classmethod
    def modify_bucks(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType], amount: int, reason: str = None, **__) -> CommonExecutionResult:
        """modify_bucks(sim_info, bucks_type, amount, reason=None, **__)

        Modify the number of points available for a specific Bucks Type.

        .. note:: A Sim needs to be spawned before their Bucks can be modified.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perk points.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :param amount: The amount of points that will be added/removed from the Sim.
        :type amount: int
        :param reason: The reason the perk points are being modified. Default is None.
        :type reason: str, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before their perk points can be modified.', hide_tooltip=True)
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return CommonExecutionResult(False, reason=f'Bucks Type {bucks_type} was not valid.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        current_bucks_count = cls.get_bucks_amount(sim_info, bucks_type)
        if amount < 0 and ((amount * -1) > current_bucks_count):
            amount = -current_bucks_count
        bucks_tracker.try_modify_bucks(vanilla_bucks_type, amount, reason=reason, **__)
        return CommonExecutionResult.TRUE

    @classmethod
    def set_bucks(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType], amount: int, reason: str = None, **__) -> CommonExecutionResult:
        """set_bucks(sim_info, bucks_type, amount, reason=None, **__)

        Set the amount of Bucks available to a Sim.

        .. note:: A Sim needs to be spawned before their Bucks can be modified.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The Bucks associated with the perk points.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :param amount: The amount of points that will be available to the Sim. The value should be at or above zero.
        :type amount: int
        :param reason: The reason the perk points are being modified. Default is None.
        :type reason: str, optional
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonExecutionResult(False, reason=f'{sim_info} is not currently spawned. They need to be spawned before their perk points can be modified.', hide_tooltip=True)
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return CommonExecutionResult(False, reason=f'Bucks Type {bucks_type} was not valid.', hide_tooltip=True)
        bucks_tracker: BucksTrackerBase = cls.get_bucks_tracker(sim_info, bucks_type, add_if_none=True)
        if bucks_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} does not have a tracker for the specified bucks. {bucks_type}', hide_tooltip=True)
        if amount < 0:
            amount = 0
        current_bucks_amount = cls.get_bucks_amount(sim_info, bucks_type)
        if current_bucks_amount > 0:
            bucks_tracker.try_modify_bucks(vanilla_bucks_type, -current_bucks_amount, reason=reason)
        bucks_tracker.try_modify_bucks(vanilla_bucks_type, amount, reason=reason, **__)
        return CommonExecutionResult.TRUE

    @classmethod
    def get_perk_unlock_cost(cls, perk: Union[BucksPerk, int]) -> int:
        """get_perk_unlock_cost(sim_info, perk)

        Retrieve the amount of points a perk costs to unlock.

        :param perk: The identifier or instance of a Perk.
        :type perk: Union[BucksPerk, int]
        :return: The amount of points the perk costs to unlock.
        :rtype: int
        """
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return 0
        if hasattr(perk, 'unlock_cost'):
            return perk.unlock_cost
        return 0

    @classmethod
    def get_perk_bucks_type(cls, perk: Union[BucksPerk, int]) -> CommonBucksType:
        """get_perk_bucks_type(sim_info, perk)

        Retrieve the Bucks Type associated with a Perk.

        :param perk: The identifier or instance of a Perk.
        :type perk: Union[BucksPerk, int]
        :return: The type of bucks the perk is associated to.
        :rtype: CommonBucksType
        """
        perk = cls.load_perk_by_guid(perk)
        if perk is None:
            return CommonBucksType.INVALID
        if hasattr(perk, 'associated_bucks_type'):
            return CommonBucksType.convert_from_vanilla(perk.associated_bucks_type)
        return CommonBucksType.INVALID

    @classmethod
    def get_bucks_tracker(cls, sim_info: SimInfo, bucks_type: Union[CommonBucksType, BucksType], add_if_none: bool = False) -> Union[BucksTrackerBase, None]:
        """get_bucks_tracker(sim_info, bucks_type, add_if_none=False)

        Retrieve the tracker on a Sim for a specified bucks type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param bucks_type: The type of tracker to retrieve.
        :type bucks_type: Union[CommonBucksType, BucksType]
        :param add_if_none: Set True, to add the tracker to the Sim when it does not exist. Set False to only return the tracker if it exists. Default is False.
        :type add_if_none: bool, optional
        :return: The tracker on the Sim associated with the specified Bucks Type or None when not found.
        :rtype: Union[BucksTrackerBase, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
        if vanilla_bucks_type is None:
            return None
        return BucksUtils.get_tracker_for_bucks_type(vanilla_bucks_type, owner_id=sim.id, add_if_none=add_if_none)

    @classmethod
    def load_perk_by_guid(cls, perk: Union[int, BucksPerk]) -> Union[BucksPerk, None]:
        """load_perk_by_guid(perk)

        Load an instance of a Bucks Perk by its GUID.

        :param perk: The decimal identifier of a Bucks Perk.
        :type perk: Union[int, BucksPerk]
        :return: An instance of a Bucks Perk matching the decimal identifier or None if not found.
        :rtype: Union[BucksPerk, None]
        """
        if isinstance(perk, BucksPerk):
            return perk
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            perk_instance = perk()
            if isinstance(perk_instance, BucksPerk):
                # noinspection PyTypeChecker
                return perk
        except:
            pass
        # noinspection PyBroadException
        try:
            perk: int = int(perk)
        except:
            # noinspection PyTypeChecker
            perk: BucksPerk = perk
            return perk

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.BUCKS_PERK, perk)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_bucks',
    'Set the number of Bucks a Sim has.',
    command_arguments=(
        CommonConsoleCommandArgument('bucks_type', 'CommonBucksType', 'The type of bucks to modify.'),
        CommonConsoleCommandArgument('amount', 'Number', 'The number of Bucks to set. If below zero, this value will become zero.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.set_perk_points',
    )
)
def _common_set_bucks(
    output: CommonConsoleCommandOutput,
    bucks_type: CommonBucksType,
    amount: int,
    sim_info: SimInfo = None
):
    output(f'Setting {bucks_type.name} Bucks to {amount} for Sim {sim_info}')
    result = CommonSimBucksUtils.set_bucks(sim_info, bucks_type, amount, reason='S4CL Console Command')
    if result:
        output(f'Successfully set {bucks_type.name} Bucks to {amount} for Sim {sim_info}')
    else:
        output(f'Failed to set {bucks_type.name} Bucks {amount} for Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_bucks',
    'Add Bucks to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('bucks_type', 'CommonBucksType', 'The type of bucks to modify.'),
        CommonConsoleCommandArgument('amount', 'Number', 'The number of Bucks to add.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.add_perk_points',
    )
)
def _common_add_bucks(
    output: CommonConsoleCommandOutput,
    bucks_type: CommonBucksType,
    amount: int,
    sim_info: SimInfo = None
):
    if bucks_type is None:
        return False
    output(f'Adding {amount} {bucks_type.name} Bucks to Sim {sim_info}')
    result = CommonSimBucksUtils.modify_bucks(sim_info, bucks_type, amount, reason='S4CL Console Command')
    if result:
        output(f'Successfully added {amount} {bucks_type.name} Bucks to Sim {sim_info}')
    else:
        output(f'Failed to add {amount} {bucks_type.name} Bucks to Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_bucks',
    'Add Bucks from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('bucks_type', 'CommonBucksType', 'The type of bucks to modify.'),
        CommonConsoleCommandArgument('amount', 'Number', 'The number of Bucks to remove.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.remove_perk_points',
    )
)
def _common_remove_bucks(
    output: CommonConsoleCommandOutput,
    bucks_type: CommonBucksType,
    amount: int,
    sim_info: SimInfo = None
):
    if bucks_type is None:
        return False
    output(f'Removing {amount} {bucks_type.name} Bucks from Sim {sim_info}')
    result = CommonSimBucksUtils.modify_bucks(sim_info, bucks_type, -amount, reason='S4CL Console Command')
    if result:
        output(f'Successfully removed {amount} {bucks_type.name} Bucks from Sim {sim_info}')
    else:
        output(f'Failed to remove {amount} {bucks_type.name} Bucks from Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.unlock_perk',
    'Unlock a Bucks perk for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('perk', 'Perk Id or Tuning Name', 'The decimal identifier or name of a perk to unlock.'),
        CommonConsoleCommandArgument('no_cost', 'True or False', 'If True, the perk will be unlocked for free. If False, the perk will be unlocked using points (The Sim must have enough points).', is_optional=True, default_value=True),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.add_perk',
    )
)
def _common_add_perks(
    output: CommonConsoleCommandOutput,
    perk: TunableInstanceParam(Types.BUCKS_PERK),
    no_cost: bool = True,
    sim_info: SimInfo = None
):
    if isinstance(perk, str):
        output(f'No perk found for {perk}')
        return False
    cost_text = ' at No Cost' if no_cost else ''
    output(f'Unlocking perk {perk} for Sim {sim_info}{cost_text}.')
    result = CommonSimBucksUtils.unlock_perk(sim_info, perk, no_cost=no_cost)
    if result:
        output(f'Successfully unlocked perk {perk} for Sim {sim_info}.')
    else:
        output(f'Failed to unlock perk {perk} for Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.lock_perk',
    'Lock a Bucks Perk for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('perk', 'Perk Id or Tuning Name',
                                     'The decimal identifier or name of a perk to lock.'),
        CommonConsoleCommandArgument('refund_cost', 'True or False',
                                     'If True, the cost to unlock the perk will be refunded to the Sim. If False, the cost of to unlock the perk will not be refunded.',
                                     is_optional=True, default_value=True),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.remove_perk',
    )
)
def _common_remove_perk(
    output: CommonConsoleCommandOutput,
    perk: TunableInstanceParam(Types.BUCKS_PERK),
    refund_cost: bool = True,
    sim_info: SimInfo = None
):
    if isinstance(perk, str):
        output(f'No perk found for {perk}')
        return False
    cost_text = ' at No Cost' if refund_cost else ''
    output(f'Unlocking perk {perk} for Sim {sim_info}{cost_text}.')
    result = CommonSimBucksUtils.lock_perk(sim_info, perk, refund_cost=refund_cost)
    if result:
        output(f'Successfully unlocked perk {perk} for Sim {sim_info}.')
    else:
        output(f'Failed to unlock perk {perk} for Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.lock_all_perks',
    'Lock all Bucks Perk for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('bucks_type', 'CommonBucksType', 'The type of bucks to remove the perks of.'),
        CommonConsoleCommandArgument('refund_cost', 'True or False',
                                     'If True, the cost to unlock the perks will be refunded to the Sim. If False, the cost of to unlock the perks will not be refunded.',
                                     is_optional=True, default_value=True),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.remove_all_perks',
    )
)
def _common_remove_all_perks(
    output: CommonConsoleCommandOutput,
    bucks_type: CommonBucksType,
    refund_cost: bool = True,
    sim_info: SimInfo = None
):
    if bucks_type is None:
        return False
    cost_text = ' and refunding the Cost' if refund_cost else ''
    output(f'Locking all perks for Sim {sim_info}{cost_text}.')
    result = CommonSimBucksUtils.remove_all_perks(sim_info, bucks_type, refund_cost=refund_cost)
    if result:
        output(f'Successfully locked all {bucks_type.name} perk for Sim {sim_info}.')
    else:
        output(f'Failed to lock all {bucks_type.name} perks for Sim {sim_info}. Reason: {result.reason}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.unlock_all_perks',
    'Unlock all Bucks Perk for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('bucks_type', 'CommonBucksType', 'The type of bucks to add the perks of.'),
        CommonConsoleCommandArgument('no_cost', 'True or False', 'If True, the perk will be unlocked for free. If False, the perk will be unlocked using points (The Sim must have enough points).', is_optional=True, default_value=True),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Id or Name of a Sim to modify.',
                                     is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.add_all_perks',
    )
)
def _common_add_all_perks(
    output: CommonConsoleCommandOutput,
    bucks_type: CommonBucksType,
    no_cost: bool = True,
    sim_info: SimInfo = None
):
    if bucks_type is None:
        return False
    cost_text = ' at No Cost' if no_cost else ''
    output(f'Unlocking all {bucks_type.name} perks for Sim {sim_info}{cost_text}.')
    result = CommonSimBucksUtils.add_all_perks(sim_info, bucks_type, no_cost=no_cost)
    if result:
        output(f'Successfully unlocked all {bucks_type.name} perks for Sim {sim_info}.')
    else:
        output(f'Failed to unlock all {bucks_type.name} perks for Sim {sim_info}. Reason: {result.reason}')
