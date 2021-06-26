"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from pprint import pformat
from typing import Tuple, Any, Union, List, Set
from event_testing.results import TestResult
from interactions import ParticipantType
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from native.animation import NativeAsm
from postures.posture_state import PostureState
from sims.sim import Sim
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from singletons import DEFAULT

# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.base.interaction import Interaction
else:
    # noinspection PyMissingOrEmptyDocstring
    class MockClass(object):
        # noinspection PyMissingTypeHints,PyUnusedLocal
        def __init__(self, *args, **kwargs):
            super(MockClass, self).__init__()

        # noinspection PyMissingTypeHints
        def __call__(self, *args, **kwargs):
            return None

    # noinspection PyMissingOrEmptyDocstring
    class Interaction(MockClass):
        # noinspection PyPropertyDefinition
        @property
        def sim(self) -> Sim:
            pass

        # noinspection PyPropertyDefinition
        @property
        def target(self) -> Any:
            pass

        # noinspection PyPropertyDefinition
        @property
        def context(self) -> InteractionContext:
            pass

        # noinspection PyPropertyDefinition
        @property
        def super_affordance(self) -> Any:
            pass


class CommonInteraction(Interaction, HasClassLog):
    """CommonInteraction(...)

    An inheritable class that provides a way to create Custom Interactions.

    .. note::

       It is recommended to inherit from one of the following classes instead of :class:`CommonInteraction` directly:

       * :class:`CommonImmediateSuperInteraction`
       * :class:`CommonMixerInteraction`
       * :class:`CommonSocialMixerInteraction`
       * :class:`CommonSuperInteraction`
       * :class:`CommonTerrainInteraction`

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    def __init__(self, *_: Any, **__: Any):
        super().__init__(*_, **__)
        HasClassLog.__init__(self)

    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=TestResult.NONE)
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        try:
            test_result = cls.on_test(context.sim, target, context, **kwargs)
        except Exception as ex:
            mod_identity = cls.get_mod_identity()
            CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while running interaction \'{}\' on_test.'.format(cls.__name__), exception=ex)
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

    def _trigger_interaction_start_event(self: 'CommonInteraction'):
        try:
            super()._trigger_interaction_start_event()
            self.on_started(self.sim, self.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

    # noinspection PyMissingOrEmptyDocstring
    def apply_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT):
        try:
            (new_posture_state, new_participant_type, new_sim) = self.modify_posture_state(posture_state, participant_type=participant_type, sim=sim)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' modify_posture_state.'.format(self.__class__.__name__), exception=ex)
            return None, None, None
        return super().apply_posture_state(new_posture_state, participant_type=new_participant_type, sim=new_sim)

    def kill(self) -> bool:
        """kill()

        Kill the interaction. (Hard Cancel)

        :return: True, if the interaction was killed successfully. False, if the interaction was not killed successfully.
        :rtype: bool
        """
        try:
            self.on_killed(self.sim, self.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' on_killed.'.format(self.__class__.__name__), exception=ex)
        return super().kill()

    def cancel(self, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> bool:
        """cancel(finishing_type, cancel_reason_msg, **kwargs)

        Cancel the interaction. (Soft Cancel)

        :param finishing_type: The type of cancellation occurring.
        :type finishing_type: FinishingType
        :param cancel_reason_msg: The reason the interaction was cancelled.
        :type cancel_reason_msg: str
        :return: True, if the interaction was cancelled successfully. False, if the interaction was not cancelled successfully.
        :rtype: bool
        """
        try:
            self.on_cancelled(self.sim, self.target, finishing_type, cancel_reason_msg, **kwargs)
            return super().cancel(finishing_type, cancel_reason_msg, **kwargs)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' cancel.'.format(self.__class__.__name__), exception=ex)

    def on_reset(self: 'CommonInteraction'):
        """on_reset()

        A function that occurs upon an interaction being reset.

        """
        try:
            self._on_reset(self.sim, self.target)
            return super().on_reset()
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' on_reset.'.format(self.__class__.__name__), exception=ex)

    def _post_perform(self: 'CommonInteraction'):
        try:
            self.on_performed(self.sim, self.target)
            return super()._post_perform()
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' _post_perform.'.format(self.__class__.__name__), exception=ex)

    def send_current_progress(self, *args: Any, **kwargs: Any):
        """send_current_progress(*args, **kwargs)

        A function that occurs upon a progress bar update.

        """
        try:
            result = self._send_current_progress(self.sim, self.target, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' send_current_progress.'.format(self.__class__.__name__), exception=ex)
        return super().send_current_progress(*args, **kwargs)

    def setup_asm_default(self, asm: NativeAsm, *args, **kwargs) -> bool:
        """setup_asm_default(asm, *args, **kwargs)

        A function that occurs when setting up the Animation State Machine.

        :param asm: An instance of the Animation State Machine
        :type asm: NativeAsm
        :return: True, if the ASM was setup properly. False, if not.
        :rtype: bool
        """
        try:
            result = self._setup_asm_default(self.sim, self.target, asm, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' setup_asm_default.'.format(self.__class__.__name__), exception=ex)
        return super().setup_asm_default(asm, *args, **kwargs)

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=TestResult.NONE)
    def create_test_result(
        result: bool,
        reason: str=None,
        text_tokens: Union[Tuple[Any], List[Any], Set[Any]]=(),
        tooltip: Union[int, str, CommonLocalizationUtils.LocalizedTooltip]=None,
        icon=None,
        influence_by_active_mood: bool=False
    ) -> TestResult:
        """create_test_result(\
            result,\
            reason=None,\
            text_tokens=(),\
            tooltip=None,\
            icon=None,\
            influence_by_active_mood=False\
        )

        Create a TestResult with the specified information.

        .. note:: TestResult is an object used to disable, hide, or display tooltips on interactions. See :func:`~on_test` for more information.

        :param result: The result of a test. True for passed, False for failed.
        :type result: bool
        :param reason: The reason for the Test Result (This is displayed as a tooltip to the player when the interaction is disabled).
        :type reason: str, optional
        :param text_tokens: Any text tokens to include format into the reason.
        :type text_tokens: Union[Tuple[Any], List[Any], Set[Any]], optional
        :param tooltip: The tooltip displayed when hovering the interaction while it is disabled.
        :type tooltip: Union[int, str, LocalizedTooltip], optional
        :param icon: The icon of the outcome.
        :type icon: _resourceman.Key, optional
        :param influence_by_active_mood: If true, the Test Result will be influenced by the active mood.
        :type influence_by_active_mood: bool, optional
        :return: The desired outcome for a call of :func:`~on_test`, default is `TestResult.NONE`
        :rtype: TestResult
        """
        return TestResult(
            result,
            reason,
            *text_tokens,
            tooltip=tooltip,
            icon=icon,
            influence_by_active_mood=influence_by_active_mood
        )

    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        """on_test(interaction_sim, interaction_target, interaction_context, **kwargs)

        A hook that occurs upon the interaction being tested for availability.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: TestResult
        """
        return TestResult.TRUE

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """on_started(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being started.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        pass

    # noinspection PyUnusedLocal
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        """on_killed(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being killed.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        return True

    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs) -> None:
        """on_cancelled(interaction_sim, interaction_target, finishing_type, cancel_reason_msg, **kwargs)

        A hook that occurs upon the interaction being cancelled.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param finishing_type: The type of cancellation of the interaction.
        :type finishing_type: FinishingType
        :param cancel_reason_msg: The reason the interaction was cancelled.
        :type cancel_reason_msg: str
        """
        pass

    def _on_reset(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """_on_reset(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being reset.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        """
        pass

    def on_performed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """on_performed(interaction_sim, interaction_target)

        A hook that occurs after the interaction has been performed.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        """
        pass

    def modify_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT) -> Tuple[PostureState, ParticipantType, Sim]:
        """modify_posture_state(posture_state, participant_type=ParticipantType.Actor, sim=DEFAULT)

        A hook that allows modification of the posture state of the interactions participants.

        :param posture_state: The posture state being modified.
        :type posture_state: PostureState
        :param participant_type: The position in the interaction that the `sim` is considered at. Example: `ParticipantType.Actor` represents the source Sim of the interaction.
        :type participant_type: ParticipantType, optional
        :param sim: The Sim the posture state is being applied to.
        :type sim: Sim, optional
        :return: Return a modified PostureState, ParticipantType, and Sim.
        :rtype: Tuple[PostureState, ParticipantType, Sim]
        """
        return posture_state, participant_type, sim

    # noinspection PyUnusedLocal
    def _setup_asm_default(self, interaction_sim: Sim, interaction_target: Any, interaction_asm: NativeAsm, *args, **kwargs) -> Union[bool, None]:
        """_setup_asm_default(interaction_sim, interaction_target, asm, *args, **kwargs)

        A hook that occurs upon the animation state machine being setup for the interaction.

        .. warning:: The returned value from here replaces the original returned value. Return None from here to return the original value.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_asm: An instance of an Animation State Machine
        :type interaction_asm: NativeAsm
        :return: True, if the ASM was setup properly. False, if not. or None to run through the original code.
        :rtype: bool
        """
        return None

    # noinspection PyUnusedLocal
    def _send_current_progress(self, interaction_sim: Sim, interaction_target: Any, *args, **kwargs) -> Union[bool, None]:
        """_send_current_progress(interaction_sim, interaction_target, *args, **kwargs)

        A hook that occurs upon sending the current progress for the interaction.

        .. warning:: The returned value from here replaces the original returned value.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: True, if progress was sent successfully. False, if not. Return None to run the original code.
        :rtype: bool
        """
        return None

    def set_current_progress_bar(self, percent: float, rate_change: float, start_message: bool=True):
        """set_current_progress_bar(initial_value, progress_rate)

        Set the current progress rate of the interaction.

        :param percent: A percentage indicating the starting progress.
        :type percent: float
        :param rate_change: A value that indicates how fast progress will be made.
        :type rate_change: float
        :param start_message: If True, progress will begin changing immediately. If False, it will not. Default is True.
        :type start_message: bool, optional
        """
        try:
            self._send_progress_bar_update_msg(percent, rate_change, start_msg=start_message)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' set_current_progress_bar.'.format(self.__class__.__name__), exception=ex)


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
