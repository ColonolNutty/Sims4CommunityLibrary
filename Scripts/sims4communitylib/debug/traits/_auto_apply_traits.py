"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class _S4CLAutoApplyTraits:
    """ Auto apply the S4CL main traits. """

    def _try_apply_traits(self, sim_info: SimInfo):
        if CommonSpeciesUtils.is_human(sim_info):
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT
            )
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_HUMAN):
                return
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_HUMAN)
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT
            )
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG):
                return
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG)
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT
            )
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG):
                return
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG)
        elif CommonSpeciesUtils.is_cat(sim_info):
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG
            )
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_CAT):
                return
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_CAT)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_auto_apply_traits_on_sim_spawned(event_data: S4CLSimSpawnedEvent):
    _S4CLAutoApplyTraits()._try_apply_traits(event_data.sim_info)
