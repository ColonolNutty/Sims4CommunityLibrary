"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union, Any, Callable

from event_testing.results import EnqueueResult, TestResult
from interactions.aop import AffordanceObjectPair
from interactions.base.interaction import Interaction
from interactions.context import InteractionSource, InteractionContext, QueueInsertStrategy
from interactions.interaction_finisher import FinishingType
from interactions.priority import Priority
from sims.sim_info import SimInfo
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'common_sim_interaction_utils')


class CommonSimInteractionUtils:
    """Utilities for manipulating the interactions of Sims.

    """
    @staticmethod
    def is_sitting(sim_info: SimInfo) -> bool:
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
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, interactions)

    @staticmethod
    def is_standing(sim_info: SimInfo) -> bool:
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
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, interactions)

    @staticmethod
    def is_swimming(sim_info: SimInfo) -> bool:
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
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, interactions)

    @staticmethod
    def get_swim_interaction(sim_info: SimInfo) -> Union[int, CommonInteractionId]:
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

    @staticmethod
    def get_stand_interaction(sim_info: SimInfo) -> Union[int, CommonInteractionId]:
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
        return -1

    @staticmethod
    def lock_interaction_queue(sim_info: SimInfo):
        """lock_interaction_queue(sim_info)

        Lock the interaction queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.queue is None:
            return
        sim.queue.lock()

    @staticmethod
    def unlock_interaction_queue(sim_info: SimInfo):
        """unlock_interaction_queue(sim_info)

        Unlock the interaction queue of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.queue is None:
            return
        sim.queue.unlock()

    @staticmethod
    def has_interaction_running_or_queued(sim_info: SimInfo, interaction_id: Union[int, CommonInteractionId]) -> bool:
        """has_interaction_running_or_queued(sim_info, interaction_id)

        Determine if a Sim has the specified interaction running or in their interaction queue.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_id: The identifier of the interaction to check for.
        :type interaction_id: Union[int, CommonInteractionId]
        :return: True, if the Sim has the specified interaction running or queued. False, if not.
        :rtype: bool
        """
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, (interaction_id, ))

    @staticmethod
    def has_interaction_running(sim_info: SimInfo, interaction_id: Union[int, CommonInteractionId]) -> bool:
        """has_interaction_running(sim_info, interaction_id)

        Determine if a Sim is running the specified interaction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_id: The identifier of the interaction to check for.
        :type interaction_id: Union[int, CommonInteractionId]
        :return: True, if the Sim has the specified interaction running. False, if not.
        :rtype: bool
        """
        return CommonSimInteractionUtils.has_interactions_running(sim_info, (interaction_id, ))

    @staticmethod
    def has_interaction_queued(sim_info: SimInfo, interaction_id: Union[int, CommonInteractionId]) -> bool:
        """has_interaction_queued(sim_info, interaction_id)

        Determine if a Sim is running the specified interaction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_id: The identifier of the interaction to check for.
        :type interaction_id: Union[int, CommonInteractionId]
        :return: True, if the Sim has the specified interaction queued. False, if not.
        :rtype: bool
        """
        return CommonSimInteractionUtils.has_interactions_queued(sim_info, (interaction_id, ))

    @staticmethod
    def has_interactions_running_or_queued(sim_info: SimInfo, interaction_ids: Iterator[Union[int, CommonInteractionId]]) -> bool:
        """has_interactions_running_or_queued(sim_info, interaction_ids)

        Determine if a Sim has any of the specified interactions running or in their interaction queue.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_ids: An iterable of identifiers of the interactions to check for.
        :type interaction_ids: Union[int, CommonInteractionId]
        :return: True, if the Sim has any of the specified interactions running or queued. False, if not.
        :rtype: bool
        """
        return CommonSimInteractionUtils.has_interactions_running(sim_info, interaction_ids)\
               or CommonSimInteractionUtils.has_interactions_queued(sim_info, interaction_ids)

    @staticmethod
    def has_interactions_running(sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """has_interactions_running(sim_info, interaction_ids)

        Determine if a Sim is running any of the specified interactions.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_ids: An iterable of identifiers of the interactions to check for.
        :type interaction_ids: Union[int, CommonInteractionId]
        :return: True, if the Sim has any of the specified interactions running. False, if not.
        :rtype: bool
        """
        for interaction in CommonSimInteractionUtils.get_running_interactions_gen(sim_info):
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            if interaction_id in interaction_ids:
                return True
        return False

    @staticmethod
    def has_interactions_queued(sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """has_interactions_queued(sim_info, interaction_ids)

        Determine if a Sim has any of the specified interactions in their interaction queue.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param interaction_ids: An iterable of identifiers of the interactions to check for.
        :type interaction_ids: Union[int, CommonInteractionId]
        :return: True, if the Sim has any of the specified interactions queued. False, if not.
        :rtype: bool
        """
        for interaction in CommonSimInteractionUtils.get_queued_interactions_gen(sim_info):
            interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
            if interaction_id in interaction_ids:
                return True
        return False

    @staticmethod
    def cancel_all_queued_or_running_interactions(sim_info: SimInfo, cancel_reason: str, finishing_type: FinishingType=FinishingType.USER_CANCEL, include_interaction_callback: Callable[[Interaction], bool]=None, **kwargs) -> bool:
        """cancel_all_queued_or_running_interactions(sim_info, cancel_reason, finishing_type=FinishingType.USER_CANCEL, include_interaction_callback=None, **kwargs)

        Cancel all interactions that a Sim currently has queued or is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be cancelled. If set to None, All interactions will be cancelled. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: True, if all queued and running interactions were successfully cancelled. False, if not.
        :rtype: bool
        """
        return CommonSimInteractionUtils.cancel_all_queued_interactions(sim_info, cancel_reason, finishing_type=finishing_type, include_interaction_callback=include_interaction_callback, **kwargs)\
               and CommonSimInteractionUtils.cancel_all_running_interactions(sim_info, cancel_reason, finishing_type=finishing_type, include_interaction_callback=include_interaction_callback, **kwargs)

    @staticmethod
    def cancel_all_running_interactions(sim_info: SimInfo, cancel_reason: str, finishing_type: FinishingType=FinishingType.USER_CANCEL, include_interaction_callback: Callable[[Interaction], bool]=None, **kwargs) -> bool:
        """cancel_all_running_interactions(sim_info, cancel_reason, finishing_type=FinishingType.USER_CANCEL, include_interaction_callback=None, **kwargs)

        Cancel all interactions that a Sim is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be cancelled. If set to None, All interactions will be cancelled. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: True, if all running interactions were successfully cancelled. False, if not.
        :rtype: bool
        """
        for interaction in CommonSimInteractionUtils.get_running_interactions_gen(sim_info, include_interaction_callback=include_interaction_callback):
            interaction.cancel(finishing_type, cancel_reason_msg=cancel_reason, **kwargs)
        return True

    @staticmethod
    def cancel_all_queued_interactions(sim_info: SimInfo, cancel_reason: str, finishing_type: FinishingType=FinishingType.USER_CANCEL, include_interaction_callback: Callable[[Interaction], bool]=None, **kwargs) -> bool:
        """cancel_all_queued_interactions(sim_info, cancel_reason, finishing_type=FinishingType.USER_CANCEL, include_interaction_callback=None, **kwargs)

        Cancel all interactions that a Sim currently has queued.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cancel_reason: The reason for the cancellation.
        :type cancel_reason: str
        :param finishing_type: The type of finish to finish the interaction with. Default is FinishingType.USER_CANCEL.
        :type finishing_type: FinishingType, optional
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be cancelled. If set to None, All interactions will be cancelled. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: True, if all queued interactions were successfully cancelled. False, if not.
        :rtype: bool
        """
        for interaction in CommonSimInteractionUtils.get_queued_interactions_gen(sim_info, include_interaction_callback=include_interaction_callback):
            interaction.cancel(finishing_type, cancel_reason_msg=cancel_reason, **kwargs)
        return True

    @staticmethod
    def get_running_interactions_gen(sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool]=None) -> Iterator[Interaction]:
        """get_running_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim is currently running.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterable of Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return tuple()
        if sim.si_state is None or not tuple(sim.si_state):
            return tuple()
        for interaction in sim.si_state:
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction

    @staticmethod
    def get_queued_interactions_gen(sim_info: SimInfo, include_interaction_callback: Callable[[Interaction], bool]=None) -> Iterator[Interaction]:
        """get_queued_interactions_gen(sim_info, include_interaction_callback=None)

        Retrieve all interactions that a Sim currently has queued.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterable of Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return tuple()
        if sim.queue is None or not tuple(sim.queue):
            return tuple()
        for interaction in sim.queue:
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction

    @staticmethod
    def queue_interaction(
        sim_info: SimInfo,
        interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId]=None,
        target: Any=None,
        picked_object: Any=None,
        interaction_context: InteractionContext=None,
        skip_if_running: bool=False,
        **kwargs
    ) -> EnqueueResult:
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
        :rtype: EnqueueResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.si_state is None or sim.queue is None or sim.posture_state is None or sim.posture is None:
            return EnqueueResult.NONE
        interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction_id)
        if interaction_instance is None:
            return EnqueueResult.NONE
        if skip_if_running and CommonSimInteractionUtils.has_interaction_running_or_queued(sim_info, interaction_id):
            return EnqueueResult.NONE

        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(
            sim_info,
            insert_strategy=QueueInsertStrategy.LAST
        )

        if CommonInteractionUtils.is_super_interaction(interaction_instance):
            return CommonSimInteractionUtils.queue_super_interaction(
                sim_info,
                interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        if CommonInteractionUtils.is_social_mixer_interaction(interaction_instance):
            return CommonSimInteractionUtils.queue_social_mixer_interaction(
                sim_info,
                interaction_id,
                social_super_interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        return CommonSimInteractionUtils.queue_mixer_interaction(
            sim_info,
            interaction_id,
            target=target,
            interaction_context=interaction_context
        )

    @staticmethod
    def queue_super_interaction(
        sim_info: SimInfo,
        super_interaction_id: Union[int, CommonInteractionId],
        target: Any=None,
        picked_object: Any=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> EnqueueResult:
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
        :rtype: EnqueueResult
        """
        log.format_with_message('Pushing super interaction', sim=sim_info, interaction_id=super_interaction_id, target=target, interaction_context=interaction_context)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            log.debug('No sim instance.')
            return EnqueueResult.NONE

        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)

        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(sim_info)
        super_interaction_instance = CommonInteractionUtils.load_interaction_by_id(super_interaction_id)
        if super_interaction_instance is None:
            log.format_with_message('No super interaction instance found for id.', super_interaction_id=super_interaction_id)
            return EnqueueResult.NONE

        return sim.push_super_affordance(
            super_interaction_instance,
            target,
            interaction_context,
            picked_object=picked_object or target,
            **kwargs
        )

    @staticmethod
    def queue_social_mixer_interaction(
        sim_info: SimInfo,
        social_mixer_interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId],
        target: SimInfo=None,
        picked_object: Any=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> EnqueueResult:
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
        :rtype: EnqueueResult
        """
        if social_super_interaction_id is not None and social_mixer_interaction_id is None:
            return CommonSimInteractionUtils.queue_super_interaction(
                sim_info,
                social_super_interaction_id,
                target=target,
                picked_object=picked_object,
                interaction_context=interaction_context,
                **kwargs
            )

        social_super_interaction_id: Union[int, CommonInteractionId] = social_super_interaction_id
        sim = CommonSimUtils.get_sim_instance(sim_info)
        social_mixer_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_mixer_interaction_id)
        if social_mixer_affordance_instance is None:
            log.debug('No social mixer affordance instance found with id.')
            return EnqueueResult.NONE

        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(
            sim_info,
            picked_object=picked_object or target,
            **kwargs
        )
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
                si_result = CommonSimInteractionUtils.queue_interaction(
                    sim_info,
                    social_super_interaction_id,
                    target=target,
                    picked_object=picked_object or target,
                    interaction_context=interaction_context,
                    **kwargs
                )
                if not si_result:
                    log.format_with_message('Failed to locate existing super interaction.', super_interaction=super_interaction)
                    return EnqueueResult.NONE
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

    @staticmethod
    def queue_mixer_interaction(
        sim_info: SimInfo,
        mixer_interaction_id: Union[int, CommonInteractionId],
        target: Any=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> EnqueueResult:
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
        :rtype: EnqueueResult
        """
        from autonomy.content_sets import get_valid_aops_gen

        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return EnqueueResult.NONE
        if sim.posture is None:
            return EnqueueResult.NONE
        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)
        mixer_interaction_instance = CommonInteractionUtils.load_interaction_by_id(mixer_interaction_id)
        if mixer_interaction_instance is None:
            return EnqueueResult.NONE
        source_interaction = sim.posture.source_interaction
        if source_interaction is None:
            return EnqueueResult.NONE
        if hasattr(mixer_interaction_instance, 'lock_out_time') and mixer_interaction_instance.lock_out_time:
            sim_specific_lockout = mixer_interaction_instance.lock_out_time.target_based_lock_out
        else:
            sim_specific_lockout = False

        if sim_specific_lockout and sim.is_sub_action_locked_out(mixer_interaction_instance):
            return EnqueueResult.NONE

        super_interaction_instance = source_interaction.super_affordance
        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(sim_info)
        for (aop, test_result) in get_valid_aops_gen(
            target,
            mixer_interaction_instance,
            super_interaction_instance,
            source_interaction,
            interaction_context,
            False,
            push_super_on_prepare=False
        ):
            test_result: TestResult = test_result
            if test_result is None or test_result.result:
                continue
            interaction_constraint = aop.constraint_intersection(sim=sim, posture_state=None)
            # noinspection PyPropertyAccess
            posture_constraint = sim.posture_state.posture_constraint_strict
            constraint_intersection = interaction_constraint.intersect(posture_constraint)
            if not constraint_intersection.valid:
                continue
            return aop.execute(interaction_context, **kwargs)

    @staticmethod
    def test_interaction(
        sim_info: SimInfo,
        interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId]=None,
        target: Any=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> TestResult:
        """test_interaction(\
            sim_info,\
            interaction_id,\
            social_super_interaction_id=None,\
            target=None,\
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
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: TestResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.si_state is None or sim.queue is None or sim.posture_state is None or sim.posture is None:
            return TestResult.NONE
        interaction_instance = CommonInteractionUtils.load_interaction_by_id(interaction_id)
        if interaction_instance is None:
            return TestResult.NONE

        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(
            sim_info,
            insert_strategy=QueueInsertStrategy.LAST
        )

        if CommonInteractionUtils.is_super_interaction(interaction_instance):
            return CommonSimInteractionUtils.test_super_interaction(
                sim_info,
                interaction_id,
                target=target,
                interaction_context=interaction_context,
                **kwargs
            )

        if CommonInteractionUtils.is_social_mixer_interaction(interaction_instance):
            return CommonSimInteractionUtils.test_social_mixer_interaction(
                sim_info,
                interaction_id,
                social_super_interaction_id,
                target=target,
                interaction_context=interaction_context,
                **kwargs
            )

        return CommonSimInteractionUtils.test_mixer_interaction(
            sim_info,
            interaction_id,
            target=target,
            interaction_context=interaction_context
        )

    @staticmethod
    def test_super_interaction(
        sim_info: SimInfo,
        super_interaction_id: Union[int, CommonInteractionId],
        target: Any=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> TestResult:
        """test_super_interaction(\
            sim_info,\
            super_interaction_id,\
            target=None,\
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
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: TestResult
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return TestResult.NONE

        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)

        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(sim_info)
        super_interaction_instance = CommonInteractionUtils.load_interaction_by_id(super_interaction_id)
        if super_interaction_instance is None:
            return TestResult.NONE

        return sim.test_super_affordance(
            super_interaction_instance,
            target,
            interaction_context,
            picked_object=target,
            **kwargs
        )

    @staticmethod
    def test_social_mixer_interaction(
        sim_info: SimInfo,
        social_mixer_interaction_id: Union[int, CommonInteractionId],
        social_super_interaction_id: Union[int, CommonInteractionId],
        target: SimInfo=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> TestResult:
        """test_social_mixer_interaction(\
            sim_info,\
            social_mixer_interaction_id,\
            social_super_interaction_id,\
            target=None,\
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
        :param interaction_context: The context to queue the interaction with. See also :func:`~create_interaction_context`. Default is None.
        :type interaction_context: InteractionContext, optional
        :return: The result of testing a push of the interaction to the queue of a Sim.
        :rtype: TestResult
        """
        if social_super_interaction_id is not None and social_mixer_interaction_id is None:
            return CommonSimInteractionUtils.test_super_interaction(sim_info, social_super_interaction_id, target=target, interaction_context=interaction_context)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        # noinspection PyTypeChecker
        super_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_super_interaction_id)
        if super_affordance_instance is None:
            return TestResult.NONE
        mixer_affordance_instance = CommonInteractionUtils.load_interaction_by_id(social_mixer_interaction_id)
        if mixer_affordance_instance is None:
            return TestResult.NONE

        def _get_existing_social_super_interaction(si_iter) -> Interaction:
            for si in si_iter:
                if si.super_affordance != super_affordance_instance:
                    continue
                if si.social_group is None:
                    continue
                target_sim = CommonSimUtils.get_sim_instance(target)
                if target_sim is not None and target_sim not in si.social_group:
                    continue
                return si.super_interaction

        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(sim_info)
        super_interaction = _get_existing_social_super_interaction(sim.si_state) or _get_existing_social_super_interaction(sim.queue)
        if super_interaction is None:
            si_result = sim.test_super_affordance(
                super_affordance_instance,
                target,
                interaction_context,
                picked_object=target,
                **kwargs
            )
            if not si_result or not si_result.result:
                return TestResult.NONE
            super_interaction = si_result.interaction

        pick = super_interaction.context.pick
        preferred_objects = super_interaction.context.preferred_objects
        context = super_interaction.context.clone_for_continuation(
            super_interaction,
            insert_strategy=interaction_context.insert_strategy,
            source_interaction_id=super_interaction.id,
            source_interaction_sim_id=CommonSimUtils.get_sim_id(sim_info),
            pick=pick,
            preferred_objects=preferred_objects,
            must_run_next=interaction_context.must_run_next
        )
        aop = AffordanceObjectPair(
            mixer_affordance_instance,
            target,
            super_affordance_instance,
            super_interaction,
            picked_object=target,
            push_super_on_prepare=True
        )
        return aop.test(context)

    @staticmethod
    def test_mixer_interaction(
        sim_info: SimInfo,
        mixer_interaction_id: Union[int, CommonInteractionId],
        target: Any=None,
        interaction_context: InteractionContext=None,
        **kwargs
    ) -> TestResult:
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
        :rtype: TestResult
        """
        from autonomy.content_sets import get_valid_aops_gen

        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return TestResult.NONE
        if sim.posture is None:
            return TestResult.NONE
        if target is not None and CommonTypeUtils.is_sim_or_sim_info(target):
            target = CommonSimUtils.get_sim_instance(target)
        mixer_interaction_instance = CommonInteractionUtils.load_interaction_by_id(mixer_interaction_id)
        if mixer_interaction_instance is None:
            return TestResult.NONE
        source_interaction = sim.posture.source_interaction
        if source_interaction is None:
            return TestResult.NONE
        if hasattr(mixer_interaction_instance, 'lock_out_time') and mixer_interaction_instance.lock_out_time:
            sim_specific_lockout = mixer_interaction_instance.lock_out_time.target_based_lock_out
        else:
            sim_specific_lockout = False

        if sim_specific_lockout and sim.is_sub_action_locked_out(mixer_interaction_instance):
            return TestResult.NONE

        super_interaction_instance = source_interaction.super_affordance
        interaction_context = interaction_context or CommonSimInteractionUtils.create_interaction_context(sim_info)
        for (aop, test_result) in get_valid_aops_gen(
            target,
            mixer_interaction_instance,
            super_interaction_instance,
            source_interaction,
            interaction_context,
            False,
            push_super_on_prepare=False
        ):
            test_result: TestResult = test_result
            if test_result is None or test_result.result:
                continue
            interaction_constraint = aop.constraint_intersection(sim=sim, posture_state=None)
            # noinspection PyPropertyAccess
            posture_constraint = sim.posture_state.posture_constraint_strict
            constraint_intersection = interaction_constraint.intersect(posture_constraint)
            if not constraint_intersection.valid:
                continue
            return aop.test(interaction_context, **kwargs)

    @staticmethod
    def create_interaction_context(
        sim_info: SimInfo,
        interaction_source: InteractionSource=InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT,
        priority: Priority=Priority.High,
        run_priority: Union[Priority, None]=Priority.High,
        insert_strategy: QueueInsertStrategy=QueueInsertStrategy.NEXT,
        must_run_next: bool=False,
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
