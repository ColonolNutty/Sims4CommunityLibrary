"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Union, Callable, Iterator, Tuple

from distributor.shared_messages import IconInfoData
from relationships.relationship_tracker import RelationshipTracker
from relationships.sim_knowledge import SimKnowledge
from server_commands.argument_helpers import TunableInstanceParam
from sims.pregnancy.pregnancy_offspring_data import PregnancyOffspringData
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4.resources import Types
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommandArgument, \
    CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from traits.traits import Trait


class CommonTraitUtils(_HasS4CLClassLog):
    """Utilities for manipulating Traits on Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_trait_utils'

    @classmethod
    def is_player(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_player(sim_info)

        Determine if a Sim has the Player trait.

        .. note:: This does not indicate whether the Sim is one of the Players Sims, it simply indicates if they have the trait that makes other Sims less jealous.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.PLAYER)

    @classmethod
    def is_special_npc(cls, sim_info: SimInfo) -> CommonTestResult:
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
        :return: The result of testing. True, if the Sim is a special NPC. False, if the Sim is not a Special NPC.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.HIDDEN_IS_EVENT_NPC_CHALLENGE,
            CommonTraitId.IS_GRIM_REAPER,
            CommonTraitId.SCARECROW,
            CommonTraitId.FLOWER_BUNNY
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_active(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_active(sim_info)

        Determine if a Sim is active.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.ACTIVE)

    @classmethod
    def is_aggressive_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_aggressive_pet(sim_info)

        Determine if a pet Sim is Aggressive.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_AGGRESSIVE_DOG,
            CommonTraitId.PET_AGGRESSIVE_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_alluring(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_alluring(sim_info)

        Determine if a Sim is Alluring.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.ALLURING)

    @classmethod
    def is_antiseptic(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_antiseptic(sim_info)

        Determine if a Sim is Antiseptic.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.ANTISEPTIC)

    @classmethod
    def is_bro(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_bro(sim_info)

        Determine if a Sim is a Bro.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.BRO)

    @classmethod
    def is_carefree(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_carefree(sim_info)

        Determine if a Sim is Care Free.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.CAREFREE)

    @classmethod
    def is_cat_lover(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_cat_lover(sim_info)

        Determine if a Sim is a Cat Lover.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.CAT_LOVER)

    @classmethod
    def is_dog_lover(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_dog_lover(sim_info)

        Determine if a Sim is a Dog Lover.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.DOG_LOVER)

    @classmethod
    def is_clumsy(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_clumsy(sim_info)

        Determine if a Sim is Clumsy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.CLUMSY)

    @classmethod
    def is_dastardly(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_dastardly(sim_info)

        Determine if a Sim is Dastardly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.DASTARDLY)

    @classmethod
    def is_criminal(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_criminal(sim_info)

        Determine if a Sim is a Criminal.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.DETECTIVE_CAREER_CRIMINAL,
            CommonTraitId.DETECTIVE_CAREER_POLICE_STATION_CRIMINAL_NPC
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_evil(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_evil(sim_info)

        Determine if a Sim is Evil.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.EVIL,
            CommonTraitId.EVIL_BEGONIA_SCENT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_fertile(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_fertile(sim_info)

        Determine if a Sim is Fertile.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.FERTILE)

    @classmethod
    def is_friendly_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_friendly_pet(sim_info)

        Determine if a pet Sim is Friendly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_FRIENDLY_DOG,
            CommonTraitId.PET_FRIENDLY_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_geek(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_geek(sim_info)

        Determine if a Sim is a geek.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.GEEK)

    @classmethod
    def is_genius(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_genius(sim_info)

        Determine if a Sim is a Genius.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.GENIUS)

    @classmethod
    def is_good(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_good(sim_info)

        Determine if a Sim is Good.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.GOOD)

    @classmethod
    def is_glutton(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_glutton(sim_info)

        Determine if a Sim is a Glutton.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.is_glutton_human(sim_info) or cls.is_glutton_pet(sim_info)

    @classmethod
    def is_glutton_human(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_glutton_human(sim_info)

        Determine if a non pet Sim is a Glutton

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.GLUTTON)

    @classmethod
    def is_glutton_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_glutton_pet(sim_info)

        Determine if a pet Sim is a Glutton.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_GLUTTON_DOG,
            CommonTraitId.PET_GLUTTON_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_gregarious(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_gregarious(sim_info)

        Determine if a Sim is Gregarious.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.GREGARIOUS)

    @classmethod
    def is_hot_headed(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_hot_headed(sim_info)

        Determine if a Sim is Hot Headed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.HOT_HEADED)

    @classmethod
    def is_hunter_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_hunter_pet(sim_info)

        Determine if a pet Sim is a Hunter.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_HUNTER_DOG,
            CommonTraitId.PET_HUNTER_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_incredibly_friendly(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_incredibly_friendly(sim_info)

        Determine if a Sim is Incredibly Friendly.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.INCREDIBLY_FRIENDLY)

    @classmethod
    def is_insane(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_insane(sim_info)

        Determine if a Sim is Insane.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.INSANE)

    @classmethod
    def is_insider(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_insider(sim_info)

        Determine if a Sim is an Insider.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.INSIDER)

    @classmethod
    def is_loyal_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_loyal_pet(sim_info)

        Determine if a pet Sim is Loyal.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_LOYAL_DOG,
            CommonTraitId.PET_LOYAL_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_mean(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_mean(sim_info)

        Determine if a Sim is Mean.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.MEAN)

    @classmethod
    def is_mentor(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_mentor(sim_info)

        Determine if a Sim is a Mentor.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.MENTOR)

    @classmethod
    def is_morning_person(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_morning_person(sim_info)

        Determine if a Sim is a Morning Person.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.MORNING_PERSON)

    @classmethod
    def is_naughty_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_naughty_pet(sim_info)

        Determine if a pet Sim is Naughty.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_NAUGHTY_DOG,
            CommonTraitId.PET_NAUGHTY_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_neat(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_neat(sim_info)

        Determine if a Sim is neat.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.NEAT)

    @classmethod
    def is_night_owl(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_night_owl(sim_info)

        Determine if a Sim is a Night Owl.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.NIGHT_OWL,
            CommonTraitId.NIGHT_OWL_CRYSTAL_HELMET
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_lazy(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_lazy(sim_info)

        Determine if a Sim is Lazy.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.LAZY)

    @classmethod
    def is_loner(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_loner(sim_info)

        Determine if a Sim is a Loner.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.LONER)

    @classmethod
    def is_love_guru(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_love_guru(sim_info)

        Determine if a Sim is a Love Guru.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.LOVE_GURU)

    @classmethod
    def is_self_absorbed(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_self_absorbed(sim_info)

        Determine if a Sim is Self Absorbed.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SELF_ABSORBED)

    @classmethod
    def is_self_assured(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_self_assured(sim_info)

        Determine if a Sim is Self Assured.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SELF_ASSURED)

    @classmethod
    def is_service_sim(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_service_sim(sim_info)

        Determine if a Sim is a service Sim.

        ..warning:: Obsolete: Use :func:`~is_service_sim` in :class:`.CommonSimTypeUtils` instead.

        """
        from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
        return CommonSimTypeUtils.is_service_sim(sim_info)

    @classmethod
    def is_shameless(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_shameless(sim_info)

        Determine if a Sim is Shameless.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SHAMELESS)

    @classmethod
    def is_sincere(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_sincere(sim_info)

        Determine if a Sim is Sincere.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SINCERE)

    @classmethod
    def is_skittish_pet(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_skittish_pet(sim_info)

        Determine if a pet Sim is Skittish.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        traits = (
            CommonTraitId.PET_SKITTISH_DOG,
            CommonTraitId.PET_SKITTISH_CAT
        )
        return cls.has_any_traits(sim_info, traits)

    @classmethod
    def is_slob(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_slob(sim_info)

        Determine if a Sim is a Slob.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SLOB)

    @classmethod
    def is_snob(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_snob(sim_info)

        Determine if a Sim is a Snob.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SNOB)

    @classmethod
    def is_squeamish(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_squeamish(sim_info)

        Determine if a Sim is Squeamish.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SQUEAMISH)

    @classmethod
    def is_survivalist(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_survivalist(sim_info)

        Determine if a Sim is a Survivalist.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.SURVIVALIST)

    @classmethod
    def is_unflirty(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_unflirty(sim_info)

        Determine if a Sim is Unflirty.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if the Sim does not have the Trait.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.UNFLIRTY)

    @classmethod
    def hates_children(cls, sim_info: SimInfo) -> CommonTestResult:
        """hates_children(sim_info)

        Determine if a Sim Hates Children.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Hates Children trait. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.HATES_CHILDREN)

    @classmethod
    def has_animal_attraction(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_animal_attraction(sim_info)

        Determine if a Sim has an Animal Attraction.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.ANIMAL_ATTRACTION)

    @classmethod
    def has_animal_whisperer(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_animal_whisperer(sim_info)

        Determine if a Sim is an Animal Whisperer.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.ANIMAL_WHISPERER)

    @classmethod
    def has_challenge_kindness_ambassador(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_challenge_kindness_ambassador(sim_info)

        Determine if a Sim has Challenged the Kindness Ambassador.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has challenged the kindness ambassador. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.CHALLENGE_KINDNESS_AMBASSADOR)

    @classmethod
    def has_commitment_issues(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_commitment_issues(sim_info)

        Determine if a Sim has Commitment Issues.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has the Trait. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_trait(sim_info, CommonTraitId.COMMITMENT_ISSUES)

    @classmethod
    def has_masculine_frame(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_masculine_frame(sim_info)

        Determine if a Sim has a Masculine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has a masculine frame. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.has_masculine_frame(sim_info)

    @classmethod
    def has_feminine_frame(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_feminine_frame(sim_info)

        Determine if a Sim has a Feminine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has a feminine frame. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.has_feminine_frame(sim_info)

    @classmethod
    def prefers_menswear(cls, sim_info: SimInfo) -> CommonTestResult:
        """prefers_menswear(sim_info)

        Determine if a Sim prefers Mens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim prefers menswear. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.prefers_menswear(sim_info)

    @classmethod
    def prefers_womenswear(cls, sim_info: SimInfo) -> CommonTestResult:
        """prefers_womenswear(sim_info)

        Determine if a Sim prefers Womens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim prefers womenswear. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.prefers_womenswear(sim_info)

    @classmethod
    def can_impregnate(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_impregnate(sim_info)

        Determine if a Sim Can Impregnate.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: This will check for a Sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can impregnate other Sims. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_impregnate(sim_info)

    @classmethod
    def can_not_impregnate(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_not_impregnate(sim_info)

        Determine if a Sim Can Not Impregnate.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: This will check for a Sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can not impregnate other Sims. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_impregnate(sim_info)

    @classmethod
    def can_be_impregnated(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_be_impregnated(sim_info)

        Determine if a Sim Can Be Impregnated.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: Will return False if the Sim has the GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can be impregnated. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_be_impregnated(sim_info)

    @classmethod
    def can_not_be_impregnated(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_not_be_impregnated(sim_info)

        Determine if a Sim Can Not Be Impregnated.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: Will return False if the Sim has the GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can not be impregnated. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info)

    @classmethod
    def can_create_pregnancy(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_create_pregnancy(sim_info)

        Determine if a Sim can either impregnate, be impregnated, or can reproduce.

        .. note:: Will return False if the Sim can both impregnate and not impregnate,\
            if the Sim can both be impregnated and not be impregnated\
            or if the Sim can both reproduce and not reproduce.

        .. note:: A Sim can impregnate when they can either impregnate other Sims, can be impregnated by other Sims, or if they are a Pet, can reproduce.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can create pregnancies. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_create_pregnancy(sim_info)

    @classmethod
    def can_reproduce(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_reproduce(sim_info)

        Determine if a pet Sim can reproduce.

        .. note:: Use :func:`~can_impregnate` and :func:`~can_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet Sim has the PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can reproduce. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_reproduce(sim_info)

    @classmethod
    def can_not_reproduce(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_not_reproduce(sim_info)

        Determine if a pet Sim can reproduce.

        ..note:: Use :func:`~can_not_impregnate` and :func:`~can_not_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet Sim has the PREGNANCY_OPTIONS_PET_CAN_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can not reproduce. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.can_not_reproduce(sim_info)

    @classmethod
    def uses_toilet_standing(cls, sim_info: SimInfo) -> CommonTestResult:
        """uses_toilet_standing(sim_info)

        Determine if a Sim uses the toilet while standing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim uses toilets while standing. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.uses_toilet_standing(sim_info)

    @classmethod
    def uses_toilet_sitting(cls, sim_info: SimInfo) -> CommonTestResult:
        """uses_toilet_sitting(sim_info)

        Determine if a Sim uses the toilet while sitting.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim uses toilets while sitting. False, if not.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        return CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info)

    @classmethod
    def is_ghost_trait(cls, trait_identifier: Union[int, CommonTraitId, Trait]) -> bool:
        """is_ghost_trait(trait_identifier)

        Determine if a trait is a Ghost trait.

        :param trait_identifier: An identifier of a trait.
        :type trait_identifier: Union[int, CommonTraitId, Trait]
        :return: True, if the specified trait is a ghost trait. False, if not.
        """
        trait = cls.load_trait_by_id(trait_identifier)
        if trait is None:
            return False
        return getattr(trait, 'is_ghost_trait', None) is True

    @classmethod
    def has_trait(cls, sim_info: SimInfo, *trait: Union[int, CommonTraitId, Trait]) -> CommonTestResult:
        """has_trait(sim_info, trait)

        Determine if a Sim has a Trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param trait: The trait to check for.
        :type trait: Union[int, CommonTraitId, Trait]
        :return: The result of testing. True, if the Sim has the specified trait. False, if not.
        :rtype: CommonTestResult
        """
        if isinstance(sim_info, SimInfo):
            for _trait in trait:
                __trait = cls.load_trait_by_id(_trait)
                if __trait is None:
                    continue
                if sim_info.has_trait(__trait):
                    return CommonTestResult(True, reason=f'{sim_info} has trait {__trait}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_TRAIT, tooltip_tokens=(sim_info, str(__trait)))
        elif isinstance(sim_info, SimInfoBaseWrapper):
            sim_info: SimInfoBaseWrapper = sim_info
            any_traits = cls.get_trait_ids(sim_info)
            if not any_traits:
                return CommonTestResult(False, reason=f'{sim_info} does not have any traits.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_ANY_TRAITS, tooltip_tokens=(sim_info,))
            for _trait in trait:
                __trait = cls.get_trait_id(_trait)
                if __trait is None:
                    continue
                if _trait in any_traits:
                    return CommonTestResult(True, reason=f'{sim_info} has trait {__trait}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_TRAIT, tooltip_tokens=(sim_info, str(__trait)))
        elif isinstance(sim_info, PregnancyOffspringData):
            sim_info: PregnancyOffspringData = sim_info
            any_traits = [cls.get_trait_id(trait) for trait in sim_info.traits]
            if not any_traits:
                return CommonTestResult(False, reason=f'{sim_info} does not have any traits.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_ANY_TRAITS, tooltip_tokens=(sim_info,))
            for _trait in trait:
                __trait = cls.get_trait_id(_trait)
                if __trait is None:
                    continue
                if _trait in any_traits:
                    return CommonTestResult(True, reason=f'{sim_info} has trait {__trait}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_TRAIT, tooltip_tokens=(sim_info, str(__trait)))
        return CommonTestResult(False, reason=f'{sim_info} does not have trait(s) {trait}', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_TRAITS, tooltip_tokens=(sim_info, str(trait)))

    @classmethod
    def has_any_traits(cls, sim_info: SimInfo, traits: Iterator[Union[int, CommonTraitId, Trait]]) -> CommonTestResult:
        """has_any_traits(sim_info, trait_ids)

        Determine if a Sim has any of the specified traits.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param traits: An iterator of identifiers of Traits.
        :type traits: Iterator[Union[int, CommonTraitId, Trait]]
        :return: The result of testing. True, if the Sim has any of the specified traits. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not traits:
            return CommonTestResult(False, reason='No traits were specified.', hide_tooltip=True)
        if isinstance(sim_info, SimInfo):
            for trait in traits:
                _trait = cls.load_trait_by_id(trait)
                if _trait is None:
                    continue
                if sim_info.has_trait(_trait):
                    return CommonTestResult(True, reason=f'{sim_info} has trait {_trait}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_TRAIT, tooltip_tokens=(sim_info, str(_trait)))
        elif isinstance(sim_info, SimInfoBaseWrapper):
            sim_info: SimInfoBaseWrapper = sim_info
            any_traits = cls.get_trait_ids(sim_info)
            if not any_traits:
                return CommonTestResult(False, reason=f'{sim_info} does not have any traits.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_ANY_TRAITS, tooltip_tokens=(sim_info,))
            for _trait in traits:
                __trait = cls.get_trait_id(_trait)
                if __trait is None:
                    continue
                if _trait in any_traits:
                    return CommonTestResult(True, reason=f'{sim_info} has trait {__trait}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_TRAIT, tooltip_tokens=(sim_info, str(__trait)))
        elif isinstance(sim_info, PregnancyOffspringData):
            sim_info: PregnancyOffspringData = sim_info
            any_traits = [cls.get_trait_id(trait) for trait in sim_info.traits]
            if not any_traits:
                return CommonTestResult(False, reason=f'{sim_info} does not have any traits.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_ANY_TRAITS, tooltip_tokens=(sim_info,))
            for _trait in traits:
                __trait = cls.get_trait_id(_trait)
                if __trait is None:
                    continue
                if _trait in any_traits:
                    return CommonTestResult(True, reason=f'{sim_info} has trait {__trait}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_TRAIT, tooltip_tokens=(sim_info, str(__trait)))
        return CommonTestResult(False, reason=f'{sim_info} does not have any trait(s) {traits}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_TRAITS, tooltip_tokens=(sim_info, str(trait)))

    @classmethod
    def has_all_traits(cls, sim_info: SimInfo, traits: Iterator[Union[int, CommonTraitId, Trait]]) -> CommonTestResult:
        """has_all_traits(sim_info, trait_ids)

        Determine if a Sim has any of the specified traits.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param traits: An iterator of identifiers of Traits.
        :type traits: Iterator[Union[int, CommonTraitId, Trait]]
        :return: The result of testing. True, if the Sim has any of the specified traits. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not traits:
            return CommonTestResult(False, reason='No traits were specified.', hide_tooltip=True)
        if isinstance(sim_info, SimInfo):
            for trait in traits:
                _trait = cls.load_trait_by_id(trait)
                if _trait is None:
                    continue
                if not sim_info.has_trait(_trait):
                    return CommonTestResult(False, reason=f'{sim_info} does not have trait {_trait}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_TRAIT, tooltip_tokens=(sim_info, str(_trait)))
        elif isinstance(sim_info, SimInfoBaseWrapper):
            sim_info: SimInfoBaseWrapper = sim_info
            any_traits = cls.get_trait_ids(sim_info)
            if not any_traits:
                return CommonTestResult(False, reason=f'{sim_info} does not have any traits.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_ANY_TRAITS, tooltip_tokens=(sim_info,))
            for _trait in traits:
                __trait = cls.get_trait_id(_trait)
                if __trait is None:
                    continue
                if _trait not in any_traits:
                    return CommonTestResult(False, reason=f'{sim_info} does not have trait {_trait}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_TRAIT, tooltip_tokens=(sim_info, str(_trait)))
        elif isinstance(sim_info, PregnancyOffspringData):
            sim_info: PregnancyOffspringData = sim_info
            any_traits = cls.get_trait_ids(sim_info)
            if not any_traits:
                return CommonTestResult(False, reason=f'{sim_info} does not have any traits.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_ANY_TRAITS, tooltip_tokens=(sim_info,))
            for _trait in traits:
                __trait = cls.get_trait_id(_trait)
                if __trait is None:
                    continue
                if _trait not in any_traits:
                    return CommonTestResult(False, reason=f'{sim_info} does not have trait {_trait}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_TRAIT, tooltip_tokens=(sim_info, str(_trait)))
        return CommonTestResult(True, reason=f'{sim_info} has all traits {traits}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_ALL_TRAITS, tooltip_tokens=(sim_info, str(traits)))

    @classmethod
    def is_conflicting_trait(cls, sim_info: SimInfo, trait_id: Union[int, CommonTraitId, Trait]) -> CommonTestResult:
        """is_conflicting_trait(sim_info, trait_id)

        Determine if a Trait conflicts with any of the Sims current Traits.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param trait_id: The identifier of the trait to check.
        :type trait_id: int
        :return: The result of testing. True, if the specified Trait conflicts with any Traits the Sim currently has. False, if not.
        :rtype: CommonTestResult
        """
        trait_to_check = cls.load_trait_by_id(trait_id)
        if trait_to_check is None:
            return CommonTestResult(False, reason=f'Trait {trait_id} did not exist, thus it cannot conflict.', hide_tooltip=True)
        from traits.trait_tracker import TraitTracker
        trait_tracker: TraitTracker = sim_info.trait_tracker
        return trait_tracker.is_conflicting(trait_to_check)

    @classmethod
    def get_trait_ids(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper, PregnancyOffspringData]) -> List[int]:
        """get_trait_ids(sim_info)

        Retrieve decimal identifiers for all Traits of a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper, PregnancyOffspringData]
        :return: A collection of Trait identifiers on a Sim.
        :rtype: List[int]
        """
        trait_ids = list()
        if isinstance(sim_info, SimInfo) or isinstance(sim_info, PregnancyOffspringData):
            for trait in cls.get_traits(sim_info):
                trait_id = cls.get_trait_id(trait)
                if trait_id is None:
                    continue
                trait_ids.append(trait_id)
        elif isinstance(sim_info, SimInfoBaseWrapper):
            return list(sim_info._get_trait_ids())
        return trait_ids

    @classmethod
    def get_traits(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper, PregnancyOffspringData]) -> List[Trait]:
        """get_traits(sim_info)

        Retrieve all Traits of a Sim.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper, PregnancyOffspringData]
        :return: A collection of Traits on a Sim.
        :rtype: List[int]
        """
        if isinstance(sim_info, SimInfo):
            if not hasattr(sim_info, 'get_traits'):
                return list()
            traits = list(sim_info.get_traits())
            if traits:
                return traits
            if not hasattr(sim_info, '_base'):
                return traits
            return list([cls.load_trait_by_id(trait_id) for trait_id in (*sim_info._base.trait_ids, *sim_info._base.base_trait_ids) if cls.load_trait_by_id(trait_id) is not None])
        elif isinstance(sim_info, PregnancyOffspringData):
            return sim_info.traits
        elif isinstance(sim_info, SimInfoBaseWrapper):
            return [cls.load_trait_by_id(trait_id) for trait_id in cls.get_trait_ids(sim_info)]
        return list()

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
            return trait.__name__ or trait.__class__.__name__
        except:
            # noinspection PyBroadException
            try:
                return trait.__class__.__name__
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
                name = cls.get_trait_name(trait)
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
                return list([cls.load_trait_by_id(trait_id) for trait_id in (*sim_info._base.trait_ids, *sim_info._base.base_trait_ids) if cls.load_trait_by_id(trait_id) is not None])
            return list()
        return list(sim_info.trait_tracker.equipped_traits)

    @classmethod
    def add_trait(cls, sim_info: SimInfo, *trait: Union[int, CommonTraitId, Trait]) -> CommonExecutionResult:
        """add_trait(sim_info, trait)

        Add a Trait to a Sim.

        :param sim_info: The Sim to add the specified traits to.
        :type sim_info: SimInfo
        :param trait: The trait being added.
        :type trait: Union[int, CommonTraitId, Trait]
        :return: The result of adding the trait. True, if the trait was successfully added to the Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.add_traits(sim_info, trait)

    @classmethod
    def add_traits(cls, sim_info: SimInfo, traits: Iterator[Union[int, CommonTraitId, Trait]]) -> CommonExecutionResult:
        """add_traits(sim_info, traits)

        Add Traits to a Sim.

        :param sim_info: The Sim to add the specified traits to.
        :type sim_info: SimInfo
        :param traits: An iterator of identifiers of traits being added.
        :type traits: Iterator[Union[int, CommonTraitId, Trait]]
        :return: The result of adding the traits. True, if all specified traits were successfully added to the Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        has_any = False
        success = True
        failed_to_add_traits = list()
        for trait_id in traits:
            trait = cls.load_trait_by_id(trait_id)
            if trait is None:
                cls.get_log().format_with_message('Failed to load trait by its id.', sim=sim_info, trait_id=trait_id)
                failed_to_add_traits.append(trait_id)
                continue
            has_any = True
            if cls.has_trait(sim_info, trait):
                cls.get_log().format_with_message('Sim already had trait.', sim=sim_info, trait=trait)
                continue
            cls.get_log().format_with_message('Attempting to add trait', sim=sim_info, trait=trait, trait_id=trait_id)
            add_result = sim_info.add_trait(trait)
            if not add_result:
                cls.get_log().format_with_message('Failed to add trait.', sim=sim_info, trait=trait, trait_id=trait_id, reason=add_result)
                success = False
                failed_to_add_traits.append(trait)
            else:
                cls.get_log().format_with_message('Successfully added trait.', sim=sim_info, trait=trait, trait_id=trait_id)
        if not success:
            failed_to_add_traits_str = ', '.join([cls.get_trait_name(trait) or str(trait) if isinstance(trait, Trait) else str(trait) for trait in failed_to_add_traits])
            return CommonExecutionResult(False, reason=f'Failed to add traits to {sim_info}. {failed_to_add_traits_str}', tooltip_text=CommonStringId.S4CL_FAILED_TO_ADD_TRAITS_TO_SIM, tooltip_tokens=(sim_info, failed_to_add_traits_str))
        if not has_any:
            return CommonExecutionResult(True, reason=f'Finished "adding" traits to {sim_info}, but none of the specified traits were loaded.', tooltip_text=CommonStringId.S4CL_TRAITS_WERE_ADDED_TO_SIM_BUT_NONE_WERE_LOADED, tooltip_tokens=(sim_info,))
        return CommonExecutionResult(True, reason=f'Successfully added traits to {sim_info}.', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_ADDED_TRAITS_TO_SIM, tooltip_tokens=(sim_info,))

    @classmethod
    def remove_trait(cls, sim_info: SimInfo, *trait: Union[int, CommonTraitId, Trait]) -> CommonExecutionResult:
        """remove_trait(sim_info, trait)

        Remove a Trait from a Sim.

        :param sim_info: The Sim to remove the specified traits from.
        :type sim_info: SimInfo
        :param trait: The trait being removed.
        :type trait: Union[int, CommonTraitId, Trait]
        :return: The result of removing the trait. True, if the trait was successfully removed from the Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        return cls.remove_traits(sim_info, trait)

    @classmethod
    def remove_traits(cls, sim_info: SimInfo, traits: Iterator[Union[int, CommonTraitId, Trait]]) -> CommonExecutionResult:
        """remove_traits(sim_info, traits)

        Remove Traits from a Sim.

        :param sim_info: The Sim to remove the specified traits from.
        :type sim_info: SimInfo
        :param traits: An iterator of Trait identifiers of traits being removed.
        :type traits: Iterator[Union[int, CommonTraitId, Trait]]
        :return: The result of removing the traits. True, if all specified traits were successfully removed from the Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        has_any_loaded = False
        success = True
        failed_to_remove_traits = list()
        for trait_id in traits:
            trait = cls.load_trait_by_id(trait_id)
            if trait is None:
                failed_to_remove_traits.append(trait_id)
                continue
            # If the Sim does not have the trait, the remove_trait function will return False. We check if they have it before attempting, so we don't run into this.
            if not cls.has_trait(sim_info, trait):
                continue
            has_any_loaded = True
            if not sim_info.remove_trait(trait):
                failed_to_remove_traits.append(trait)
                success = False

        if not success:
            failed_to_remove_traits_str = ', '.join([cls.get_trait_name(trait) or str(trait) if isinstance(trait, Trait) else str(trait) for trait in failed_to_remove_traits])
            return CommonExecutionResult(False, reason=f'Failed to remove traits from {sim_info}. {failed_to_remove_traits_str}', tooltip_text=CommonStringId.S4CL_FAILED_TO_REMOVE_TRAITS_FROM_SIM, tooltip_tokens=(sim_info, failed_to_remove_traits_str))
        if not has_any_loaded:
            return CommonExecutionResult(True, reason=f'Finished "removing" traits from {sim_info}, but none of the specified traits were loaded.', tooltip_text=CommonStringId.S4CL_TRAITS_WERE_REMOVED_FROM_SIM_BUT_NONE_WERE_LOADED, tooltip_tokens=(sim_info,))
        return CommonExecutionResult(True, reason=f'Successfully removed traits from {sim_info}.', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_REMOVED_TRAITS_FROM_SIM, tooltip_tokens=(sim_info,))

    @classmethod
    def swap_traits(cls, sim_info: SimInfo, trait_id_one: Union[int, CommonTraitId, Trait], trait_id_two: Union[int, CommonTraitId, Trait]) -> CommonExecutionResult:
        """swap_traits(sim_info, trait_id_one, trait_id_two)

        Remove one trait and add another to a Sim.

        .. note:: If `trait_id_one` exists on the Sim, it will be removed and `trait_id_two` will be added.
        .. note:: If `trait_id_two` exists on the Sim, it will be removed and `trait_id_one` will be added.

        :param sim_info: The Sim to remove the specified traits from.
        :type sim_info: SimInfo
        :param trait_id_one: The first trait to remove/add
        :type trait_id_one: Union[int, CommonTraitId, Trait]
        :param trait_id_two: The second trait to remove/add
        :type trait_id_two: Union[int, CommonTraitId, Trait]
        :return: The result of swapping traits. True, if the Traits were swapped successfully. False, if neither Trait exists on a Sim or the traits were not swapped successfully.
        :rtype: CommonExecutionResult
        """
        # Has Trait One
        if cls.has_trait(sim_info, trait_id_one):
            cls.remove_trait(sim_info, trait_id_one)
            if not cls.has_trait(sim_info, trait_id_two):
                return cls.add_trait(sim_info, trait_id_two)
            return CommonExecutionResult(True, reason=f'Successfully swapped Traits {trait_id_one} and {trait_id_two} on {sim_info}.', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_SWAP_TRAIT_AND_TRAIT_ON_SIM, tooltip_tokens=(str(trait_id_one), str(trait_id_two), sim_info))
        # Has Trait Two
        elif cls.has_trait(sim_info, trait_id_two):
            cls.remove_trait(sim_info, trait_id_two)
            if not cls.has_trait(sim_info, trait_id_one):
                return cls.add_trait(sim_info, trait_id_one)
            return CommonExecutionResult(True, reason=f'Successfully swapped Traits {trait_id_two} and {trait_id_one} on {sim_info}.', tooltip_text=CommonStringId.S4CL_SUCCESSFULLY_SWAP_TRAIT_AND_TRAIT_ON_SIM, tooltip_tokens=(str(trait_id_two), str(trait_id_one), sim_info))
        return CommonExecutionResult(False, reason=f'{sim_info} had neither Trait One {trait_id_one} nor Trait Two {trait_id_two}.', tooltip_text=CommonStringId.S4CL_SIM_HAD_NEITHER_TRAIT_NOR_TRAIT_TO_SWAP, tooltip_tokens=(sim_info, str(trait_id_one), str(trait_id_two)))

    @classmethod
    def add_trait_to_all_sims(cls, trait_id: Union[int, CommonTraitId, Trait], include_sim_callback: Callable[[SimInfo], bool] = None):
        """add_trait_to_all_sims(trait_id, include_sim_callback=None)

        Add a trait to all Sims that match the specified include filter.

        :param trait_id: The identifier of the Trait to add to all Sims.
        :type trait_id: Union[int, CommonTraitId, Trait]
        :param include_sim_callback: Only Sims that match this filter will have the Trait added.
        :type include_sim_callback: Callback[[SimInfo], bool], optional
        """
        for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            if cls.has_trait(sim_info, trait_id):
                continue
            cls.add_trait(sim_info, trait_id)

    @classmethod
    def remove_trait_from_all_sims(cls, trait_id: Union[int, CommonTraitId, Trait], include_sim_callback: Callable[[SimInfo], bool] = None):
        """remove_trait_from_all_sims(trait_id, include_sim_callback=None)

        Remove a trait from all Sims that match the specified include filter.

        :param trait_id: The identifier of the Trait to remove from all Sims.
        :type trait_id: Union[int, CommonTraitId, Trait]
        :param include_sim_callback: Only Sims that match this filter will have the Trait removed.
        :type include_sim_callback: Callback[[SimInfo], bool], optional
        """
        for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            if not cls.has_trait(sim_info, trait_id):
                continue
            cls.remove_trait(sim_info, trait_id)

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
    def is_trait_available(cls, trait: Union[int, CommonTraitId, Trait]) -> bool:
        """is_trait_available(trait)

        Determine if a Trait is available for use.

        .. note:: If the Trait is part of a package that is not installed, it will be considered as not available.

        :param trait: The trait to check for.
        :type trait: Union[int, CommonTraitId, Trait]
        :return: True, if the Trait is available for use. False, if not.
        :rtype: bool
        """
        return cls.load_trait_by_id(trait) is not None

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
            # noinspection PyCallingNonCallable
            trait_instance = trait()
            if isinstance(trait_instance, Trait):
                # noinspection PyTypeChecker
                return trait
        except:
            pass
        # noinspection PyBroadException
        try:
            trait: int = int(trait)
        except:
            # noinspection PyTypeChecker
            trait: Trait = trait
            return trait

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.TRAIT, trait)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_known_traits',
    'Print a list of all personality, occult, and other types of traits Sim A knows about Sim B. (For example Sim A could know that Sim B is Childish)',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info_a', 'Sim Id or Name', 'The instance id or name of a Sim to check.', is_optional=True, default_value='Active Sim'),
        CommonConsoleCommandArgument('sim_info_b', 'Sim Id or Name', 'The instance id or name of a Sim to check.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_print_known_traits(output: CommonConsoleCommandOutput, sim_info_a: SimInfo = None, sim_info_b: SimInfo = None):
    if sim_info_a is None:
        return
    if sim_info_b is None:
        return
    if sim_info_a is sim_info_b:
        output('ERROR: Sim A knows all traits about Sim B, because Sim A IS Sim B. Please specify at least one other Sim for either Sim A or Sim B when running this command!')
        return
    output(f'Attempting to print the traits that Sim A knows about Sim B.')
    sim_id_b = CommonSimUtils.get_sim_id(sim_info_b)
    relationship_tracker: RelationshipTracker = sim_info_a.relationship_tracker
    knowledge: SimKnowledge = relationship_tracker.get_knowledge(sim_id_b, initialize=False)
    if knowledge.known_traits is None and knowledge.known_traits:
        output('SUCCESS: Sim A knows zero traits about Sim B.')
        return
    output(f'Traits that Sim A {sim_info_a} knows about Sim B {sim_info_b}:')
    for trait in knowledge.known_traits:
        output(f'- {trait}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_trait',
    'Add a trait to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('trait', 'Trait Id or Tuning Name', 'The decimal identifier or Tuning Name of the Trait to add.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to add the trait to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.addtrait',
    )
)
def _common_add_trait(output: CommonConsoleCommandOutput, trait: TunableInstanceParam(Types.TRAIT), sim_info: SimInfo = None):
    if trait is None:
        return
    if sim_info is None:
        return
    output(f'Adding trait {trait} to Sim {sim_info}')
    result = CommonTraitUtils.add_trait(sim_info, trait)
    if result:
        output(f'SUCCESS: Successfully added trait {trait} to Sim {sim_info}: {result.reason}')
    else:
        output(f'FAILED: Failed to add trait {trait} to Sim {sim_info}. {result.reason}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_trait',
    'Remove a trait from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('trait', 'Trait Id or Tuning Name', 'The decimal identifier or Tuning Name of the Trait to remove.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to remove the trait from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.removetrait',
    )
)
def _common_remove_trait(output: CommonConsoleCommandOutput, trait: TunableInstanceParam(Types.TRAIT), sim_info: SimInfo = None):
    if trait is None:
        return
    if sim_info is None:
        return
    output(f'Removing trait {trait} from Sim {sim_info}')
    result = CommonTraitUtils.remove_trait(sim_info, trait)
    if result:
        output(f'SUCCESS: Successfully removed trait {trait} from Sim {sim_info}: {result.reason}')
    else:
        output(f'FAILED: Failed to remove trait {trait} from Sim {sim_info}: {result.reason}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_traits',
    'Print a list of all traits on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printtraits',
    )
)
def _common_show_traits(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    log = CommonTraitUtils.get_log()
    try:
        log.enable()
        output(f'Showing traits of Sim {sim_info}')
        trait_strings: List[str] = list()
        for trait in CommonTraitUtils.get_traits(sim_info):
            trait_name = CommonTraitUtils.get_trait_name(trait)
            trait_id = CommonTraitUtils.get_trait_id(trait)
            trait_strings.append(f'{trait_name} ({trait_id})')

        trait_strings = sorted(trait_strings, key=lambda x: x)
        sim_traits = ', '.join(trait_strings)
        text = ''
        text += f'Traits:\n{sim_traits}\n\n'
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        log.debug(f'{sim_info} Traits ({sim_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'{sim_info} Traits ({sim_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=CommonSimUtils.get_sim_instance(sim_info))
        )
    finally:
        log.disable()
