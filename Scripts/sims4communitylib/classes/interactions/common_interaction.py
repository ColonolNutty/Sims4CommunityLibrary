"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, Union, List, Set
from event_testing.results import TestResult
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from postures.posture_state import PostureState
from sims.sim import Sim
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from singletons import DEFAULT


class CommonInteraction(Interaction):
    """ Enables hooks into the functionality of an Interaction """
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=TestResult.NONE)
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        test_result = cls.on_test(context.sim, target, context, **kwargs)
        if test_result is None:
            return super()._test(target, context, **kwargs)
        if not isinstance(test_result, TestResult):
            raise RuntimeError('Interaction on_test did not result in a TestResult. {}'.format(cls.__name__))
        if test_result.result is False:
            if test_result.tooltip is not None:
                tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.tooltip)
            elif test_result.reason is not None:
                tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.reason)
            else:
                tooltip = None
            return cls.create_test_result(test_result.result, test_result.reason, tooltip=tooltip)
        return super()._test(target, context, **kwargs)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def _trigger_interaction_start_event(self):
        super()._trigger_interaction_start_event()
        self.on_started(self.sim, self.target)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def apply_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT):
        """
            Apply a posture to a sim.
        :param posture_state: The posture state to apply.
        :param participant_type: The ParticipantType of the actor.
        :param sim: The sim to apply posture states to.
        :return: Unknown
        """
        (new_posture_state, new_participant_type, new_sim) = self.modify_posture_state(posture_state, participant_type=participant_type, sim=sim)
        return super().apply_posture_state(new_posture_state, participant_type=new_participant_type, sim=new_sim)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=False)
    def kill(self) -> bool:
        """
            Kill the interaction. (Hard Cancel)
        """
        self.on_killed(self.sim, self.target)
        return super().kill()

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=False)
    def cancel(self, finishing_type, cancel_reason_msg, **kwargs) -> bool:
        """
            Cancel the interaction.
        :param finishing_type: The type of cancellation occurring.
        :param cancel_reason_msg: The reason it was cancelled.
        :return: True if cancellation is successful, False if cancellation failed.
        """
        self.on_cancelled(self.sim, self.target, finishing_type, cancel_reason_msg, **kwargs)
        return super().cancel(finishing_type, cancel_reason_msg, **kwargs)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def _post_perform(self):
        self.on_performed(self.sim, self.target)
        return super()._post_perform()

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    @staticmethod
    def create_test_result(result: bool, reason: str=None, text_tokens: Union[Tuple[Any], List[Any], Set[Any]]=(), tooltip: Union[int, str, CommonLocalizationUtils.LocalizedTooltip]=None, icon=None, influence_by_active_mood: bool=False) -> TestResult:
        """
            Create a TestResult with the specified information.
        :param result: The result of a test. True for passed, False for failed.
        :param reason: The reason for the Test Result (This is displayed as a tooltip to the player when the interaction is disabled).
        :param text_tokens: Any text tokens to include format into the reason.
        :param tooltip: The tooltip displayed when hovering the interaction while it is disabled.
        :param icon: The icon of the outcome. (It is currently unknown exactly where this icon would show)
        :param influence_by_active_mood: If true, the Test Result will be influenced by the active mood.
        :return: An object of type TestResult.
        """
        return TestResult(result, reason, *text_tokens, tooltip=tooltip, icon=icon, influence_by_active_mood=influence_by_active_mood)

    # noinspection PyUnusedLocal
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        """
            A hook that occurs upon the interaction being tested for run.
        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :param interaction_context: The context of the interaction.
        :return The result of successfully running the test.
        """
        return TestResult.TRUE

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=True)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """
            Occurs upon the interaction being started.
        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :return: True if the interaction hook was executed successfully.
        """
        pass

    # noinspection PyUnusedLocal
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=True)
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """
            Occurs upon the interaction being killed.
        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :return: True if the interaction hook was executed successfully.
        """
        return True

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=True)
    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> None:
        """
            Occurs upon the interaction being cancelled.
        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :param finishing_type: The type of cancellation.
        :param cancel_reason_msg: The reason for the cancellation.
        """
        pass

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=True)
    def on_performed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """
            Occurs after the interaction has been performed.
        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        """
        pass

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=True)
    def modify_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT) -> Tuple[PostureState, ParticipantType, Any]:
        """
            Modify the posture state, participant type or sim of the interaction.
        :param posture_state: The posture state to modify.
        :param participant_type: The ParticipantType of the actor to modify.
        :param sim: The sim to apply posture states to.
        :return: Return a modified PostureState, ParticipantType, and Sim.
        """
        return posture_state, participant_type, sim


# The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
class _ExampleInteraction(CommonInteraction):
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        result = 1 + 1
        if result == 2:
            # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
            return cls.create_test_result(False, reason="Test Tooltip")
            # Alternative way to specify a tooltip with the text "Test Tooltip"
            # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
        if result == 3:
            # Interaction will be hidden completely.
            return TestResult.NONE
        # Interaction will display and be enabled.
        return TestResult.TRUE

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        result = True
        if not result:
            return False
        # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
        return True
