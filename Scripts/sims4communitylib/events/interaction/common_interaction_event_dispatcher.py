"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union
from event_testing.results import TestResult
from interactions.base.interaction import Interaction
from interactions.interaction_queue import InteractionQueue
from interactions.utils.outcome import InteractionOutcome
from interactions.utils.outcome_enums import OutcomeResult
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_outcome import S4CLInteractionOutcomeEvent
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.events.interaction.events.interaction_run import S4CLInteractionRunEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonInteractionEventDispatcherService(CommonService):
    """A service for dispatching interaction events.

    """

    # noinspection PyUnusedLocal
    def _on_interaction_run(self, interaction_queue: InteractionQueue, timeline, interaction: Interaction, *_, **__):
        if interaction is None or interaction.sim is None:
            return False
        return CommonEventRegistry.get().dispatch(S4CLInteractionRunEvent(interaction, interaction_queue))

    def _on_interaction_queued(self, interaction_queue: InteractionQueue, interaction: Interaction, *_, **__) -> Union[TestResult, None]:
        if interaction is None or interaction.sim is None:
            return None
        if not CommonEventRegistry.get().dispatch(S4CLInteractionQueuedEvent(interaction, interaction_queue)):
            return TestResult(False, 'Interaction \'{}\' Failed to Queue'.format(pformat(interaction)))
        return None

    def _on_interaction_outcome(self, interaction: Interaction, outcome: InteractionOutcome, result: OutcomeResult):
        if interaction.sim is None:
            return False
        return CommonEventRegistry.get().dispatch(S4CLInteractionOutcomeEvent(interaction, outcome, result))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, InteractionQueue, InteractionQueue.run_interaction_gen.__name__)
def _common_on_interaction_run(original, self, *_, **__):
    result = original(self, *_, **__)
    if result:
        CommonInteractionEventDispatcherService.get()._on_interaction_run(self, *_, **__)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, InteractionQueue, InteractionQueue.append.__name__)
def _common_on_interaction_queued(original, self, *_, **__):
    result = CommonInteractionEventDispatcherService.get()._on_interaction_queued(self, *_, **__)
    if result is None:
        return original(self, *_, **__)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, Interaction, Interaction.store_result_for_outcome.__name__)
def _common_on_interaction_outcome(original, self, *_, **__):
    CommonInteractionEventDispatcherService.get()._on_interaction_outcome(self, *_, **__)
    return original(self, *_, **__)
