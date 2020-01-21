"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 's4cl_age_species_utils')


class CommonAgeSpeciesUtils:
    """Utilities for combinations of a Sims age and species.

    """
    @staticmethod
    def is_baby_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Baby Human.

        """
        return CommonAgeUtils.is_baby(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_toddler_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Toddler Human.

        """
        return CommonAgeUtils.is_toddler(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_child_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Child Human.

        """
        return CommonAgeUtils.is_child(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Teen Human.

        """
        return CommonAgeUtils.is_teen(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_young_adult_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Young Adult Human.

        """
        return CommonAgeUtils.is_young_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_mature_adult_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Adult Human.

        """
        return CommonAgeUtils.is_mature_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_elder_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Elder Human.

        """
        return CommonAgeUtils.is_elder(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_adult_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Young Adult or Adult Human.

        """
        return CommonAgeUtils.is_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_baby_or_toddler_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Baby or Toddler Human.

        """
        return CommonAgeUtils.is_baby_or_toddler(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_child_or_teen_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Child or Teen Human.

        """
        return CommonAgeUtils.is_child_or_teen(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_toddler_or_child_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Toddler or Child Human.

        """
        return CommonAgeUtils.is_toddler_or_child(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_baby_toddler_or_child_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Baby, Toddler, or Child Human.

        """
        return CommonAgeUtils.is_baby_toddler_or_child(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_or_young_adult_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Teen or Young Adult Human.

        """
        return CommonAgeUtils.is_teen_or_young_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_or_adult_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Teen, Young Adult, or Adult Human.

        """
        return CommonAgeUtils.is_teen_or_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_mature_adult_or_elder_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Adult or Elder Human.

        """
        return CommonAgeUtils.is_mature_adult_or_elder(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_adult_or_elder_human(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Teen, Young Adult, Adult, or Elder Human.

        """
        return CommonAgeUtils.is_teen_adult_or_elder(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_child_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Child Pet.

        """
        return CommonAgeUtils.is_child(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_adult_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Adult Pet.

        """
        return CommonAgeUtils.is_adult(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_elder_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Elder Pet.

        """
        return CommonAgeUtils.is_elder(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_old_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Adult or Elder Pet.

        """
        return CommonAgeUtils.is_adult_or_elder(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_adult_human_or_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is a Young Adult or Adult Human or an Adult Pet.

        """
        return CommonAgeSpeciesUtils.is_adult_human(sim_info) or CommonAgeSpeciesUtils.is_adult_pet(sim_info)

    @staticmethod
    def is_elder_human_or_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is an Elder Human or Pet.

        """
        return CommonAgeSpeciesUtils.is_elder_human(sim_info) or CommonAgeSpeciesUtils.is_elder_pet(sim_info)

    @staticmethod
    def is_young_human_or_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is a young (Baby, Toddler, Child) Human or a young (Child) Pet.

        """
        return CommonAgeSpeciesUtils.is_baby_toddler_or_child_human(sim_info) or CommonAgeSpeciesUtils.is_child_pet(sim_info)

    @staticmethod
    def is_old_human_or_pet(sim_info: SimInfo) -> bool:
        """Determine if a sim is an old (Teen, Young Adult, Adult, Elder) Human or an old (Adult, Elder) Pet.

        """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info) or CommonAgeSpeciesUtils.is_old_pet(sim_info)

    @staticmethod
    def are_same_age_and_species(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """Determine if two Sims are the same Age and the same Species.

        """
        return CommonAgeUtils.are_same_age(sim_info, other_sim_info) and CommonSpeciesUtils.are_same_species(sim_info, other_sim_info)
