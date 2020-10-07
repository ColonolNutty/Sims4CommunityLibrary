"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils


class CommonSimGenderPreferenceUtils:
    """ Utilities for Sim gender preferences. """
    LOW_PREFERENCE_THRESHOLD = 5
    HIGH_PREFERENCE_THRESHOLD = 20

    @staticmethod
    def set_gender_preference_amount(sim_info: SimInfo, gender: Gender, amount: int) -> bool:
        """set_gender_preference_amount(sim_info, gender, amount)

        Set the amount a Sim prefers the specified Gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: A Gender.
        :type gender: Gender
        :param amount: The amount the Sim prefers the specified Gender.
        :type amount: int
        :return: True, if successfully set. False, it not.
        :rtype: bool
        """
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.STATISTIC):
            return False
        gender_preference = sim_info.get_gender_preference(gender)
        if gender_preference is None:
            return False
        gender_preference.set_value(amount)
        return True

    @staticmethod
    def get_gender_preference_amount(sim_info: SimInfo, gender: Gender) -> int:
        """get_gender_preference_value(sim_info, gender)

        Retrieve the amount a Sim prefers the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: A Gender.
        :type gender: Gender
        :return: The amount the Sim prefers the specified Gender.
        :rtype: int
        """
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.STATISTIC):
            return 0
        gender_preference = sim_info.get_gender_preference(gender)
        if gender_preference is None:
            return 0
        return gender_preference.get_value()

    @staticmethod
    def get_default_preferred_genders(sim_info: SimInfo) -> Tuple[Gender]:
        """get_default_preferred_genders(sim_info)

        Retrieve a collection of default gender preferences.

        .. note:: By default Male Sims prefer Female Sims and Female Sims prefer Male Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A collection of preferred Genders.
        :rtype: Tuple[Gender]
        """
        if CommonGenderUtils.is_male(sim_info):
            return Gender.FEMALE,
        return Gender.MALE,

    @staticmethod
    def has_preference_for_gender(sim_info: SimInfo, gender: Gender, like_threshold: int=None, love_threshold: int=None) -> bool:
        """has_preference_for_gender(sim_info, gender, like_threshold=None, love_threshold=None)

        Determine if a Sim has a preference for the specified Gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: A Gender.
        :type gender: Gender
        :param like_threshold: A value indicating a low amount of preference. Default is CommonSimGenderPreferenceUtils.LOW_PREFERENCE_THRESHOLD.
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is CommonSimGenderPreferenceUtils.HIGH_PREFERENCE_THRESHOLD.
        :type love_threshold: int, optional
        :return: True, if the Sim has a preference for the Gender. False, if not.
        :rtype: bool
        """
        preferences = CommonSimGenderPreferenceUtils.determine_preferred_genders(
            sim_info,
            like_threshold=like_threshold,
            love_threshold=love_threshold
        )
        return gender in preferences

    @staticmethod
    def has_preference_for(sim_info: SimInfo, target_sim_info: SimInfo, like_threshold: int=None, love_threshold: int=None) -> bool:
        """has_preference_for(sim_info, target_sim_info, like_threshold=None, love_threshold=None)

        Determine if a Sim has a preference for another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param target_sim_info: An instance of a Sim.
        :type target_sim_info: SimInfo
        :param like_threshold: A value indicating a low amount of preference. Default is CommonSimGenderPreferenceUtils.LOW_PREFERENCE_THRESHOLD.
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is CommonSimGenderPreferenceUtils.HIGH_PREFERENCE_THRESHOLD.
        :type love_threshold: int, optional
        :return: True, if the Sim has a preference for the Gender. False, if not.
        :rtype: bool
        """
        return CommonSimGenderPreferenceUtils.has_preference_for_gender(
            sim_info,
            CommonGenderUtils.get_gender(target_sim_info),
            like_threshold=like_threshold,
            love_threshold=love_threshold
        )

    @classmethod
    def determine_preferred_genders(cls, sim_info: SimInfo, like_threshold: int=None, love_threshold: int=None) -> Tuple[Gender]:
        """determine_preferred_genders(sim_info, like_threshold=None, love_threshold=None)

        Determine which genders a Sim prefers.

        .. note::

            The math is as follows (The first match will return):

            - Default Gender Preferences = MALE_PREF < like_threshold and FEMALE_PREF < like_threshold
            - Prefers both Genders = absolute(MALE_PREF - FEMALE_PREF) <= love_threshold
            - Prefers Male = MALE_PREF > FEMALE_PREF
            - Prefers Female = FEMALE_PREF > MALE_PREF

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param like_threshold: A value indicating a low amount of preference. Default is cls.LOW_PREFERENCE_THRESHOLD.
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is cls.HIGH_PREFERENCE_THRESHOLD.
        :type love_threshold: int, optional
        :return: A collection of Genders the specified Sim prefers.
        :rtype: Tuple[Gender]
        """
        if like_threshold is None:
            like_threshold = cls.LOW_PREFERENCE_THRESHOLD
        if love_threshold is None:
            love_threshold = cls.HIGH_PREFERENCE_THRESHOLD
        male_preference = CommonSimGenderPreferenceUtils.get_gender_preference_amount(sim_info, Gender.MALE)
        female_preference = CommonSimGenderPreferenceUtils.get_gender_preference_amount(sim_info, Gender.FEMALE)
        if male_preference == female_preference and male_preference > 0:
            result: Tuple[Gender] = (Gender.MALE, Gender.FEMALE)
            return result
        if male_preference < like_threshold and female_preference < like_threshold:
            return CommonSimGenderPreferenceUtils.get_default_preferred_genders(sim_info)
        if abs(male_preference - female_preference) <= love_threshold:
            result: Tuple[Gender] = (Gender.MALE, Gender.FEMALE)
            return result
        if male_preference > female_preference:
            return Gender.MALE,
        return Gender.FEMALE,
