"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo


class CommonSimTypeUtils:
    """ Utilities for determining the type of a Sim. i.e. Player, NPC, Service, etc. """

    @staticmethod
    def is_non_player_sim(sim_info: SimInfo) -> bool:
        """
            Determine if a Sim is a Non Player Sim.

            Note: An NPC Sim is a sim that is not a part of the active household.
        """
        return sim_info.is_npc

    @staticmethod
    def is_player_sim(sim_info: SimInfo) -> bool:
        """
            Determine if a Sim is a Player Sim.

            Note: A Player Sim is a sim that is a part of the active household.
        """
        return sim_info.is_player_sim

    @staticmethod
    def is_played_sim(sim_info: SimInfo) -> bool:
        """
            Determine if a Sim is a Played Sim.

            Note: This does not indicate whether or not a Sim is a Player Sim or Non Player Sim.
        """
        return sim_info.is_played_sim

    @staticmethod
    def is_service_sim(sim_info: SimInfo) -> bool:
        """
            Determine if a Sim is a Service Sim.

            Service Sims:
            - Butler
            - Chalet
            - City Repair
            - Forest Ranger
            - Gardener
            - Grim Reaper
            - Maid
            - Mailman
            - Massage Therapist
            - Master Fisherman
            - Master Gardener
            - Master Herbalist
            - Nanny
            - Pizza Delivery
            - Repairman
            - Restaurant Critic
            - Statue Busker
        """
        from sims4communitylib.enums.traits_enum import CommonTraitId
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        trait_ids = (
            CommonTraitId.IS_BUTLER,
            CommonTraitId.IS_CHALET_GARDENS_GHOST,
            CommonTraitId.IS_CITY_REPAIR,
            CommonTraitId.IS_FOREST_RANGER,
            CommonTraitId.IS_GARDENER,
            CommonTraitId.IS_GARDENER_SERVICE,
            CommonTraitId.IS_GRIM_REAPER,
            CommonTraitId.IS_MAID,
            CommonTraitId.IS_MAILMAN,
            CommonTraitId.IS_MASSAGE_THERAPIST,
            CommonTraitId.IS_MASTER_FISHERMAN,
            CommonTraitId.IS_MASTER_GARDENER,
            CommonTraitId.IS_MASTER_HERBALIST,
            CommonTraitId.IS_NANNY,
            CommonTraitId.IS_PIZZA_DELIVERY,
            CommonTraitId.IS_REPAIR,
            CommonTraitId.IS_RESTAURANT_CRITIC,
            CommonTraitId.IS_STATUE_BUSKER
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)
