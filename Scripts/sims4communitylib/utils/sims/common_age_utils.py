"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Union, Iterator

import services
from event_testing.test_events import TestEvent
from sims.sim_info import SimInfo
from sims.sim_info_types import Age, Species, SpeciesExtended
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class CommonAgeUtils:
    """Utilities for manipulating Ages of Sims.

    """
    @classmethod
    def get_age(cls, sim_info: SimInfo, exact_age: bool = False) -> Union[Age, int, None]:
        """get_age(sim_info, exact_age=False)

        Retrieve the Age of a Sim.

        :param sim_info: The Sim to get the Age of.
        :type sim_info: SimInfo
        :param exact_age: If set to True, the exact age of the Sim will be returned (Age 24 will be returned as 24). If set to False, the age of the Sim rounded to the nearest Age value will be returned. (Age 24 will be returned as Age.YOUNGADULT). Default is False.
        :type exact_age: bool, optional
        :return: The Age of the Sim or None if a problem occurs.
        :rtype: Union[Age, None]
        """
        if sim_info is None:
            return None
        age: Union[Age, None] = None
        if hasattr(sim_info, 'age'):
            # noinspection PyPropertyAccess
            age = sim_info.age
        elif hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age') and exact_age:
            age = sim_info.sim_info._base.age
        elif hasattr(sim_info, '_base') and hasattr(sim_info._base, 'age'):
            age = sim_info._base.age
        elif hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age') and exact_age:
            age = sim_info.sim_info._base.age
        elif hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'age'):
            age = sim_info.sim_info.age
        if age is None:
            return None
        if exact_age:
            return age
        return cls.convert_to_approximate_age(age)

    @classmethod
    def get_birth_age(cls, sim_info: SimInfo) -> Age:
        """get_birth_age(sim_info)

        Retrieve the Age that New Sims will be, if they are born from a specified Sim.

        .. note:: Human Sims start at the BABY age. Pet Sims (Large Dog, Small Dog, Cat, Horse) start at the CHILD age. Fox Sims start at the ADULT age.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: The Age that New Sims will be, if they are born from the specified Sim.
        :rtype: Age
        """
        return sim_info.get_birth_age()

    @classmethod
    def get_birth_age_from_species(cls, species: Union[Species, SpeciesExtended, int]) -> Union[Age, None]:
        """get_birth_age_from_species(species)

        Retrieve the Age that New Sims will be, if they are born with a specified Species.

        .. note:: The HUMAN species starts at the BABY age. The Pet species (Large Dog, Small Dog, Cat, Horse) start at the CHILD age. The FOX species starts at the ADULT age.

        :param species: The species to retrieve information for.
        :type species: Union[Species, SpeciesExtended, int]
        :return: The Age that New Sims will be, if they are born with the specified Species or None if an Age is not found for the specified Species.
        :rtype: Union[Age, None]
        """
        from sims.aging.aging_tuning import AgingTuning
        cleaned_species = species
        if cleaned_species == SpeciesExtended.SMALLDOG:
            cleaned_species = Species.DOG
        cleaned_species = Species(cleaned_species)
        if cleaned_species in AgingTuning.AGING_DATA:
            aging_data = AgingTuning.get_aging_data(cleaned_species)
            return aging_data.get_birth_age()

        if species == SpeciesExtended.HUMAN:
            return Age.BABY

        if species == SpeciesExtended.FOX:
            return Age.ADULT

        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        if CommonSpeciesUtils.is_animal_species(species) or species == SpeciesExtended.SMALLDOG:
            return Age.CHILD
        return None

    @classmethod
    def convert_to_approximate_age(cls, age: Union[CommonAge, Age, int]) -> Age:
        """convert_to_approximate_age(age)

        Convert an age to an approximate Age value.

        :param age: An Age.
        :type age: Union[CommonAge, Age, int]
        :return: The specified Age converted into an approximate Age value.
        :rtype: Age
        """
        if isinstance(age, CommonAge):
            return CommonAge.convert_to_vanilla(age)
        if isinstance(age, Age):
            return age
        age: int = int(age)
        if int(age) == int(Age.INFANT):
            return Age.INFANT
        if int(Age.BABY) <= age < int(Age.INFANT):
            return Age.BABY
        if int(Age.INFANT) <= age < int(Age.TODDLER):
            return Age.INFANT
        if int(Age.TODDLER) <= age < int(Age.CHILD):
            return Age.TODDLER
        if int(Age.CHILD) <= age < int(Age.TEEN):
            return Age.CHILD
        if int(Age.TEEN) <= age < int(Age.YOUNGADULT):
            return Age.TEEN
        if int(Age.YOUNGADULT) <= age < int(Age.ADULT):
            return Age.YOUNGADULT
        if int(Age.ADULT) <= age < int(Age.ELDER):
            return Age.ADULT
        if int(Age.ELDER) <= age:
            return Age.ELDER
        return Age.INFANT

    @classmethod
    def get_total_days_sim_has_been_in_their_current_age(cls, sim_info: SimInfo) -> float:
        """get_total_days_sim_has_been_in_their_current_age(sim_info)

        Retrieve the total number of days a Sim has been in their current Age.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A total number of days the specified Sim has been in their current Age.
        :rtype: float
        """
        return sim_info.age_progress

    @classmethod
    def get_percentage_total_days_sim_has_been_in_their_current_age(cls, sim_info: SimInfo) -> float:
        """get_percentage_total_days_sim_has_been_in_their_current_age(sim_info)

        Retrieve the percentage total days a Sim has been in their current age.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The percentage total days the specified Sim has been in their current age.
        :rtype: float
        """
        return sim_info.age_progress/sim_info._age_time*sim_info.AGE_PROGRESS_BAR_FACTOR

    @classmethod
    def get_total_days_until_sim_ages_up(cls, sim_info: SimInfo) -> int:
        """get_total_days_until_sim_ages_up(sim_info)

        Retrieve the total number of days a Sim has left until they age up.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The total number of days the specified Sim has left until they age up.
        :rtype: int
        """
        return sim_info.days_until_ready_to_age()

    @classmethod
    def get_total_days_to_age_up(cls, sim_info: SimInfo) -> float:
        """get_total_days_to_age_up(sim_info)

        Retrieve the total number of days required for the next age of a Sim to be required. (Not to be confused with the amount of days they have left)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The total number of days required for the specified Sim to reach their next age.
        :rtype: float
        """
        sim_age = cls.get_age(sim_info, exact_age=False)
        age_transition_data = sim_info.get_age_transition_data(sim_age)
        return sim_info._age_time/age_transition_data.get_age_duration(sim_info)

    @classmethod
    def set_total_days_sim_has_been_in_their_current_age(cls, sim_info: SimInfo, days: float) -> None:
        """set_total_days_sim_has_been_in_their_current_age(sim_info, days)

        Set the total number of days of progress made towards the next age of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param days: The total number of days the Sim has been in their current age.
        :type days: float
        """
        delta_age = days
        new_age_value = min(delta_age, sim_info._age_time)
        sim_info._set_age_progress(new_age_value - sim_info.FILL_AGE_PROGRESS_BAR_BUFFER)

    @classmethod
    def set_percentage_total_days_sim_has_been_in_their_current_age(cls, sim_info: SimInfo, percentage_progress: float) -> None:
        """set_percentage_total_days_sim_has_been_in_their_current_age(sim_info, percentage_progress)

        Set the percentage total days a Sim has been in their current age.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param percentage_progress: A percentage total days a Sim has been in their current age.
        :type percentage_progress: int
        """
        if percentage_progress < 0:
            percentage_progress *= -1
        delta_age = cls.get_total_days_to_age_up(sim_info) * (percentage_progress / 100)
        new_age_value = min(delta_age, sim_info._age_time)
        sim_info._set_age_progress(new_age_value - sim_info.FILL_AGE_PROGRESS_BAR_BUFFER)

    @classmethod
    def set_age(cls, sim_info: SimInfo, age: Union[CommonAge, Age, int]) -> bool:
        """set_age(sim_info, age)

        Set the Age of a Sim.

        :param sim_info: The Sim to set the Age of.
        :type sim_info: SimInfo
        :param age: The Age to set the Sim to.
        :type age: Union[CommonAge, Age, int]
        :return: True, if the Age was set successfully. False, if not.
        :rtype: bool
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        age = cls.convert_to_approximate_age(age)
        if age is None:
            return False
        current_age = cls.get_age(sim_info, exact_age=False)
        approximate_age = cls.convert_to_approximate_age(age)
        if current_age is None:
            return False
        if current_age == approximate_age:
            return True
        sim_info.change_age(age, current_age)
        services.get_event_manager().process_event(TestEvent.AgedUp, sim_info=sim_info)
        school_data = sim_info.get_school_data()
        if school_data is not None:
            school_data.update_school_data(sim_info, create_homework=True)
        if sim_info.is_npc:
            if sim_info.is_child or sim_info.is_teen:
                available_aspirations = []
                aspiration_track_manager = CommonResourceUtils.get_instance_manager(Types.ASPIRATION_TRACK)
                aspiration_tracker = sim_info.aspiration_tracker
                for aspiration_track in aspiration_track_manager.types.values():
                    track_available = not aspiration_track.is_hidden_unlockable
                    if aspiration_tracker is not None:
                        track_available = aspiration_tracker.is_aspiration_track_visible(aspiration_track)
                    if track_available:
                        if sim_info.is_child and hasattr(aspiration_track, 'is_child_aspiration_track') and aspiration_track.is_child_aspiration_track:
                            available_aspirations.append(aspiration_track)
                        elif sim_info.is_teen:
                            available_aspirations.append(aspiration_track)
                if available_aspirations:
                    sim_info.primary_aspiration = random.choice(available_aspirations)
            number_of_empty_trait_slots = sim_info.trait_tracker.empty_slot_number
            if number_of_empty_trait_slots:
                # noinspection PyUnresolvedReferences
                available_traits = [trait for trait in services.trait_manager().types.values() if trait.is_personality_trait]
                while number_of_empty_trait_slots > 0 and available_traits:
                    trait = random.choice(available_traits)
                    available_traits.remove(trait)
                    if sim_info.trait_tracker.can_add_trait(trait) and sim_info.add_trait(trait):
                        number_of_empty_trait_slots -= 1
        age_transition = sim_info.get_age_transition_data(age)
        age_transition.apply_aging_transition_loot(sim_info)
        sim_info._create_additional_statistics()
        sim_info._apply_life_skill_traits()
        sim_info._relationship_tracker.update_compatibilities()
        return cls.get_age(sim_info) == age or cls.get_age(sim_info, exact_age=True) == age

    @classmethod
    def are_same_age(cls, sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_age(sim_info, other_sim_info)

        Determine if two Sims are the same Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The other Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Age.
        :rtype: bool
        """
        return int(cls.get_age(sim_info)) == int(cls.get_age(other_sim_info))

    @classmethod
    def is_younger_than(cls, sim_info: SimInfo, age: Union[CommonAge, Age, int], or_equal: bool = False) -> bool:
        """is_younger_than(sim_info, age, or_equal=False)

        Determine if a Sim is younger than the specified Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param age: The age to check with.
        :type age: Union[CommonAge, Age, int]
        :param or_equal: If True, the age check will be younger than or equal to. If False, the age check will be younger than.
        :type or_equal: bool
        :return: True, if the Sim is younger than the specified Age or equal to the specified age if `or_equal` is True. False, if not.
        :rtype: bool
        """
        age = int(age)
        sim_age = int(cls.get_age(sim_info))
        if or_equal:
            return sim_age <= age
        return sim_age < age

    @classmethod
    def is_older_than(cls, sim_info: SimInfo, age: Union[CommonAge, Age, int], or_equal: bool = False) -> bool:
        """is_older_than(sim_info, age, or_equal=False)

        Determine if a Sim is older than the specified Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param age: The age to check with.
        :type age: Union[CommonAge, Age, int]
        :param or_equal: If True, the age check will be older than or equal to. If False, the Age check will be older than.
        :type or_equal: bool
        :return: True, if the Sim is older than the specified Age or equal to the specified Age if `or_equal` is True. False, if not.
        :rtype: bool
        """
        age = age
        sim_age = cls.get_age(sim_info)
        if or_equal:
            return sim_age >= age
        return sim_age > age

    @classmethod
    def is_baby_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_age(age)

        Determine if an Age is a Baby.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.BABY

    @classmethod
    def is_infant_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_infant_age(age)

        Determine if an Age is an Infant.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.INFANT

    @classmethod
    def is_toddler_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_toddler_age(age)

        Determine if an Age is a Toddler.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.TODDLER

    @classmethod
    def is_child_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_child_age(age)

        Determine if an Age is a Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.CHILD

    @classmethod
    def is_teen_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_age(age)

        Determine if an Age is a Teen.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.TEEN

    @classmethod
    def is_adult_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_adult_age(age)

        Determine if an Age is a Young Adult or an Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_young_adult_age(age) or cls.is_mature_adult_age(age)

    @classmethod
    def is_young_adult_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_young_adult_age(age)

        Determine if an Age is a Young Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.YOUNGADULT

    @classmethod
    def is_mature_adult_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_mature_adult_age(age)

        Determine if an Age is an Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.ADULT

    @classmethod
    def is_elder_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_elder_age(age)

        Determine if an Age is an Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        if isinstance(age, CommonAge):
            age = CommonAge.convert_to_vanilla(age)
        return age == Age.ELDER

    @classmethod
    def is_baby_or_toddler_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_or_toddler_age(age)

        Determine if an age is Baby or Toddler.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_baby_age(age) or cls.is_toddler_age(age)

    @classmethod
    def is_baby_infant_or_toddler_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_infant_or_toddler_age(age)

        Determine if an age is Baby or Toddler.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_baby_age(age) or cls.is_infant_age(age) or cls.is_toddler_age(age)

    @classmethod
    def is_baby_toddler_or_child_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_toddler_or_child_age(age)

        Determine if an age is Baby, Toddler, or Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_baby_age(age) or cls.is_toddler_age(age) or cls.is_child_age(age)

    @classmethod
    def is_baby_infant_toddler_or_child_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_infant_toddler_or_child_age(age)

        Determine if an age is Baby, Infant, Toddler, or Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_baby_age(age) or cls.is_infant_age(age) or cls.is_toddler_age(age) or cls.is_child_age(age)

    @classmethod
    def is_toddler_or_child_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_toddler_or_child_age(age)

        Determine if an age is Toddler or Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_toddler_age(age) or cls.is_child_age(age)

    @classmethod
    def is_child_or_teen_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_child_or_teen_age(age)

        Determine if an age is Child or Teen.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_child_age(age) or cls.is_teen_age(age)

    @classmethod
    def is_teen_or_young_adult_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_or_young_adult_age(age)

        Determine if an age is Teen or Young Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_teen_age(age) or cls.is_young_adult_age(age)

    @classmethod
    def is_teen_or_adult_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_or_adult_age(age)

        Determine if an age is Teen, Young Adult, or Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_teen_age(age) or cls.is_adult_age(age)

    @classmethod
    def is_teen_adult_or_elder_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_adult_or_elder_age(age)

        Determine if an age is Teen, Young Adult, Adult, or Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_teen_age(age) or cls.is_adult_age(age) or cls.is_elder_age(age)

    @classmethod
    def is_adult_or_elder_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_adult_or_elder_age(age)

        Determine if an age is Young Adult, Adult, or Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_adult_age(age) or cls.is_elder_age(age)

    @classmethod
    def is_mature_adult_or_elder_age(cls, age: Union[CommonAge, Age, int]) -> bool:
        """is_mature_adult_or_elder_age(age)

        Determine if an age is Adult or Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return cls.is_mature_adult_age(age) or cls.is_elder_age(age)

    @classmethod
    def is_baby(cls, sim_info: SimInfo) -> bool:
        """is_baby(sim_info)

        Determine if a Sim is a Baby.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_baby_age(cls.get_age(sim_info))

    @classmethod
    def is_infant(cls, sim_info: SimInfo) -> bool:
        """is_infant(sim_info)

        Determine if a Sim is an Infant.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_infant_age(cls.get_age(sim_info))

    @classmethod
    def is_toddler(cls, sim_info: SimInfo) -> bool:
        """is_toddler(sim_info)

        Determine if a Sim is a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_toddler_age(cls.get_age(sim_info))

    @classmethod
    def is_child(cls, sim_info: SimInfo) -> bool:
        """is_child(sim_info)

        Determine if a Sim is a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_child_age(cls.get_age(sim_info))

    @classmethod
    def is_teen(cls, sim_info: SimInfo) -> bool:
        """is_teen(sim_info)

        Determine if a Sim is a Teen.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_teen_age(cls.get_age(sim_info))

    @classmethod
    def is_young_adult(cls, sim_info: SimInfo) -> bool:
        """is_young_adult(sim_info)

        Determine if a Sim is a Young Adult.

        .. note:: This function does not determine whether they are an Adult or not. Use "is_adult" to check for both.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_young_adult_age(cls.get_age(sim_info))

    @classmethod
    def is_mature_adult(cls, sim_info: SimInfo) -> bool:
        """is_mature_adult(sim_info)

        Determine if a Sim is an Adult.

        .. note:: This function does not determine whether they are a Young Adult or not. Use 'is_adult' to check for both.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_mature_adult_age(cls.get_age(sim_info))

    @classmethod
    def is_elder(cls, sim_info: SimInfo) -> bool:
        """is_elder(sim_info)

        Determine if a Sim is an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_elder_age(cls.get_age(sim_info))

    @classmethod
    def is_adult(cls, sim_info: SimInfo) -> bool:
        """is_adult(sim_info)

        Determine if a Sim is either a Young Adult or an Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_adult_age(cls.get_age(sim_info))

    @classmethod
    def is_baby_or_toddler(cls, sim_info: SimInfo) -> bool:
        """is_baby_or_toddler(sim_info)

        Determine if a Sim is a Baby or a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_baby_or_toddler_age(cls.get_age(sim_info))

    @classmethod
    def is_baby_infant_or_toddler(cls, sim_info: SimInfo) -> bool:
        """is_baby_infant_or_toddler(sim_info)

        Determine if a Sim is a Baby, Infant, or a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_baby_infant_or_toddler_age(cls.get_age(sim_info))

    @classmethod
    def is_toddler_or_child(cls, sim_info: SimInfo) -> bool:
        """is_toddler_or_child(sim_info)

        Determine if a Sim is a Toddler or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_toddler_or_child_age(cls.get_age(sim_info))

    @classmethod
    def is_baby_toddler_or_child(cls, sim_info: SimInfo) -> bool:
        """is_baby_toddler_or_child(sim_info)

        Determine if a Sim is a Baby, a Toddler, or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_baby_toddler_or_child_age(cls.get_age(sim_info))

    @classmethod
    def is_baby_infant_toddler_or_child(cls, sim_info: SimInfo) -> bool:
        """is_baby_infant_toddler_or_child(sim_info)

        Determine if a Sim is a Baby, Infant, a Toddler, or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_baby_infant_toddler_or_child_age(cls.get_age(sim_info))

    @classmethod
    def is_child_or_teen(cls, sim_info: SimInfo) -> bool:
        """is_child_or_teen(sim_info)

        Determine if a Sim is a Child or a Teen.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_child_or_teen_age(cls.get_age(sim_info))

    @classmethod
    def is_teen_or_young_adult(cls, sim_info: SimInfo) -> bool:
        """is_teen_or_young_adult(sim_info)

        Determine if a Sim is a Teen or a Young Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_teen_or_young_adult_age(cls.get_age(sim_info))

    @classmethod
    def is_teen_or_adult(cls, sim_info: SimInfo) -> bool:
        """is_teen_or_adult(sim_info)

        Determine if a Sim is a Teen, a Young Adult, or an Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_teen_or_adult_age(cls.get_age(sim_info))

    @classmethod
    def is_teen_adult_or_elder(cls, sim_info: SimInfo) -> bool:
        """is_teen_adult_or_elder(sim_info)

        Determine if a Sim is a Teen, a Young Adult, an Adult, or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_teen_adult_or_elder_age(cls.get_age(sim_info))

    @classmethod
    def is_adult_or_elder(cls, sim_info: SimInfo) -> bool:
        """is_adult_or_elder(sim_info)

        Determine if a Sim is a Young Adult, an Adult, or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_adult_or_elder_age(cls.get_age(sim_info))

    @classmethod
    def is_mature_adult_or_elder(cls, sim_info: SimInfo) -> bool:
        """is_mature_adult_or_elder(sim_info)

        Determine if a Sim is an Adult or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return cls.is_mature_adult_or_elder_age(cls.get_age(sim_info))

    # Obsolete Functionality

    @classmethod
    def is_baby_child_or_toddler(cls, sim_info: SimInfo) -> bool:
        """is_baby_child_or_toddler(sim_info)

        .. warning:: Obsolete: Don't use this function. Use the :func:'~is_baby_toddler_or_child' function instead.

        """
        return cls.is_baby_toddler_or_child(sim_info)

    @classmethod
    def is_age_available_for_sim(cls, sim_info: SimInfo, age: CommonAge) -> bool:
        """is_age_available_for_sim(sim_info, age)

        Determine if an Age is available for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param age: The age to check.
        :type age: CommonAge
        :return: True, if the specified Age is available for the specified Sim. False, if not.
        :rtype: bool
        """
        if sim_info is None or age == CommonAge.INVALID:
            return False
        from sims.aging.aging_data import AgingData
        aging_data: AgingData = sim_info.get_aging_data()
        if aging_data is None:
            return False
        vanilla_age = CommonAge.convert_to_vanilla(age)
        if vanilla_age is None:
            return False
        # noinspection PyBroadException
        try:
            # noinspection PyUnresolvedReferences
            aging_data_ages = aging_data.ages
            return vanilla_age in aging_data_ages
        except:
            return False

    @classmethod
    def has_age(cls, sim_info: SimInfo, age: Union[CommonAge, Age, int], exact_age: bool = False) -> bool:
        """has_age(sim_info, age, exact_age=False)

        Determine if a Sim has a matching Age.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :param exact_age: If True, the Sims exact age will be used. If False, the Sims approximate age will be used. In most cases, this should be False. Default is False.
        :type exact_age: bool, optional
        :return: True, if the age of the specified Sim matches the specified age. False, if not.
        :rtype: bool
        """
        current_age = cls.get_age(sim_info, exact_age=exact_age)
        if current_age is None:
            return False
        return int(current_age) == int(age)

    @classmethod
    def has_any_age(cls, sim_info: SimInfo, ages: Iterator[Union[CommonAge, Age, int]], exact_age: bool = False) -> bool:
        """has_any_age(sim_info, ages, exact_age=False)

        Determine if a Sim has an Age matching any of the specified Ages.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param ages: The ages to check.
        :type ages: Iterator[Union[CommonAge, Age, int]]
        :param exact_age: If True, the Sims exact age will be used. If False, the Sims approximate age will be used. In most cases, this should be False. Default is False.
        :type exact_age: bool, optional
        :return: True, if the age of the specified Sim matches any of the specified ages. False, if not.
        :rtype: bool
        """
        current_age = cls.get_age(sim_info, exact_age=exact_age)
        if current_age is None:
            return False
        for age in ages:
            if int(current_age) == int(age):
                return True
        return False


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_age_progress_percentage',
    'Set the percentage of total days a Sim has been in their current age.',
    command_arguments=(
        CommonConsoleCommandArgument('progress_percentage', 'Decimal Percentage', 'The percentage of total days to set the Age Progress of the Sim. Values are 0.0 to 100.0'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.setageprogresspercentage',
    )
)
def _common_set_age_progress_percentage(output: CommonConsoleCommandOutput, progress_percentage: float, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    output(f'Attempting to set the age progress of {sim_info} to {progress_percentage}%')
    if CommonAgeUtils.set_percentage_total_days_sim_has_been_in_their_current_age(sim_info, progress_percentage):
        output(f'SUCCESS: Successfully set the age progress of Sim {sim_info} to {progress_percentage}%')
    else:
        output(f'FAILED: Failed to set the age progress of Sim {sim_info} to {progress_percentage}%')
    output(f'Done setting the age progress of Sim {sim_info} to {progress_percentage}%')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.randomize_age_progress',
    'Randomize the progress made towards the next age of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.randomizeageprogress',
    )
)
def _common_randomize_age_progress(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    progress = CommonAgeUtils.get_total_days_to_age_up(sim_info) * random.random()
    percentage_progress = (progress / CommonAgeUtils.get_total_days_to_age_up(sim_info)) * 100
    output(f'Attempting to randomize the age progress of {sim_info} to {percentage_progress}%')
    CommonAgeUtils.set_percentage_total_days_sim_has_been_in_their_current_age(sim_info, percentage_progress)
    output(f'Done randomizing the age progress of Sim {sim_info} to {percentage_progress}%')
    return True


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_age',
    'Set the age of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('age', 'CommonAge', f'The age to set the Sim to. Valid Ages: {CommonAge.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.setage',
    )
)
def _common_set_age(output: CommonConsoleCommandOutput, age: CommonAge, sim_info: SimInfo = None):
    if age is None:
        return
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    age_name = age.name
    output(f'Setting the age of {sim_info} to {age_name}')
    if CommonAgeUtils.set_age(sim_info, age):
        output(f'SUCCESS: Successfully set the age of Sim {sim_info} to {age_name}')
    else:
        output(f'FAILED: Failed to set the age of Sim {sim_info} to {age_name}')
    output(f'Done setting the age of Sim {sim_info} to {age_name}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_sim_age',
    'Print information about the Age of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printsimage',
    )
)
def _common_print_sim_age(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    output(f'Attempting to print Age Info for Sim {sim_info}.')
    if hasattr(sim_info, '_base') and hasattr(sim_info._base, 'age'):
        output(f'_base.age {sim_info._base.age}')
    if hasattr(sim_info, 'age'):
        # noinspection PyPropertyAccess
        output(f'age {sim_info.age}')
    if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age'):
        output(f'sim_info._base.age {sim_info.sim_info._base.age}')
    if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'age'):
        output(f'sim_info.age {sim_info.sim_info.age}')
    get_age_result = CommonAgeUtils.get_age(sim_info)
    output(f'Approximate Age: {get_age_result}')
    get_age_exact_result = CommonAgeUtils.get_age(sim_info, exact_age=True)
    output(f'Exact Age: {get_age_exact_result}')
    total_days_has_been_in_current_age = CommonAgeUtils.get_total_days_sim_has_been_in_their_current_age(sim_info)
    output(f'Age Progress: {total_days_has_been_in_current_age}')
    percentage_total_days_sim_has_been_in_current_age = CommonAgeUtils.get_percentage_total_days_sim_has_been_in_their_current_age(sim_info)
    output(f'Age Progress (In Days): {percentage_total_days_sim_has_been_in_current_age}')
    total_days_until_sim_ages_up = CommonAgeUtils.get_total_days_until_sim_ages_up(sim_info)
    output(f'Days Until Ready To Age: {total_days_until_sim_ages_up}')
    total_days_to_age_up = CommonAgeUtils.get_total_days_to_age_up(sim_info)
    output(f'Max Total Days To Age Up: {total_days_to_age_up}')
    output(f'Done printing Age Info for Sim {sim_info}.')
