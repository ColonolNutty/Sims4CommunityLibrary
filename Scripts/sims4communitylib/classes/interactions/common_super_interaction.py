"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any

from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.constraints import Constraint
from sims.sim import Sim
from sims4.utils import flexmethod
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo

# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.base.super_interaction import SuperInteraction
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


class CommonSuperInteraction(CommonInteraction, SuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions.

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

            def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
                result = True
                if not result:
                    return False
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return True

    """

    # noinspection PyMissingTypeHints
    @classmethod
    def _tuning_loaded_callback(cls):
        return super()._tuning_loaded_callback()

    def _run_interaction_gen(self, timeline: Any):
        super()._run_interaction_gen(timeline)
        try:
            return self.on_run(self.sim, self.target, timeline)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred while running interaction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        return False

    # noinspection PyUnusedLocal
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=True)
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline) -> bool:
        """on_run(interaction_sim, interaction_target, timeline)

        A hook that occurs upon the interaction being run.

        :param interaction_sim: The sim performing the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target of the interaction.
        :type interaction_target: Any
        :param timeline: The timeline the interaction is running on.
        :type timeline: Any
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        return True


class CommonConstrainedSuperInteraction(SuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions that provide custom constraints.

    .. note:: For more information see :class:`.CommonSuperInteraction`.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    """

    # noinspection PyMethodParameters
    @flexmethod
    def _constraint_gen(cls, inst: Interaction, sim: Sim, target: Any, participant_type: ParticipantType=ParticipantType.Actor, **kwargs) -> Constraint:
        interaction_instance = inst if inst is not None else cls
        try:
            yield cls.on_constraint_gen(interaction_instance, sim or interaction_instance.sim, target or interaction_instance.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred while running interaction \'{}\' _on_constraint_gen.'.format(cls.__name__), exception=ex)
        return super(CommonConstrainedSuperInteraction, interaction_instance)._constraint_gen(sim, interaction_instance.get_constraint_target(target), participant_type=participant_type)

    @classmethod
    def on_constraint_gen(cls, inst: Interaction, sim: Sim, target: Any) -> Constraint:
        """on_constraint_gen(inst, sim, target)

        A hook that occurs when generating the constraints of an interaction to enable modification or replacement of the constraints.

        :param inst: An instance of the interaction.
        :type inst: Interaction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: The constraints of the interaction.
        :rtype: Constraint
        """
        raise NotImplementedError()
