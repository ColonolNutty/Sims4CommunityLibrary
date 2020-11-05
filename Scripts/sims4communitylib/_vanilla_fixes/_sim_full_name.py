"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# The purpose of this file is to fix the fact that when trying to access the "full_name" attribute on Sims an empty string is returned.
# noinspection PyBroadException
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, 'full_name')
def _common_fix_full_name_returning_empty_string(original, self: SimInfo, *_, **__):
    original_value = original(self, *_, **__)
    if original_value == '':
        return CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(self))
    return original_value
