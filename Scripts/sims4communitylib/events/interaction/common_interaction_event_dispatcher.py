"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union, Any
from event_testing.results import TestResult
from interactions.base.interaction import Interaction
from interactions.base.mixer_interaction import MixerInteraction
from interactions.base.super_interaction import SuperInteraction
from interactions.interaction_finisher import FinishingType
from interactions.interaction_queue import InteractionQueue
from interactions.utils.outcome import InteractionOutcome
from interactions.utils.outcome_enums import OutcomeResult
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_cancelled import S4CLInteractionCancelledEvent
from sims4communitylib.events.interaction.events.interaction_outcome import S4CLInteractionOutcomeEvent
from sims4communitylib.events.interaction.events.interaction_post_queued import S4CLInteractionPostQueuedEvent
from sims4communitylib.events.interaction.events.interaction_pre_run import S4CLInteractionPreRunEvent
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.events.interaction.events.interaction_run import S4CLInteractionRunEvent
from sims4communitylib.events.interaction.events.mixer_interaction_cancelled import S4CLMixerInteractionCancelledEvent
from sims4communitylib.events.interaction.events.super_interaction_cancelled import S4CLSuperInteractionCancelledEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonInteractionEventDispatcherService(CommonService):
    """A service that dispatches interaction events (Run, Queued, Performed, etc.).

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    # noinspection PyUnusedLocal
    def _on_interaction_pre_run(self, interaction_queue: InteractionQueue, timeline, interaction: Interaction, *_, **__) -> Union[bool, None]:
        if interaction is None or interaction.sim is None:
            return None
        if not CommonEventRegistry.get().dispatch(S4CLInteractionPreRunEvent(interaction, interaction_queue)):
            return False
        return None

    # noinspection PyUnusedLocal
    def _on_interaction_run(self, interaction_queue: InteractionQueue, timeline, interaction: Interaction, *_, **__) -> Union[bool, None]:
        if interaction is None or interaction.sim is None:
            return None
        return CommonEventRegistry.get().dispatch(S4CLInteractionRunEvent(interaction, interaction_queue))

    def _on_interaction_queued(self, interaction_queue: InteractionQueue, interaction: Interaction, *_, **__) -> Union[TestResult, None]:
        if interaction is None or interaction.sim is None:
            return None
        if not CommonEventRegistry.get().dispatch(S4CLInteractionQueuedEvent(interaction, interaction_queue)):
            return TestResult(False, 'Interaction \'{}\' Failed to Queue'.format(pformat(interaction)))
        return None

    def _on_interaction_post_queued(self, interaction_queue: InteractionQueue, interaction: Interaction, *_, **__) -> bool:
        if interaction is None or interaction.sim is None:
            return False
        return CommonEventRegistry.get().dispatch(S4CLInteractionPostQueuedEvent(interaction, interaction_queue))

    def _on_interaction_outcome(self, interaction: Interaction, outcome: InteractionOutcome, result: OutcomeResult) -> Union[bool, Any]:
        if interaction.sim is None:
            return False
        return CommonEventRegistry.get().dispatch(S4CLInteractionOutcomeEvent(interaction, outcome, result))

    def _on_interaction_cancelled(self, interaction: Interaction, finishing_type: FinishingType, cancel_reason_msg: str, ignore_must_run: bool=False, **kwargs) -> Union[bool, None]:
        if finishing_type is None:
            return None
        if not CommonEventRegistry.get().dispatch(S4CLInteractionCancelledEvent(interaction, finishing_type, cancel_reason_msg, ignore_must_run=ignore_must_run, **kwargs)):
            return False
        return None

    def _on_mixer_interaction_cancelled(self, interaction: MixerInteraction, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> Union[bool, None]:
        if finishing_type is None:
            return None
        if not CommonEventRegistry.get().dispatch(S4CLMixerInteractionCancelledEvent(interaction, finishing_type, cancel_reason_msg, **kwargs)):
            return False
        return None

    def _on_super_interaction_cancelled(self, interaction: SuperInteraction, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> Union[bool, None]:
        if interaction is None or finishing_type is None:
            return None
        if not CommonEventRegistry.get().dispatch(S4CLSuperInteractionCancelledEvent(interaction, finishing_type, cancel_reason_msg, **kwargs)):
            return False
        return None


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InteractionQueue, InteractionQueue.run_interaction_gen.__name__)
def _common_on_interaction_run(original, self, *_, **__) -> Any:
    result = CommonInteractionEventDispatcherService.get()._on_interaction_pre_run(self, *_, **__)
    if result is None:
        original_result = original(self, *_, **__)
        CommonInteractionEventDispatcherService.get()._on_interaction_run(self, *_, **__)
        return original_result
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InteractionQueue, InteractionQueue.append.__name__)
def _common_on_interaction_queued(original, self, *_, **__) -> Any:
    result = CommonInteractionEventDispatcherService.get()._on_interaction_queued(self, *_, **__)
    if result is None:
        original_result = original(self, *_, **__)
        CommonInteractionEventDispatcherService.get()._on_interaction_post_queued(self, *_, **__)
        return original_result
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Interaction, Interaction.store_result_for_outcome.__name__)
def _common_on_interaction_outcome(original, self, *_, **__) -> Any:
    CommonInteractionEventDispatcherService.get()._on_interaction_outcome(self, *_, **__)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Interaction, Interaction.cancel.__name__)
def _common_on_interaction_cancelled(original, self, *_, **__) -> Any:
    CommonInteractionEventDispatcherService.get()._on_interaction_cancelled(self, *_, **__)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), MixerInteraction, MixerInteraction.cancel.__name__)
def _common_on_mixer_interaction_cancelled(original, self, *_, **__) -> Any:
    CommonInteractionEventDispatcherService.get()._on_mixer_interaction_cancelled(self, *_, **__)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SuperInteraction, SuperInteraction.cancel.__name__)
def _common_on_super_interaction_cancelled(original, self, *_, **__) -> Any:
    CommonInteractionEventDispatcherService.get()._on_super_interaction_cancelled(self, *_, **__)
    return original(self, *_, **__)
