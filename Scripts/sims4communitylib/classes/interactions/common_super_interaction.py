"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.base.super_interaction import SuperInteraction
from interactions.constraints import Constraint
from sims.sim import Sim
from sims4.utils import flexmethod
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonSuperInteraction(CommonInteraction, SuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions.

    The main use for this class is to create interactions that wrap sub interactions.
    One example Super interaction is the `sim-chat` interaction, where other interactions (Such as the `Get To Know` interaction), runs as sub interactions of `sim-chat`

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonSuperInteraction):
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

    """

    def _run_interaction_gen(self, timeline):
        super()._run_interaction_gen(timeline)
        try:
            return self.on_run(self.sim, self.target, timeline)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred while running interaction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        return False

    # noinspection PyUnusedLocal
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=True)
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline) -> bool:
        """on_run(interaction_sim, interaction_target, timeline)
        Occurs upon the interaction being run.

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

    See also :class:`CommonSuperInteraction`
    """

    # noinspection PyMethodParameters
    @flexmethod
    def _constraint_gen(cls, inst: Interaction, sim: Sim, target: Any, participant_type: ParticipantType=ParticipantType.Actor, **kwargs) -> Constraint:
        interaction_instance = inst if inst is not None else cls
        try:
            yield cls.on_constraint_gen(interaction_instance, sim or interaction_instance.sim, target or interaction_instance.target)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred while running interaction \'{}\' on_constraint_gen.'.format(cls.__name__), exception=ex)
        return None

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
