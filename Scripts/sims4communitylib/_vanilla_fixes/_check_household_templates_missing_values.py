"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from filters.tunable import TunableSimFilter
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_template_error_catcher')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TunableSimFilter, 'create_template_matching_sim_creator', handle_exceptions=False)
def _common_give_details_when_templates_missing(original, self, sim_creator) -> Any:
    try:
        if self._household_templates_override and None in self._household_templates_override:
            household_template_overrides = list()
            for household_template_override in self._household_templates_override:
                if household_template_override is not None:
                    household_template_overrides.append(household_template_override)
            self._household_templates_override = tuple(household_template_overrides)
        original_result = original(self, sim_creator)
    except Exception as ex:
        log.format_error_with_message('Error occurred trying to get templates.', me=self, _household_templates_override=self._household_templates_override, exception=ex)
        raise ex
    return original_result
