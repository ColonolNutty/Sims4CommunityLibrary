"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.aging.aging_mixin import AgingMixin
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'aging_mixin_log')

if hasattr(AgingMixin, 'get_age_transition_data'):
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AgingMixin, AgingMixin.get_age_transition_data.__name__)
    def _common_fix_vanilla_aging_mixin_fox_key_error(original, self: AgingMixin, age, *_, **__):
        try:
            return original(self, age, *_, **__)
        except Exception as ex:
            if 'KeyError: 5' in str(ex):
                log.format_error_with_message('Failed to get age transition data, a mod that replaces the AGING_MIXIN tuning, needs to be updated! (This exception is not caused by S4CL, but rather caught)', owner=self, age=age, species=self.species if hasattr(self, 'species') else None, argles=_, kwargles=__, exception=ex)
            else:
                log.format_error_with_message('Failed to get age transition data (This exception is not caused by S4CL, but rather caught)', owner=self, age=age, species=self.species if hasattr(self, 'species') else None, argles=_, kwargles=__, exception=ex)
            raise ex
