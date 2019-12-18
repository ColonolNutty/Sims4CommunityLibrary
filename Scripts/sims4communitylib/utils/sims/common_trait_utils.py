"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Union
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from traits.traits import Trait


class CommonTraitUtils:
    """ Utilities for handling traits on sims. """
    @staticmethod
    def is_special_npc(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Special NPC.

            Special NPCs:
            - Hidden Event NPC
            - Grim Reaper
            - Scarecrow
            - Flower Bunny
        """
        traits = (
            CommonTraitId.HIDDEN_IS_EVENT_NPC_CHALLENGE,
            CommonTraitId.IS_GRIM_REAPER,
            CommonTraitId.SCARECROW,
            CommonTraitId.FLOWER_BUNNY
        )
        return CommonTraitUtils.has_trait(sim_info, *traits)

    @staticmethod
    def is_aggressive_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is Aggressive.
        """
        trait_ids = (
            CommonTraitId.PET_AGGRESSIVE_DOG,
            CommonTraitId.PET_AGGRESSIVE_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_alluring(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Alluring.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ALLURING)

    @staticmethod
    def is_antiseptic(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Antiseptic.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANTISEPTIC)

    @staticmethod
    def is_bro(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Bro.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.BRO)

    @staticmethod
    def is_carefree(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Care Free.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAREFREE)

    @staticmethod
    def is_cat_lover(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Cat Lover.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAT_LOVER)

    @staticmethod
    def is_dog_lover(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Dog Lover.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DOG_LOVER)

    @staticmethod
    def is_clumsy(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Clumsy.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CLUMSY)

    @staticmethod
    def is_dastardly(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Dastardly.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DASTARDLY)

    @staticmethod
    def is_criminal(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Criminal.
        """
        trait_ids = (
            CommonTraitId.DETECTIVE_CAREER_CRIMINAL,
            CommonTraitId.DETECTIVE_CAREER_POLICE_STATION_CRIMINAL_NPC
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_evil(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Evil.
        """
        trait_ids = (
            CommonTraitId.EVIL,
            CommonTraitId.EVIL_BEGONIA_SCENT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_fertile(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Fertile.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.FERTILE)

    @staticmethod
    def is_friendly_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is Friendly.
        """
        trait_ids = (
            CommonTraitId.PET_FRIENDLY_DOG,
            CommonTraitId.PET_FRIENDLY_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_genius(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Genius.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENIUS)

    @staticmethod
    def is_good(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Good.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GOOD)

    @staticmethod
    def is_glutton(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Glutton.
        """
        return CommonTraitUtils.is_glutton_human(sim_info) or CommonTraitUtils.is_glutton_pet(sim_info)

    @staticmethod
    def is_glutton_human(sim_info: SimInfo) -> bool:
        """
            Determine if a non pet sim is a Glutton
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GLUTTON)

    @staticmethod
    def is_glutton_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is a Glutton.
        """
        trait_ids = (
            CommonTraitId.PET_GLUTTON_DOG,
            CommonTraitId.PET_GLUTTON_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_gregarious(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Gregarious.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GREGARIOUS)

    @staticmethod
    def is_hot_headed(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Hot Headed.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HOT_HEADED)

    @staticmethod
    def is_hunter_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is a Hunter.
        """
        trait_ids = (
            CommonTraitId.PET_HUNTER_DOG,
            CommonTraitId.PET_HUNTER_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_incredibly_friendly(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Incredibly Friendly.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INCREDIBLY_FRIENDLY)

    @staticmethod
    def is_insane(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Insane.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSANE)

    @staticmethod
    def is_insider(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is an Insider.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSIDER)

    @staticmethod
    def is_loyal_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is Loyal.
        """
        trait_ids = (
            CommonTraitId.PET_LOYAL_DOG,
            CommonTraitId.PET_LOYAL_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_mean(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Mean.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MEAN)

    @staticmethod
    def is_mentor(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Mentor.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MENTOR)

    @staticmethod
    def is_morning_person(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Morning Person.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MORNING_PERSON)

    @staticmethod
    def is_naughty_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is Naughty.
        """
        trait_ids = (
            CommonTraitId.PET_NAUGHTY_DOG,
            CommonTraitId.PET_NAUGHTY_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_night_owl(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Night Owl.
        """
        trait_ids = (
            CommonTraitId.NIGHT_OWL,
            CommonTraitId.NIGHT_OWL_CRYSTAL_HELMET
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_lazy(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Lazy.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LAZY)

    @staticmethod
    def is_loner(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Loner.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LONER)

    @staticmethod
    def is_love_guru(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Love Guru.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LOVE_GURU)

    @staticmethod
    def is_self_absorbed(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Self Absorbed.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ABSORBED)

    @staticmethod
    def is_self_assured(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Self Assured.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ASSURED)

    @staticmethod
    def is_service_sim(sim_info: SimInfo) -> bool:
        """
            Obsolete: Please use CommonSimTypeUtils.is_service_sim instead.
        """
        from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
        return CommonSimTypeUtils.is_service_sim(sim_info)

    @staticmethod
    def is_shameless(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Shameless.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SHAMELESS)

    @staticmethod
    def is_sincere(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Sincere.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SINCERE)

    @staticmethod
    def is_skittish_pet(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim is Skittish.
        """
        trait_ids = (
            CommonTraitId.PET_SKITTISH_DOG,
            CommonTraitId.PET_SKITTISH_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_slob(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Slob.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SLOB)

    @staticmethod
    def is_snob(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Snob.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SNOB)

    @staticmethod
    def is_squeamish(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Squeamish.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SQUEAMISH)

    @staticmethod
    def is_survivalist(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is a Survivalist.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SURVIVALIST)

    @staticmethod
    def is_unflirty(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is Unflirty.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.UNFLIRTY)

    @staticmethod
    def hates_children(sim_info: SimInfo) -> bool:
        """
            Determine if a sim Hates Children.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HATES_CHILDREN)

    @staticmethod
    def has_animal_attraction(sim_info: SimInfo) -> bool:
        """
            Determine if a sim has an Animal Attraction.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_ATTRACTION)

    @staticmethod
    def has_animal_whisperer(sim_info: SimInfo) -> bool:
        """
            Determine if a sim is an Animal Whisperer.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_WHISPERER)

    @staticmethod
    def has_challenge_kindness_ambassador(sim_info: SimInfo) -> bool:
        """
            Determine if a sim has Challenged the Kindness Ambassador.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CHALLENGE_KINDNESS_AMBASSADOR)

    @staticmethod
    def has_commitment_issues(sim_info: SimInfo) -> bool:
        """
            Determine if a sim has Commitment Issues.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.COMMITMENT_ISSUES)

    @staticmethod
    def has_masculine_frame(sim_info: SimInfo) -> bool:
        """
            Determine if a sim has a Masculine Body Frame.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)

    @staticmethod
    def has_feminine_frame(sim_info: SimInfo) -> bool:
        """
            Determine if a sim has a Feminine Body Frame.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)

    @staticmethod
    def prefers_menswear(sim_info: SimInfo) -> bool:
        """
            Determine if a sim prefers Mens Clothing.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)

    @staticmethod
    def prefers_womenswear(sim_info: SimInfo) -> bool:
        """
            Determine if a sim prefers Womens Clothing.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)

    @staticmethod
    def can_impregnate(sim_info: SimInfo) -> bool:
        """
            Determine if a sim Can Impregnate.

            Use can_reproduce for Pet Sims.
            Note: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE trait.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE)\
               and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE)

    @staticmethod
    def can_not_impregnate(sim_info: SimInfo) -> bool:
        """
            Determine if a sim Can Not Impregnate.

            Use can_not_reproduce for Pet Sims.
            Note: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE trait.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE)\
               and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE)

    @staticmethod
    def can_be_impregnated(sim_info: SimInfo) -> bool:
        """
            Determine if a sim Can Be Impregnated.

            Use can_reproduce for Pet Sims.
            Note: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED trait.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED)\
               and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED)

    @staticmethod
    def can_not_be_impregnated(sim_info: SimInfo) -> bool:
        """
            Determine if a sim Can Not Be Impregnated.

            Use can_not_reproduce for Pet Sims.
            Note: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED trait.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED)\
               and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED)

    @staticmethod
    def can_create_pregnancy(sim_info: SimInfo) -> bool:
        """
            Determine if a sim can either impregnate or be impregnated.

            Note: Will return False if the sim can both impregnate and not impregnate
            or if the sim can both be impregnated and not be impregnated.
        """
        return CommonTraitUtils.can_impregnate(sim_info) or CommonTraitUtils.can_be_impregnated(sim_info)

    @staticmethod
    def can_reproduce(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim can reproduce.

            Use can_impregnate and can_be_impregnated for Human Sims.
            Note: Will return False if the pet sim has the PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE trait.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)\
               and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)

    @staticmethod
    def can_not_reproduce(sim_info: SimInfo) -> bool:
        """
            Determine if a pet sim can reproduce.

            Use can_not_impregnate and can_not_be_impregnated for Human Sims.
            Note: Will return False if the pet sim has the PREGNANCY_OPTIONS_PET_CAN_REPRODUCE trait.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)\
               and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)

    @staticmethod
    def uses_toilet_standing(sim_info: SimInfo) -> bool:
        """
            Determine if a sim uses the toilet while standing.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)

    @staticmethod
    def uses_toilet_sitting(sim_info: SimInfo) -> bool:
        """
            Determine if a sim uses the toilet while sitting.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)

    @staticmethod
    def has_trait(sim_info: SimInfo, *trait_ids: int) -> bool:
        """
            Determine if a sim has any of the specified traits.
        :param sim_info: The sim to check.
        :param trait_ids: The decimal identifiers of traits to look for.
        :return: True if the sim has any of the specified traits.
        """
        if not trait_ids:
            return False
        sim_traits = CommonTraitUtils.get_traits(sim_info)
        for trait in sim_traits:
            trait_id = getattr(trait, 'guid64', None)
            if trait_id in trait_ids:
                return True
        return False

    @staticmethod
    def get_trait_ids(sim_info: SimInfo) -> List[int]:
        """
            Retrieve decimal identifiers for all Traits of a sim.
        """
        trait_ids = []
        for trait in CommonTraitUtils.get_traits(sim_info):
            trait_id = getattr(trait, 'guid64', None)
            if trait_id is None:
                continue
            trait_ids.append(trait_id)
        return trait_ids

    @staticmethod
    def get_traits(sim_info: SimInfo) -> List[Trait]:
        """
            Retrieve all Traits of a sim.
        """
        if not hasattr(sim_info, 'get_traits'):
            return list()
        return list(sim_info.get_traits())

    @staticmethod
    def get_equipped_traits(sim_info: SimInfo) -> List[Trait]:
        """
            Retrieve sims currently equipped traits. This is useful mainly for checking occult types.
        """
        if not hasattr(sim_info, 'trait_tracker') or not hasattr(sim_info.trait_tracker, 'equipped_traits'):
            return list()
        return list(sim_info.trait_tracker.equipped_traits)

    @staticmethod
    def add_trait(sim_info: SimInfo, *trait_ids: int) -> bool:
        """
            Add the specified traits to a sim.
        :param sim_info: The sim to add the specified traits to.
        :param trait_ids: The decimal identifiers of traits being added.
        :return: True if all of the traits were successfully added to the sim.
        """
        success = True
        for trait_id in trait_ids:
            trait_instance = CommonTraitUtils._load_trait_instance(trait_id)
            if trait_instance is None:
                continue
            if not sim_info.add_trait(trait_instance):
                success = False
        return success

    @staticmethod
    def remove_trait(sim_info: SimInfo, *trait_ids: int) -> bool:
        """
            Remove the specified traits from a sim.
        :param sim_info: The sim to remove the specified traits from.
        :param trait_ids: The decimal identifier of the trait being removed.
        :return: True if the trait was successfully removed from the sim.
        """
        success = True
        for trait_id in trait_ids:
            trait_instance = CommonTraitUtils._load_trait_instance(trait_id)
            if trait_instance is None:
                continue
            if not sim_info.remove_trait(trait_instance):
                success = False
        return success

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _load_trait_instance(trait_id: int) -> Union[Trait, None]:
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.TRAIT, trait_id)
