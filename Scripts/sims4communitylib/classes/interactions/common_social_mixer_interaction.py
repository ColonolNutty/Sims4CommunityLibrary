"""The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from pprint import pformat
from typing import Any

from event_testing.results import TestResult
from interactions.context import InteractionContext
from native.animation import NativeAsm
from sims.sim import Sim
from sims4.utils import classproperty
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

# ReadTheDocs
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


class CommonSocialMixerInteraction(SocialMixerInteraction, CommonInteraction):
    """An inheritable class that provides a way to create Custom Social Mixer Interactions.

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
                    return TestResult.NONE
                # Interaction will display and be enabled.
                return TestResult.TRUE

            def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
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
        return SocialMixerInteraction._tunable_tests_enabled()

    def _trigger_interaction_start_event(self: 'CommonSocialMixerInteraction'):
        try:
            super()._trigger_interaction_start_event()
            from interactions import ParticipantType
            target = self.get_participant(ParticipantType.TargetSim)
            self.on_started(self.context.sim, target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' on_started.'.format(self.__class__.__name__), exception=ex)

    # noinspection PyMissingOrEmptyDocstring
    def setup_asm_default(self, asm: NativeAsm, *args, **kwargs) -> bool:
        try:
            result = self._setup_asm_default(self.sim, self.target, asm, *args, **kwargs)
            if result is not None:
                return result
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while running interaction \'{}\' setup_asm_default.'.format(self.__class__.__name__), exception=ex)
        return super().setup_asm_default(asm, *args, **kwargs)

    # SocialMixerInteraction has a different signature for its _test function, so we override it in here.
    @classmethod
    def _test(cls, target: Any, context: InteractionContext, *args, **kwargs) -> TestResult:
        try:
            if context.sim is target:
                return TestResult(False, 'Social Mixer Interactions cannot target self!')
            if context.pick is not None:
                pick_target = context.pick.target if context.source == context.SOURCE_PIE_MENU else None
                if context.sim is pick_target:
                    return TestResult(False, 'Social Mixer Interactions cannot target self!')
            test_result = cls.on_test(context.sim, target, context, *args, **kwargs)
        except Exception as ex:
            mod_identity = cls.get_mod_identity()
            CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while running interaction \'{}\' on_test.'.format(cls.__name__), exception=ex)
            return TestResult.NONE
        if test_result is None:
            return super()._test(target, context, *args, **kwargs)
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
        return super()._test(target, context, *args, **kwargs)

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
