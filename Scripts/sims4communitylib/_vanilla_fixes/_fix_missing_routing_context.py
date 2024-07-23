"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.script_object import ScriptObject
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils

# This fix resolves the "AttributeError: 'NoneType' object has no attribute 'object_footprint_id'" error.


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ScriptObject, ScriptObject._fill_ignored_objects_and_test_halfwalls.__name__)
def _common_fix_object_footprint_id_error(original, self: ScriptObject, routing_context, sim_loc, obj, ignored_object_set):
    original_result = original(self, routing_context, sim_loc, obj, ignored_object_set)
    to_remove_ignored_object_set = set()
    for ignored_object_set_item in ignored_object_set:
        if ignored_object_set_item.routing_context is None:
            to_remove_ignored_object_set.add(ignored_object_set_item)

    for to_remove_ignored_object in to_remove_ignored_object_set:
        ignored_object_set.remove(to_remove_ignored_object)
    return original_result
