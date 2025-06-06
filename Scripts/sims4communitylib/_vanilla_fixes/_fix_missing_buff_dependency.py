"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from objects.components.buff_component import BuffComponent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


# This error can occur because the buff is not available, such as a mod dependency
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), BuffComponent, BuffComponent._can_add_buff_type.__name__, handle_exceptions=False)
def _common_fix_missing_buff_type(original, self, buff_type, *_, **__) -> Any:
    if buff_type is None:
        return False, None
    return original(self, buff_type, *_, **__)
