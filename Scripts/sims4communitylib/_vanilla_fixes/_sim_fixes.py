"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from traits.trait_tracker import TraitTracker

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'sim_fixes_log')

if hasattr(Sim, 'can_see'):
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.can_see.__name__)
    def _common_fix_can_see_error(original, self: Sim, *_, **__):
        try:
            if not hasattr(self, 'los_constraint') or self.los_constraint is None:
                return False
            return original(self, *_, **__)
        except Exception as ex:
            raise ex


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TraitTracker, TraitTracker._add_default_gender_option_traits.__name__)
def _common_fix_add_default_gender_option_traits_being_busted(original, self: TraitTracker, *_, **__):
    sim_info = self.get_sim_info_from_provider()
    if sim_info is None:
        return
    uses_toilet_standing = CommonSimGenderOptionUtils.uses_toilet_standing(sim_info)
    uses_toilet_sitting = CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info)
    gender_option_traits = self.DEFAULT_GENDER_OPTION_TRAITS.get(self._sim_info.gender)
    for gender_option_trait in gender_option_traits:
        trait_id = CommonTraitUtils.get_trait_id(gender_option_trait)
        if trait_id == CommonTraitId.GENDER_OPTIONS_TOILET_STANDING:
            if uses_toilet_standing or uses_toilet_sitting:
                continue
        if trait_id == CommonTraitId.GENDER_OPTIONS_TOILET_SITTING:
            if uses_toilet_standing or uses_toilet_sitting:
                continue
        if trait_id == CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_FEMALE:
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_NOT_FEMALE):
                continue
        if trait_id == CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_MALE:
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_NOT_MALE):
                continue
        if trait_id == CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_NOT_FEMALE:
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_FEMALE):
                continue
        if trait_id == CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_NOT_MALE:
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_ATTRACTED_TO_MALE):
                continue
        if not self.has_trait(gender_option_trait):
            self._add_trait(gender_option_trait)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.send_satisfaction_points_update.__name__)
def _common_fix_missing_satisfaction_tracker_send_satisfaction_points_update(original, self: SimInfo, *_, **__):
    if not self._satisfaction_tracker:
        return
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.apply_satisfaction_points_delta.__name__)
def _common_fix_missing_satisfaction_tracker_apply_satisfaction_points_delta(original, self: SimInfo, *_, **__):
    if not self._satisfaction_tracker:
        return
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.get_satisfaction_points.__name__)
def _common_fix_missing_satisfaction_tracker_get_satisfaction_points(original, self: SimInfo, *_, **__):
    if not self._satisfaction_tracker:
        return 0
    return original(self, *_, **__)
