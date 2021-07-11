"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Union

import services
from event_testing.test_events import TestEvent
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.common_age import CommonAge


class CommonAgeUtils:
    """Utilities for manipulating Ages of Sims.

    """
    @staticmethod
    def get_age(sim_info: SimInfo, exact_age: bool=False) -> Union[Age, int, None]:
        """get_age(sim_info, exact_age=False)

        Retrieve the Age of a Sim.

        :param sim_info: The Sim to get the Age of.
        :type sim_info: SimInfo
        :param exact_age: If set to True, the exact age of the Sim will be returned (Age 24 will be returned as 24). If set to False, the age of the Sim rounded to the nearest Age value will be returned. (Age 24 will be returned as Age.YOUNGADULT) Default is False.
        :type exact_age: bool, optional
        :return: The Age of the Sim or None if a problem occurs.
        :rtype: Union[Age, None]
        """
        if sim_info is None:
            return None
        age: Age = None
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age') and exact_age:
            age = sim_info.sim_info._base.age
        elif hasattr(sim_info, '_base') and hasattr(sim_info._base, 'age'):
            age = sim_info._base.age
        elif hasattr(sim_info, 'age'):
            # noinspection PyPropertyAccess
            age = sim_info.age
        elif hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age') and exact_age:
            age = sim_info.sim_info._base.age
        elif hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'age'):
            age = sim_info.sim_info.age
        if age is None:
            return None
        if exact_age:
            return age
        return CommonAgeUtils.convert_to_approximate_age(age)

    @staticmethod
    def convert_to_approximate_age(age: Union[CommonAge, Age, int]) -> Age:
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
        if int(Age.BABY) <= age < int(Age.TODDLER):
            return Age.BABY
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
        return Age.ELDER

    @staticmethod
    def set_age(sim_info: SimInfo, age: Union[CommonAge, Age, int]) -> bool:
        """set_age(sim_info, age)

        Set the Age of a Sim.

        :param sim_info: The Sim to set the Age of.
        :type sim_info: SimInfo
        :param age: The Age to set the Sim to.
        :type age: Union[CommonAge, Age, int]
        :return: True, if the Age was set successfully. False, if not.
        :rtype: bool
        """
        age = CommonAgeUtils.convert_to_approximate_age(age)
        if age is None:
            return False
        current_age = CommonAgeUtils.get_age(sim_info, exact_age=False)
        approximate_age = CommonAgeUtils.convert_to_approximate_age(age)
        if current_age is None:
            return False
        if current_age == approximate_age:
            return True
        sim_info._relationship_tracker.update_bits_on_age_up(current_age)
        sim_info.change_age(age, current_age)
        services.get_event_manager().process_event(TestEvent.AgedUp, sim_info=sim_info)
        school_data = sim_info.get_school_data()
        if school_data is not None:
            school_data.update_school_data(sim_info, create_homework=True)
        if sim_info.is_npc:
            if sim_info.is_child or sim_info.is_teen:
                available_aspirations = []
                aspiration_track_manager = services.get_instance_manager(Types.ASPIRATION_TRACK)
                aspiration_tracker = sim_info.aspiration_tracker
                for aspiration_track in aspiration_track_manager.types.values():
                    track_available = not aspiration_track.is_hidden_unlockable
                    if aspiration_tracker is not None:
                        track_available = aspiration_tracker.is_aspiration_track_visible(aspiration_track)
                    if track_available:
                        if sim_info.is_child and aspiration_track.is_child_aspiration_track:
                            available_aspirations.append(aspiration_track)
                        elif sim_info.is_teen:
                            available_aspirations.append(aspiration_track)
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
        return CommonAgeUtils.get_age(sim_info) == age

    @staticmethod
    def are_same_age(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_age(sim_info, other_sim_info)

        Determine if two Sims are the same Age.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The other Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Age.
        :rtype: bool
        """
        return int(CommonAgeUtils.get_age(sim_info)) == int(CommonAgeUtils.get_age(other_sim_info))

    @staticmethod
    def is_younger_than(sim_info: SimInfo, age: Union[CommonAge, Age, int], or_equal: bool=False) -> bool:
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
        sim_age = int(CommonAgeUtils.get_age(sim_info))
        if or_equal:
            return sim_age <= age
        return sim_age < age

    @staticmethod
    def is_older_than(sim_info: SimInfo, age: Union[CommonAge, Age, int], or_equal: bool=False) -> bool:
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
        age = int(age)
        sim_age = int(CommonAgeUtils.get_age(sim_info))
        if or_equal:
            return sim_age >= age
        return sim_age > age

    @staticmethod
    def is_baby_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_age(age)

        Determine if an Age is a Baby.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.BABY)

    @staticmethod
    def is_toddler_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_toddler_age(age)

        Determine if an Age is a Toddler.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.TODDLER)

    @staticmethod
    def is_child_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_child_age(age)

        Determine if an Age is a Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.CHILD)

    @staticmethod
    def is_teen_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_age(age)

        Determine if an Age is a Teen.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.TEEN)

    @staticmethod
    def is_adult_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_adult_age(age)

        Determine if an Age is a Young Adult or an Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_young_adult_age(age) or CommonAgeUtils.is_mature_adult_age(age)

    @staticmethod
    def is_young_adult_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_young_adult_age(age)

        Determine if an Age is a Young Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.YOUNGADULT)

    @staticmethod
    def is_mature_adult_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_mature_adult_age(age)

        Determine if an Age is an Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.ADULT)

    @staticmethod
    def is_elder_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_elder_age(age)

        Determine if an Age is an Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        if age is None:
            return False
        return int(age) == int(Age.ELDER)

    @staticmethod
    def is_baby_or_toddler_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_or_toddler_age(age)

        Determine if an age is Baby or Toddler.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_age(age) or CommonAgeUtils.is_toddler_age(age)

    @staticmethod
    def is_baby_toddler_or_child_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_baby_toddler_or_child_age(age)

        Determine if an age is Baby, Toddler, or Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_age(age) or CommonAgeUtils.is_toddler_age(age) or CommonAgeUtils.is_child_age(age)

    @staticmethod
    def is_toddler_or_child_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_toddler_or_child_age(age)

        Determine if an age is Toddler or Child.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_age(age) or CommonAgeUtils.is_child_age(age)

    @staticmethod
    def is_child_or_teen_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_child_or_teen_age(age)

        Determine if an age is Child or Teen.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_age(age) or CommonAgeUtils.is_teen_age(age)

    @staticmethod
    def is_teen_or_young_adult_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_or_young_adult_age(age)

        Determine if an age is Teen or Young Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(age) or CommonAgeUtils.is_young_adult_age(age)

    @staticmethod
    def is_teen_or_adult_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_or_adult_age(age)

        Determine if an age is Teen, Young Adult, or Adult.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(age) or CommonAgeUtils.is_adult_age(age)

    @staticmethod
    def is_teen_adult_or_elder_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_teen_adult_or_elder_age(age)

        Determine if an age is Teen, Young Adult, Adult, or Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(age) or CommonAgeUtils.is_adult_age(age) or CommonAgeUtils.is_elder_age(age)

    @staticmethod
    def is_adult_or_elder_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_adult_or_elder_age(age)

        Determine if an age is Young Adult, Adult, or Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_age(age) or CommonAgeUtils.is_elder_age(age)

    @staticmethod
    def is_mature_adult_or_elder_age(age: Union[CommonAge, Age, int]) -> bool:
        """is_mature_adult_or_elder_age(age)

        Determine if an age is Adult or Elder.

        :param age: The age to check.
        :type age: Union[CommonAge, Age, int]
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_age(age) or CommonAgeUtils.is_elder_age(age)

    @staticmethod
    def is_baby(sim_info: SimInfo) -> bool:
        """is_baby(sim_info)

        Determine if a sim is a Baby.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_toddler(sim_info: SimInfo) -> bool:
        """is_toddler(sim_info)

        Determine if a sim is a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_child(sim_info: SimInfo) -> bool:
        """is_child(sim_info)

        Determine if a sim is a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen(sim_info: SimInfo) -> bool:
        """is_teen(sim_info)

        Determine if a sim is a Teen.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_young_adult(sim_info: SimInfo) -> bool:
        """is_young_adult(sim_info)

        Determine if a sim is an Young Adult.

        .. note:: This function does not determine whether they are an Adult or not. Use "is_adult" to check for both.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_young_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_mature_adult(sim_info: SimInfo) -> bool:
        """is_mature_adult(sim_info)

        Determine if a sim is an Adult.

        .. note:: This function does not determine whether they are a Young Adult or not. Use 'is_adult' to check for both.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_elder(sim_info: SimInfo) -> bool:
        """is_elder(sim_info)

        Determine if a sim is an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_adult(sim_info: SimInfo) -> bool:
        """is_adult(sim_info)

        Determine if a sim is either a Young Adult or an Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_baby_or_toddler(sim_info: SimInfo) -> bool:
        """is_baby_or_toddler(sim_info)

        Determine if a sim is a Baby or a Toddler.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_or_toddler_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_toddler_or_child(sim_info: SimInfo) -> bool:
        """is_toddler_or_child(sim_info)

        Determine if a sim is a Toddler or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_toddler_or_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_baby_toddler_or_child(sim_info: SimInfo) -> bool:
        """is_baby_toddler_or_child(sim_info)

        Determine if a sim is a Baby, a Toddler, or a Child.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_baby_toddler_or_child_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_child_or_teen(sim_info: SimInfo) -> bool:
        """is_child_or_teen(sim_info)

        Determine if a sim is a Child or a Teen.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_child_or_teen_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen_or_young_adult(sim_info: SimInfo) -> bool:
        """is_teen_or_young_adult(sim_info)

        Determine if a sim is a Teen or a Young Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_or_young_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen_or_adult(sim_info: SimInfo) -> bool:
        """is_teen_or_adult(sim_info)

        Determine if a sim is a Teen, a Young Adult, or an Adult.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_or_adult_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_teen_adult_or_elder(sim_info: SimInfo) -> bool:
        """is_teen_adult_or_elder(sim_info)

        Determine if a sim is a Teen, a Young Adult, an Adult, or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_teen_adult_or_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_adult_or_elder(sim_info: SimInfo) -> bool:
        """is_adult_or_elder(sim_info)

        Determine if a sim is a Young Adult, an Adult, or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_adult_or_elder_age(CommonAgeUtils.get_age(sim_info))

    @staticmethod
    def is_mature_adult_or_elder(sim_info: SimInfo) -> bool:
        """is_mature_adult_or_elder(sim_info)

        Determine if a sim is an Adult or an Elder.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is. False, if the Sim is not.
        :rtype: bool
        """
        return CommonAgeUtils.is_mature_adult_or_elder_age(CommonAgeUtils.get_age(sim_info))

    # Obsolete Functionality

    @staticmethod
    def is_baby_child_or_toddler(sim_info: SimInfo) -> bool:
        """is_baby_child_or_toddler(sim_info)

        .. warning:: Obsolete: Don't use this function. Use the :func:'~is_baby_toddler_or_child' function instead.

        """
        return CommonAgeUtils.is_baby_toddler_or_child(sim_info)


@Command('s4clib.show_sim_age', command_type=CommandType.Live)
def _s4clib_show_sim_age(_connection: int=None):
    output = CheatOutput(_connection)
    output('Showing Sim age.')
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    sim_info = CommonSimUtils.get_active_sim_info()
    if hasattr(sim_info, '_base') and hasattr(sim_info._base, 'age'):
        output('_base.age {}'.format(sim_info._base.age))
    if hasattr(sim_info, 'age'):
        # noinspection PyPropertyAccess
        output('age {}'.format(sim_info.age))
    if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, '_base') and hasattr(sim_info.sim_info._base, 'age'):
        output('sim_info._base.age {}'.format(sim_info.sim_info._base.age))
    if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'age'):
        output('sim_info.age {}'.format(sim_info.sim_info.age))
    get_age_result = CommonAgeUtils.get_age(sim_info)
    output('Get Age Result: {}'.format(get_age_result))
    get_age_exact_result = CommonAgeUtils.get_age(sim_info, exact_age=True)
    output('Get Age Exact Result: {}'.format(get_age_exact_result))
    output('Done showing Sim age.')
