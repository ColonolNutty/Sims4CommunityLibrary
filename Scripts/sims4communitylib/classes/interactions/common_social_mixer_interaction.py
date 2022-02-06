"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
import os
from singletons import DEFAULT
from typing import Any, Union, Tuple, List, Set, Iterator

from interactions import ParticipantType
from interactions.constraints import Constraint
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from native.animation import NativeAsm
from protocolbuffers.Localization_pb2 import LocalizedString
from scheduling import Timeline
from sims.sim import Sim
from sims4.utils import flexmethod
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.social.social_mixer_interaction import SocialMixerInteraction
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
    class SocialMixerInteraction(MockClass):
        pass


class CommonSocialMixerInteraction(SocialMixerInteraction, HasClassLog):
    """CommonSocialMixerInteraction(*_, **__)

    An inheritable class that provides a way to create Custom Social Mixer Interactions.

    .. note:: The main use for this class is to create interactions that involve two or more Sims interacting with each other.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonSocialMixerInteraction):
            @classmethod
            def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
                result = 1 + 1
                if result == 2:
                    # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
                    return cls.create_test_result(False, reason="Test Tooltip")
                    # Alternative way to specify a tooltip with the text "Test Tooltip"
                    # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
                if result == 3:
                    # Interaction will be hidden completely.
                    return CommonTestResult.NONE
                # Interaction will display and be enabled.
                return CommonTestResult.TRUE

            def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
                result = True
                if not result:
                    return CommonExecutionResult.FALSE
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return CommonExecutionResult.TRUE

            def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs):
                result = True
                if not result:
                    return False
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return True

    """

    __slots__ = {'context'}

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> Union[CommonModIdentity, None]:
        return None

    def __init__(self, *_: Any, **__: Any):
        super().__init__(*_, **__)
        HasClassLog.__init__(self)

    # SocialMixerInteraction has a different signature for its _test function, so we override it in here.
    @classmethod
    def _test(cls, target: Any, context: InteractionContext, *args, **kwargs) -> CommonTestResult:
        from event_testing.results import TestResult
        from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
        log = cls.get_log()
        verbose_log = cls.get_verbose_log()
        stop_watch = CommonStopWatch()
        stop_watch.start()
        try:
            try:
                verbose_log.format_with_message(
                    'Running on_test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                test_result = cls.on_test(context.sim, target, context, *args, **kwargs)
                verbose_log.format_with_message('Test Result (CommonSocialMixerInteraction)', test_result=test_result)
            except Exception as ex:
                log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' on_test.'.format(cls.__name__), exception=ex)
                return cls.create_test_result(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/mod_logs/<mod_name>_Exceptions.txt"')

            if test_result is not None:
                if isinstance(test_result, CommonTestResult):
                    if test_result.is_success is False:
                        return test_result
                elif isinstance(test_result, TestResult) and test_result.result is False:
                    if test_result.tooltip is not None:
                        tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.tooltip)
                    elif test_result.reason is not None:
                        tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.reason)
                    else:
                        tooltip = None
                    return cls.create_test_result(test_result.result, test_result.reason, tooltip=tooltip, icon=test_result.icon, influence_by_active_mood=test_result.influence_by_active_mood)

            try:
                verbose_log.format_with_message(
                    'Running super()._test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                super_test_result: TestResult = super()._test(target, context, *args, **kwargs)
                verbose_log.format_with_message('Super Test Result (CommonSocialMixerInteraction)', super_test_result=super_test_result)

                if super_test_result is not None and (isinstance(test_result, TestResult) and not super_test_result.result):
                    return CommonTestResult.convert_from_vanilla(super_test_result)
            except Exception as ex:
                log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' super()._test.'.format(cls.__name__), exception=ex)
                return cls.create_test_result(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/mod_logs/<mod_name>_Exceptions.txt"')

            try:
                verbose_log.format_with_message(
                    'Running on_post_super_test.',
                    class_name=cls.__name__,
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                post_super_test_result = cls.on_post_super_test(context.sim, target, context, *args, **kwargs)
                verbose_log.format_with_message('Post Test Result (CommonSocialMixerInteraction)', post_super_test_result=post_super_test_result)
            except Exception as ex:
                log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' on_post_super_test.'.format(cls.__name__), exception=ex)
                return cls.create_test_result(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/mod_logs/<mod_name>_Exceptions.txt"')

            if post_super_test_result is not None:
                if isinstance(post_super_test_result, CommonTestResult):
                    if post_super_test_result.is_success is False:
                        return post_super_test_result
                elif isinstance(post_super_test_result, TestResult) and post_super_test_result.result is False:
                    if post_super_test_result.tooltip is not None:
                        post_super_test_result_tooltip = CommonLocalizationUtils.create_localized_tooltip(post_super_test_result.tooltip)
                    elif post_super_test_result.reason is not None:
                        post_super_test_result_tooltip = CommonLocalizationUtils.create_localized_tooltip(post_super_test_result.reason)
                    else:
                        post_super_test_result_tooltip = None
                    return cls.create_test_result(post_super_test_result.result, post_super_test_result.reason, tooltip=post_super_test_result_tooltip, icon=post_super_test_result.icon, influence_by_active_mood=post_super_test_result.influence_by_active_mood)

            return cls.create_test_result(True)
        except Exception as ex:
            log.error('Error occurred while running _test of CommonSocialMixerInteraction \'{}\''.format(cls.__name__), exception=ex)
            return cls.create_test_result(False, f'An error occurred {ex}. See the log for more details. "The Sims 4/mod_logs/<mod_name>_Exceptions.txt"')
        finally:
            if verbose_log.enabled:
                verbose_log.format_with_message('Took {} seconds to return result from CommonSocialMixerInteraction.'.format(stop_watch.stop()), class_name=cls.__name__)
            else:
                stop_watch.stop()

    # noinspection PyMethodParameters,PyMissingOrEmptyDocstring
    @flexmethod
    def get_name(cls, inst: 'CommonSocialMixerInteraction', target: Any=DEFAULT, context: InteractionContext=DEFAULT, **interaction_parameters) -> Union[LocalizedString, None]:
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
            cls.get_log().error('An error occurred while running get_name of CommonSocialMixerInteraction {}'.format(cls.__name__), exception=ex)
        return super(CommonSocialMixerInteraction, inst_or_cls).get_name(target=target, context=context, **interaction_parameters)

    def _trigger_interaction_start_event(self: 'CommonSocialMixerInteraction'):
        try:
            self.verbose_log.format_with_message(
                'Running on_started.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            result = self.on_started(self.sim, self.target)
            if result is not None and ((isinstance(result, CommonExecutionResult) and not result.is_success) or (isinstance(result, bool) and not result)):
                self.cancel(FinishingType.CONDITIONAL_EXIT, str(result))
                return False
            return super()._trigger_interaction_start_event()
        except Exception as ex:
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

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
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' on_killed.'.format(self.__class__.__name__), exception=ex)
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
            self.verbose_log.format_with_message(
                'Running on_cancelled.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target,
                finishing_type=finishing_type,
                cancel_reason_msg=cancel_reason_msg,
                kwargles=kwargs
            )
            self.on_cancelled(self.sim, self.target, finishing_type, cancel_reason_msg, **kwargs)
        except Exception as ex:
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' cancel.'.format(self.__class__.__name__), exception=ex)
        return super().cancel(finishing_type, cancel_reason_msg, **kwargs)

    def on_reset(self: 'CommonSocialMixerInteraction'):
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
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' on_reset.'.format(self.__class__.__name__), exception=ex)
        return super().on_reset()

    def _post_perform(self: 'CommonSocialMixerInteraction'):
        super_result = super()._post_perform()
        try:
            self.verbose_log.format_with_message(
                'Running on_performed.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            self.on_performed(self.sim, self.target)
        except Exception as ex:
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' _post_perform.'.format(self.__class__.__name__), exception=ex)
        return super_result

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
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' send_current_progress.'.format(self.__class__.__name__), exception=ex)
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
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' setup_asm_default.'.format(self.__class__.__name__), exception=ex)
        return super().setup_asm_default(asm, *args, **kwargs)

    def _run_interaction_gen(self, timeline: Timeline):
        try:
            self.verbose_log.format_with_message(
                'Running on_run.',
                class_name=self.__class__.__name__,
                interaction_sim=self.sim,
                interaction_target=self.target,
                timeline=timeline
            )
            self.on_run(self.sim, self.target, timeline)
        except Exception as ex:
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        yield from super()._run_interaction_gen(timeline)

    @classmethod
    def _constraint_gen(cls, sim: Sim, target: Any, participant_type: ParticipantType=ParticipantType.Actor, interaction: 'CommonSocialMixerInteraction'=None) -> Constraint:
        inst_or_cls = interaction if interaction is not None else cls
        try:
            replacement_results = cls.on_replacement_constraints_gen(inst_or_cls, sim or inst_or_cls.sim, inst_or_cls.get_constraint_target(target) or target or inst_or_cls.target)
            if replacement_results is not None:
                if inspect.isgenerator(replacement_results):
                    yield from replacement_results
                else:
                    yield replacement_results
            else:
                yield from super()._constraint_gen(sim, target, participant_type=participant_type, interaction=interaction)
                result = cls.on_constraint_gen(inst_or_cls, sim or inst_or_cls.sim, inst_or_cls.get_constraint_target(target) or target or inst_or_cls.target)
                if result is not None:
                    if inspect.isgenerator(result):
                        yield from result
                    else:
                        yield result
        except Exception as ex:
            cls.get_log().error('Error occurred while running CommonSocialMixerInteraction \'{}\' _on_constraint_gen.'.format(cls.__name__), exception=ex)

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    # noinspection PyUnusedLocal
    @classmethod
    def on_replacement_constraints_gen(cls, inst_or_cls: 'CommonSocialMixerInteraction', sim: Sim, target: Any) -> Union[Iterator[Constraint], None]:
        """on_replacement_constraints_gen(inst_or_cls, sim, target)

        A hook that occurs before the normal constraints of an interaction, these constraints will replace the normal constraints of the interaction.

        .. note:: If None is returned, the normal constraints will be used. (Plus any additional constraints from on_constraint_gen)

        :param inst_or_cls: An instance or the class of the interaction.
        :type inst_or_cls: CommonSocialMixerInteraction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: An iterable of constraints to replace the normal constraints of the interaction or None if replacement constraints are not wanted.
        :rtype: Union[Iterator[Constraint], None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def on_constraint_gen(cls, inst_or_cls: 'CommonSocialMixerInteraction', sim: Sim, target: Any) -> Union[Iterator[Constraint], Constraint, None]:
        """on_constraint_gen(inst_or_cls, sim, target)

        A hook that occurs after generating the constraints of an interaction, this constraint will be returned in addition to the normal constraints of the interaction.

        .. note:: Return None from this function to exclude any custom constraints.

        :param inst_or_cls: An instance or the class of the interaction.
        :type inst_or_cls: CommonSocialMixerInteraction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: A constraint or an iterable of constraints to return in addition to the normal constraints or None if no additional constraints should be added.
        :rtype: Union[Iterator[Constraint], Constraint, None]
        """
        return None

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
        :return: The desired outcome for a call of :func:`~on_test`.
        :rtype: CommonTestResult
        """
        try:
            return CommonTestResult(
                result,
                reason=reason.format(*text_tokens) if reason is not None else reason,
                tooltip_text=tooltip,
                tooltip_tokens=tooltip_tokens,
                icon=icon,
                influenced_by_active_mood=influence_by_active_mood
            )
        except Exception as ex:
            cls.get_log().error('An error occurred while creating a test result for {}'.format(cls.__name__), exception=ex)

    # noinspection PyUnusedLocal
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonExecutionResult:
        """on_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs upon the interaction being tested for availability.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def on_post_super_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonExecutionResult:
        """on_post_super_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs after the interaction being tested for availability by on_test and the super _test functions.

        .. note:: This will only run if both on_test and _test returns CommonExecutionResult.TRUE or similar.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.TRUE

    # noinspection PyUnusedLocal
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
        """on_started(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being started.

        .. note:: If CommonExecutionResult.FALSE, CommonExecutionResult.NONE, or False is returned from here, then the interaction will be cancelled instead of starting.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.TRUE

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

    @classmethod
    def _create_override_display_name(
        cls,
        interaction_sim: Sim,
        interaction_target: Any,
        interaction: 'CommonSocialMixerInteraction'=None,
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
        :type interaction: CommonSocialMixerInteraction
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
            self.log.error('Error occurred while running CommonSocialMixerInteraction \'{}\' set_current_progress_bar.'.format(self.__class__.__name__), exception=ex)

    # noinspection PyUnusedLocal
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline: Timeline):
        """on_run(interaction_sim, interaction_target, timeline)

        A hook that occurs upon the interaction being run.

        :param interaction_sim: The sim performing the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target of the interaction.
        :type interaction_target: Any
        :param timeline: The timeline the interaction is running on.
        :type timeline: Timeline
        """
        pass
