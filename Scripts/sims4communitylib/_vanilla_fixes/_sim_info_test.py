"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from event_testing.results import TestResult
from sims.sim_info_tests import SimInfoTest
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


# noinspection PyUnusedLocal,SpellCheckingInspection
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfoTest, SimInfoTest._test_sim_info.__name__, handle_exceptions=False)
def _common_fix_issues_with_missing_death_object_assigned(original, self, *_, **__) -> TestResult:
    if not hasattr(self, 'death_object_assigned'):
        self.death_object_assigned = False
    return original(self, *_, **__)
