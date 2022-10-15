"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Any
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from whims.whims_tracker import WhimsTracker

# noinspection PyTypeChecker
log = CommonLogRegistry().register_log(None, 'whims_error_catcher')


# noinspection PyUnusedLocal,SpellCheckingInspection
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), WhimsTracker, WhimsTracker._generate_whim_buckets_for_type_and_whimset.__name__, handle_exceptions=False)
def _common_catch_errors_related_to_whims_from_outdated_mods(original, self, whim_type, whimset, *_, **__) -> List[Any]:
    try:
        return original(self, whim_type, whimset, *_, **__)
    except Exception as ex:
        log.format_error_with_message(
            'An error occurred when attempting to generate Whims for Sims. (This exception is not caused by S4CL, but rather caught)',
            whim_type=whim_type,
            whimset_name=whimset,
            whimset_guid=getattr(whimset, 'guid64', None),
            argles=_,
            kwargles=__,
            exception=ex
        )
        return list()
