"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Any, Union, List, Set
from event_testing.results import TestResult
from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from postures.posture_state import PostureState
from sims.sim import Sim
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from singletons import DEFAULT


class CommonInteraction(Interaction, HasLog):
    """Enables hooks into the functionality of an Interaction

    """
    def __init__(self, *_, **__):
        super().__init__(*_, **__)
        HasLog.__init__(self)

    @property
    def mod_identity(self) -> CommonModIdentity:
        """The Identity of the mod that owns this class.

        """
        return ModInfo.get_identity()

    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=TestResult.NONE)
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        try:
            test_result = cls.on_test(context.sim, target, context, **kwargs)
        except Exception as ex:
            try:
                if hasattr(cls, 'mod_identity'):
                    mod_identity = cls.mod_identity
                else:
                    mod_identity = ModInfo.get_identity()
            except Exception as ex1:
                mod_identity = ModInfo.get_identity()
                CommonExceptionHandler.log_exception(mod_identity.name, 'Error occurred attempting to retrieve mod info for interaction {}.'.format(cls.__name__), exception=ex1)
            CommonExceptionHandler.log_exception(mod_identity.name, 'Error occurred while running interaction \'{}\' on_test.'.format(cls.__name__), exception=ex)
            return TestResult.NONE
        if test_result is None:
            return super()._test(target, context, **kwargs)
        if not isinstance(test_result, TestResult):
            raise RuntimeError('Interaction on_test did not result in a TestResult, instead got {}. {}'.format(pformat(test_result), cls.__name__))
        if test_result.result is False:
            if test_result.tooltip is not None:
                tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.tooltip)
            elif test_result.reason is not None:
                tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.reason)
            else:
                tooltip = None
            return cls.create_test_result(test_result.result, test_result.reason, tooltip=tooltip)
        return super()._test(target, context, **kwargs)

    def _trigger_interaction_start_event(self):
        try:
            super()._trigger_interaction_start_event()
            self.on_started(self.sim, self.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while running interaction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

    def apply_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT):
        """Apply a posture to a sim.

        :param posture_state: The posture state to apply.
        :param participant_type: The ParticipantType of the actor.
        :param sim: The sim to apply posture states to.
        :return: Unknown
        """
        try:
            (new_posture_state, new_participant_type, new_sim) = self.modify_posture_state(posture_state, participant_type=participant_type, sim=sim)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while running interaction \'{}\' modify_posture_state.'.format(self.__class__.__name__), exception=ex)
            return None, None, None
        return super().apply_posture_state(new_posture_state, participant_type=new_participant_type, sim=new_sim)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def kill(self) -> bool:
        """Kill the interaction. (Hard Cancel)

        """
        try:
            self.on_killed(self.sim, self.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while running interaction \'{}\' on_killed.'.format(self.__class__.__name__), exception=ex)
        return super().kill()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def cancel(self, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> bool:
        """Cancel the interaction.

        :param finishing_type: The type of cancellation occurring.
        :param cancel_reason_msg: The reason it was cancelled.
        :return: True if cancellation is successful, False if cancellation failed.
        """
        try:
            self.on_cancelled(self.sim, self.target, finishing_type, cancel_reason_msg, **kwargs)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while running interaction \'{}\' on_cancelled.'.format(self.__class__.__name__), exception=ex)
        return super().cancel(finishing_type, cancel_reason_msg, **kwargs)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def on_reset(self) -> None:
        """Occurs upon the interaction being reset.

        """
        try:
            self._on_reset(self.sim, self.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while running interaction \'{}\' _on_reset.'.format(self.__class__.__name__), exception=ex)
        return super().on_reset()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def _post_perform(self):
        try:
            self.on_performed(self.sim, self.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'Error occurred while running interaction \'{}\' on_performed.'.format(self.__class__.__name__), exception=ex)
        return super()._post_perform()

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=TestResult.NONE)
    def create_test_result(result: bool, reason: str=None, text_tokens: Union[Tuple[Any], List[Any], Set[Any]]=(), tooltip: Union[int, str, CommonLocalizationUtils.LocalizedTooltip]=None, icon=None, influence_by_active_mood: bool=False) -> TestResult:
        """Create a TestResult with the specified information.

        :param result: The result of a test. True for passed, False for failed.
        :param reason: The reason for the Test Result (This is displayed as a tooltip to the player when the interaction is disabled).
        :param text_tokens: Any text tokens to include format into the reason.
        :param tooltip: The tooltip displayed when hovering the interaction while it is disabled.
        :param icon: The icon of the outcome.
        :param influence_by_active_mood: If true, the Test Result will be influenced by the active mood.
        :return: An object of type TestResult.
        """
        return TestResult(result, reason, *text_tokens, tooltip=tooltip, icon=icon, influence_by_active_mood=influence_by_active_mood)

    # noinspection PyUnusedLocal
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        """A hook that occurs upon the interaction being tested for run.

        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :param interaction_context: The context of the interaction.
        :return The result of successfully running the test.
        """
        return TestResult.TRUE

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """Occurs upon the interaction being started.

        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :return: True if the interaction hook was executed successfully.
        """
        pass

    # noinspection PyUnusedLocal
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """Occurs upon the interaction being killed.

        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :return: True if the interaction hook was executed successfully.
        """
        return True

    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> None:
        """Occurs upon the interaction being cancelled.

        :param interaction_sim: The sim performing the interaction.
        :param interaction_target: The target of the interaction.
        :param finishing_type: The type of cancellation.
        :param cancel_reason_msg: The reason for the cancellation.
        """
        pass

    def _on_reset(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """Occurs upon the interaction being reset.

        :param interaction_sim: The source Sim of the interaction.
        :param interaction_target: The target Sim of the interaction.
        """
        pass

    def on_performed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """Occurs after the interaction has been performed.

        :param interaction_sim: The source Sim of the interaction.
        :param interaction_target: The target Sim of the interaction.
        """
        pass

    def modify_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT) -> Tuple[PostureState, ParticipantType, Any]:
        """Modify the posture state, participant type or sim of the interaction.

        :param posture_state: The posture state to modify.
        :param participant_type: The ParticipantType of the actor to modify.
        :param sim: The sim to apply posture states to.
        :return: Return a modified PostureState, ParticipantType, and Sim.
        """
        return posture_state, participant_type, sim


# The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
class _ExampleInteraction(CommonInteraction):
    # noinspection PyMissingOrEmptyDocstring
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

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        result = True
        if not result:
            return False
        # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
        return True
