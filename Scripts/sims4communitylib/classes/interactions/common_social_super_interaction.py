"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from pprint import pformat
from typing import Any
from sims4communitylib.classes.interactions.common_super_interaction import CommonSuperInteraction
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

# ReadTheDocs
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
            self.log.format_with_message(
                'Running \'{}\' on_run.'.format(self.__class__.__name__),
                interaction_sim=self.sim,
                interaction_target=self.target,
                timeline=timeline
            )
            return self.on_run(self.sim, self.target, timeline)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        return False

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
            self.log.format_with_message(
                'Running \'{}\' on_started.'.format(self.__class__.__name__),
                interaction_sim=self.context.sim,
                interaction_target=target
            )
            self.on_started(self.context.sim, target)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

    # noinspection PyMissingOrEmptyDocstring
    def setup_asm_default(self, asm: NativeAsm, *args, **kwargs) -> bool:
        try:
            result = self._setup_asm_default(self.sim, self.target, asm, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' setup_asm_default.'.format(self.__class__.__name__), exception=ex)
        return super().setup_asm_default(asm, *args, **kwargs)

    # SocialSuperInteraction has a different signature for its _test function, so we override it in here.
    # noinspection PyMethodParameters
    @flexmethod
    def _test(cls, inst, target: Any, context: InteractionContext, *args, **kwargs) -> TestResult:
        try:
            inst_or_cls = inst if inst is not None else cls
            try:
                if context.sim is target:
                    return TestResult(False, 'Cannot run a social as a self interaction.')
                if target is None:
                    return TestResult(False, 'Cannot run a social with no target.')
                if target.is_sim and target.socials_locked:
                    return TestResult(False, 'Cannot socialize with a Sim who has socials_locked set to true. This Sim is leaving the lot.')
                if context.source == context.SOURCE_AUTONOMY:
                    sim = inst.sim if inst is not None else context.sim
                    social_group = cls._get_social_group_for_sim(sim)
                    if social_group is not None and target in social_group:
                        attached_si = social_group.get_si_registered_for_sim(sim, affordance=cls)
                        if inst is not None:
                            if attached_si is not inst:
                                return TestResult(False, 'Cannot run social since sim already has an interaction that is registered to group.')
                        else:
                            return TestResult(False, 'Sim {} is already running matching affordance:{} ', sim, cls)
                cls.get_log().format_with_message(
                    'Running \'{}\' on_test.'.format(cls.__name__),
                    interaction_sim=context.sim,
                    interaction_target=target,
                    interaction_context=context,
                    argles=args,
                    kwargles=kwargs
                )
                test_result = cls.on_test(context.sim, target, context, *args, **kwargs)
            except Exception as ex:
                cls.get_log().error('Error occurred while running interaction \'{}\' on_test.'.format(cls.__name__), exception=ex)
                return TestResult.NONE

            if test_result is None:
                return super(CommonSocialSuperInteraction, inst_or_cls)._test(target, context, *args, **kwargs)
            if not isinstance(test_result, TestResult):
                raise RuntimeError('SocialSuperInteraction on_test did not result in a TestResult, instead got {}. {}'.format(pformat(test_result), cls.__name__))
            if test_result.result is False:
                if test_result.tooltip is not None:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.tooltip)
                elif test_result.reason is not None:
                    tooltip = CommonLocalizationUtils.create_localized_tooltip(test_result.reason)
                else:
                    tooltip = None
                return cls.create_test_result(test_result.result, test_result.reason, tooltip=tooltip)
            return super(CommonSocialSuperInteraction, inst_or_cls)._test(target, context, *args, **kwargs)
        except Exception as ex:
            cls.get_log().error('Error occurred while running _test of interaction \'{}\''.format(cls.__name__), exception=ex)
        return TestResult(False)

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
