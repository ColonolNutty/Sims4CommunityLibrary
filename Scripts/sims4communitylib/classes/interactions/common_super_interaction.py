"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any, Union, Tuple, List, Set, Iterator

from event_testing.results import TestResult
from interactions import ParticipantType
from interactions.constraints import Constraint
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from native.animation import NativeAsm
from postures.posture_state import PostureState
from protocolbuffers.Localization_pb2 import LocalizedString

# ReadTheDocs
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from singletons import DEFAULT

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.base.super_interaction import SuperInteraction
    from scheduling import Timeline
    from sims4.utils import flexmethod
    from sims.sim import Sim
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
    class SuperInteraction(MockClass):
        pass


    # noinspection PyMissingOrEmptyDocstring
    class Sim:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass


    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring,SpellCheckingInspection
    def flexmethod(*_, **__):
        pass


class CommonBaseSuperInteraction(SuperInteraction, HasClassLog):
    """CommonBaseSuperInteraction(*_, **__)

    An inheritable class that provides a way to create custom Super Interactions.

    .. note:: Use this Base class when you don't wish _run_interaction_gen to be overridden.

    .. note::

        The main use for this class is to create interactions that wrap sub interactions.
        One example Super interaction is the `sim-chat` interaction, where other interactions (Such as the `Get To Know` interaction), run as sub interactions of `sim-chat`

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonBaseSuperInteraction):
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

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> Union[CommonModIdentity, None]:
        return None

    def __init__(self, *_: Any, **__: Any):
        super().__init__(*_, **__)
        HasClassLog.__init__(self)


class CommonSuperInteraction(CommonBaseSuperInteraction):
    """CommonSuperInteraction(*_, **__)

    An inheritable class that provides a way to create custom Super Interactions.

    .. note::

        The main use for this class is to create interactions that wrap sub interactions.
        One example Super interaction is the `sim-chat` interaction, where other interactions (Such as the `Get To Know` interaction), run as sub interactions of `sim-chat`

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonSuperInteraction):
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

            # Instead of on_started, SuperInteractions use on_run.
            def on_run(self, interaction_sim: Sim, interaction_target: Any: timeline: Timeline) -> bool:
                result = True
                if not result:
                    return False
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return True
    """

    @classmethod
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
        stop_watch = CommonStopWatch()
        stop_watch.start()
        try:
            try:
                cls.get_verbose_log().format_with_message(
                    'Running on_test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    kwargles=kwargs
                )
                test_result = cls.on_test(context.sim, target, context, **kwargs)
                cls.get_verbose_log().format_with_message('Test Result (CommonSuperInteraction)', test_result=test_result)
            except Exception as ex:
                cls.get_log().error('Error occurred while running super interaction \'{}\' on_test.'.format(cls.__name__), exception=ex)
                cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return TestResult.NONE

            if test_result is not None and isinstance(test_result, TestResult) and test_result.result is False:
                if test_result.tooltip is not None:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.tooltip)
                elif test_result.reason is not None:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.reason)
                else:
                    tooltip = None
                cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return cls.create_test_result(test_result.result, test_result.reason, tooltip=tooltip, icon=test_result.icon, influence_by_active_mood=test_result.influence_by_active_mood)

            try:
                cls.get_verbose_log().format_with_message(
                    'Running super()._test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    kwargles=kwargs
                )
                super_test_result: TestResult = super()._test(target, context, **kwargs)
                cls.get_verbose_log().format_with_message('Super Test Result (CommonSuperInteraction)', super_test_result=super_test_result)
            except Exception as ex:
                cls.get_log().error('Error occurred while running super interaction \'{}\' super()._test.'.format(cls.__name__), exception=ex)
                cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return TestResult.NONE

            if super_test_result is not None and not super_test_result.result:
                cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return super_test_result

            try:
                cls.get_verbose_log().format_with_message(
                    'Running on_post_super_test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    kwargles=kwargs
                )
                post_super_test_result = cls.on_post_super_test(context.sim, target, context, **kwargs)
                cls.get_verbose_log().format_with_message('Post Test Result (CommonSuperInteraction)', post_super_test_result=post_super_test_result)
            except Exception as ex:
                cls.get_log().error('Error occurred while running super interaction \'{}\' on_post_super_test.'.format(cls.__name__), exception=ex)
                cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return TestResult.NONE

            if post_super_test_result is not None and isinstance(test_result, TestResult) and post_super_test_result.result is False:
                if post_super_test_result.tooltip is not None:
                    post_super_test_result_tooltip = CommonLocalizationUtils.create_localized_tooltip(post_super_test_result.tooltip)
                elif post_super_test_result.reason is not None:
                    post_super_test_result_tooltip = CommonLocalizationUtils.create_localized_tooltip(post_super_test_result.reason)
                else:
                    post_super_test_result_tooltip = None
                cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return cls.create_test_result(post_super_test_result.result, post_super_test_result.reason, tooltip=post_super_test_result_tooltip, icon=post_super_test_result.icon, influence_by_active_mood=post_super_test_result.influence_by_active_mood)

            cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
            return TestResult.TRUE
        except Exception as ex:
            cls.get_log().error('Error occurred while running _test of interaction \'{}\''.format(cls.__name__), exception=ex)
        cls.get_verbose_log().format_with_message('Took {} seconds to return result from super interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
        return TestResult(False)

    # noinspection PyMethodParameters,PyMissingOrEmptyDocstring
    @flexmethod
    def get_name(cls, inst: 'CommonSuperInteraction', target: Any=DEFAULT, context: InteractionContext=DEFAULT, **interaction_parameters) -> Union[LocalizedString, None]:
        inst_or_cls = inst or cls
        try:
            context_inst_or_cls = context or inst_or_cls
            interaction_sim = context_inst_or_cls.sim
            interaction_target = target or context_inst_or_cls.target

            cls.get_verbose_log().format_with_message(
                'Running get_name.',
                class_name=cls.__name__,
                interaction_sim=interaction_sim,
                interaction_target=interaction_target,
                interaction=inst,
                interaction_context=context
            )
            override_name = cls._create_override_display_name(
                interaction_sim,
                interaction_target,
                interaction=inst,
                interaction_context=context,
                **interaction_parameters
            )
            if override_name is not None:
                return override_name
        except Exception as ex:
            cls.get_log().error('An error occurred while running get_name of super interaction {}'.format(cls.__name__), exception=ex)
        return super(CommonSuperInteraction, inst_or_cls).get_name(target=target, context=context, **interaction_parameters)

    def _trigger_interaction_start_event(self: 'CommonSuperInteraction'):
        try:
            super_result = super()._trigger_interaction_start_event()
            self.verbose_log.format_with_message(
                'Running on_started.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            if not self.on_started(self.sim, self.target):
                return False
            return super_result
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

    # noinspection PyMissingOrEmptyDocstring
    def apply_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, sim: Sim=DEFAULT):
        try:
            self.verbose_log.format_with_message(
                'Running modify_posture_state.',
                class_name=self.__class__.__name__,
                posture_state=posture_state,
                participant_type=participant_type,
                sim=sim
            )
            (new_posture_state, new_participant_type, new_sim) = self.modify_posture_state(posture_state, participant_type=participant_type, sim=sim)
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' modify_posture_state.'.format(self.__class__.__name__), exception=ex)
            return None, None, None
        return super().apply_posture_state(new_posture_state, participant_type=new_participant_type, sim=new_sim)

    def kill(self) -> bool:
        """kill()

        Kill the interaction. (Hard Cancel)

        :return: True, if the interaction was killed successfully. False, if the interaction was not killed successfully.
        :rtype: bool
        """
        try:
            self.verbose_log.format_with_message(
                'Running on_killed.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            self.on_killed(self.sim, self.target)
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' on_killed.'.format(self.__class__.__name__), exception=ex)
        return super().kill()

    def _cancel(self, finishing_type: FinishingType, cancel_reason_msg: str, *args, **kwargs) -> bool:
        """cancel(finishing_type, cancel_reason_msg, *args, **kwargs)

        Cancel the interaction. (Soft Cancel)

        :param finishing_type: The type of cancellation occurring.
        :type finishing_type: FinishingType
        :param cancel_reason_msg: The reason the interaction was cancelled.
        :type cancel_reason_msg: str
        :return: True, if the interaction was cancelled successfully. False, if the interaction was not cancelled successfully.
        :rtype: bool
        """
        try:
            self.verbose_log.format_with_message(
                'Running on_cancelled.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target,
                finishing_type=finishing_type,
                cancel_reason_msg=cancel_reason_msg,
                argles=args,
                kwargles=kwargs
            )
            self.on_cancelled(self.sim, self.target, finishing_type, cancel_reason_msg, *args, **kwargs)
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' cancel.'.format(self.__class__.__name__), exception=ex)
        return super()._cancel(finishing_type, cancel_reason_msg, *args, **kwargs)

    def on_reset(self: 'CommonSuperInteraction'):
        """on_reset()

        A function that occurs upon an interaction being reset.

        """
        try:
            self.verbose_log.format_with_message(
                'Running on_reset.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            self._on_reset(self.sim, self.target)
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' on_reset.'.format(self.__class__.__name__), exception=ex)
        return super().on_reset()

    def _post_perform(self: 'CommonSuperInteraction'):
        try:
            self.verbose_log.format_with_message(
                'Running on_performed.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            self.on_performed(self.sim, self.target)
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' _post_perform.'.format(self.__class__.__name__), exception=ex)
        return super()._post_perform()

    def send_current_progress(self, *args: Any, **kwargs: Any):
        """send_current_progress(*args, **kwargs)

        A function that occurs upon a progress bar update.

        """
        try:
            self.verbose_log.format_with_message(
                'Running _send_current_progress.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target,
                argles=args,
                kwargles=kwargs
            )
            result = self._send_current_progress(self.sim, self.target, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' send_current_progress.'.format(self.__class__.__name__), exception=ex)
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
            self.verbose_log.format_with_message(
                'Running _setup_asm_default.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target,
                asm=asm,
                argles=args,
                kwargles=kwargs
            )
            result = self._setup_asm_default(self.sim, self.target, asm, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' setup_asm_default.'.format(self.__class__.__name__), exception=ex)
        return super().setup_asm_default(asm, *args, **kwargs)

    def _run_interaction_gen(self, timeline: Timeline):
        super_run_result = super()._run_interaction_gen(timeline)
        try:
            self.verbose_log.format_with_message(
                'Running on_run.',
                class_name=self.__class__.__name__,
                interaction_sim=self.sim,
                interaction_target=self.target,
                timeline=timeline
            )
            if not self.on_run(self.sim, self.target, timeline):
                return False
            return super_run_result
        except Exception as ex:
            self.log.error('Error occurred while running super interaction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        return False

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    @classmethod
    def create_test_result(
        cls,
        result: bool,
        reason: str=None,
        text_tokens: Union[Tuple[Any], List[Any], Set[Any]]=(),
        tooltip: Union[int, str, CommonLocalizationUtils.LocalizedTooltip]=None,
        tooltip_tokens: Iterator[Any]=(),
        icon=None,
        influence_by_active_mood: bool=False
    ) -> CommonTestResult:
        """create_test_result(\
            result,\
            reason=None,\
            text_tokens=(),\
            tooltip=None,\
            tooltip_tokens=(),\
            icon=None,\
            influence_by_active_mood=False\
        )

        Create a CommonTestResult with the specified information.

        .. note:: CommonTestResult is an object used to disable, hide, or display tooltips on interactions. See :func:`~on_test` for more information.

        :param result: The result of a test. True for passed, False for failed.
        :type result: bool
        :param reason: The reason for the Test Result (This is displayed as a tooltip to the player when the interaction is disabled).
        :type reason: str, optional
        :param text_tokens: Any text tokens to include format into the reason.
        :type text_tokens: Union[Tuple[Any], List[Any], Set[Any]], optional
        :param tooltip: The tooltip displayed when hovering the interaction while it is disabled.
        :type tooltip: Union[int, str, LocalizedTooltip], optional
        :param tooltip_tokens: A collection of objects to format into the localized tooltip. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few) Default is an empty collection.
        :type tooltip_tokens: Iterable[Any], optional
        :param icon: The icon of the outcome.
        :type icon: CommonResourceKey, optional
        :param influence_by_active_mood: If true, the Test Result will be influenced by the active mood.
        :type influence_by_active_mood: bool, optional
        :return: The desired outcome for a call of :func:`~on_test`, default is `CommonTestResult.NONE`
        :rtype: CommonTestResult
        """
        try:
            return CommonTestResult(
                result,
                reason.format(*text_tokens) if reason is not None else reason,
                tooltip_text=tooltip,
                tooltip_tokens=tooltip_tokens,
                icon=icon,
                influenced_by_active_mood=influence_by_active_mood
            )
        except Exception as ex:
            cls.get_log().error('An error occurred while creating a test result for {}'.format(cls.__name__), exception=ex)

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

    # noinspection PyUnusedLocal
    @classmethod
    def on_post_super_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        """on_post_super_test(interaction_sim, interaction_target, interaction_context, **kwargs)

        A hook that occurs after the interaction being tested for availability by on_test and the super _test functions.

        .. note:: This will only run if both on_test and _test returns TestResult.TRUE or similar.

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

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> None:
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
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """on_killed(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being killed.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        pass

    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, *args, **kwargs) -> None:
        """on_cancelled(interaction_sim, interaction_target, finishing_type, cancel_reason_msg, *args, **kwargs)

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

    @classmethod
    def _create_override_display_name(
        cls,
        interaction_sim: Sim,
        interaction_target: Any,
        interaction: 'CommonSuperInteraction'=None,
        interaction_context: InteractionContext=None,
        **interaction_parameters
    ) -> Union[LocalizedString, None]:
        """_create_override_display_name(\
            interaction_sim,\
            interaction_target,\
            interaction=None,\
            interaction_context=None,\
            **interaction_parameters\
        )

        If overridden you may supply a custom name for the interaction to display.

        .. warning:: The returned value from here replaces the original returned value. Return None from here to return the original value.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction: The interaction being performed or None.
        :type interaction: CommonSuperInteraction
        :param interaction_context: The context of the interaction being performed or None.
        :type interaction_context: InteractionContext
        :param interaction_parameters: Parameters for the interaction.
        :type interaction_parameters: Iterator[Any]
        :return: The name to use in place of the original name of the interaction or None if you want the original name to be used.
        :rtype: Union[LocalizedString, None]
        """
        pass

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
            self.log.error('Error occurred while running super interaction \'{}\' set_current_progress_bar.'.format(self.__class__.__name__), exception=ex)

    # noinspection PyUnusedLocal
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline: Timeline) -> bool:
        """on_run(interaction_sim, interaction_target, timeline)

        A hook that occurs upon the interaction being run.

        :param interaction_sim: The sim performing the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target of the interaction.
        :type interaction_target: Any
        :param timeline: The timeline the interaction is running on.
        :type timeline: Timeline
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        return True


class CommonConstrainedSuperInteraction(CommonSuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions that provide custom constraints.

    .. note:: For more information see :class:`.CommonSuperInteraction`.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    """

    # noinspection PyMethodParameters
    @flexmethod
    def _constraint_gen(cls, inst: 'CommonConstrainedSuperInteraction', sim: Sim, target: Any, participant_type: ParticipantType=ParticipantType.Actor, **kwargs) -> Constraint:
        inst_or_cls = inst if inst is not None else cls
        try:
            result = cls.on_constraint_gen(inst if inst is not None else cls, sim or inst_or_cls.sim, target or inst_or_cls.target)
            if result is not None:
                yield result
            else:
                return super(CommonConstrainedSuperInteraction, inst_or_cls)._constraint_gen(sim, target, participant_type=participant_type, **kwargs)
        except Exception as ex:
            cls.get_log().error('Error occurred while running super interaction \'{}\' _on_constraint_gen.'.format(cls.__name__), exception=ex)

    @classmethod
    def on_constraint_gen(cls, inst: 'CommonConstrainedSuperInteraction', sim: Sim, target: Any) -> Union[Constraint, None]:
        """on_constraint_gen(inst, sim, target)

        A hook that occurs when generating the constraints of an interaction to enable modification or replacement of the constraints.

        .. note:: Return None from this function to use the original constraints.

        :param inst: An instance of the interaction.
        :type inst: CommonConstrainedSuperInteraction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: The constraints of the interaction.
        :rtype: Union[Constraint, None]
        """
        raise NotImplementedError()
