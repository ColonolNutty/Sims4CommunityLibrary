"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from pprint import pformat
from typing import Union, Any
from interactions.base.interaction import Interaction
from interactions.base.mixer_interaction import MixerInteraction
from interactions.base.super_interaction import SuperInteraction
from interactions.interaction_finisher import FinishingType
from interactions.interaction_queue import InteractionQueue
from interactions.utils.outcome import InteractionOutcome
from interactions.utils.outcome_enums import OutcomeResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_cancelled import S4CLInteractionCancelledEvent
from sims4communitylib.events.interaction.events.interaction_outcome import S4CLInteractionOutcomeEvent
from sims4communitylib.events.interaction.events.interaction_post_queued import S4CLInteractionPostQueuedEvent
from sims4communitylib.events.interaction.events.interaction_pre_run import S4CLInteractionPreRunEvent
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.events.interaction.events.interaction_run import S4CLInteractionRunEvent
from sims4communitylib.events.interaction.events.interaction_started import S4CLInteractionStartedEvent
from sims4communitylib.events.interaction.events.mixer_interaction_cancelled import S4CLMixerInteractionCancelledEvent
from sims4communitylib.events.interaction.events.super_interaction_cancelled import S4CLSuperInteractionCancelledEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass

if not ON_RTD:
    from scheduling import Timeline


class CommonInteractionEventDispatcherService(CommonService, HasLog):
    """A service that dispatches interaction events (Run, Queued, Performed, etc.).

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyUnusedLocal
    def _on_interaction_pre_run(self, interaction_queue: InteractionQueue, timeline: Timeline, interaction: Interaction, *_, **__) -> Union[bool, None]:
        if interaction is None or interaction.sim is None:
            return None
        try:
            if not CommonEventRegistry().dispatch(S4CLInteractionPreRunEvent(interaction, interaction_queue, timeline)):
                return False
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_pre_run for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'
                    .format(
                        pformat(interaction),
                        CommonInteractionUtils.get_interaction_short_name(interaction),
                        CommonInteractionUtils.get_interaction_display_name(interaction),
                        _,
                        __
                    ),
                exception=ex
            )
        return None

    # noinspection PyUnusedLocal
    def _on_interaction_run(self, interaction_queue: InteractionQueue, timeline: Timeline, interaction: Interaction, run_result: bool, *_, **__) -> None:
        if interaction is None or interaction.sim is None:
            return None
        try:
            CommonEventRegistry().dispatch(S4CLInteractionRunEvent(interaction, interaction_queue, run_result))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_run for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Original Run Result: {}, Args: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    str(run_result),
                    _,
                    __
                ),
                exception=ex
            )
        return None

    # noinspection PyUnusedLocal
    def _on_interaction_started(self, interaction: Interaction, *_, **__) -> None:
        if interaction is None or interaction.sim is None:
            return None
        try:
            source_sim_info = CommonSimUtils.get_sim_info(interaction.sim)
            target = interaction.target
            CommonEventRegistry().dispatch(S4CLInteractionStartedEvent(interaction, source_sim_info, target))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_started for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    _,
                    __
                ),
                exception=ex
            )
        return None

    def _on_interaction_queued(self, interaction_queue: InteractionQueue, interaction: Interaction, *_, **__) -> Union[CommonTestResult, None]:
        if interaction is None or interaction.sim is None:
            return None
        try:
            if not CommonEventRegistry().dispatch(S4CLInteractionQueuedEvent(interaction, interaction_queue)):
                return CommonTestResult(False, reason='Interaction \'{}\' Failed to Queue'.format(pformat(interaction)), hide_tooltip=True)
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_queued for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    _,
                    __
                ),
                exception=ex
            )
        return None

    def _on_interaction_post_queued(self, interaction_queue: InteractionQueue, interaction: Interaction, queue_result: CommonTestResult, *_, **__) -> None:
        if interaction is None or interaction.sim is None:
            return None
        try:
            CommonEventRegistry().dispatch(S4CLInteractionPostQueuedEvent(interaction, interaction_queue, queue_result))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_post_queued for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Queue Result: {}, Args: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    queue_result,
                    _,
                    __
                ),
                exception=ex
            )
        return None

    def _on_interaction_outcome(self, interaction: Interaction, outcome: InteractionOutcome, result: OutcomeResult) -> None:
        if interaction.sim is None:
            return None
        try:
            CommonEventRegistry().dispatch(S4CLInteractionOutcomeEvent(interaction, outcome, result))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_outcome for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Outcome: {}, Result: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    outcome,
                    result
                ),
                exception=ex
            )
        return None

    def _on_interaction_cancelled(self, interaction: Interaction, finishing_type: FinishingType, cancel_reason_msg: str, ignore_must_run: bool=False, **__) -> None:
        if finishing_type is None:
            return None
        try:
            CommonEventRegistry().dispatch(S4CLInteractionCancelledEvent(interaction, finishing_type, cancel_reason_msg, ignore_must_run=ignore_must_run, **__))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Finishing Type: {}, Cancel Reason: {}, Ignore Must Run: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    finishing_type,
                    cancel_reason_msg,
                    ignore_must_run,
                    __
                ),
                exception=ex
            )
        return None

    def _on_mixer_interaction_cancelled(self, interaction: MixerInteraction, finishing_type: FinishingType, cancel_reason_msg: str, **__) -> None:
        if finishing_type is None:
            return None
        try:
            CommonEventRegistry().dispatch(S4CLMixerInteractionCancelledEvent(interaction, finishing_type, cancel_reason_msg, **__))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_mixer_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Finishing Type: {}, Cancel Reason: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    finishing_type,
                    cancel_reason_msg,
                    __
                ),
                exception=ex
            )
        return None

    def _on_super_interaction_cancelled(self, interaction: SuperInteraction, finishing_type: FinishingType, cancel_reason_msg: str, **__) -> None:
        if interaction is None or finishing_type is None:
            return None
        try:
            CommonEventRegistry().dispatch(S4CLSuperInteractionCancelledEvent(interaction, finishing_type, cancel_reason_msg, **__))
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _on_super_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Finishing Type: {}, Cancel Reason: {}, Kwargs: {}'.format(
                    pformat(interaction),
                    CommonInteractionUtils.get_interaction_short_name(interaction),
                    CommonInteractionUtils.get_interaction_display_name(interaction),
                    finishing_type,
                    cancel_reason_msg,
                    __
                ),
                exception=ex
            )
        return None


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InteractionQueue, InteractionQueue.run_interaction_gen.__name__)
def _common_on_interaction_run(original, self, timeline: Timeline, interaction: Interaction, *_, **__) -> bool:
    try:
        result = CommonInteractionEventDispatcherService()._on_interaction_pre_run(self, timeline, interaction, *_, **__)
        if result is None or result:
            try:
                original_result = original(self, timeline, interaction, *_, **__)
            except Exception as ex:
                CommonExceptionHandler.log_exception(
                    None,
                    'Error occurred while running _on_interaction_run for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                        pformat(interaction),
                        CommonInteractionUtils.get_interaction_short_name(interaction),
                        CommonInteractionUtils.get_interaction_display_name(interaction),
                        _,
                        __
                    ),
                    exception=ex
                )
                return False
            CommonInteractionEventDispatcherService()._on_interaction_run(self, timeline, interaction, original_result, *_, **__)
            return original_result
        return result
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _on_interaction_run for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(interaction),
                CommonInteractionUtils.get_interaction_short_name(interaction),
                CommonInteractionUtils.get_interaction_display_name(interaction),
                _,
                __
            ),
            exception=ex
        )
    return False


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Interaction, Interaction._trigger_interaction_start_event.__name__)
def _common_on_interaction_started(original, self, *_, **__) -> bool:
    try:
        try:
            original_result = original(self, *_, **__)
        except Exception as ex:
            CommonExceptionHandler.log_exception(
                None,
                'Error occurred while running _trigger_interaction_start_event for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                    pformat(self),
                    CommonInteractionUtils.get_interaction_short_name(self),
                    CommonInteractionUtils.get_interaction_display_name(self),
                    _,
                    __
                ),
                exception=ex
            )
            return False
        CommonInteractionEventDispatcherService()._on_interaction_started(self, *_, **__)
        return original_result
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _trigger_interaction_start_event for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )
    return False


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), InteractionQueue, InteractionQueue.append.__name__)
def _common_on_interaction_queued(original, self, interaction: Interaction, *_, **__) -> CommonTestResult:
    try:
        result = CommonInteractionEventDispatcherService()._on_interaction_queued(self, interaction, *_, **__)
        if result is None or result:
            try:
                original_result = original(self, interaction, *_, **__)
            except Exception as ex:
                CommonExceptionHandler.log_exception(
                    None,
                    'Error occurred while running _on_interaction_queued for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                        pformat(interaction),
                        CommonInteractionUtils.get_interaction_short_name(interaction),
                        CommonInteractionUtils.get_interaction_display_name(interaction),
                        _,
                        __
                    ),
                    exception=ex
                )
                return CommonTestResult.NONE
            original_result: CommonTestResult = CommonTestResult.convert_from_vanilla(original_result)
            CommonInteractionEventDispatcherService()._on_interaction_post_queued(self, interaction, original_result, *_, **__)
            return original_result
        return result
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _on_interaction_queued for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(interaction),
                CommonInteractionUtils.get_interaction_short_name(interaction),
                CommonInteractionUtils.get_interaction_display_name(interaction),
                _,
                __
            ),
            exception=ex
        )
    return CommonTestResult(False, reason='Interaction \'{}\' with short name \'{}\' Failed to Queue'.format(
        pformat(interaction),
        CommonInteractionUtils.get_interaction_short_name(interaction)
    ), hide_tooltip=True)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Interaction, Interaction.store_result_for_outcome.__name__)
def _common_on_interaction_outcome(original, self, *_, **__) -> Any:
    try:
        CommonInteractionEventDispatcherService()._on_interaction_outcome(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _on_interaction_outcome for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )

    try:
        return original(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            None,
            'Error occurred while running _on_interaction_outcome for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )
    return False


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Interaction, Interaction.cancel.__name__)
def _common_on_interaction_cancelled(original, self, *_, **__) -> Any:
    try:
        CommonInteractionEventDispatcherService()._on_interaction_cancelled(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _on_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )

    try:
        return original(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            None,
            'Error occurred while running _on_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )
    return False


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), MixerInteraction, MixerInteraction.cancel.__name__)
def _common_on_mixer_interaction_cancelled(original, self, *_, **__) -> Any:
    try:
        CommonInteractionEventDispatcherService()._on_mixer_interaction_cancelled(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _on_mixer_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )

    try:
        return original(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            None,
            'Error occurred while running _on_mixer_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )
    return False


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SuperInteraction, SuperInteraction.cancel.__name__)
def _common_on_super_interaction_cancelled(original, self, *_, **__) -> Any:
    try:
        CommonInteractionEventDispatcherService()._on_super_interaction_cancelled(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            ModInfo.get_identity(),
            'Error occurred while running _on_super_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )

    try:
        return original(self, *_, **__)
    except Exception as ex:
        CommonExceptionHandler.log_exception(
            None,
            'Error occurred while running _on_super_interaction_cancelled for interaction {} with short name \'{}\' and display name {}. (This exception is not caused by S4CL, but rather caught) Args: {}, Kwargs: {}'.format(
                pformat(self),
                CommonInteractionUtils.get_interaction_short_name(self),
                CommonInteractionUtils.get_interaction_display_name(self),
                _,
                __
            ),
            exception=ex
        )
    return None
