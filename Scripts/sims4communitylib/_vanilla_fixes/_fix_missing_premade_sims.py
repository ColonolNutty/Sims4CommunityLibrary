"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from world.premade_sim_fixup_helper import PremadeSimFixupHelper


# This error can occur because the buff is not available, such as a mod dependency
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PremadeSimFixupHelper, PremadeSimFixupHelper._apply_household_fixup.__name__, handle_exceptions=False)
def _common_fix_missing_pre_made_sim_templates(original, self, *_, **__) -> Any:
    new_premade_sim_infos = dict()
    for (template, sim_info) in tuple(self._premade_sim_infos.items()):
        if template is None:
            continue
        new_premade_sim_infos[template] = sim_info
    self._premade_sim_infos = new_premade_sim_infos
    return original(self, *_, **__)
