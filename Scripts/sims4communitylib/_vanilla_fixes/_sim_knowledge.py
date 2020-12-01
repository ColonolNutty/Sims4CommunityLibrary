"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from relationships.sim_knowledge import SimKnowledge
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils

if hasattr(SimKnowledge, 'remove_known_trait'):
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimKnowledge, SimKnowledge.remove_known_trait.__name__, handle_exceptions=False)
    def _common_fix_vanilla_remove_known_trait_not_checking_known_traits(original, self: SimKnowledge, trait, *_, **__):
        if self._known_traits is not None and trait not in self._known_traits:
            return
        return original(self, trait, *_, **__)
