"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.funds import FamilyFunds
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.common_currency_modify_reasons import CommonCurrencyModifyReason
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


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
            return CommonExecutionResult(False, reason=f'{sim_info} was not a part of a household that has funds.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_PART_OF_A_HOUSEHOLD_THAT_HAS_FUNDS, tooltip_tokens=(sim_info,))
        household_funds.add(amount, reason, **kwargs)
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_simoleons_from_household(cls, sim_info: SimInfo, amount: int, reason: CommonCurrencyModifyReason, require_full_amount: bool=True, **kwargs) -> float:
        """remove_simoleons_from_household(sim_info, amount, reason, require_full_amount=True, **kwargs)

        Remove an amount of simoleons from the Household of a Sim.

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


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_simoleons',
    'Add simoleons to a household.',
    command_arguments=(
        CommonConsoleCommandArgument('amount', 'Number', 'The amount of money to add to the household.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_add_simoleons(output: CommonConsoleCommandOutput, amount: int, sim_info: SimInfo = None):
    if sim_info is None:
        return False
    result = CommonSimCurrencyUtils.add_simoleons_to_household(sim_info, amount, CommonCurrencyModifyReason.CHEAT)
    if result:
        output(f'SUCCESS: Successfully added currency to Sim {sim_info}')
        return True
    output(f'FAILED: Failed to add currency to Sim {sim_info}. {result.reason}')
    return False


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_simoleons',
    'Remove simoleons from a household.',
    command_arguments=(
        CommonConsoleCommandArgument('amount', 'Number', 'The amount of money to remove from the household.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_remove_simoleons(output: CommonConsoleCommandOutput, amount: int, sim_info: SimInfo = None):
    if sim_info is None:
        return False
    result = CommonSimCurrencyUtils.remove_simoleons_from_household(sim_info, amount, CommonCurrencyModifyReason.CHEAT)
    if result != amount:
        output(f'SUCCESS: Successfully removed currency from Sim {sim_info}, {result} was left over.')
        return True
    output(f'FAILED: Failed to remove currency from Sim {sim_info}. Could not remove {result} Simoleons')
    return False
