"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, List
from sims4.resources import Types
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from traits.traits import Trait


class CommonTraitUtils:
    """ Utilities for handling traits on sims. """
    @staticmethod
    def flip_mutually_exclusive_traits(sim_info: Union[SimInfo, SimInfoBaseWrapper], trait_one: int, trait_two: int) -> bool:
        """

        :param sim_info:
        :param trait_one:
        :param trait_two:
        :return:
        """
        # Has Trait One
        if CommonTraitUtils.has_trait(sim_info, trait_one):
            CommonTraitUtils.remove_trait(sim_info, trait_one)
            if not CommonTraitUtils.has_trait(sim_info, trait_two):
                CommonTraitUtils.add_trait(sim_info, trait_two)
            return True
        # Has Trait Two
        elif CommonTraitUtils.has_trait(sim_info, trait_two):
            CommonTraitUtils.remove_trait(sim_info, trait_two)
            if not CommonTraitUtils.has_trait(sim_info, trait_one):
                CommonTraitUtils.add_trait(sim_info, trait_one)
            return True
        return False

    @staticmethod
    def is_special_npc(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
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
    def is_aggressive_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is Aggressive.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_AGGRESSIVE_DOG, CommonTraitId.PET_AGGRESSIVE_CAT)

    @staticmethod
    def is_alluring(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Alluring.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ALLURING)

    @staticmethod
    def is_antiseptic(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Antiseptic.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANTISEPTIC)

    @staticmethod
    def is_bro(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Bro.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.BRO)

    @staticmethod
    def is_carefree(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Care Free.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAREFREE)

    @staticmethod
    def is_cat_lover(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Cat Lover.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAT_LOVER)

    @staticmethod
    def is_dog_lover(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Dog Lover.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DOG_LOVER)

    @staticmethod
    def is_clumsy(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Clumsy.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CLUMSY)

    @staticmethod
    def is_dastardly(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Dastardly.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DASTARDLY)

    @staticmethod
    def is_criminal(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Criminal.
        """
        traits = (
            CommonTraitId.DETECTIVE_CAREER_CRIMINAL,
            CommonTraitId.DETECTIVE_CAREER_POLICE_STATION_CRIMINAL_NPC
        )
        return CommonTraitUtils.has_trait(sim_info, *traits)

    @staticmethod
    def is_evil(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Evil.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.EVIL, CommonTraitId.EVIL_BEGONIA_SCENT)

    @staticmethod
    def is_fertile(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Fertile.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.FERTILE)

    @staticmethod
    def is_friendly_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is Friendly.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_FRIENDLY_DOG, CommonTraitId.PET_FRIENDLY_CAT)

    @staticmethod
    def is_genius(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Genius.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENIUS)

    @staticmethod
    def is_good(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Good.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GOOD)

    @staticmethod
    def is_glutton(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Glutton.
        """
        return CommonTraitUtils.is_glutton_human(sim_info) or CommonTraitUtils.is_glutton_pet(sim_info)

    @staticmethod
    def is_glutton_human(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a non pet sim is a Glutton
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GLUTTON)

    @staticmethod
    def is_glutton_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is a Glutton.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_GLUTTON_DOG, CommonTraitId.PET_GLUTTON_CAT)

    @staticmethod
    def is_gregarious(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Gregarious.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GREGARIOUS)

    @staticmethod
    def is_hot_headed(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Hot Headed.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HOT_HEADED)

    @staticmethod
    def is_hunter_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is a Hunter.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_HUNTER_DOG, CommonTraitId.PET_HUNTER_CAT)

    @staticmethod
    def is_incredibly_friendly(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Incredibly Friendly.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INCREDIBLY_FRIENDLY)

    @staticmethod
    def is_insane(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Insane.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSANE)

    @staticmethod
    def is_insider(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is an Insider.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSIDER)

    @staticmethod
    def is_loyal_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is Loyal.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_LOYAL_DOG, CommonTraitId.PET_LOYAL_CAT)

    @staticmethod
    def is_mean(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Mean.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MEAN)

    @staticmethod
    def is_mentor(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Mentor.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MENTOR)

    @staticmethod
    def is_morning_person(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Morning Person.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MORNING_PERSON)

    @staticmethod
    def is_naughty_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is Naughty.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_NAUGHTY_DOG, CommonTraitId.PET_NAUGHTY_CAT)

    @staticmethod
    def is_night_owl(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Night Owl.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.NIGHT_OWL, CommonTraitId.NIGHT_OWL_CRYSTAL_HELMET)

    @staticmethod
    def is_lazy(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Lazy.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LAZY)

    @staticmethod
    def is_loner(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Loner.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LONER)

    @staticmethod
    def is_love_guru(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Love Guru.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LOVE_GURU)

    @staticmethod
    def is_self_absorbed(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Self Absorbed.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ABSORBED)

    @staticmethod
    def is_self_assured(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Self Assured.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ASSURED)

    @staticmethod
    def is_service_sim(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Service Sim.

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
        traits = (
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
        return CommonTraitUtils.has_trait(sim_info, *traits)

    @staticmethod
    def is_shameless(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Shameless.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SHAMELESS)

    @staticmethod
    def is_sincere(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Sincere.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SINCERE)

    @staticmethod
    def is_skittish_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a pet sim is Skittish.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PET_SKITTISH_DOG, CommonTraitId.PET_SKITTISH_CAT)

    @staticmethod
    def is_slob(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Slob.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SLOB)

    @staticmethod
    def is_snob(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Snob.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SNOB)

    @staticmethod
    def is_squeamish(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Squeamish.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SQUEAMISH)

    @staticmethod
    def is_survivalist(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Survivalist.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SURVIVALIST)

    @staticmethod
    def is_unflirty(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is Unflirty.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.UNFLIRTY)

    @staticmethod
    def hates_children(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim Hates Children.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HATES_CHILDREN)

    @staticmethod
    def has_animal_attraction(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim has an Animal Attraction.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_ATTRACTION)

    @staticmethod
    def has_animal_whisperer(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is an Animal Whisperer.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_WHISPERER)

    @staticmethod
    def has_challenge_kindness_ambassador(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim has Challenged the Kindness Ambassador.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CHALLENGE_KINDNESS_AMBASSADOR)

    @staticmethod
    def has_commitment_issues(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim has Commitment Issues.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.COMMITMENT_ISSUES)

    @staticmethod
    def has_masculine_frame(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim has a Masculine Body Frame.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)

    @staticmethod
    def has_feminine_frame(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim has a Feminine Body Frame.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)

    @staticmethod
    def prefers_menswear(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim prefers Mens Clothing.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)

    @staticmethod
    def prefers_womenswear(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim prefers Womens Clothing.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)

    @staticmethod
    def has_trait(sim_info: Union[SimInfo, SimInfoBaseWrapper], *trait_identifiers: int) -> bool:
        """
            Determine if the sim has any of the specified traits.
        :param sim_info: The sim to check.
        :param trait_identifiers: The decimal identifiers of traits to look for.
        :return: True if the sim has any of the specified traits.
        """
        if not trait_identifiers:
            return False
        sim_traits = CommonTraitUtils.get_traits(sim_info)
        return any((getattr(trait, 'guid64', None) in trait_identifiers for trait in sim_traits))

    @staticmethod
    def get_trait_ids(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> List[int]:
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
    def get_traits(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> List[Trait]:
        """
            Retrieve all Traits of a sim.
        """
        if not hasattr(sim_info, 'get_traits'):
            return list()
        return list(sim_info.get_traits())

    @staticmethod
    def get_equipped_traits(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> List[int]:
        """
            Retrieve sims currently equipped traits.
        """
        if not hasattr(sim_info, 'trait_tracker') or not hasattr(sim_info.trait_tracker, 'equipped_traits'):
            return list()
        return list(sim_info.trait_tracker.equipped_traits)

    @staticmethod
    def add_trait(sim_info: Union[SimInfo, SimInfoBaseWrapper], trait_identifier: int) -> bool:
        """
            Add the specified trait to a sim.
        :param sim_info: The sim to add the trait to.
        :param trait_identifier: The decimal identifier of the trait being added.
        :return: True if the trait was successfully added to the sim.
        """
        trait_instance = CommonResourceUtils.load_instance(Types.TRAIT, trait_identifier)
        if trait_instance is None:
            return False
        return sim_info.add_trait(trait_instance)

    @staticmethod
    def remove_trait(sim_info: Union[SimInfo, SimInfoBaseWrapper], trait_identifier: int) -> bool:
        """
            Remove the specified trait from a sim.
        :param sim_info: The sim to remove the trait from.
        :param trait_identifier: The decimal identifier of the trait being removed.
        :return: True if the trait was successfully removed from the sim.
        """
        trait_instance = CommonResourceUtils.load_instance(Types.TRAIT, trait_identifier)
        if trait_instance is None:
            return False
        return sim_info.remove_trait(trait_instance)
