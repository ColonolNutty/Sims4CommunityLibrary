"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Union, Callable, Iterator, Tuple
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from traits.traits import Trait


class CommonTraitUtils:
    """Utilities for manipulating Traits on Sims.

    """
    @staticmethod
    def is_special_npc(sim_info: SimInfo) -> bool:
        """is_special_npc(sim_info)

        Determine if a sim is a Special NPC.

        .. note::

            Special NPCs:

            - Hidden Event NPC
            - Grim Reaper
            - Scarecrow
            - Flower Bunny

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        traits = (
            CommonTraitId.HIDDEN_IS_EVENT_NPC_CHALLENGE,
            CommonTraitId.IS_GRIM_REAPER,
            CommonTraitId.SCARECROW,
            CommonTraitId.FLOWER_BUNNY
        )
        return CommonTraitUtils.has_trait(sim_info, *traits)

    @staticmethod
    def is_active(sim_info: SimInfo) -> bool:
        """is_active(sim_info)

        Determine if a Sim is active.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ACTIVE)

    @staticmethod
    def is_aggressive_pet(sim_info: SimInfo) -> bool:
        """is_aggressive_pet(sim_info)

        Determine if a pet sim is Aggressive.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_AGGRESSIVE_DOG,
            CommonTraitId.PET_AGGRESSIVE_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_alluring(sim_info: SimInfo) -> bool:
        """is_alluring(sim_info)

        Determine if a sim is Alluring.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ALLURING)

    @staticmethod
    def is_antiseptic(sim_info: SimInfo) -> bool:
        """is_antiseptic(sim_info)

        Determine if a sim is Antiseptic.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANTISEPTIC)

    @staticmethod
    def is_bro(sim_info: SimInfo) -> bool:
        """is_bro(sim_info)

        Determine if a sim is a Bro.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.BRO)

    @staticmethod
    def is_carefree(sim_info: SimInfo) -> bool:
        """is_carefree(sim_info)

        Determine if a sim is Care Free.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAREFREE)

    @staticmethod
    def is_cat_lover(sim_info: SimInfo) -> bool:
        """is_cat_lover(sim_info)

        Determine if a sim is a Cat Lover.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAT_LOVER)

    @staticmethod
    def is_dog_lover(sim_info: SimInfo) -> bool:
        """is_dog_lover(sim_info)

        Determine if a sim is a Dog Lover.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DOG_LOVER)

    @staticmethod
    def is_clumsy(sim_info: SimInfo) -> bool:
        """is_clumsy(sim_info)

        Determine if a sim is Clumsy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CLUMSY)

    @staticmethod
    def is_dastardly(sim_info: SimInfo) -> bool:
        """is_dastardly(sim_info)

        Determine if a sim is Dastardly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DASTARDLY)

    @staticmethod
    def is_criminal(sim_info: SimInfo) -> bool:
        """is_criminal(sim_info)

        Determine if a sim is a Criminal.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.DETECTIVE_CAREER_CRIMINAL,
            CommonTraitId.DETECTIVE_CAREER_POLICE_STATION_CRIMINAL_NPC
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_evil(sim_info: SimInfo) -> bool:
        """is_evil(sim_info)

        Determine if a sim is Evil.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.EVIL,
            CommonTraitId.EVIL_BEGONIA_SCENT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_fertile(sim_info: SimInfo) -> bool:
        """is_fertile(sim_info)

        Determine if a sim is Fertile.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.FERTILE)

    @staticmethod
    def is_friendly_pet(sim_info: SimInfo) -> bool:
        """is_friendly_pet(sim_info)

        Determine if a pet sim is Friendly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_FRIENDLY_DOG,
            CommonTraitId.PET_FRIENDLY_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_geek(sim_info: SimInfo) -> bool:
        """is_geek(sim_info)

        Determine if a Sim is a geek.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GEEK)

    @staticmethod
    def is_genius(sim_info: SimInfo) -> bool:
        """is_genius(sim_info)

        Determine if a sim is a Genius.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENIUS)

    @staticmethod
    def is_good(sim_info: SimInfo) -> bool:
        """is_good(sim_info)

        Determine if a sim is Good.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GOOD)

    @staticmethod
    def is_glutton(sim_info: SimInfo) -> bool:
        """is_glutton(sim_info)

        Determine if a sim is a Glutton.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.is_glutton_human(sim_info) or CommonTraitUtils.is_glutton_pet(sim_info)

    @staticmethod
    def is_glutton_human(sim_info: SimInfo) -> bool:
        """is_glutton_human(sim_info)

        Determine if a non pet sim is a Glutton

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GLUTTON)

    @staticmethod
    def is_glutton_pet(sim_info: SimInfo) -> bool:
        """is_glutton_pet(sim_info)

        Determine if a pet sim is a Glutton.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_GLUTTON_DOG,
            CommonTraitId.PET_GLUTTON_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_gregarious(sim_info: SimInfo) -> bool:
        """is_gregarious(sim_info)

        Determine if a sim is Gregarious.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GREGARIOUS)

    @staticmethod
    def is_hot_headed(sim_info: SimInfo) -> bool:
        """is_hot_headed(sim_info)

        Determine if a sim is Hot Headed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HOT_HEADED)

    @staticmethod
    def is_hunter_pet(sim_info: SimInfo) -> bool:
        """is_hunter_pet(sim_info)

        Determine if a pet sim is a Hunter.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_HUNTER_DOG,
            CommonTraitId.PET_HUNTER_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_incredibly_friendly(sim_info: SimInfo) -> bool:
        """is_incredibly_friendly(sim_info)

        Determine if a sim is Incredibly Friendly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INCREDIBLY_FRIENDLY)

    @staticmethod
    def is_insane(sim_info: SimInfo) -> bool:
        """is_insane(sim_info)

        Determine if a sim is Insane.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSANE)

    @staticmethod
    def is_insider(sim_info: SimInfo) -> bool:
        """is_insider(sim_info)

        Determine if a sim is an Insider.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSIDER)

    @staticmethod
    def is_loyal_pet(sim_info: SimInfo) -> bool:
        """is_loyal_pet(sim_info)

        Determine if a pet sim is Loyal.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_LOYAL_DOG,
            CommonTraitId.PET_LOYAL_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_mean(sim_info: SimInfo) -> bool:
        """is_mean(sim_info)

        Determine if a sim is Mean.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MEAN)

    @staticmethod
    def is_mentor(sim_info: SimInfo) -> bool:
        """is_mentor(sim_info)

        Determine if a sim is a Mentor.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MENTOR)

    @staticmethod
    def is_morning_person(sim_info: SimInfo) -> bool:
        """is_morning_person(sim_info)

        Determine if a sim is a Morning Person.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MORNING_PERSON)

    @staticmethod
    def is_naughty_pet(sim_info: SimInfo) -> bool:
        """is_naughty_pet(sim_info)

        Determine if a pet sim is Naughty.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_NAUGHTY_DOG,
            CommonTraitId.PET_NAUGHTY_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_neat(sim_info: SimInfo) -> bool:
        """is_neat(sim_info)

        Determine if a Sim is neat.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.NEAT)

    @staticmethod
    def is_night_owl(sim_info: SimInfo) -> bool:
        """is_night_owl(sim_info)

        Determine if a sim is a Night Owl.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.NIGHT_OWL,
            CommonTraitId.NIGHT_OWL_CRYSTAL_HELMET
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_lazy(sim_info: SimInfo) -> bool:
        """is_lazy(sim_info)

        Determine if a sim is Lazy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LAZY)

    @staticmethod
    def is_loner(sim_info: SimInfo) -> bool:
        """is_loner(sim_info)

        Determine if a sim is a Loner.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LONER)

    @staticmethod
    def is_love_guru(sim_info: SimInfo) -> bool:
        """is_love_guru(sim_info)

        Determine if a sim is a Love Guru.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LOVE_GURU)

    @staticmethod
    def is_self_absorbed(sim_info: SimInfo) -> bool:
        """is_self_absorbed(sim_info)

        Determine if a sim is Self Absorbed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ABSORBED)

    @staticmethod
    def is_self_assured(sim_info: SimInfo) -> bool:
        """is_self_assured(sim_info)

        Determine if a sim is Self Assured.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ASSURED)

    @staticmethod
    def is_service_sim(sim_info: SimInfo) -> bool:
        """is_service_sim(sim_info)

        Determine if a sim is a service sim.

        ..warning:: Obsolete: Use :func:`~is_service_sim` in :class:`.CommonSimTypeUtils` instead.

        """
        from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
        return CommonSimTypeUtils.is_service_sim(sim_info)

    @staticmethod
    def is_shameless(sim_info: SimInfo) -> bool:
        """is_shameless(sim_info)

        Determine if a sim is Shameless.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SHAMELESS)

    @staticmethod
    def is_sincere(sim_info: SimInfo) -> bool:
        """is_sincere(sim_info)

        Determine if a sim is Sincere.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SINCERE)

    @staticmethod
    def is_skittish_pet(sim_info: SimInfo) -> bool:
        """is_skittish_pet(sim_info)

        Determine if a pet sim is Skittish.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        trait_ids = (
            CommonTraitId.PET_SKITTISH_DOG,
            CommonTraitId.PET_SKITTISH_CAT
        )
        return CommonTraitUtils.has_trait(sim_info, *trait_ids)

    @staticmethod
    def is_slob(sim_info: SimInfo) -> bool:
        """is_slob(sim_info)

        Determine if a sim is a Slob.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SLOB)

    @staticmethod
    def is_snob(sim_info: SimInfo) -> bool:
        """is_snob(sim_info)

        Determine if a sim is a Snob.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SNOB)

    @staticmethod
    def is_squeamish(sim_info: SimInfo) -> bool:
        """is_squeamish(sim_info)

        Determine if a sim is Squeamish.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SQUEAMISH)

    @staticmethod
    def is_survivalist(sim_info: SimInfo) -> bool:
        """is_survivalist(sim_info)

        Determine if a sim is a Survivalist.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SURVIVALIST)

    @staticmethod
    def is_unflirty(sim_info: SimInfo) -> bool:
        """is_unflirty(sim_info)

        Determine if a sim is Unflirty.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.UNFLIRTY)

    @staticmethod
    def hates_children(sim_info: SimInfo) -> bool:
        """hates_children(sim_info)

        Determine if a sim Hates Children.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HATES_CHILDREN)

    @staticmethod
    def has_animal_attraction(sim_info: SimInfo) -> bool:
        """has_animal_attraction(sim_info)

        Determine if a sim has an Animal Attraction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_ATTRACTION)

    @staticmethod
    def has_animal_whisperer(sim_info: SimInfo) -> bool:
        """has_animal_whisperer(sim_info)

        Determine if a sim is an Animal Whisperer.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_WHISPERER)

    @staticmethod
    def has_challenge_kindness_ambassador(sim_info: SimInfo) -> bool:
        """has_challenge_kindness_ambassador(sim_info)

        Determine if a sim has Challenged the Kindness Ambassador.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CHALLENGE_KINDNESS_AMBASSADOR)

    @staticmethod
    def has_commitment_issues(sim_info: SimInfo) -> bool:
        """has_commitment_issues(sim_info)

        Determine if a sim has Commitment Issues.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.COMMITMENT_ISSUES)

    @staticmethod
    def has_masculine_frame(sim_info: SimInfo) -> bool:
        """has_masculine_frame(sim_info)

        Determine if a sim has a Masculine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.has_masculine_frame(sim_info)

    @staticmethod
    def has_feminine_frame(sim_info: SimInfo) -> bool:
        """has_feminine_frame(sim_info)

        Determine if a sim has a Feminine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.has_feminine_frame(sim_info)

    @staticmethod
    def prefers_menswear(sim_info: SimInfo) -> bool:
        """prefers_menswear(sim_info)

        Determine if a sim prefers Mens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.prefers_menswear(sim_info)

    @staticmethod
    def prefers_womenswear(sim_info: SimInfo) -> bool:
        """prefers_womenswear(sim_info)

        Determine if a sim prefers Womens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.prefers_womenswear(sim_info)

    @staticmethod
    def can_impregnate(sim_info: SimInfo) -> bool:
        """can_impregnate(sim_info)

        Determine if a sim Can Impregnate.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can impregnate other Sims. False, if the Sim can not impregnate other Sims.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_impregnate(sim_info)

    @staticmethod
    def can_not_impregnate(sim_info: SimInfo) -> bool:
        """can_not_impregnate(sim_info)

        Determine if a sim Can Not Impregnate.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not impregnate other Sims. False, if the Sim can impregnate other Sims.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_impregnate(sim_info)

    @staticmethod
    def can_be_impregnated(sim_info: SimInfo) -> bool:
        """can_be_impregnated(sim_info)

        Determine if a sim Can Be Impregnated.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can be impregnated. False, if the Sim can not be impregnated.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_be_impregnated(sim_info)

    @staticmethod
    def can_not_be_impregnated(sim_info: SimInfo) -> bool:
        """can_not_be_impregnated(sim_info)

        Determine if a sim Can Not Be Impregnated.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not be impregnated. False, if the Sim can be impregnated.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info)

    @staticmethod
    def can_create_pregnancy(sim_info: SimInfo) -> bool:
        """can_create_pregnancy(sim_info)

        Determine if a Sim can either impregnate, be impregnated, or can reproduce.

        .. note:: Will return False if the Sim can both impregnate and not impregnate,\
            if the Sim can both be impregnated and not be impregnated\
            or if the Sim can both reproduce and not reproduce.

        .. note:: A Sim can impregnate when they can either impregnate other Sims, can be impregnated by other Sims, or if they are a Pet, can reproduce.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can create pregnancies. False, if the Sim can not create pregnancies.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_create_pregnancy(sim_info)

    @staticmethod
    def can_reproduce(sim_info: SimInfo) -> bool:
        """can_reproduce(sim_info)

        Determine if a pet sim can reproduce.

        .. note:: Use :func:`~can_impregnate` and :func:`~can_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet sim has the PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can reproduce. False, if the Sim can not reproduce.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_reproduce(sim_info)

    @staticmethod
    def can_not_reproduce(sim_info: SimInfo) -> bool:
        """can_not_reproduce(sim_info)

        Determine if a pet sim can reproduce.

        ..note:: Use :func:`~can_not_impregnate` and :func:`~can_not_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet sim has the PREGNANCY_OPTIONS_PET_CAN_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not reproduce. False, if the Sim can reproduce.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_reproduce(sim_info)

    @staticmethod
    def uses_toilet_standing(sim_info: SimInfo) -> bool:
        """uses_toilet_standing(sim_info)

        Determine if a sim uses the toilet while standing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim uses toilets while standing. False, if the Sim does not use toilets while standing.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.uses_toilet_standing(sim_info)

    @staticmethod
    def uses_toilet_sitting(sim_info: SimInfo) -> bool:
        """uses_toilet_sitting(sim_info)

        Determine if a sim uses the toilet while sitting.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim uses toilets while sitting. False, if the Sim does not use toilets while sitting.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info)

    @staticmethod
    def has_trait(sim_info: SimInfo, *trait_ids: Union[int, CommonTraitId]) -> bool:
        """has_trait(sim_info, *trait_ids)

        Determine if a sim has any of the specified traits.

        :param sim_info: The sim to check.
        :type sim_info: SimInfo
        :param trait_ids: An iterable of identifiers of Traits.
        :type trait_ids: Union[int, CommonTraitId]
        :return: True, if the sim has any of the specified traits. False, if not.
        :rtype: bool
        """
        if not trait_ids:
            return False
        sim_trait_ids = CommonTraitUtils.get_trait_ids(sim_info)
        for trait_id in sim_trait_ids:
            if trait_id in trait_ids:
                return True
        return False

    @staticmethod
    def get_trait_ids(sim_info: SimInfo) -> List[int]:
        """get_trait_ids(sim_info)

        Retrieve decimal identifiers for all Traits of a sim.

        :param sim_info: The sim to check.
        :type sim_info: SimInfo
        :return: A collection of Trait identifiers on a Sim.
        :rtype: List[int]
        """
        trait_ids = []
        for trait in CommonTraitUtils.get_traits(sim_info):
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id is None:
                continue
            trait_ids.append(trait_id)
        return trait_ids

    @staticmethod
    def get_traits(sim_info: SimInfo) -> List[Trait]:
        """get_traits(sim_info)

        Retrieve all Traits of a sim.

        :param sim_info: The sim to check.
        :type sim_info: SimInfo
        :return: A collection of Traits on a Sim.
        :rtype: List[int]
        """
        if not hasattr(sim_info, 'get_traits'):
            return list()
        return list(sim_info.get_traits())

    @staticmethod
    def get_trait_name(trait: Trait) -> Union[str, None]:
        """get_trait_name(trait)

        Retrieve the Name of a Trait.

        :param trait: An instance of a Trait.
        :type trait: Trait
        :return: The name of a Trait or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if trait is None:
            return None
        # noinspection PyBroadException
        try:
            return trait.__name__ or ''
        except:
            return ''

    @staticmethod
    def get_trait_names(traits: Iterator[Trait]) -> Tuple[str]:
        """get_trait_names(traits)

        Retrieve the Names of a collection of Trait.

        :param traits: A collection of Trait instances.
        :type traits: Iterator[Trait]
        :return: A collection of names for all specified Traits.
        :rtype: Tuple[str]
        """
        if traits is None or not traits:
            return tuple()
        names: List[str] = []
        for trait in traits:
            # noinspection PyBroadException
            try:
                name = CommonTraitUtils.get_trait_name(trait)
                if not name:
                    continue
            except:
                continue
            names.append(name)
        return tuple(names)

    @staticmethod
    def get_equipped_traits(sim_info: SimInfo) -> List[Trait]:
        """get_equipped_traits(sim_info)

        Retrieve Sims currently equipped traits.

        .. note:: The main use of this function is to check Occult Types.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A collection of equipped Traits on a Sim.
        :rtype: List[int]
        """
        if not hasattr(sim_info, 'trait_tracker') or not hasattr(sim_info.trait_tracker, 'equipped_traits'):
            return list()
        return list(sim_info.trait_tracker.equipped_traits)

    @staticmethod
    def add_trait(sim_info: SimInfo, *trait_ids: Union[int, CommonTraitId]) -> bool:
        """add_trait(sim_info, *trait_ids)

        Add the specified traits to a Sim.

        :param sim_info: The Sim to add the specified traits to.
        :type sim_info: SimInfo
        :param trait_ids: An iterable of Trait identifiers of traits being added.
        :type trait_ids: Union[int, CommonTraitId]
        :return: True, if all specified traits were successfully added to the Sim. False, if not.
        :rtype: bool
        """
        success = True
        for trait_id in trait_ids:
            trait_instance = CommonTraitUtils.load_trait_by_id(trait_id)
            if trait_instance is None:
                continue
            if not sim_info.add_trait(trait_instance):
                success = False
        return success

    @staticmethod
    def remove_trait(sim_info: SimInfo, *trait_ids: Union[int, CommonTraitId]) -> bool:
        """remove_trait(sim_info, *trait_ids)

        Remove the specified traits from a Sim.

        :param sim_info: The Sim to remove the specified traits from.
        :type sim_info: SimInfo
        :param trait_ids: The decimal identifier of the trait being removed.
        :type trait_ids: Union[int, CommonTraitId]
        :return: True, if all specified traits were successfully removed from the Sim. False, if not.
        :rtype: bool
        """
        success = True
        for trait_id in trait_ids:
            trait_instance = CommonTraitUtils.load_trait_by_id(trait_id)
            if trait_instance is None:
                continue
            if not sim_info.remove_trait(trait_instance):
                success = False
        return success

    @staticmethod
    def swap_traits(sim_info: SimInfo, trait_id_one: Union[int, CommonTraitId], trait_id_two: Union[int, CommonTraitId]) -> bool:
        """swap_traits(sim_info, trait_id_one, trait_id_two)

        Remove one trait and add another to a Sim.

        .. note:: If `trait_id_one` exists on the Sim, it will be removed and `trait_id_two` will be added.
        .. note:: If `trait_id_two` exists on the Sim, it will be removed and `trait_id_one` will be added.

        :param sim_info: The Sim to remove the specified traits from.
        :type sim_info: SimInfo
        :param trait_id_one: The first trait to remove/add
        :type trait_id_one: Union[int, CommonTraitId]
        :param trait_id_two: The second trait to remove/add
        :type trait_id_two: Union[int, CommonTraitId]
        :return: True, if the Traits were swapped successfully. False, if neither Trait exists on a Sim or the traits were not swapped successfully.
        :rtype: bool
        """
        # Has Trait One
        if CommonTraitUtils.has_trait(sim_info, trait_id_one):
            CommonTraitUtils.remove_trait(sim_info, trait_id_one)
            if not CommonTraitUtils.has_trait(sim_info, trait_id_two):
                CommonTraitUtils.add_trait(sim_info, trait_id_two)
            return True
        # Has Trait Two
        elif CommonTraitUtils.has_trait(sim_info, trait_id_two):
            CommonTraitUtils.remove_trait(sim_info, trait_id_two)
            if not CommonTraitUtils.has_trait(sim_info, trait_id_one):
                CommonTraitUtils.add_trait(sim_info, trait_id_one)
            return True
        return False

    @staticmethod
    def add_trait_to_all_sims(trait_id: Union[int, CommonTraitId], include_sim_callback: Callable[[SimInfo], bool]=None):
        """add_trait_to_all_sims(trait_id, include_sim_callback=None)

        Add a trait to all Sims that match the specified include filter.

        :param trait_id: The identifier of the Trait to add to all Sims.
        :type trait_id: Union[int, CommonTraitId]
        :param include_sim_callback: Only Sims that match this filter will have the Trait added.
        :type include_sim_callback: Callback[[SimInfo], bool], optional
        """
        for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            if CommonTraitUtils.has_trait(sim_info, trait_id):
                continue
            CommonTraitUtils.add_trait(sim_info, trait_id)

    @staticmethod
    def remove_trait_from_all_sims(trait_id: Union[int, CommonTraitId], include_sim_callback: Callable[[SimInfo], bool]=None):
        """remove_trait_from_all_sims(trait_id, include_sim_callback=None)

        Remove a trait from all Sims that match the specified include filter.

        :param trait_id: The identifier of the Trait to remove from all Sims.
        :type trait_id: Union[int, CommonTraitId]
        :param include_sim_callback: Only Sims that match this filter will have the Trait removed.
        :type include_sim_callback: Callback[[SimInfo], bool], optional
        """
        for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            if not CommonTraitUtils.has_trait(sim_info, trait_id):
                continue
            CommonTraitUtils.remove_trait(sim_info, trait_id)

    @staticmethod
    def get_trait_id(trait_identifier: Union[int, Trait]) -> Union[int, None]:
        """get_trait_id(trait_identifier)

        Retrieve the decimal identifier of a Trait.

        :param trait_identifier: The identifier or instance of a Trait.
        :type trait_identifier: Union[int, Trait]
        :return: The decimal identifier of the Trait or None if the Trait does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(trait_identifier, int):
            return trait_identifier
        return getattr(trait_identifier, 'guid64', None)

    @staticmethod
    def load_trait_by_id(trait_id: Union[int, CommonTraitId]) -> Union[Trait, None]:
        """load_trait_by_id(trait_id)

        Load an instance of a Trait by its decimal identifier.

        :param trait_id: The decimal identifier of a Trait.
        :type trait_id: Union[int, CommonTraitId]
        :return: An instance of a Trait matching the decimal identifier or None if not found.
        :rtype: Union[Trait, None]
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.TRAIT, trait_id)
