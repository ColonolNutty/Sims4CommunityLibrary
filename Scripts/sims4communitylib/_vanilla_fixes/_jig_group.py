"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from socials.jig_group import JigGroup


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), JigGroup, JigGroup._can_picked_object_be_jig.__name__)
def _common_check_picked_object_has_slot_attribute(original, cls, picked_object) -> bool:
    if not hasattr(picked_object, 'slot'):
        return False
    return original(picked_object)
