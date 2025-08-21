"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from apartments.apartment_zone_director import ApartmentZoneDirectorPlayer
from sims.sim_info import SimInfo
from sims4.tuning.tunable_perf import TuningAttrCleanupHelper
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


# @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TuningAttrCleanupHelper, '_register_for_cleanup_internal')
def _common_fix_bad_check(original, self: TuningAttrCleanupHelper, *_, **__):
    if self._tracked_objects is None:
        self._tracked_objects = list()
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ApartmentZoneDirectorPlayer, ApartmentZoneDirectorPlayer._register_zone_aspriations_for_sim.__name__)
def _common_fix_bad_check_2(original, self: ApartmentZoneDirectorPlayer, sim_info: SimInfo, *_, **__):
    if sim_info.aspiration_tracker is None:
        return
    return original(self, sim_info, *_, **__)
