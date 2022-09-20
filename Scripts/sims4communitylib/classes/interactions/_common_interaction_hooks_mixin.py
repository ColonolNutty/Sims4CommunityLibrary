"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, Iterator, Tuple

from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.constraints import Constraint
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from native.animation import NativeAsm
from postures.posture_state import PostureState
from protocolbuffers.Localization_pb2 import LocalizedString
from scheduling import Timeline
from sims.sim import Sim
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from singletons import DEFAULT


class _CommonInteractionHooksMixin:
    """Hooks that are called from the various custom interactions."""

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    # noinspection PyUnusedLocal
    @classmethod
    def on_replacement_constraints_gen(cls, inst_or_cls: 'Interaction', sim: Sim, target: Any) -> Union[Iterator[Constraint], None]:
        """on_replacement_constraints_gen(inst_or_cls, sim, target)

        A hook that occurs before the normal constraints of an interaction, these constraints will replace the normal constraints of the interaction.

        .. note:: If None is returned, the normal constraints will be used. (Plus any additional constraints from on_constraint_gen)

        :param inst_or_cls: An instance or the class of the interaction.
        :type inst_or_cls: Interaction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: An iterator of constraints to replace the normal constraints of the interaction or None if replacement constraints are not wanted.
        :rtype: Union[Iterator[Constraint], None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def on_constraint_gen(cls, inst_or_cls: 'Interaction', sim: Sim, target: Any) -> Union[Iterator[Constraint], Constraint, None]:
        """on_constraint_gen(inst_or_cls, sim, target)

        A hook that occurs after generating the constraints of an interaction, this constraint will be returned in addition to the normal constraints of the interaction.

        .. note:: Return None from this function to exclude any custom constraints.

        :param inst_or_cls: An instance or the class of the interaction.
        :type inst_or_cls: Interaction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: A constraint or an iterator of constraints to return in addition to the normal constraints or None if no additional constraints should be added.
        :rtype: Union[Iterator[Constraint], Constraint, None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonTestResult:
        """on_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs upon the interaction being tested for availability.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: CommonTestResult
        """
        return CommonTestResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def on_post_super_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonTestResult:
        """on_post_super_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs after the interaction being tested for availability by on_test and the super _test functions.

        .. note:: This will only run if both on_test and _test returns CommonTestResult.TRUE or similar.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: CommonTestResult
        """
        return CommonTestResult.TRUE

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

    # noinspection PyUnusedLocal
    @classmethod
    def get_custom_replacement_participants(cls, participant_type: ParticipantType, sim: Union[Sim, None], target: Union[Sim, None], carry_target: Union[Any, None], interaction: 'Interaction'=None, **kwargs) -> Union[Tuple[Any], None]:
        """get_custom_replacement_participants(participant_type, sim=None, target=None, carry_target=None, interaction=None, **kwargs)

        A hook used to replace the result of the get_participants function with custom participants.

        :param participant_type: The type of participant being searched for.
        :type participant_type: ParticipantType
        :param sim: The Source of the interaction.
        :type sim: Union[Sim, None]
        :param target: The Target of the interaction.
        :type sim: Union[Sim, None]
        :param carry_target: The target being carried while the interaction is being run.
        :type carry_target: Union[Any, None]
        :param interaction: An instance of the interaction, if get_participants was invoked using an instance or None if get_participants was invoked using the class. Default is None.
        :type interaction: Interaction, optional
        :return: A collection of custom participants to use as replacements for the normal result of get_participants. Return None to keep the original participants. Default return is None.
        :rtype: Union[Tuple[Any], None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def get_custom_participants(cls, participant_type: ParticipantType, sim: Union[Sim, None], target: Union[Sim, None], carry_target: Union[Any, None], interaction: 'Interaction'=None, **kwargs) -> Tuple[Any]:
        """get_custom_participants(participant_type, sim=None, target=None, carry_target=None, interaction=None, **kwargs)

        A hook used to add custom participants to the result of the get_participants function.

        :param participant_type: The type of participant being searched for.
        :type participant_type: ParticipantType
        :param sim: The Source of the interaction.
        :type sim: Union[Sim, None]
        :param target: The Target of the interaction.
        :type sim: Union[Sim, None]
        :param carry_target: The target being carried while the interaction is being run.
        :type carry_target: Union[Any, None]
        :param interaction: An instance of the interaction, if get_participants was invoked using an instance or None if get_participants was invoked using the class. Default is None.
        :type interaction: Interaction, optional
        :return: A collection of custom participants to add to the normal result of get_participants.
        :rtype: Tuple[Any]
        """
        return tuple()

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
        interaction: 'Interaction'=None,
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
        :type interaction: Interaction
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
