"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""

from typing import Iterator

from sims.sim_info import SimInfo
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimInteractionUtils:
    """Utilities for managing interactions.

    """
    @staticmethod
    def is_sitting(sim_info: SimInfo) -> bool:
        """Determine if a Sim is currently sitting.

        """
        interactions = (
            CommonInteractionId.SEATING_SIT,
            CommonInteractionId.SEATING_SIT_CTYAE,
            CommonInteractionId.SEATING_SIT_RESTAURANT_RALLY_ONLY,
            CommonInteractionId.SEATING_SIT_SINGLE,
            CommonInteractionId.SEATING_SIT_TODDLER_BED,
            CommonInteractionId.SIT_PASSIVE,
            CommonInteractionId.SEATING_SIT_POST_GRAND_MEAL_WAIT_ENJOY_COMPANY,
            CommonInteractionId.SEATING_SIT_DIRECTOR_CHAIR,
            CommonInteractionId.SEATING_SIT_HAIR_MAKE_UP_CHAIR
        )
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, interactions)

    @staticmethod
    def has_interaction_running_or_queued(sim_info: SimInfo, interaction_id: int) -> bool:
        """Determine if a Sim has the specified interaction running or in their interaction queue.

        """
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, (interaction_id, ))

    @staticmethod
    def has_interaction_running(sim_info: SimInfo, interaction_id: int) -> bool:
        """Determine if a Sim is running the specified interaction.

        """
        return CommonSimInteractionUtils.has_interactions_running(sim_info, (interaction_id, ))

    @staticmethod
    def has_interaction_queued(sim_info: SimInfo, interaction_id: int) -> bool:
        """Determine if a Sim is running the specified interaction.

        """
        return CommonSimInteractionUtils.has_interactions_queued(sim_info, (interaction_id, ))

    @staticmethod
    def has_interactions_running_or_queued(sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """Determine if a Sim has any of the specified interactions running or in their interaction queue.

        """
        return CommonSimInteractionUtils.has_interactions_running(sim_info, interaction_ids)\
               or CommonSimInteractionUtils.has_interactions_queued(sim_info, interaction_ids)

    @staticmethod
    def has_interactions_running(sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """Determine if a Sim is running any of the specified interactions.

        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.si_state is None:
            return False
        for interaction in sim.si_state:
            interaction_id = getattr(interaction, 'guid64', None)
            if interaction_id in interaction_ids:
                return True
        return False

    @staticmethod
    def has_interactions_queued(sim_info: SimInfo, interaction_ids: Iterator[int]) -> bool:
        """Determine if a Sim has any of the specified interactions in their interaction queue.

        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or sim.queue is None:
            return False
        for interaction in sim.queue:
            interaction_id = getattr(interaction, 'guid64', None)
            if interaction_id in interaction_ids:
                return True
        return False
