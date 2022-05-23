"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim import Sim
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'sim_fixes_log')

if hasattr(Sim, 'can_see'):
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.can_see.__name__)
    def _common_fix_can_see_error(original, self: Sim, *_, **__):
        try:
            if not hasattr(self, 'los_constraint') or self.los_constraint is None:
                return False
            return original(self, *_, **__)
        except Exception as ex:
            raise ex
