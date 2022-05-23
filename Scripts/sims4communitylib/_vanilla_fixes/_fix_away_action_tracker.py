"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from away_actions.away_action_tracker import AwayActionTracker
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AwayActionTracker, AwayActionTracker.remove_on_away_action_ended_callback.__name__)
def _common_fix_remove_on_away_action_ended_callback(original, self: AwayActionTracker, callback):
    if callback not in self._on_away_action_ended:
        return
    return original(self, callback)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AwayActionTracker, AwayActionTracker.remove_on_away_action_started_callback.__name__)
def _common_fix_remove_on_away_action_started_callback(original, self: AwayActionTracker, callback):
    if callback not in self._on_away_action_started:
        return
    return original(self, callback)
