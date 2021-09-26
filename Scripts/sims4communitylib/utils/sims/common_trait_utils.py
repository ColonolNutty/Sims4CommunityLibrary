"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import List, Union, Callable, Iterator, Tuple

from distributor.shared_messages import IconInfoData
from relationships.relationship_tracker import RelationshipTracker
from relationships.sim_knowledge import SimKnowledge
from server_commands.argument_helpers import TunableInstanceParam, OptionalTargetParam
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from traits.traits import Trait


class CommonTraitUtils(HasClassLog):
    """Utilities for manipulating Traits on Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_trait_utils'

    @classmethod
    def is_special_npc(cls, sim_info: SimInfo) -> bool:
        """is_special_npc(sim_info)

        Determine if a Sim is a Special NPC.

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

    @classmethod
    def is_active(cls, sim_info: SimInfo) -> bool:
        """is_active(sim_info)

        Determine if a Sim is active.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ACTIVE)

    @classmethod
    def is_aggressive_pet(cls, sim_info: SimInfo) -> bool:
        """is_aggressive_pet(sim_info)

        Determine if a pet Sim is Aggressive.

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

    @classmethod
    def is_alluring(cls, sim_info: SimInfo) -> bool:
        """is_alluring(sim_info)

        Determine if a Sim is Alluring.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ALLURING)

    @classmethod
    def is_antiseptic(cls, sim_info: SimInfo) -> bool:
        """is_antiseptic(sim_info)

        Determine if a Sim is Antiseptic.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANTISEPTIC)

    @classmethod
    def is_bro(cls, sim_info: SimInfo) -> bool:
        """is_bro(sim_info)

        Determine if a Sim is a Bro.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.BRO)

    @classmethod
    def is_carefree(cls, sim_info: SimInfo) -> bool:
        """is_carefree(sim_info)

        Determine if a Sim is Care Free.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAREFREE)

    @classmethod
    def is_cat_lover(cls, sim_info: SimInfo) -> bool:
        """is_cat_lover(sim_info)

        Determine if a Sim is a Cat Lover.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CAT_LOVER)

    @classmethod
    def is_dog_lover(cls, sim_info: SimInfo) -> bool:
        """is_dog_lover(sim_info)

        Determine if a Sim is a Dog Lover.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DOG_LOVER)

    @classmethod
    def is_clumsy(cls, sim_info: SimInfo) -> bool:
        """is_clumsy(sim_info)

        Determine if a Sim is Clumsy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CLUMSY)

    @classmethod
    def is_dastardly(cls, sim_info: SimInfo) -> bool:
        """is_dastardly(sim_info)

        Determine if a Sim is Dastardly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.DASTARDLY)

    @classmethod
    def is_criminal(cls, sim_info: SimInfo) -> bool:
        """is_criminal(sim_info)

        Determine if a Sim is a Criminal.

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

    @classmethod
    def is_evil(cls, sim_info: SimInfo) -> bool:
        """is_evil(sim_info)

        Determine if a Sim is Evil.

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

    @classmethod
    def is_fertile(cls, sim_info: SimInfo) -> bool:
        """is_fertile(sim_info)

        Determine if a Sim is Fertile.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.FERTILE)

    @classmethod
    def is_friendly_pet(cls, sim_info: SimInfo) -> bool:
        """is_friendly_pet(sim_info)

        Determine if a pet Sim is Friendly.

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

    @classmethod
    def is_geek(cls, sim_info: SimInfo) -> bool:
        """is_geek(sim_info)

        Determine if a Sim is a geek.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GEEK)

    @classmethod
    def is_genius(cls, sim_info: SimInfo) -> bool:
        """is_genius(sim_info)

        Determine if a Sim is a Genius.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENIUS)

    @classmethod
    def is_good(cls, sim_info: SimInfo) -> bool:
        """is_good(sim_info)

        Determine if a Sim is Good.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GOOD)

    @classmethod
    def is_glutton(cls, sim_info: SimInfo) -> bool:
        """is_glutton(sim_info)

        Determine if a Sim is a Glutton.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.is_glutton_human(sim_info) or CommonTraitUtils.is_glutton_pet(sim_info)

    @classmethod
    def is_glutton_human(cls, sim_info: SimInfo) -> bool:
        """is_glutton_human(sim_info)

        Determine if a non pet Sim is a Glutton

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GLUTTON)

    @classmethod
    def is_glutton_pet(cls, sim_info: SimInfo) -> bool:
        """is_glutton_pet(sim_info)

        Determine if a pet Sim is a Glutton.

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

    @classmethod
    def is_gregarious(cls, sim_info: SimInfo) -> bool:
        """is_gregarious(sim_info)

        Determine if a Sim is Gregarious.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GREGARIOUS)

    @classmethod
    def is_hot_headed(cls, sim_info: SimInfo) -> bool:
        """is_hot_headed(sim_info)

        Determine if a Sim is Hot Headed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HOT_HEADED)

    @classmethod
    def is_hunter_pet(cls, sim_info: SimInfo) -> bool:
        """is_hunter_pet(sim_info)

        Determine if a pet Sim is a Hunter.

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

    @classmethod
    def is_incredibly_friendly(cls, sim_info: SimInfo) -> bool:
        """is_incredibly_friendly(sim_info)

        Determine if a Sim is Incredibly Friendly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INCREDIBLY_FRIENDLY)

    @classmethod
    def is_insane(cls, sim_info: SimInfo) -> bool:
        """is_insane(sim_info)

        Determine if a Sim is Insane.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSANE)

    @classmethod
    def is_insider(cls, sim_info: SimInfo) -> bool:
        """is_insider(sim_info)

        Determine if a Sim is an Insider.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.INSIDER)

    @classmethod
    def is_loyal_pet(cls, sim_info: SimInfo) -> bool:
        """is_loyal_pet(sim_info)

        Determine if a pet Sim is Loyal.

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

    @classmethod
    def is_mean(cls, sim_info: SimInfo) -> bool:
        """is_mean(sim_info)

        Determine if a Sim is Mean.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MEAN)

    @classmethod
    def is_mentor(cls, sim_info: SimInfo) -> bool:
        """is_mentor(sim_info)

        Determine if a Sim is a Mentor.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MENTOR)

    @classmethod
    def is_morning_person(cls, sim_info: SimInfo) -> bool:
        """is_morning_person(sim_info)

        Determine if a Sim is a Morning Person.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.MORNING_PERSON)

    @classmethod
    def is_naughty_pet(cls, sim_info: SimInfo) -> bool:
        """is_naughty_pet(sim_info)

        Determine if a pet Sim is Naughty.

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

    @classmethod
    def is_neat(cls, sim_info: SimInfo) -> bool:
        """is_neat(sim_info)

        Determine if a Sim is neat.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.NEAT)

    @classmethod
    def is_night_owl(cls, sim_info: SimInfo) -> bool:
        """is_night_owl(sim_info)

        Determine if a Sim is a Night Owl.

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

    @classmethod
    def is_lazy(cls, sim_info: SimInfo) -> bool:
        """is_lazy(sim_info)

        Determine if a Sim is Lazy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LAZY)

    @classmethod
    def is_loner(cls, sim_info: SimInfo) -> bool:
        """is_loner(sim_info)

        Determine if a Sim is a Loner.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LONER)

    @classmethod
    def is_love_guru(cls, sim_info: SimInfo) -> bool:
        """is_love_guru(sim_info)

        Determine if a Sim is a Love Guru.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.LOVE_GURU)

    @classmethod
    def is_self_absorbed(cls, sim_info: SimInfo) -> bool:
        """is_self_absorbed(sim_info)

        Determine if a Sim is Self Absorbed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ABSORBED)

    @classmethod
    def is_self_assured(cls, sim_info: SimInfo) -> bool:
        """is_self_assured(sim_info)

        Determine if a Sim is Self Assured.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SELF_ASSURED)

    @classmethod
    def is_service_sim(cls, sim_info: SimInfo) -> bool:
        """is_service_sim(sim_info)

        Determine if a Sim is a service Sim.

        ..warning:: Obsolete: Use :func:`~is_service_sim` in :class:`.CommonSimTypeUtils` instead.

        """
        from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
        return CommonSimTypeUtils.is_service_sim(sim_info)

    @classmethod
    def is_shameless(cls, sim_info: SimInfo) -> bool:
        """is_shameless(sim_info)

        Determine if a Sim is Shameless.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SHAMELESS)

    @classmethod
    def is_sincere(cls, sim_info: SimInfo) -> bool:
        """is_sincere(sim_info)

        Determine if a Sim is Sincere.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SINCERE)

    @classmethod
    def is_skittish_pet(cls, sim_info: SimInfo) -> bool:
        """is_skittish_pet(sim_info)

        Determine if a pet Sim is Skittish.

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

    @classmethod
    def is_slob(cls, sim_info: SimInfo) -> bool:
        """is_slob(sim_info)

        Determine if a Sim is a Slob.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SLOB)

    @classmethod
    def is_snob(cls, sim_info: SimInfo) -> bool:
        """is_snob(sim_info)

        Determine if a Sim is a Snob.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SNOB)

    @classmethod
    def is_squeamish(cls, sim_info: SimInfo) -> bool:
        """is_squeamish(sim_info)

        Determine if a Sim is Squeamish.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SQUEAMISH)

    @classmethod
    def is_survivalist(cls, sim_info: SimInfo) -> bool:
        """is_survivalist(sim_info)

        Determine if a Sim is a Survivalist.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.SURVIVALIST)

    @classmethod
    def is_unflirty(cls, sim_info: SimInfo) -> bool:
        """is_unflirty(sim_info)

        Determine if a Sim is Unflirty.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.UNFLIRTY)

    @classmethod
    def hates_children(cls, sim_info: SimInfo) -> bool:
        """hates_children(sim_info)

        Determine if a Sim Hates Children.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.HATES_CHILDREN)

    @classmethod
    def has_animal_attraction(cls, sim_info: SimInfo) -> bool:
        """has_animal_attraction(sim_info)

        Determine if a Sim has an Animal Attraction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_ATTRACTION)

    @classmethod
    def has_animal_whisperer(cls, sim_info: SimInfo) -> bool:
        """has_animal_whisperer(sim_info)

        Determine if a Sim is an Animal Whisperer.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.ANIMAL_WHISPERER)

    @classmethod
    def has_challenge_kindness_ambassador(cls, sim_info: SimInfo) -> bool:
        """has_challenge_kindness_ambassador(sim_info)

        Determine if a Sim has Challenged the Kindness Ambassador.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.CHALLENGE_KINDNESS_AMBASSADOR)

    @classmethod
    def has_commitment_issues(cls, sim_info: SimInfo) -> bool:
        """has_commitment_issues(sim_info)

        Determine if a Sim has Commitment Issues.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.COMMITMENT_ISSUES)

    @classmethod
    def has_masculine_frame(cls, sim_info: SimInfo) -> bool:
        """has_masculine_frame(sim_info)

        Determine if a Sim has a Masculine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.has_masculine_frame(sim_info)

    @classmethod
    def has_feminine_frame(cls, sim_info: SimInfo) -> bool:
        """has_feminine_frame(sim_info)

        Determine if a Sim has a Feminine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.has_feminine_frame(sim_info)

    @classmethod
    def prefers_menswear(cls, sim_info: SimInfo) -> bool:
        """prefers_menswear(sim_info)

        Determine if a Sim prefers Mens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.prefers_menswear(sim_info)

    @classmethod
    def prefers_womenswear(cls, sim_info: SimInfo) -> bool:
        """prefers_womenswear(sim_info)

        Determine if a Sim prefers Womens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.prefers_womenswear(sim_info)

    @classmethod
    def can_impregnate(cls, sim_info: SimInfo) -> bool:
        """can_impregnate(sim_info)

        Determine if a Sim Can Impregnate.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: This will check for a Sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can impregnate other Sims. False, if the Sim can not impregnate other Sims.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_impregnate(sim_info)

    @classmethod
    def can_not_impregnate(cls, sim_info: SimInfo) -> bool:
        """can_not_impregnate(sim_info)

        Determine if a Sim Can Not Impregnate.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: This will check for a Sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not impregnate other Sims. False, if the Sim can impregnate other Sims.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_impregnate(sim_info)

    @classmethod
    def can_be_impregnated(cls, sim_info: SimInfo) -> bool:
        """can_be_impregnated(sim_info)

        Determine if a Sim Can Be Impregnated.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: Will return False if the Sim has the GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can be impregnated. False, if the Sim can not be impregnated.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_be_impregnated(sim_info)

    @classmethod
    def can_not_be_impregnated(cls, sim_info: SimInfo) -> bool:
        """can_not_be_impregnated(sim_info)

        Determine if a Sim Can Not Be Impregnated.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: Will return False if the Sim has the GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not be impregnated. False, if the Sim can be impregnated.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info)

    @classmethod
    def can_create_pregnancy(cls, sim_info: SimInfo) -> bool:
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

    @classmethod
    def can_reproduce(cls, sim_info: SimInfo) -> bool:
        """can_reproduce(sim_info)

        Determine if a pet Sim can reproduce.

        .. note:: Use :func:`~can_impregnate` and :func:`~can_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet Sim has the PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can reproduce. False, if the Sim can not reproduce.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_reproduce(sim_info)

    @classmethod
    def can_not_reproduce(cls, sim_info: SimInfo) -> bool:
        """can_not_reproduce(sim_info)

        Determine if a pet Sim can reproduce.

        ..note:: Use :func:`~can_not_impregnate` and :func:`~can_not_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet Sim has the PREGNANCY_OPTIONS_PET_CAN_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not reproduce. False, if the Sim can reproduce.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_reproduce(sim_info)

    @classmethod
    def uses_toilet_standing(cls, sim_info: SimInfo) -> bool:
        """uses_toilet_standing(sim_info)

        Determine if a Sim uses the toilet while standing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim uses toilets while standing. False, if the Sim does not use toilets while standing.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.uses_toilet_standing(sim_info)

    @classmethod
    def uses_toilet_sitting(cls, sim_info: SimInfo) -> bool:
        """uses_toilet_sitting(sim_info)

        Determine if a Sim uses the toilet while sitting.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim uses toilets while sitting. False, if the Sim does not use toilets while sitting.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info)

    @classmethod
    def has_trait(cls, sim_info: SimInfo, *trait_ids: Union[int, CommonTraitId]) -> bool:
        """has_trait(sim_info, *trait_ids)

        Determine if a Sim has any of the specified traits.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param trait_ids: An iterable of identifiers of Traits.
        :type trait_ids: Union[int, CommonTraitId]
        :return: True, if the Sim has any of the specified traits. False, if not.
        :rtype: bool
        """
        if not trait_ids:
            return False
        sim_trait_ids = CommonTraitUtils.get_trait_ids(sim_info)
        for trait_id in sim_trait_ids:
            if trait_id in trait_ids:
                return True
        return False

    @classmethod
    def has_any_traits(cls, sim_info: SimInfo, trait_ids: Iterator[Union[int, CommonTraitId]]) -> bool:
        """has_any_traits(sim_info, trait_ids)

        Determine if a Sim has any of the specified traits.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param trait_ids: An iterable of identifiers of Traits.
        :type trait_ids: Iterator[Union[int, CommonTraitId]]
        :return: True, if the Sim has any of the specified traits. False, if not.
        :rtype: bool
        """
        trait_ids = tuple(trait_ids)
        if not trait_ids:
            return False
        sim_trait_ids = CommonTraitUtils.get_trait_ids(sim_info)
        for trait_id in sim_trait_ids:
            if trait_id in trait_ids:
                return True
        return False

    @classmethod
    def has_all_traits(cls, sim_info: SimInfo, trait_ids: Iterator[Union[int, CommonTraitId]]) -> bool:
        """has_all_traits(sim_info, trait_ids)

        Determine if a Sim has any of the specified traits.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param trait_ids: An iterable of identifiers of Traits.
        :type trait_ids: Iterator[Union[int, CommonTraitId]]
        :return: True, if the Sim has any of the specified traits. False, if not.
        :rtype: bool
        """
        trait_ids = tuple(trait_ids)
        if not trait_ids:
            return False
        sim_trait_ids = CommonTraitUtils.get_trait_ids(sim_info)
        for trait_id in sim_trait_ids:
            if trait_id in trait_ids:
                return True
        return False

    @classmethod
    def is_conflicting_trait(cls, sim_info: SimInfo, trait_id: Union[int, CommonTraitId]) -> bool:
        """is_conflicting_trait(sim_info, trait_id)

        Determine if a Trait conflicts with any of the Sims current Traits.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param trait_id: The identifier of the trait to check.
        :type trait_id: int
        :return: True, if the specified Trait conflicts with any Traits the Sim currently has. False, if not.
        :rtype: bool
        """
        trait_to_check = CommonTraitUtils.load_trait_by_id(trait_id)
        if trait_to_check is None:
            return False
        from traits.trait_tracker import TraitTracker
        trait_tracker: TraitTracker = sim_info.trait_tracker
        return trait_tracker.is_conflicting(trait_to_check)

    @classmethod
    def get_trait_ids(cls, sim_info: SimInfo) -> List[int]:
        """get_trait_ids(sim_info)

        Retrieve decimal identifiers for all Traits of a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: A collection of Trait identifiers on a Sim.
        :rtype: List[int]
        """
        trait_ids = list()
        for trait in CommonTraitUtils.get_traits(sim_info):
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id is None:
                continue
            trait_ids.append(trait_id)
        return trait_ids

    @classmethod
    def get_traits(cls, sim_info: SimInfo) -> List[Trait]:
        """get_traits(sim_info)

        Retrieve all Traits of a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: A collection of Traits on a Sim.
        :rtype: List[int]
        """
        if not hasattr(sim_info, 'get_traits'):
            return list()
        traits = list(sim_info.get_traits())
        if traits:
            return traits
        if not hasattr(sim_info, '_base'):
            return traits
        return list([CommonTraitUtils.load_trait_by_id(trait_id) for trait_id in (*sim_info._base.trait_ids, *sim_info._base.base_trait_ids) if CommonTraitUtils.load_trait_by_id(trait_id) is not None])

    @classmethod
    def get_trait_name(cls, trait: Trait) -> Union[str, None]:
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

    @classmethod
    def get_trait_names(cls, traits: Iterator[Trait]) -> Tuple[str]:
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

    @classmethod
    def get_equipped_traits(cls, sim_info: SimInfo) -> List[Trait]:
        """get_equipped_traits(sim_info)

        Retrieve Sims currently equipped traits.

        .. note:: The main use of this function is to check Occult Types.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A collection of equipped Traits on a Sim.
        :rtype: List[int]
        """
        if not hasattr(sim_info, 'trait_tracker') or not hasattr(sim_info.trait_tracker, 'equipped_traits'):
            if hasattr(sim_info, '_base'):
                return list([CommonTraitUtils.load_trait_by_id(trait_id) for trait_id in (*sim_info._base.trait_ids, *sim_info._base.base_trait_ids) if CommonTraitUtils.load_trait_by_id(trait_id) is not None])
            return list()
        return list(sim_info.trait_tracker.equipped_traits)

    @classmethod
    def add_trait(cls, sim_info: SimInfo, *traits: Union[int, CommonTraitId, Trait]) -> bool:
        """add_trait(sim_info, *traits)

        Add the specified traits to a Sim.

        :param sim_info: The Sim to add the specified traits to.
        :type sim_info: SimInfo
        :param traits: An iterable of Trait identifiers of traits being added.
        :type traits: Union[int, CommonTraitId, Trait]
        :return: True, if all specified traits were successfully added to the Sim. False, if not.
        :rtype: bool
        """
        success = False
        for trait_id in traits:
            trait = cls.load_trait_by_id(trait_id)
            if trait is None:
                cls.get_log().format_with_message('Failed to load trait by its id.', trait_id=trait_id)
                continue
            cls.get_log().format_with_message('Attempting to add trait', trait=trait, trait_id=trait_id)
            if sim_info.add_trait(trait):
                cls.get_log().format_with_message('Successfully added trait.', trait=trait, trait_id=trait_id)
                success = True
            else:
                cls.get_log().format_with_message('Failed to add trait.', trait=trait, trait_id=trait_id)
        return success

    @classmethod
    def remove_trait(cls, sim_info: SimInfo, *traits: Union[int, CommonTraitId, Trait]) -> bool:
        """remove_trait(sim_info, *trait)

        Remove the specified traits from a Sim.

        :param sim_info: The Sim to remove the specified traits from.
        :type sim_info: SimInfo
        :param traits: An iterable of Trait identifiers of traits being removed.
        :type traits: Union[int, CommonTraitId, Trait]
        :return: True, if all specified traits were successfully removed from the Sim. False, if not.
        :rtype: bool
        """
        success = False
        for trait in traits:
            if isinstance(trait, int) or isinstance(trait, CommonTraitId):
                trait = CommonTraitUtils.load_trait_by_id(trait)
            if trait is None:
                continue
            if sim_info.remove_trait(trait):
                success = True
        return success

    @classmethod
    def swap_traits(cls, sim_info: SimInfo, trait_id_one: Union[int, CommonTraitId], trait_id_two: Union[int, CommonTraitId]) -> bool:
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

    @classmethod
    def add_trait_to_all_sims(cls, trait_id: Union[int, CommonTraitId], include_sim_callback: Callable[[SimInfo], bool]=None):
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

    @classmethod
    def remove_trait_from_all_sims(cls, trait_id: Union[int, CommonTraitId], include_sim_callback: Callable[[SimInfo], bool]=None):
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

    @classmethod
    def get_trait_id(cls, trait_identifier: Union[int, Trait]) -> Union[int, None]:
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

    @classmethod
    def load_trait_by_id(cls, trait: Union[int, CommonTraitId, Trait]) -> Union[Trait, None]:
        """load_trait_by_id(trait)

        Load an instance of a Trait by its identifier.

        :param trait: The identifier of a Trait.
        :type trait: Union[int, CommonTraitId, Trait]
        :return: An instance of a Trait matching the decimal identifier or None if not found.
        :rtype: Union[Trait, None]
        """
        if isinstance(trait, Trait):
            return trait
        # noinspection PyBroadException
        try:
            trait: int = int(trait)
        except:
            trait: Trait = trait
            return trait

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.TRAIT, trait)


@Command('s4clib.show_known_traits', command_type=CommandType.Live)
def _common_show_known_traits(opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    output('Attempting to show known traits.')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    output('Active Sim: {}'.format(CommonSimNameUtils.get_full_name(active_sim_info)))
    target_sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if target_sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    if active_sim_info is target_sim_info:
        output('Failed, Target Sim is the same as the Active Sim.')
        return
    target_sim_id = CommonSimUtils.get_sim_id(target_sim_info)
    try:
        output('Getting relationship of {} towards {}'.format(CommonSimNameUtils.get_full_name(active_sim_info), CommonSimNameUtils.get_full_name(target_sim_info)))
        relationship_tracker: RelationshipTracker = active_sim_info.relationship_tracker
        output('Getting knowledge')
        knowledge: SimKnowledge = relationship_tracker.get_knowledge(target_sim_id, initialize=False)
        output('Printing knowledge')
        if knowledge.known_traits is None:
            output('No known traits.')
            return
        output('Known Traits:')
        output(pformat(knowledge.known_traits))
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to retrieve knowledge for Sim {} to Sim {}'.format(CommonSimNameUtils.get_full_name(active_sim_info), CommonSimNameUtils.get_full_name(target_sim_info)), exception=ex)
        output('Failed to retrieve knowledge for Sim {} to Sim {}. {}'.format(CommonSimNameUtils.get_full_name(active_sim_info), CommonSimNameUtils.get_full_name(target_sim_info), str(ex)))


@Command('s4clib.add_trait', command_type=CommandType.Live)
def _common_add_trait(trait: TunableInstanceParam(Types.TRAIT), opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if trait is None:
        output('Failed, Trait not specified or Trait did not exist! s4clib.add_trait <trait_name_or_id> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Adding trait {} to Sim {}'.format(str(trait), sim_name))
    try:
        if CommonTraitUtils.add_trait(sim_info, trait):
            output('Successfully added trait.')
        else:
            output('Failed to add trait.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to add trait {} to Sim {}.'.format(str(trait), sim_name), exception=ex)
        output('Failed to add trait {} to Sim {}. {}'.format(str(trait), sim_name, str(ex)))


@Command('s4clib.remove_trait', command_type=CommandType.Live)
def _common_remove_trait(trait: TunableInstanceParam(Types.TRAIT), opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    if trait is None:
        output('Failed, Trait not specified or Trait did not exist! s4clib.remove_trait <trait_name_or_id> [opt_sim=None]')
        return
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Removing trait {} from Sim {}'.format(str(trait), sim_name))
    try:
        if CommonTraitUtils.remove_trait(sim_info, trait):
            output('Successfully removed trait.')
        else:
            output('Failed to remove trait.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to remove trait {} from Sim {}.'.format(str(trait), sim_name), exception=ex)
        output('Failed to remove trait {} from Sim {}. {}'.format(str(trait), sim_name, str(ex)))


@Command('s4clib.show_traits', command_type=CommandType.Live)
def _common_show_traits(opt_sim: OptionalTargetParam=None, _connection: int=None):
    from server_commands.argument_helpers import get_optional_target
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    sim_info = CommonSimUtils.get_sim_info(sim)
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Showing traits of Sim {}'.format(sim_name))
    try:
        trait_strings: List[str] = list()
        for trait in CommonTraitUtils.get_traits(sim_info):
            trait_name = CommonTraitUtils.get_trait_name(trait)
            trait_id = CommonTraitUtils.get_trait_id(trait)
            trait_strings.append('{} ({})'.format(trait_name, trait_id))

        trait_strings = sorted(trait_strings, key=lambda x: x)
        sim_traits = ', '.join(trait_strings)
        text = ''
        text += 'Traits:\n{}\n\n'.format(sim_traits)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string('{} Traits ({})'.format(sim_name, CommonSimUtils.get_sim_id(sim_info))),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=sim)
        )
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show traits of Sim {}.'.format(sim_name), exception=ex)
        output('Failed to show traits of Sim {}. {}'.format(sim_name, str(ex)))
