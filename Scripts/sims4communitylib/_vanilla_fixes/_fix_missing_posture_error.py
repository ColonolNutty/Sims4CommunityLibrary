"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.interaction import Interaction
from interactions.interaction_finisher import FinishingType
from postures.posture import Posture
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Posture, Posture.get_registered_asm.__name__, handle_exceptions=False)
def _common_fix_missing_asm_freeze_error(original, self: Posture, *_, **__):
    # noinspection PyBroadException
    try:
        result = original(self, *_, **__)
        if not result:
            source_interaction: Interaction = self.source_interaction
            if source_interaction is not None:
                source_interaction.cancel(FinishingType.KILLED, cancel_reason_msg='Failed to locate a Posture for Sim.', ignore_must_run=True)
        return result
    except:
        source_interaction: Interaction = self.source_interaction
        if source_interaction is not None:
            source_interaction.cancel(FinishingType.KILLED, cancel_reason_msg='Failed to locate a Posture for Sim.', ignore_must_run=True)
    return None
