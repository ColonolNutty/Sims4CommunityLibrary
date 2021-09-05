"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any, Union, Tuple

from interactions import ParticipantType
from interactions.interaction_finisher import FinishingType
from postures.posture_state import PostureState
from sims4communitylib.classes.interactions.common_super_interaction import CommonSuperInteraction
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

# ReadTheDocs
from singletons import DEFAULT

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.social.social_super_interaction import SocialSuperInteraction
    from event_testing.results import TestResult
    from interactions.context import InteractionContext
    from native.animation import NativeAsm
    from scheduling import Timeline
    from sims.sim import Sim
    from sims4.utils import classproperty, flexmethod
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
    class SocialSuperInteraction(MockClass):
        pass


    # noinspection PyMissingOrEmptyDocstring
    class TestResult:
        pass


    # noinspection PyMissingOrEmptyDocstring
    class Sim:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass


    # noinspection PyMissingOrEmptyDocstring
    class NativeAsm:
        pass


    # noinspection PyMissingOrEmptyDocstring
    class InteractionContext:
        pass


    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring,SpellCheckingInspection
    def flexmethod(*_, **__):
        pass

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring,SpellCheckingInspection
    def classproperty(*_, **__):
        pass


class CommonSocialSuperInteraction(SocialSuperInteraction, CommonSuperInteraction):
    """An inheritable class that provides a way to create Custom Social Super Interactions.

    .. note::

        The main use for this class is to create interactions that wrap sub interactions.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonSocialSuperInteraction):
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
                    return TestResult.NONE
                # Interaction will display and be enabled.
                return TestResult.TRUE

            # Instead of on_started, SocialSuperInteractions use on_run.
            def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline: Timeline) -> bool:
                result = True
                if not result:
                    return False
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return True

            def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, **kwargs):
                result = True
                if not result:
                    return False
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return True

    """

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring,PyMethodParameters
    @classproperty
    def is_social(cls):
        return super().is_social

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    @property
    def social_group(self):
        return super().social_group

    # noinspection PyMissingTypeHints
    @staticmethod
    def _tunable_tests_enabled():
        return SocialSuperInteraction._tunable_tests_enabled()

    def _run_interaction_gen(self, timeline: Timeline):
        super()._run_interaction_gen(timeline)
        try:
            self.verbose_log.format_with_message(
                'Running \'{}\' on_run.'.format(self.__class__.__name__),
                interaction_sim=self.sim,
                interaction_target=self.target,
                timeline=timeline
            )
            return self.on_run(self.sim, self.target, timeline)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        return super()._run_interaction_gen(timeline)

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

    def _trigger_interaction_start_event(self: 'CommonSocialSuperInteraction'):
        try:
            super()._trigger_interaction_start_event()
            from interactions import ParticipantType
            target = self.get_participant(ParticipantType.TargetSim)
            self.verbose_log.format_with_message(
                'Running \'{}\' on_started.'.format(self.__class__.__name__),
                interaction_sim=self.context.sim,
                interaction_target=target
            )
            self.on_started(self.context.sim, target)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

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

    def _post_perform(self: 'CommonSocialSuperInteraction'):
        try:
            self.verbose_log.format_with_message(
                'Running on_performed.',
                class_name=self.__class__.__name__,
                sim=self.sim,
                target=self.target
            )
            self.on_performed(self.sim, self.target)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' _post_perform.'.format(self.__class__.__name__), exception=ex)
        return super()._post_perform()

    def on_performed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """on_performed(interaction_sim, interaction_target)

        A hook that occurs after the interaction has been performed.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        """
        pass

    # noinspection PyMissingOrEmptyDocstring
    def setup_asm_default(self, asm: NativeAsm, *args, **kwargs) -> bool:
        try:
            result = self._setup_asm_default(self.sim, self.target, asm, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' setup_asm_default.'.format(self.__class__.__name__), exception=ex)
        return super().setup_asm_default(asm, *args, **kwargs)

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

    # noinspection PyMissingOrEmptyDocstring
    def apply_posture_state(self, posture_state: PostureState, participant_type: ParticipantType=ParticipantType.Actor, **kwargs):
        try:
            self.verbose_log.format_with_message(
                'Running modify_posture_state.',
                class_name=self.__class__.__name__,
                posture_state=posture_state,
                participant_type=participant_type,
                sim=self.sim,
                kwargles=kwargs
            )
            (new_posture_state, new_participant_type, new_sim) = self.modify_posture_state(posture_state, participant_type=participant_type, sim=self.sim)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' modify_posture_state.'.format(self.__class__.__name__), exception=ex)
            return None, None, None
        kwargs['sim'] = new_sim
        return super().apply_posture_state(new_posture_state, participant_type=new_participant_type, **kwargs)

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

    # SocialSuperInteraction has a different signature for its _test function, so we override it in here.
    # noinspection PyMethodParameters
    @flexmethod
    def _test(cls, inst, target: Any, context: InteractionContext, *args, **kwargs) -> TestResult:
        from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
        stop_watch = CommonStopWatch()
        stop_watch.start()
        try:
            inst_or_cls = inst if inst is not None else cls
            try:
                if context.sim is target:
                    cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                    return TestResult(False, 'Cannot run a social as a self interaction.')
                if target is None:
                    cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                    return TestResult(False, 'Cannot run a social with no target.')
                if target.is_sim and target.socials_locked:
                    cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                    return TestResult(False, 'Cannot socialize with a Sim who has socials_locked set to true. This Sim is leaving the lot.')
                if context.source == context.SOURCE_AUTONOMY:
                    sim = inst.sim if inst is not None else context.sim
                    social_group = cls._get_social_group_for_sim(sim)
                    if social_group is not None and target in social_group:
                        attached_si = social_group.get_si_registered_for_sim(sim, affordance=cls)
                        if inst is not None:
                            if attached_si is not inst:
                                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                                return TestResult(False, 'Cannot run social since sim already has an interaction that is registered to group.')
                        else:
                            cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                            return TestResult(False, 'Sim {} is already running matching affordance:{} ', sim, cls)

                cls.get_verbose_log().format_with_message(
                    'Running \'{}\' on_test.'.format(cls.__name__),
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                test_result = cls.on_test(context.sim, target, context, *args, **kwargs)
                cls.get_verbose_log().format_with_message('Test Result', test_result=test_result)
            except Exception as ex:
                cls.get_log().error('Error occurred while running interaction \'{}\' on_test.'.format(cls.__name__), exception=ex)
                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return TestResult.NONE

            if test_result is not None and isinstance(test_result, TestResult) and test_result.result is False:
                if test_result.tooltip is not None:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.tooltip)
                elif test_result.reason is not None:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.reason)
                else:
                    tooltip = None
                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return cls.create_test_result(test_result.result, test_result.reason, tooltip=tooltip, icon=test_result.icon, influence_by_active_mood=test_result.influence_by_active_mood)

            try:
                cls.get_verbose_log().format_with_message(
                    'Running \'{}\' super()._test.'.format(cls.__name__),
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                super_test_result = super(CommonSocialSuperInteraction, inst_or_cls)._test(target, context, **kwargs)
                cls.get_verbose_log().format_with_message('Super Test Result', super_test_result=super_test_result)
            except Exception as ex:
                cls.get_log().error('Error occurred while running interaction \'{}\' super()._test.'.format(cls.__name__), exception=ex)
                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return TestResult.NONE

            if super_test_result is not None and not super_test_result.result:
                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return super_test_result

            try:
                cls.get_verbose_log().format_with_message(
                    'Running \'{}\' on_post_super_test.'.format(cls.__name__),
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                post_super_test_result = cls.on_post_super_test(context.sim, target, context, *args, **kwargs)
                cls.get_verbose_log().format_with_message('Post Test Result', post_super_test_result=post_super_test_result)
            except Exception as ex:
                cls.get_log().error('Error occurred while running interaction \'{}\' on_post_super_test.'.format(cls.__name__), exception=ex)
                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return TestResult.NONE

            if post_super_test_result is not None and isinstance(test_result, TestResult) and post_super_test_result.result is False:
                if post_super_test_result.tooltip is not None:
                    post_super_test_result_tooltip = CommonLocalizationUtils.create_localized_tooltip(post_super_test_result.tooltip)
                elif post_super_test_result.reason is not None:
                    post_super_test_result_tooltip = CommonLocalizationUtils.create_localized_tooltip(post_super_test_result.reason)
                else:
                    post_super_test_result_tooltip = None
                cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
                return cls.create_test_result(post_super_test_result.result, post_super_test_result.reason, tooltip=post_super_test_result_tooltip, icon=post_super_test_result.icon, influence_by_active_mood=post_super_test_result.influence_by_active_mood)

            cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
            return TestResult.TRUE
        except Exception as ex:
            cls.get_log().error('Error occurred while running _test of interaction \'{}\''.format(cls.__name__), exception=ex)
        cls.get_log().format_with_message('Took {} seconds to return result from interaction.'.format(stop_watch.stop()), class_name=cls.__name__)
        return TestResult(False)

    # noinspection SpellCheckingInspection
    def _cancel(self, finishing_type: FinishingType, *args, propagate_cancelation_to_socials: bool=True, **kwargs) -> bool:
        existing_kwargs = dict(kwargs)
        try:
            if len(args) > 0:
                cancel_reason_msg = args[0]
                new_args = list(args)[1:0]
            else:
                cancel_reason_msg = 'Unknown Cancel Reason.'
                new_args = args
                if 'cancel_reason_msg' in kwargs:
                    cancel_reason_msg = kwargs['cancel_reason_msg']
                    del kwargs['cancel_reason_msg']
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
            self.on_cancelled(self.sim, self.target, finishing_type, cancel_reason_msg, *new_args, **kwargs)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' cancel.'.format(self.__class__.__name__), exception=ex)
        return super()._cancel(finishing_type, *args, propagate_cancelation_to_socials=propagate_cancelation_to_socials, **existing_kwargs)

    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
        """on_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

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

    @classmethod
    def on_post_super_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
        """on_post_super_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

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
