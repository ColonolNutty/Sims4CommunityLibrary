"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from socials.jig_group import JigGroup


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'jig_group_log')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), JigGroup, JigGroup._can_picked_object_be_jig.__name__)
def _common_check_picked_object_has_slot_attribute(original, cls, picked_object) -> bool:
    if not hasattr(picked_object, 'slot'):
        return False
    if picked_object.definition is None or picked_object.definition.get_slots_resource(0) is None:
        return False
    try:
        return original(picked_object)
    except Exception as ex:
        log.format_error_with_message('An error occurred when checking if a picked object be a jig. (This exception is not caused by S4CL, but rather caught)', owner=cls, picked_object=picked_object, exception=ex)
    return False
