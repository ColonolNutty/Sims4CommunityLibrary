"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# The purpose of this file is to fix vanilla game bugs with Bucks
from typing import Union

from bucks.bucks_tracker import BucksTrackerBase
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'bucks_fix')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), BucksTrackerBase, BucksTrackerBase.try_modify_bucks.__name__)
def _common_fix_bucks_when_amount_is_float(original, self, bucks_type, amount: Union[int, float], *_, **__):
    # The game can modify game bucks using a float for the amount, this causes a number of issues, especially when trying to save the game.
    # This can be caused due to a Sim being a 5 star celebrity that doubles all Bucks earnings.
    # The fix is to convert the float amount to an int as the game expects it to be.
    try:
        fixed_amount = int(amount)
        return original(self, bucks_type, fixed_amount, *_, **__)
    except Exception as ex:
        log.format_error_with_message('An error occurred while modifying bucks. (This exception is not caused by S4CL, but rather caught)', owner=self, bucks_type=bucks_type, amount=amount, argles=_, kwargles=__, exception=ex)
    return False

