"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from server_commands.argument_helpers import OptionalTargetParam
from sims.funds import FamilyFunds
from sims.sim_info import SimInfo
from sims4.commands import Output
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.common_currency_modify_reasons import CommonCurrencyModifyReason
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimCurrencyUtils:
    """Utilities for modifying various currency types of Sims.

    """
    @classmethod
    def can_afford_simoleons(cls, sim_info: SimInfo, amount: int) -> bool:
        """can_afford_simoleons(sim_info, amount)

        Determine if a Sim can afford an amount of simoleons.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param amount: The amount of simoleons to check.
        :type amount: int
        :return: True, if the household of the Sim can afford the simoleon amount. False, if not.
        :rtype: bool
        """
        household_funds = cls.get_household_funds(sim_info)
        if household_funds is None:
            return False
        return household_funds.can_afford(amount)

    @classmethod
    def add_simoleons_to_household(cls, sim_info: SimInfo, amount: int, reason: CommonCurrencyModifyReason, **kwargs) -> CommonExecutionResult:
        """add_simoleons_to_household(sim_info, amount, reason, **kwargs)

        Add an amount of simoleons to the Household of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param amount: The amount of simoleons to add.
        :type amount: int
        :param reason: The reason the simoleons are being added.
        :type reason: CommonCurrencyModifyReason
        :return: True, if simoleons were added successfully. False, if not.
        :rtype: bool
        """
        household_funds = cls.get_household_funds(sim_info)
        if household_funds is None:
            return CommonExecutionResult(False, 'The Sim was not a part of a household that has funds.')
        household_funds.add(amount, reason, **kwargs)
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_simoleons_from_household(cls, sim_info: SimInfo, amount: int, reason: CommonCurrencyModifyReason, require_full_amount: bool=True, **kwargs) -> float:
        """remove_simoleons_from_household(sim_info, amount, reason, require_full_amount=True, **kwargs)

        Add an amount of simoleons to the Household of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param amount: The amount of simoleons to add.
        :type amount: int
        :param reason: The reason the simoleons are being removed.
        :type reason: CommonCurrencyModifyReason
        :param require_full_amount: If True, then the Sim  must have the full amount for the removal to be successful. If False, the Sim does not require the full amount. Default is True.
        :type require_full_amount: bool, optional
        :return: The amount of simoleons removed from the household of the specified Sim. This amount may be lower than the specified amount, if the Sim did not have enough simoleons for removal.
        :rtype: float
        """
        household_funds = cls.get_household_funds(sim_info)
        if household_funds is None:
            return 0.0
        return household_funds.try_remove_amount(amount, reason, require_full_amount=require_full_amount, **kwargs)

    @classmethod
    def get_household_funds(cls, sim_info: SimInfo) -> Union[FamilyFunds, None]:
        """get_household_funds(sim_info)

        Retrieve the Funds object that manages the Household Simoleons for the Household of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The FamilyFunds object of the Household of the specified Sim or None if the Sim did not have a Household.
        :rtype: Union[FamilyFunds, None]
        """
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        household = CommonHouseholdUtils.get_household(sim_info)
        if household is None:
            return None
        return household.funds


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.add_simoleons', 'Add simoleons to a household.')
def _common_add_simoleons(output: Output, amount: int, opt_sim: OptionalTargetParam=None):
    from server_commands.argument_helpers import get_optional_target
    sim = get_optional_target(opt_sim, output._context)
    sim_info = CommonSimUtils.get_sim_info(sim)
    if sim_info is None:
        output(f'Failed, Sim {opt_sim} did not exist.')
        return False
    result = CommonSimCurrencyUtils.add_simoleons_to_household(sim_info, amount, CommonCurrencyModifyReason.CHEAT)
    if result:
        output(f'Successfully added currency to Sim {sim_info}')
        return True
    output(f'ERROR: Failed to add currency to Sim {sim_info}. {result.reason}')
    return False


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.remove_simoleons', 'Add simoleons to a household.')
def _common_add_simoleons(output: Output, amount: int, opt_sim: OptionalTargetParam=None):
    from server_commands.argument_helpers import get_optional_target
    sim = get_optional_target(opt_sim, output._context)
    sim_info = CommonSimUtils.get_sim_info(sim)
    if sim_info is None:
        output(f'Failed, Sim {opt_sim} did not exist.')
        return False
    result = CommonSimCurrencyUtils.add_simoleons_to_household(sim_info, amount, CommonCurrencyModifyReason.CHEAT)
    if result:
        output(f'Successfully removed currency from Sim {sim_info}')
        return True
    output(f'ERROR: Failed to remove currency from Sim {sim_info}. {result.reason}')
    return False
