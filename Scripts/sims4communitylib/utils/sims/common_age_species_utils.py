"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CommonAgeSpeciesUtils:
    """Utilities for checking the Age and Species of Sims.

    """
    @staticmethod
    def is_baby_human(sim_info: SimInfo) -> bool:
        """is_baby_human(sim_info)

        Determine if a sim is a Baby Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Baby Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_toddler_human(sim_info: SimInfo) -> bool:
        """is_toddler_human(sim_info)

        Determine if a sim is a Toddler Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Toddler Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_child_human(sim_info: SimInfo) -> bool:
        """is_child_human(sim_info)

        Determine if a sim is a Child Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Child Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_human(sim_info: SimInfo) -> bool:
        """is_teen_human(sim_info)

        Determine if a sim is a Teen Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Teen Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_young_adult_human(sim_info: SimInfo) -> bool:
        """is_young_adult_human(sim_info)

        Determine if a sim is a Young Adult Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Young Adult Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_young_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_mature_adult_human(sim_info: SimInfo) -> bool:
        """is_mature_adult_human(sim_info)

        Determine if a sim is an Adult Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Adult Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_elder_human(sim_info: SimInfo) -> bool:
        """is_elder_human(sim_info)

        Determine if a sim is an Elder Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Elder Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_elder(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_adult_human(sim_info: SimInfo) -> bool:
        """is_adult_human(sim_info)

        Determine if a sim is a Young Adult or Adult Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Young Adult or Adult Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_baby_or_toddler_human(sim_info: SimInfo) -> bool:
        """is_baby_or_toddler_human(sim_info)

        Determine if a sim is a Baby or Toddler Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Baby or Toddler Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_or_toddler(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_child_or_teen_human(sim_info: SimInfo) -> bool:
        """is_child_or_teen_human(sim_info)

        Determine if a sim is a Child or Teen Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Child or Teen Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_or_teen(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_toddler_or_child_human(sim_info: SimInfo) -> bool:
        """is_toddler_or_child_human(sim_info)

        Determine if a sim is a Toddler or Child Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Toddler or Child Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_or_child(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_baby_toddler_or_child_human(sim_info: SimInfo) -> bool:
        """is_baby_toddler_or_child_human(sim_info)

        Determine if a sim is a Baby, Toddler, or Child Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Baby, Toddler, or Child Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_toddler_or_child(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_or_young_adult_human(sim_info: SimInfo) -> bool:
        """is_teen_or_young_adult_human(sim_info)

        Determine if a sim is a Teen or Young Adult Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Teen or Young Adult Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_or_young_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_or_adult_human(sim_info: SimInfo) -> bool:
        """is_teen_or_adult_human(sim_info)

        Determine if a sim is a Teen, Young Adult, or Adult Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Teen, Young Adult, or Adult Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_or_adult(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_mature_adult_or_elder_human(sim_info: SimInfo) -> bool:
        """is_mature_adult_or_elder_human(sim_info)

        Determine if a sim is a Adult or Elder Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Adult or Elder Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_or_elder(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_teen_adult_or_elder_human(sim_info: SimInfo) -> bool:
        """is_teen_adult_or_elder_human(sim_info)

        Determine if a sim is a Teen, Young Adult, Adult, or Elder Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Teen, Young Adult, Adult, or Elder Human. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_adult_or_elder(sim_info) and CommonSpeciesUtils.is_human(sim_info)

    @staticmethod
    def is_child_pet(sim_info: SimInfo) -> bool:
        """is_child_pet(sim_info)

        Determine if a sim is a Child Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Child Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_adult_pet(sim_info: SimInfo) -> bool:
        """is_adult_pet(sim_info)

        Determine if a sim is an Adult Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Adult Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_elder_pet(sim_info: SimInfo) -> bool:
        """is_elder_pet(sim_info)

        Determine if a sim is an Elder Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Elder Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_elder(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_old_pet(sim_info: SimInfo) -> bool:
        """is_old_pet(sim_info)

        Determine if a sim is an Adult or Elder Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Adult or Elder Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_or_elder(sim_info) and CommonSpeciesUtils.is_pet(sim_info)

    @staticmethod
    def is_child_animal(sim_info: SimInfo) -> bool:
        """is_child_animal(sim_info)

        Determine if a sim is a Child Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Child Animal (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child(sim_info) and CommonSpeciesUtils.is_animal(sim_info)

    @staticmethod
    def is_adult_animal(sim_info: SimInfo) -> bool:
        """is_adult_animal(sim_info)

        Determine if a sim is an Adult Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Adult Pet (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult(sim_info) and CommonSpeciesUtils.is_animal(sim_info)

    @staticmethod
    def is_elder_animal(sim_info: SimInfo) -> bool:
        """is_elder_animal(sim_info)

        Determine if a sim is an Elder Pet (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Elder Pet (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_elder(sim_info) and CommonSpeciesUtils.is_animal(sim_info)

    @staticmethod
    def is_old_animal(sim_info: SimInfo) -> bool:
        """is_old_animal(sim_info)

        Determine if a Sim is an Adult or Elder Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Adult or Elder Animal (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_or_elder(sim_info) and CommonSpeciesUtils.is_animal(sim_info)

    @staticmethod
    def is_adult_human_or_pet(sim_info: SimInfo) -> bool:
        """is_adult_human_or_pet(sim_info)

        Determine if a sim is a Young Adult, Adult, or Elder Human or an Adult Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Young Adult, Adult, or Elder Human or an Adult Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_adult_human(sim_info) or CommonAgeSpeciesUtils.is_adult_pet(sim_info)

    @staticmethod
    def is_elder_human_or_pet(sim_info: SimInfo) -> bool:
        """is_elder_human_or_pet(sim_info)

        Determine if a sim is an Elder Human or Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Elder Human or Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_elder_human(sim_info) or CommonAgeSpeciesUtils.is_elder_pet(sim_info)

    @staticmethod
    def is_young_human_or_pet(sim_info: SimInfo) -> bool:
        """is_young_human_or_pet(sim_info)

        Determine if a sim is a Baby, Toddler, or Child Human or a Child Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Baby, Toddler, or Child Human or a Child Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_baby_toddler_or_child_human(sim_info) or CommonAgeSpeciesUtils.is_child_pet(sim_info)

    @staticmethod
    def is_old_human_or_pet(sim_info: SimInfo) -> bool:
        """is_old_human_or_pet(sim_info)

        Determine if a sim is a Teen, Young Adult, Adult, or Elder Human or an Adult or Elder Pet (Cat, Small Dog, Large Dog).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Teen, Young Adult, Adult, or Elder Human or an Adult or Elder Pet (Cat, Small Dog, Large Dog). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info) or CommonAgeSpeciesUtils.is_old_pet(sim_info)

    @staticmethod
    def is_adult_human_or_animal(sim_info: SimInfo) -> bool:
        """is_adult_human_or_animal(sim_info)

        Determine if a sim is a Young Adult, Adult, or Elder Human or an Adult Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Young Adult, Adult, or Elder Human or an Adult Animal (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_adult_human(sim_info) or CommonAgeSpeciesUtils.is_adult_animal(sim_info)

    @staticmethod
    def is_elder_human_or_animal(sim_info: SimInfo) -> bool:
        """is_elder_human_or_animal(sim_info)

        Determine if a sim is an Elder Human or Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Elder Human or Animal (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_elder_human(sim_info) or CommonAgeSpeciesUtils.is_elder_animal(sim_info)

    @staticmethod
    def is_young_human_or_animal(sim_info: SimInfo) -> bool:
        """is_young_human_or_animal(sim_info)

        Determine if a sim is a Baby, Toddler, or Child Human or a Child Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Baby, Toddler, or Child Human or a Child Animal (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_baby_toddler_or_child_human(sim_info) or CommonAgeSpeciesUtils.is_child_animal(sim_info)

    @staticmethod
    def is_old_human_or_animal(sim_info: SimInfo) -> bool:
        """is_old_human_or_animal(sim_info)

        Determine if a sim is a Teen, Young Adult, Adult, or Elder Human or an Adult or Elder Animal (Cat, Small Dog, Large Dog, Fox).

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Teen, Young Adult, Adult, or Elder Human or an Adult or Elder Animal (Cat, Small Dog, Large Dog, Fox). False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info) or CommonAgeSpeciesUtils.is_old_animal(sim_info)

    @staticmethod
    def are_same_age_and_species(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_age_and_species(sim_info, other_sim_info)

        Determine if two Sims are the same Age and the same Species.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The other Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Age and Species. False, if they are not.
        :rtype: bool
        """
        return CommonAgeUtils.are_same_age(sim_info, other_sim_info) and CommonSpeciesUtils.are_same_species(sim_info, other_sim_info)
