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
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class _S4CLAutoApplyTraits:
    """ Auto apply the S4CL main traits. """

    def _try_apply_traits(self, sim_info: SimInfo):
        # Main Trait
        if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT):
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT)

        if CommonSpeciesUtils.is_human(sim_info):
            # Main Trait
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT,
                CommonTraitId.S4CL_MAIN_TRAIT_FOX,
                CommonTraitId.S4CL_MAIN_TRAIT_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_HUMAN):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_HUMAN)
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            # Main Trait
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT,
                CommonTraitId.S4CL_MAIN_TRAIT_FOX,
                CommonTraitId.S4CL_MAIN_TRAIT_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG)
            # Toilet Standing/Sitting/Unknown
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN):
                CommonTraitUtils.remove_trait(
                    sim_info,
                    CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                    CommonTraitId.GENDER_OPTIONS_TOILET_SITTING,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_HORSE,
                    CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_HORSE,
                )
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG)

            # Can Impregnate
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG):
                if CommonGenderUtils.is_male(sim_info):
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG)
            # Can Be Impregnated
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG)
                else:
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG)
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            # Main Trait
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT,
                CommonTraitId.S4CL_MAIN_TRAIT_FOX,
                CommonTraitId.S4CL_MAIN_TRAIT_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG)
            # Toilet Standing/Sitting/Unknown
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                CommonTraitId.GENDER_OPTIONS_TOILET_SITTING,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG)
            # Can Impregnate
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG):
                if CommonGenderUtils.is_male(sim_info):
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG)
            # Can Be Impregnated
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG)
                else:
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG)
        elif CommonSpeciesUtils.is_cat(sim_info):
            # Main Trait
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_FOX,
                CommonTraitId.S4CL_MAIN_TRAIT_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_CAT):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_CAT)
            # Toilet Standing/Sitting/Unknown
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                CommonTraitId.GENDER_OPTIONS_TOILET_SITTING,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT)
            # Can Impregnate
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT):
                if CommonGenderUtils.is_male(sim_info):
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT)
            # Can Be Impregnated
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT)
                else:
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT)
        elif CommonSpeciesUtils.is_fox(sim_info):
            # Main Trait
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT,
                CommonTraitId.S4CL_MAIN_TRAIT_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_FOX):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_FOX)
            # Toilet Standing/Sitting/Unknown
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                CommonTraitId.GENDER_OPTIONS_TOILET_SITTING,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX)
            # Can Impregnate
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX):
                if CommonGenderUtils.is_male(sim_info):
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX)
            # Can Be Impregnated
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX)\
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX)
                else:
                    if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX)
                    else:
                        CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX)
        elif CommonSpeciesUtils.is_horse(sim_info):
            # Main Trait
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.S4CL_MAIN_TRAIT_HUMAN,
                CommonTraitId.S4CL_MAIN_TRAIT_LARGE_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_SMALL_DOG,
                CommonTraitId.S4CL_MAIN_TRAIT_CAT,
                CommonTraitId.S4CL_MAIN_TRAIT_FOX,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_HORSE):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_MAIN_TRAIT_HORSE)
            # Toilet Standing/Sitting/Unknown
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_TOILET_STANDING,
                CommonTraitId.GENDER_OPTIONS_TOILET_SITTING,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX,
            )
            if not CommonTraitUtils.has_trait(sim_info,
                                              CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_HORSE) \
                    and not CommonTraitUtils.has_trait(sim_info,
                                                       CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_HORSE) \
                    and not CommonTraitUtils.has_trait(sim_info,
                                                       CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info,
                                               CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_HORSE)
                else:
                    CommonTraitUtils.add_trait(sim_info,
                                               CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_HORSE)
            # Can Impregnate
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX,
            )
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE) \
                    and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info,
                                               CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE)
                else:
                    CommonTraitUtils.add_trait(sim_info,
                                               CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE)
            # Can Be Impregnated
            CommonTraitUtils.remove_trait(
                sim_info,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED,
                CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX,
                CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX,
            )
            if not CommonTraitUtils.has_trait(sim_info,
                                              CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE) \
                    and not CommonTraitUtils.has_trait(sim_info,
                                                       CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE):
                if CommonGenderUtils.is_male(sim_info):
                    CommonTraitUtils.add_trait(sim_info,
                                               CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE)
                else:
                    CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_auto_apply_traits_on_sim_spawned(event_data: S4CLSimSpawnedEvent):
    _S4CLAutoApplyTraits()._try_apply_traits(event_data.sim_info)
