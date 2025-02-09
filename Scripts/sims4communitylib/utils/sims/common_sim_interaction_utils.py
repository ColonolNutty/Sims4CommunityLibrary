"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union, Any, Callable, List

from distributor.shared_messages import IconInfoData
from interactions.aop import AffordanceObjectPair
from interactions.base.interaction import Interaction
from interactions.base.super_interaction import SuperInteraction
from interactions.context import InteractionSource, InteractionContext, QueueInsertStrategy
from interactions.interaction_finisher import FinishingType
from interactions.priority import Priority
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_enqueue_result import CommonEnqueueResult
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CommonSimInteractionUtils(HasClassLog):
    """Utilities for manipulating the interactions of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_interaction_utils'
    
    @classmethod
    def is_sitting(cls, sim_info: SimInfo) -> bool:
        """is_sitting(sim_info)

        Determine if a Sim is currently sitting.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is sitting. False, if not.
        :rtype: bool
        """
        interactions = (
            CommonInteractionId.SIT_PASSIVE,
            CommonInteractionId.SEATING_SIT,
            CommonInteractionId.SEATING_SIT_CTYAE,
            CommonInteractionId.SEATING_SIT_RESTAURANT_RALLY_ONLY,
            CommonInteractionId.SEATING_SIT_SINGLE,
            CommonInteractionId.SEATING_SIT_TODDLER_BED,
            CommonInteractionId.SEATING_SIT_POST_GRAND_MEAL_WAIT_ENJOY_COMPANY,
            CommonInteractionId.SEATING_SIT_DIRECTOR_CHAIR,
            CommonInteractionId.SEATING_SIT_HAIR_MAKE_UP_CHAIR,
        )
        return cls.has_interactions_running_or_queued(sim_info, interactions)

    @classmethod
    def is_standing(cls, sim_info: SimInfo) -> bool:
        """is_standing(sim_info)

        Determine if a Sim is standing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is standing. False, if not.
        :rtype: bool
        """
        interactions = (
            CommonInteractionId.STAND_PASSIVE,
            CommonInteractionId.SIM_STAND,
            CommonInteractionId.SIM_STAND_EXCLUSIVE,
            CommonInteractionId.DOG_STAND,
            CommonInteractionId.DOG_STAND_PASSIVE,
            CommonInteractionId.CAT_STAND,
            CommonInteractionId.CAT_STAND_PASSIVE
        )
        return cls.has_interactions_running_or_queued(sim_info, interactions)

    @classmethod
    def is_swimming(cls, sim_info: SimInfo) -> bool:
        """is_swimming(sim_info)

        Determine if a Sim is swimming.

        .. note: Cats cannot swim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is swimming. False, if not.
        :rtype: bool
        """
        interactions = (
            CommonInteractionId.SIM_SWIM,
            CommonInteractionId.DOG_SWIM,
            CommonInteractionId.DOG_SWIM_PASSIVE
        )
        return cls.has_interactions_running_or_queued(sim_info, interactions)

    @staticmethod
    def apply_pressure_to_next_interaction_of(sim_info: SimInfo):
        """apply_pressure_to_next_interaction_of(sim_info)

        Apply pressure to the interaction queue of a Sim for their next interaction.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.queue is None:
            return
        sim.queue._apply_next_pressure()

    @classmethod
    def get_swim_interaction(cls, sim_info: SimInfo) -> Union[int, CommonInteractionId]:
        """get_swim_interaction(sim_info)

        Retrieve a Swim interaction appropriate for a Sim.

        .. note:: Cats do not have an appropriate Swim interaction.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The decimal identifier of an interaction appropriate for the Sim or -1 if no interaction was found to be appropriate.
        :rtype: Union[int, CommonInteractionId]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonInteractionId.SIM_SWIM
        elif CommonSpeciesUtils.is_dog(sim_info):
            return CommonInteractionId.DOG_SWIM
        # Cats don't have a swim interaction. Because they cannot swim.
        return -1

    @classmethod
    def get_stand_interaction(cls, sim_info: SimInfo) -> Union[int, CommonInteractionId]:
        """get_stand_interaction(sim_info)

        Retrieve a Stand interaction appropriate for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The decimal identifier of a Stand interaction appropriate for the Sim or -1 if no Stand interaction was found to be appropriate.
        :rtype: Union[int, CommonInteractionId]
        """
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonInteractionId.SIM_STAND
        elif CommonSpeciesUtils.is_dog(sim_info):
            return CommonInteractionId.DOG_STAND
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonInteractionId.CAT_STAND
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonInteractionId.FOX_STAND
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonInteractionId.HORSE_STAND
        return -1

    @classmethod
    def get_stand_passive_interaction(cls, sim_info: SimInfo) -> Union[int, CommonInteractionId]:
        """get_stand_passive_interaction(sim_info)

        Retrieve a Stand Passive interaction appropriate for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The decimal identifier of a Stand Passive interaction appropriate for the Sim or -1 if no Stand interaction was found to be appropriate.
        :rtype: Union[int, CommonInteractionId]
        """
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonInteractionId.STAND_PASSIVE
        elif CommonSpeciesUtils.is_dog(sim_info):
            return CommonInteractionId.DOG_STAND_PASSIVE
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonInteractionId.CAT_STAND_PASSIVE
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonInteractionId.FOX_STAND_PASSIVE
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonInteractionId.HORSE_STAND_PASSIVE
        return -1

    @classmethod
    def lock_interaction_queue(cls, sim_info: SimInfo):
        """lock_interaction_queue(sim_info)

        Lock the interaction queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.queue is None:
            return
        sim.queue.lock()

    @classmethod
    def unlock_interaction_queue(cls, sim_info: SimInfo):
        """unlock_interaction_queue(sim_info)

        Unlock the interaction queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.queue is None:
            return
        sim.queue.unlock()

    @classmethod
    def has_interaction_running_or_queued(cls, sim_info: SimInfo, interaction_id: Union[int, CommonInteractionId]) -> bool:
        """has_interaction_running_or_queued(sim_info, interaction_id)

        Determine if a Sim has the specified interaction running or in their interaction queue.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_id: The identifier of the interaction to check for.
        :type interaction_id: Union[int, CommonInteractionId]
        :return: True, if the Sim has the specified interaction running or queued. False, if not.
        :rtype: bool
        """
        return cls.has_interactions_running_or_queued(sim_info, (interaction_id, ))

    @classmethod
    def has_interaction_running(cls, sim_info: SimInfo, interaction_id: Union[int, CommonInteractionId]) -> bool:
        """has_interaction_running(sim_info, interaction_id)

        Determine if a Sim is running the specified interaction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_id: The identifier of the interaction to check for.
        :type interaction_id: Union[int, CommonInteractionId]
        :return: True, if the Sim has the specified interaction running. False, if not.
        :rtype: bool
        """
        return cls.has_interactions_running(sim_info, (interaction_id, ))

    @classmethod
    def has_interaction_queued(cls, sim_info: SimInfo, interaction_id: Union[int, CommonInteractionId]) -> bool:
        """has_interaction_queued(sim_info, interaction_id)

        Determine if a Sim is running the specified interaction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_id: The identifier of the interaction to check for.
        :type interaction_id: Union[int, CommonInteractionId]
        :return: True, if the Sim has the specified interaction queued. False, if not.
        :rtype: bool
        """
        return cls.has_interactions_queued(sim_info, (interaction_id, ))

    @classmethod
    def has_interactions_running_or_queued(cls, sim_info: SimInfo, interaction_ids: Iterator[Union[int, CommonInteractionId]]) -> bool:
        """has_interactions_running_or_queued(sim_info, interaction_ids)

        Determine if a Sim has any of the specified interactions running or in their interaction queue.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_ids: An iterator of identifiers of the interactions to check for.
        :type interaction_ids: Union[int, CommonInteractionId]
        :return: True, if the Sim has any of the specified interactions running or queued. False, if not.
        :rtype: bool
        """
        for interaction in cls.get_queued_or_running_interactions_gen(sim_info):
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            if interaction_id in interaction_ids:
                return True
        return False

    @classmethod
    def has_interactions_running(cls, sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """has_interactions_running(sim_info, interaction_ids)

        Determine if a Sim is running any of the specified interactions.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_ids: An iterator of identifiers of the interactions to check for.
        :type interaction_ids: Union[int, CommonInteractionId]
        :return: True, if the Sim has any of the specified interactions running. False, if not.
        :rtype: bool
        """
        for interaction in cls.get_running_interactions_gen(sim_info):
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            if interaction_id in interaction_ids:
                return True
        return False

    @classmethod
    def has_interactions_queued(cls, sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """has_interactions_queued(sim_info, interaction_ids)

        Determine if a Sim has any of the specified interactions in their interaction queue.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_ids: An iterator of identifiers of the interactions to check for.
        :type interaction_ids: Union[int, CommonInteractionId]
        :return: True, if the Sim has any of the specified interactions queued. False, if not.
        :rtype: bool
        """
        for interaction in cls.get_queued_interactions_gen(sim_info):
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            if interaction_id in interaction_ids:
                return True
        return False

    @classmethod
    def cancel_all_queued_or_running_interactions(
        cls,
        sim_info: SimInfo,
        cancel_reason: str,
        finishing_type: FinishingType = FinishingType.USER_CANCEL,
        include_interaction_callback: Callable[[Interaction], bool] = None,
        **kwargs
    ) -> bool:
        """cancel_all_queued_or_running_interactions(\
            sim_info,\
            cancel_reason,\
            finishing_type=FinishingType.USER_CANCEL,\
            include_interaction_callback=None,\
            source=None,\
            **kwargs\
        )

        Cancel all interactions that a Sim currently has queued or is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be cancelled. If set to None, All interactions will be cancelled. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: True, if all queued and running Interactions that pass the "include" callback were successfully cancelled. False, if not.
        :rtype: bool
        """
        queued_result = cls.cancel_all_queued_interactions(
            sim_info,
            cancel_reason,
            finishing_type=finishing_type,
            include_interaction_callback=include_interaction_callback,
            **kwargs
        )
        if not queued_result:
            return False
        running_result = cls.cancel_all_running_interactions(
            sim_info,
            cancel_reason,
            finishing_type=finishing_type,
            include_interaction_callback=include_interaction_callback,
            **kwargs
        )
        if not running_result:
            return False
        return True

    @classmethod
    def cancel_all_running_interactions(
        cls,
        sim_info: SimInfo,
        cancel_reason: str,
        finishing_type: FinishingType = FinishingType.USER_CANCEL,
        include_interaction_callback: Callable[[Interaction], bool] = None,
        **kwargs
    ) -> bool:
        """cancel_all_running_interactions(\
            sim_info,\
            cancel_reason,\
            finishing_type=FinishingType.USER_CANCEL,\
            include_interaction_callback=None,\
            source=None,\
            **kwargs\
        )

        Cancel all interactions that a Sim is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be cancelled. If set to None, all interactions will be cancelled. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: True, if all running interactions were successfully cancelled. False, if not.
        :rtype: bool
        """
        for interaction in tuple(cls.get_running_interactions_gen(sim_info, include_interaction_callback=include_interaction_callback)):
            cls.cancel_interaction(interaction, cancel_reason, finishing_type=finishing_type, **kwargs)
        return True

    @classmethod
    def cancel_all_queued_interactions(
        cls,
        sim_info: SimInfo,
        cancel_reason: str,
        finishing_type: FinishingType = FinishingType.USER_CANCEL,
        include_interaction_callback: Callable[[Interaction], bool] = None,
        **kwargs
    ) -> bool:
        """cancel_all_queued_interactions(\
            sim_info,\
            cancel_reason,\
            finishing_type=FinishingType.USER_CANCEL,\
            include_interaction_callback=None,\
            **kwargs\
        )

        Cancel all interactions that a Sim currently has queued.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be cancelled. If set to None, all interactions will be cancelled. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: True, if all queued interactions were successfully cancelled. False, if not.
        :rtype: bool
        """
        for interaction in tuple(cls.get_queued_interactions_gen(sim_info, include_interaction_callback=include_interaction_callback)):
            cls.cancel_interaction(interaction, cancel_reason, finishing_type=finishing_type, **kwargs)
        return True

    @classmethod
    def cancel_interaction(
        cls,
        interaction: Interaction,
        cancel_reason: str,
        finishing_type: FinishingType = FinishingType.USER_CANCEL,
        **kwargs
    ) -> bool:
        """cancel_interaction(\
            interaction,\
            cancel_reason,\
            finishing_type=FinishingType.USER_CANCEL,\
            **kwargs\
        )

        Cancel an interaction.

        :param interaction: The interaction to cancel.
        :type interaction: Interaction
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :return: True, if the interaction was cancelled successfully. False, if not.
        :rtype: bool
        """
        if isinstance(interaction, SuperInteraction):
            immediate = kwargs.get('immediate', False)
            ignore_must_run = kwargs.get('ignore_must_run', False)
            carry_cancel_override = kwargs.get('carry_cancel_override', None)
            return interaction.cancel(
                finishing_type,
                cancel_reason,
                immediate=immediate,
                ignore_must_run=ignore_must_run,
                carry_cancel_override=carry_cancel_override
            )
        return interaction.cancel(finishing_type, cancel_reason, **kwargs)

    @classmethod
    def get_queued_or_running_interactions_gen(cls, sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool] = None) -> Iterator[Interaction]:
        """get_queued_or_running_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim has queued or is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, all interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterator of all queued or running Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        yield from cls.get_queued_interactions_gen(sim_info, include_interaction_callback=include_interaction_callback)
        yield from cls.get_running_interactions_gen(sim_info, include_interaction_callback=include_interaction_callback)

    @classmethod
    def get_running_interactions_gen(cls, sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool] = None) -> Iterator[Interaction]:
        """get_running_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, all interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterator of all running Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return tuple()
        if sim.si_state is None:
            return tuple()
        for interaction in tuple(sim.si_state):
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction

    @classmethod
    def get_queued_interactions_gen(cls, sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool] = None) -> Iterator[Interaction]:
        """get_queued_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim currently has queued.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterator of all queued Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return tuple()
        if sim.queue is None:
            return tuple()
        for interaction in tuple(sim.queue):
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction

    @classmethod
    def queue_interaction(
        cls,
        sim_info: SimInfo,
        interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId] = None,
        target: Any = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        skip_if_running: bool = False,
        **kwargs
    ) -> CommonEnqueueResult:
        """queue_interaction(\
            sim_info,\
            interaction_id,\
            social_super_interaction_id=None,\
            target=None,\
            picked_object=None,\
            interaction_context=None,\
            skip_if_running=False,\
            **kwargs\
        )

        Push an Interaction into the queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param interaction_id: The decimal identifier of an interaction.
        :type interaction_id: Union[int, CommonInteractionId]
        :param social_super_interaction_id: The decimal identifier of a social super interaction to queue the interaction under. Default is None
        :type social_super_interaction_id: Union[int, CommonInteractionId], optional
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :param picked_object: The picked object of the interaction. Default is None.
        :type picked_object: Any, optional
        :param skip_if_running: If True, the interaction will not be queued, if it is already queued or running. If False, the interaction will be queued, even if it is already queued or running.
        :return: The result of pushing the interaction to the queue of a Sim.
        :rtype: CommonEnqueueResult
        """
        log = cls.get_log()
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.format_with_message('No Sim instance for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        if sim.si_state is None:
            log.format_with_message('No Super Interaction State available for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Super Interaction State available for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        if sim.queue is None:
            log.format_with_message('No Queue found for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Queue found for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        # noinspection PyPropertyAccess
        if sim.posture_state is None:
            log.format_with_message('No Posture State found for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Posture State found for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        if sim.posture is None:
            log.format_with_message('No Posture found for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Posture found for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)

        interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction_id)
        if interaction_instance is None:
            log.format_with_message('No interaction found with id.', id=interaction_id)
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'No interaction was found with id {interaction_id}.', hide_tooltip=True))

        if skip_if_running and cls.has_interaction_running_or_queued(sim_info, interaction_id):
            log.debug('Skipping queue because it is already running.')
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'Interaction was already running or queued {interaction_id}.', hide_tooltip=True))

        interaction_context = interaction_context or cls.create_interaction_context(
            sim_info,
            insert_strategy=QueueInsertStrategy.LAST
        )

        if CommonInteractionUtils.is_super_interaction(interaction_instance):
            log.debug('Is super.')
            return cls.queue_super_interaction(
                sim_info,
                interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        if CommonInteractionUtils.is_social_mixer_interaction(interaction_instance):
            log.debug('Is social mixer')
            return cls.queue_social_mixer_interaction(
                sim_info,
                interaction_id,
                social_super_interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        log.debug('Is mixer')
        return cls.queue_mixer_interaction(
            sim_info,
            interaction_id,
            target=target,
            interaction_context=interaction_context
        )

    @classmethod
    def queue_super_interaction(
        cls,
        sim_info: SimInfo,
        super_interaction_id: Union[int, CommonInteractionId],
        target: Any = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonEnqueueResult:
        """queue_super_interaction(\
            sim_info,\
            super_interaction_id,\
            target=None,\
            picked_object=None,\
            interaction_context=None,\
            **kwargs\
        )

        Push a Super Interaction into the queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param super_interaction_id: The decimal identifier of a super interaction.
        :type super_interaction_id: Union[int, CommonInteractionId]
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param picked_object: The picked object of the interaction. Default is None.
        :type picked_object: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of pushing the interaction to the queue of a Sim.
        :rtype: CommonEnqueueResult
        """
        log = cls.get_log()
        log.format_with_message('Pushing super interaction', sim=sim_info, interaction_id=super_interaction_id, target=target, interaction_context=interaction_context)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.format_with_message('No sim instance for super interaction.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)

        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)

        interaction_context = interaction_context or cls.create_interaction_context(sim_info)
        super_interaction_instance = CommonInteractionUtils.load_interaction_by_id(super_interaction_id)
        if super_interaction_instance is None:
            log.format_with_message('No super interaction instance found for id.', super_interaction_id=super_interaction_id)
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'No super interaction was found with id {super_interaction_id}.', hide_tooltip=True))

        result = sim.push_super_affordance(
            super_interaction_instance,
            target,
            interaction_context,
            picked_object=picked_object or target,
            **kwargs
        )
        if not result:
            log.format_with_message('Failed to push super interaction.', result=result)
        return result

    @classmethod
    def queue_social_mixer_interaction(
        cls,
        sim_info: SimInfo,
        social_mixer_interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId],
        target: SimInfo = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonEnqueueResult:
        """queue_social_mixer_interaction(\
            sim_info,\
            social_mixer_interaction_id,\
            social_super_interaction_id,\
            target=None,\
            picked_object=None,\
            interaction_context=None,\
            **kwargs\
        )

        Push a Social Mixer Interaction into the queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param social_mixer_interaction_id: The decimal identifier of a social mixer interaction.
        :type social_mixer_interaction_id: Union[int, CommonInteractionId]
        :param social_super_interaction_id: The decimal identifier of a social super interaction to queue the social mixer interaction under.
        :type social_super_interaction_id: Union[int, CommonInteractionId]
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param picked_object: The picked object of the interaction. Default is None.
        :type picked_object: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of pushing the interaction to the queue of a Sim.
        :rtype: CommonEnqueueResult
        """
        log = cls.get_log()
        if social_super_interaction_id is not None and social_mixer_interaction_id is None:
            log.format_with_message('Interaction was actually a Super interaction!', sim=sim_info, super_interaction_id=social_super_interaction_id)
            return cls.queue_super_interaction(
                sim_info,
                social_super_interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        social_super_interaction_id: Union[int, CommonInteractionId, None] = social_super_interaction_id
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.format_with_message('No sim instance for super interaction.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)

        social_mixer_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_mixer_interaction_id)
        if social_mixer_affordance_instance is None:
            log.format_with_message('No social mixer affordance instance found with id.', interaction_id=social_mixer_interaction_id)
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'No social mixer interaction was found with id {social_mixer_interaction_id}.', hide_tooltip=True))

        interaction_context = interaction_context or cls.create_interaction_context(sim_info)
        # noinspection PyTypeChecker
        super_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_super_interaction_id)
        if super_affordance_instance is None:
            def _get_existing_social_super_interaction(si_iter) -> Interaction:
                for si in si_iter:
                    if si.super_affordance != super_affordance_instance:
                        continue
                    if si.social_group is None:
                        continue
                    target_sim = CommonSimUtils.get_sim_instance(target)
                    if target_sim is not None and target_sim not in si.social_group:
                        continue
                    log.format_with_message('Got existing super', existing_super=si.super_interaction)
                    return si.super_interaction

            log.debug('No super affordance found with id.')
            super_interaction = _get_existing_social_super_interaction(sim.si_state) or _get_existing_social_super_interaction(sim.queue)
            if super_interaction is None:
                si_result = cls.queue_interaction(
                    sim_info,
                    social_super_interaction_id,
                    target=target,
                    picked_object=picked_object or target,
                    interaction_context=interaction_context,
                    **kwargs
                )
                if not si_result:
                    log.format_with_message('Failed to locate existing super interaction.', super_interaction=super_interaction)
                    return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason='No Existing Super Interaction was found.', hide_tooltip=True))
                log.format_with_message('Found si result', si_result=si_result)
                super_interaction = si_result.interaction
                log.format_with_message('Found si interaction', si_interaction=super_interaction)
            else:
                log.format_with_message('Located existing super interaction.', existing_super=super_interaction)

            pick = interaction_context.pick if interaction_context.pick is not None else super_interaction.context.pick
            log.format_with_message('Found pick', pick=pick)
            interaction_context = super_interaction.context.clone_for_continuation(
                super_interaction,
                insert_strategy=interaction_context.insert_strategy,
                source_interaction_id=super_interaction.id,
                source_interaction_sim_id=CommonSimUtils.get_sim_id(sim_info),
                pick=pick,
                picked_object=picked_object,
                must_run_next=interaction_context.must_run_next,
                **kwargs
            )
        else:
            super_interaction = None

        aop = AffordanceObjectPair(
            social_mixer_affordance_instance,
            target,
            super_affordance_instance,
            super_interaction,
            picked_object=picked_object or target,
            push_super_on_prepare=True,
            **kwargs
        )
        result = aop.test_and_execute(interaction_context)
        if not result:
            log.format_with_message('Failed to queue social mixer interaction', result=result)
        return result

    @classmethod
    def queue_mixer_interaction(
        cls,
        sim_info: SimInfo,
        mixer_interaction_id: Union[int, CommonInteractionId],
        target: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonEnqueueResult:
        """queue_mixer_interaction(\
            sim_info,\
            mixer_interaction_id,\
            target=None,\
            interaction_context=None,\
            **kwargs\
        )

        Push a Mixer Interaction into the Queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param mixer_interaction_id: The decimal identifier of a mixer interaction.
        :type mixer_interaction_id: Union[int, CommonInteractionId]
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of pushing the interaction to the queue of a Sim.
        :rtype: CommonEnqueueResult
        """
        log = cls.get_log()
        log.format_with_message(
            'Attempting to queue mixer interaction.',
            sim=sim_info,
            target=target,
            mixer_interaction_id=mixer_interaction_id,
            interaction_context=interaction_context
        )
        from autonomy.content_sets import get_valid_aops_gen

        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.format_with_message('No sim instance for mixer interaction.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        if sim.si_state is None:
            log.format_with_message('No Super Interaction State available for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Super Interaction State available for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        if sim.queue is None:
            log.format_with_message('No Queue found for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Queue found for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        # noinspection PyPropertyAccess
        if sim.posture_state is None:
            log.format_with_message('No Posture State found for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Posture State found for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        if sim.posture is None:
            log.format_with_message('No Posture found for Sim.', sim=sim_info)
            return CommonEnqueueResult(CommonTestResult(False, reason=f'No Posture found for Sim {sim_info}', hide_tooltip=True), CommonExecutionResult.NONE)
        mixer_interaction_instance = CommonInteractionUtils.load_interaction_by_id(mixer_interaction_id)
        if mixer_interaction_instance is None:
            log.debug('No mixer interaction instance found.')
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'No mixer interaction found {mixer_interaction_id}', hide_tooltip=True))
        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)
        source_interaction = sim.posture.source_interaction
        if source_interaction is None:
            log.debug('Sim did not have a source interaction.')
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'No source interaction found on Sim {sim_info}', hide_tooltip=True))

        if hasattr(mixer_interaction_instance, 'lock_out_time') and mixer_interaction_instance.lock_out_time:
            log.debug('Using Sim specific lock out time.')
            sim_specific_lockout = mixer_interaction_instance.lock_out_time.target_based_lock_out
        else:
            log.debug('Not using Sim specific lock out time.')
            sim_specific_lockout = False

        if sim_specific_lockout and sim.is_sub_action_locked_out(mixer_interaction_instance):
            log.debug('Sim was locked out of performing the mixer interaction.')
            return CommonEnqueueResult(CommonTestResult(False, reason=f'{sim_info} is currently locked out of doing the mixer interaction, they must wait before they can do it again.', hide_tooltip=True), CommonExecutionResult.NONE)

        super_interaction_instance = source_interaction.super_affordance
        interaction_context = interaction_context or cls.create_interaction_context(sim_info)
        for (aop, test_result) in get_valid_aops_gen(
            target,
            mixer_interaction_instance,
            super_interaction_instance,
            source_interaction,
            interaction_context,
            False,
            push_super_on_prepare=False
        ):
            test_result: CommonTestResult = CommonTestResult.convert_from_vanilla(test_result)
            if test_result is None or test_result.result:
                log.format_with_message('Failed to queue using affordance.', aop=aop, affordance=aop.affordance)
                continue
            interaction_constraint = aop.constraint_intersection(sim=sim, posture_state=None)
            # noinspection PyPropertyAccess
            posture_constraint = sim.posture_state.posture_constraint_strict
            constraint_intersection = interaction_constraint.intersect(posture_constraint)
            if not constraint_intersection.valid:
                log.format_with_message('Constraint interaction was invalid.', constraint_intersection=constraint_intersection)
                continue
            log.format_with_message('Executing interaction using Aop.', aop=aop, affordance=aop.affordance)
            return aop.execute(interaction_context, **kwargs)

    @classmethod
    def test_interaction(
        cls,
        sim_info: SimInfo,
        interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId] = None,
        target: Any = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonTestResult:
        """test_interaction(\
            sim_info,\
            interaction_id,\
            social_super_interaction_id=None,\
            target=None,\
            picked_object=None,\
            interaction_context,\
            skip_if_running=False,\
            **kwargs\
        )

        Test to see if an Interaction can be pushed into the queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param interaction_id: The decimal identifier of an interaction.
        :type interaction_id: Union[int, CommonInteractionId]
        :param social_super_interaction_id: The decimal identifier of a social super interaction to queue the interaction under. Default is None
        :type social_super_interaction_id: Union[int, CommonInteractionId], optional
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param picked_object: The picked object of the interaction. Default is None.
        :type picked_object: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: CommonTestResult
        """
        log = cls.get_log()
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.format_with_message('No Sim instance for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True)
        if sim.si_state is None:
            log.format_with_message('No Super Interaction State available for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Super Interaction State available for Sim {sim_info}', hide_tooltip=True)
        if sim.queue is None:
            log.format_with_message('No Queue found for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Queue found for Sim {sim_info}', hide_tooltip=True)
        # noinspection PyPropertyAccess
        if sim.posture_state is None:
            log.format_with_message('No Posture State found for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Posture State found for Sim {sim_info}', hide_tooltip=True)
        if sim.posture is None:
            log.format_with_message('No Posture found for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Posture found for Sim {sim_info}', hide_tooltip=True)

        interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction_id)
        if interaction_instance is None:
            log.format_with_message('No interaction found with id.', id=interaction_id)
            return CommonTestResult(False, reason=f'No mixer interaction found {interaction_id}', hide_tooltip=True)

        interaction_context = interaction_context or cls.create_interaction_context(
            sim_info,
            insert_strategy=QueueInsertStrategy.LAST
        )

        if CommonInteractionUtils.is_super_interaction(interaction_instance):
            log.debug('Is super.')
            return cls.test_super_interaction(
                sim_info,
                interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        if CommonInteractionUtils.is_social_mixer_interaction(interaction_instance):
            log.debug('Is social mixer')
            return cls.test_social_mixer_interaction(
                sim_info,
                interaction_id,
                social_super_interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        log.debug('Is mixer')
        return cls.test_mixer_interaction(
            sim_info,
            interaction_id,
            target=target,
            interaction_context=interaction_context
        )

    @classmethod
    def test_super_interaction(
        cls,
        sim_info: SimInfo,
        super_interaction_id: Union[int, CommonInteractionId],
        target: Any = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonTestResult:
        """test_super_interaction(\
            sim_info,\
            super_interaction_id,\
            target=None,\
            picked_object=None,\
            interaction_context=None,\
            **kwargs\
        )

        Test to see if a Super Interaction can be pushed into the queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param super_interaction_id: The decimal identifier of a super interaction.
        :type super_interaction_id: Union[int, CommonInteractionId]
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param picked_object: The picked object of the interaction. Default is None.
        :type picked_object: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: CommonTestResult
        """
        log = cls.get_log()
        log.format_with_message('Testing super interaction', sim=sim_info, interaction_id=super_interaction_id, target=target, interaction_context=interaction_context)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.debug('No sim instance for super interaction.')
            return CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True)

        super_interaction_instance = CommonInteractionUtils.load_interaction_by_id(super_interaction_id)
        if super_interaction_instance is None:
            log.format_with_message('No super interaction instance found for id.', super_interaction_id=super_interaction_id)
            return CommonTestResult(False, reason=f'No super interaction found {super_interaction_id}', hide_tooltip=True)

        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)

        interaction_context = interaction_context or cls.create_interaction_context(sim_info)

        return CommonTestResult.convert_from_vanilla(sim.test_super_affordance(
            super_interaction_instance,
            target,
            interaction_context,
            picked_object=picked_object or target,
            **kwargs
        ))

    @classmethod
    def test_social_mixer_interaction(
        cls,
        sim_info: SimInfo,
        social_mixer_interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId],
        target: SimInfo = None,
        picked_object: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonTestResult:
        """test_social_mixer_interaction(\
            sim_info,\
            social_mixer_interaction_id,\
            social_super_interaction_id,\
            target=None,\
            picked_object=None,\
            interaction_context=None,\
            **kwargs\
        )

        Test to see if a Social Mixer Interaction can be pushed into the queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param social_mixer_interaction_id: The decimal identifier of a social mixer interaction.
        :type social_mixer_interaction_id: Union[int, CommonInteractionId]
        :param social_super_interaction_id: The decimal identifier of a social super interaction to queue the social mixer interaction under.
        :type social_super_interaction_id: Union[int, CommonInteractionId]
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param picked_object: The picked object of the interaction. Default is None.
        :type picked_object: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: CommonTestResult
        """
        log = cls.get_log()
        if social_super_interaction_id is not None and social_mixer_interaction_id is None:
            log.format_with_message('Interaction was actually a Super interaction!', sim=sim_info, super_interaction_id=social_super_interaction_id)
            return cls.queue_super_interaction(
                sim_info,
                social_super_interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        social_super_interaction_id: Union[int, CommonInteractionId, None] = social_super_interaction_id
        sim = CommonSimUtils.get_sim_instance(sim_info)
        social_mixer_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_mixer_interaction_id)
        if social_mixer_affordance_instance is None:
            log.debug('No social mixer affordance instance found with id.')
            return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason=f'No social mixer interaction found {social_mixer_interaction_id}', hide_tooltip=True))

        interaction_context = interaction_context or cls.create_interaction_context(sim_info)
        # noinspection PyTypeChecker
        super_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_super_interaction_id)
        if super_affordance_instance is None:
            def _get_existing_social_super_interaction(si_iter) -> Interaction:
                for si in si_iter:
                    if si.super_affordance != super_affordance_instance:
                        continue
                    if si.social_group is None:
                        continue
                    target_sim = CommonSimUtils.get_sim_instance(target)
                    if target_sim is not None and target_sim not in si.social_group:
                        continue
                    log.format_with_message('Got existing super', existing_super=si.super_interaction)
                    return si.super_interaction

            log.debug('No super affordance found with id.')
            super_interaction = _get_existing_social_super_interaction(sim.si_state) or _get_existing_social_super_interaction(sim.queue)
            if super_interaction is None:
                si_result = cls.queue_interaction(
                    sim_info,
                    social_super_interaction_id,
                    target=target,
                    picked_object=picked_object or target,
                    interaction_context=interaction_context,
                    **kwargs
                )
                if not si_result:
                    log.format_with_message('Failed to locate existing super interaction.', super_interaction=super_interaction)
                    return CommonEnqueueResult(CommonTestResult.TRUE, CommonExecutionResult(False, reason='No Existing Super Interaction was found.', hide_tooltip=True))
                log.format_with_message('Found si result', si_result=si_result)
                super_interaction = si_result.interaction
                log.format_with_message('Found si interaction', si_interaction=super_interaction)
            else:
                log.format_with_message('Located existing super interaction.', existing_super=super_interaction)

            pick = interaction_context.pick if interaction_context.pick is not None else super_interaction.context.pick
            log.format_with_message('Found pick', pick=pick)
            interaction_context = super_interaction.context.clone_for_continuation(
                super_interaction,
                insert_strategy=interaction_context.insert_strategy,
                source_interaction_id=super_interaction.id,
                source_interaction_sim_id=CommonSimUtils.get_sim_id(sim_info),
                pick=pick,
                picked_object=picked_object,
                must_run_next=interaction_context.must_run_next,
                **kwargs
            )
        else:
            super_interaction = None

        aop = AffordanceObjectPair(
            social_mixer_affordance_instance,
            target,
            super_affordance_instance,
            super_interaction,
            picked_object=picked_object or target,
            push_super_on_prepare=True,
            **kwargs
        )
        return CommonTestResult.convert_from_vanilla(aop.test(interaction_context))

    @classmethod
    def test_mixer_interaction(
        cls,
        sim_info: SimInfo,
        mixer_interaction_id: Union[int, CommonInteractionId],
        target: Any = None,
        interaction_context: InteractionContext = None,
        **kwargs
    ) -> CommonTestResult:
        """test_mixer_interaction(\
            sim_info,\
            mixer_interaction_id,\
            target=None,\
            interaction_context=None,\
            **kwargs\
        )

        Test to see if a Mixer Interaction can be pushed into the Queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param mixer_interaction_id: The decimal identifier of a mixer interaction.
        :type mixer_interaction_id: Union[int, CommonInteractionId]
        :param target: The target of the interaction. Default is None.
        :type target: Any, optional
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: CommonTestResult
        """
        log = cls.get_log()
        log.format_with_message(
            'Attempting to test mixer interaction.',
            sim=sim_info,
            target=target,
            mixer_interaction_id=mixer_interaction_id,
            interaction_context=interaction_context
        )
        from autonomy.content_sets import get_valid_aops_gen

        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.format_with_message('No Sim instance for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Sim instance for Sim {sim_info}', hide_tooltip=True)
        if sim.posture is None:
            log.format_with_message('No Posture found for Sim.', sim=sim_info)
            return CommonTestResult(False, reason=f'No Posture found for Sim {sim_info}', hide_tooltip=True)

        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)
        mixer_interaction_instance = CommonInteractionUtils.load_interaction_by_id(mixer_interaction_id)
        if mixer_interaction_instance is None:
            log.format_with_message('No mixer interaction instance found.', mixer_interaction_id=mixer_interaction_id)
            return CommonTestResult(False, reason=f'No mixer interaction found {mixer_interaction_id}', hide_tooltip=True)
        source_interaction = sim.posture.source_interaction
        if source_interaction is None:
            log.debug('Sim did not have a source interaction.')
            return CommonTestResult(False, reason=f'No source interaction found on Sim {sim_info}', hide_tooltip=True)
        if hasattr(mixer_interaction_instance, 'lock_out_time') and mixer_interaction_instance.lock_out_time:
            log.debug('Using Sim specific lock out time.')
            sim_specific_lockout = mixer_interaction_instance.lock_out_time.target_based_lock_out
        else:
            log.debug('Not using Sim specific lock out time.')
            sim_specific_lockout = False

        if sim_specific_lockout and sim.is_sub_action_locked_out(mixer_interaction_instance):
            log.debug('Sim was locked out of performing the mixer interaction.')
            return CommonTestResult(False, reason=f'{sim_info} is currently locked out of doing the mixer interaction, they must wait before they can do it again.', hide_tooltip=True)

        super_interaction_instance = source_interaction.super_affordance
        interaction_context = interaction_context or cls.create_interaction_context(sim_info)
        for (aop, test_result) in get_valid_aops_gen(
            target,
            mixer_interaction_instance,
            super_interaction_instance,
            source_interaction,
            interaction_context,
            False,
            push_super_on_prepare=False
        ):
            test_result = CommonTestResult.convert_from_vanilla(test_result)
            if test_result is None or test_result.result:
                log.format_with_message('Failed to queue using affordance.', aop=aop, affordance=aop.affordance)
                continue
            interaction_constraint = aop.constraint_intersection(sim=sim, posture_state=None)
            # noinspection PyPropertyAccess
            posture_constraint = sim.posture_state.posture_constraint_strict
            constraint_intersection = interaction_constraint.intersect(posture_constraint)
            if not constraint_intersection.valid:
                log.format_with_message('Constraint interaction was invalid.', constraint_intersection=constraint_intersection)
                continue
            log.format_with_message('Executing interaction using Aop.', aop=aop, affordance=aop.affordance)
            return aop.test(interaction_context, **kwargs)

    @classmethod
    def create_interaction_context(
        cls,
        sim_info: SimInfo,
        interaction_source: InteractionSource = InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT,
        priority: Priority = Priority.High,
        run_priority: Union[Priority, None] = Priority.High,
        insert_strategy: QueueInsertStrategy = QueueInsertStrategy.NEXT,
        must_run_next: bool = False,
        **kwargs
    ) -> Union[InteractionContext, None]:
        """create_interaction_context(\
            sim_info,\
            interaction_source=InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT,\
            priority=Priority.High,\
            run_priority=Priority.High,\
            insert_strategy=QueueInsertStrategy.NEXT,\
            must_run_next=False,\
            **kwargs\
        )

        Create an InteractionContext.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param interaction_source: The source of the interaction. Default is InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT.
        :type interaction_source: InteractionSource, optional
        :param priority: The priority of the interaction. Default is Priority.High.
        :type priority: Priority, optional
        :param run_priority: The priority of running the interaction. Default is Priority.High.
        :type run_priority: Union[Priority, None], optional
        :param insert_strategy: The insert strategy for the interaction. Default is QueueInsertStrategy.NEXT.
        :type insert_strategy: QueueInsertStrategy, optional
        :param must_run_next: If True, the interaction will run next. Default is False.
        :type must_run_next: bool, optional
        :return: An interaction context for use with interactions or None if a problem occurs.
        :rtype: Union[InteractionContext, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return InteractionContext(
            sim,
            interaction_source,
            priority,
            run_priority=run_priority,
            insert_strategy=insert_strategy,
            must_run_next=must_run_next,
            **kwargs
        )


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_running_interactions',
    'Print a list of all interactions a Sim is running.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printrunninginteractions',
    )
)
def _common_show_running_interactions(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    log = CommonSimInteractionUtils.get_log()
    try:
        log.enable()
        output(f'Attempting to print all running and queued interactions of Sim {sim_info}')
        from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
        running_interaction_strings: List[str] = list()
        for interaction in CommonSimInteractionUtils.get_running_interactions_gen(sim_info):
            interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction) or interaction.__class__.__name__
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            running_interaction_strings.append(f'{interaction_name} ({interaction_id})')

        running_interaction_strings = sorted(running_interaction_strings, key=lambda x: x)
        running_interaction_names = ', '.join(running_interaction_strings)

        queued_interaction_strings: List[str] = list()
        for interaction in CommonSimInteractionUtils.get_queued_interactions_gen(sim_info):
            interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction) or interaction.__class__.__name__
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            queued_interaction_strings.append(f'{interaction_name} ({interaction_id})')

        queued_interaction_strings = sorted(queued_interaction_strings, key=lambda x: x)
        queued_interaction_names = ', '.join(queued_interaction_strings)
        text = ''
        text += f'Running Interactions:\n{running_interaction_names}\n\n'
        text += f'Queued Interactions:\n{queued_interaction_names}\n\n'
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        log.debug(f'{sim_info} Interactions ({sim_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{sim_info} Interactions ({sim_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info))
        )
    finally:
        log.disable()
