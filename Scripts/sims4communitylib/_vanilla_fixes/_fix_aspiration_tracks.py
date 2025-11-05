"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from aspirations.aspirations import AspirationTracker
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AspirationTracker, AspirationTracker.initialize_aspiration.__name__, handle_exceptions=False)
def _common_fix_aspiration_traits_staying_after_aspiration_change(original, self, *_, **__) -> Any:
    if hasattr(self, '_old_track') and self._old_track is not None:
        if hasattr(self._old_track, 'provided_traits'):
            for trait in self._old_track.provided_traits:
                self.owner_sim_info.remove_trait(trait)

    self._old_track = self.active_track
    return original(self, *_, **__)
