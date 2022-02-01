"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimGenderPreferenceUtils:
    """ Utilities for Sim gender preferences. """
    LOW_PREFERENCE_THRESHOLD = 20
    HIGH_PREFERENCE_THRESHOLD = 80

    @staticmethod
    def set_gender_preference_amount(sim_info: SimInfo, gender: CommonGender, amount: int) -> bool:
        """set_gender_preference_amount(sim_info, gender, amount)

        Set the amount a Sim prefers the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a gender.
        :type gender: CommonGender
        :param amount: The amount the Sim prefers the specified gender.
        :type amount: int
        :return: True, if successfully set. False, it not.
        :rtype: bool
        """
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.STATISTIC):
            return False
        gender = CommonGender.convert_to_vanilla(gender)
        if gender is None:
            return False
        gender_preference = sim_info.get_gender_preference(gender)
        if gender_preference is None:
            return False
        gender_preference.set_value(amount)
        return True

    @staticmethod
    def get_gender_preference_amount(sim_info: SimInfo, gender: CommonGender) -> int:
        """get_gender_preference_value(sim_info, gender)

        Retrieve the amount a Sim prefers the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a gender.
        :type gender: CommonGender
        :return: The amount the Sim prefers the specified gender.
        :rtype: int
        """
        if not CommonComponentUtils.has_component(sim_info, CommonComponentType.STATISTIC):
            return 0
        gender = CommonGender.convert_to_vanilla(gender)
        if gender is None:
            return False
        gender_preference = sim_info.get_gender_preference(gender)
        if gender_preference is None:
            return 0
        return gender_preference.get_value()

    @staticmethod
    def get_default_preferred_genders(sim_info: SimInfo) -> Tuple[CommonGender]:
        """get_default_preferred_genders(sim_info)

        Retrieve a collection of default gender preferences.

        .. note:: By default Male Sims prefer Female Sims and Female Sims prefer Male Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A collection of the default preferred genders.
        :rtype: Tuple[CommonGender]
        """
        from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
        if CommonGenderUtils.is_male(sim_info):
            return CommonGender.FEMALE,
        return CommonGender.MALE,

    @staticmethod
    def has_preference_for_gender(sim_info: SimInfo, gender: CommonGender, like_threshold: int=None, love_threshold: int=None) -> bool:
        """has_preference_for_gender(sim_info, gender, like_threshold=None, love_threshold=None)

        Determine if a Sim has a preference for the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a CommonGender.
        :type gender: CommonGender
        :param like_threshold: A value indicating a low amount of preference. Default is CommonSimGenderPreferenceUtils.LOW_PREFERENCE_THRESHOLD.
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is CommonSimGenderPreferenceUtils.HIGH_PREFERENCE_THRESHOLD.
        :type love_threshold: int, optional
        :return: True, if the Sim has a preference for the specified gender. False, if not.
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
        :return: True, if the Source Sim has a preference for the Target Sim. False, if not.
        :rtype: bool
        """
        return CommonSimGenderPreferenceUtils.has_preference_for_gender(
            sim_info,
            CommonGender.get_gender(target_sim_info),
            like_threshold=like_threshold,
            love_threshold=love_threshold
        )

    @classmethod
    def determine_preferred_genders(cls, sim_info: SimInfo, like_threshold: int=None, love_threshold: int=None) -> Tuple[CommonGender]:
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
        :return: A collection of CommonGenders the specified Sim prefers.
        :rtype: Tuple[CommonGender]
        """
        if like_threshold is None:
            like_threshold = cls.LOW_PREFERENCE_THRESHOLD
        if love_threshold is None:
            love_threshold = cls.HIGH_PREFERENCE_THRESHOLD
        male_preference = CommonSimGenderPreferenceUtils.get_gender_preference_amount(sim_info, CommonGender.MALE)
        female_preference = CommonSimGenderPreferenceUtils.get_gender_preference_amount(sim_info, CommonGender.FEMALE)
        if male_preference == female_preference and male_preference > 0:
            result: Tuple[CommonGender] = (CommonGender.MALE, CommonGender.FEMALE)
            return result
        if male_preference < like_threshold and female_preference < like_threshold:
            return CommonSimGenderPreferenceUtils.get_default_preferred_genders(sim_info)
        if abs(male_preference - female_preference) <= love_threshold:
            result: Tuple[CommonGender] = (CommonGender.MALE, CommonGender.FEMALE)
            return result
        if male_preference > female_preference:
            return CommonGender.MALE,
        return CommonGender.FEMALE,


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref',
    'Set the gender preference amount of a Sim towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preference of the Sim for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('percentage', 'Number', 'The percentage of preference between 0 and 100 for the gender.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.setgenderpref',
        's4clib.set_gender_preference',
        's4clib.setgenderpreference',
    )
)
def _common_set_gender_pref(output: CommonConsoleCommandOutput, gender: CommonGender, percentage_amount: int, sim_info: SimInfo=None):
    if gender is None:
        return
    if sim_info is None:
        return
    if percentage_amount is None:
        return
    if percentage_amount > 100 or percentage_amount < 0:
        output('ERROR: Please specify a percentage between 0 and 100.')
        return
    gender_name = gender.name
    output(f'Attempting to set the gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%')
    if CommonSimGenderPreferenceUtils.set_gender_preference_amount(sim_info, gender, percentage_amount):
        output(f'SUCCESS: Successfully set the gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%')
    else:
        output(f'FAILED: Failed to set the gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref_of_all_sims',
    'Set the gender preference amount of all Sims towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preferences of the Sims for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('percentage', 'Number', 'The percentage of preference between 0 and 100 for the gender.')
    ),
    command_aliases=(
        's4clib.setgenderprefofallsims',
        's4clib.setgenderpreferenceofallsims',
        's4clib.set_gender_preference_of_all_sims',
        's4clib.set_all_gender_preferences',
        's4clib.setallgenderpreferences',
    )
)
def _common_set_gender_pref_of_all_sims(output: CommonConsoleCommandOutput, gender: CommonGender, percentage_amount: int):
    if gender is None:
        return
    if percentage_amount is None:
        return
    if percentage_amount > 100 or percentage_amount < 0:
        output('ERROR: Please specify a percentage between 0 and 100.')
        return
    gender_name = gender.name
    count_of_sims_changed = 0
    output(f'Setting gender preference of all Sims for gender {gender_name} to {percentage_amount}%')
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        try:
            if CommonSimGenderPreferenceUtils.set_gender_preference_amount(sim_info, gender, percentage_amount):
                count_of_sims_changed += 1
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Failed to set gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%', exception=ex)
            output(f'ERROR: Failed to set gender preference of Sim {sim_info} for gender {gender} to {percentage_amount}%. Exception: {ex}')
    output(f'Updated the Gender Preferences of {count_of_sims_changed} Sims.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref_of_all_female_sims',
    'Set the gender preference amount of all Female Sims towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preferences of the Sims for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('percentage', 'Number', 'The percentage of preference between 0 and 100 for the gender.')
    ),
    command_aliases=(
        's4clib.setgenderprefofallfemalesims',
        's4clib.setgenderpreferenceofallfemalesims',
        's4clib.set_gender_preference_of_all_female_sims',
        's4clib.set_all_female_gender_preferences',
        's4clib.setallfemalegenderpreferences',
    )
)
def _common_set_gender_pref_of_all_female_sims(output: CommonConsoleCommandOutput, gender: CommonGender, percentage_amount: int):
    if gender is None:
        return
    if percentage_amount is None:
        return
    if percentage_amount > 100 or percentage_amount < 0:
        output('ERROR: Please specify a percentage between 0 and 100.')
        return
    gender_name = gender.name
    sim_count = 0
    output(f'Setting gender preference of all Female Sims for gender {gender_name} to {percentage_amount}%')
    from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonGenderUtils.is_female):
        try:
            if CommonSimGenderPreferenceUtils.set_gender_preference_amount(sim_info, gender, percentage_amount):
                sim_count += 1
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Failed to set gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%.', exception=ex)
            output(f'Failed to set gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%. Exception: {ex}')
    output(f'Updated Gender Preferences of {sim_count} Sims.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref_of_all_male_sims',
    'Set the gender preference amount of all Male Sims towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preferences of the Sims for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('percentage', 'Number', 'The percentage of preference between 0 and 100 for the gender.')
    ),
    command_aliases=(
        's4clib.setgenderprefofallmalesims',
        's4clib.setgenderpreferenceofallmalesims',
        's4clib.set_gender_preference_of_all_male_sims',
        's4clib.set_all_male_gender_preferences',
        's4clib.setallmalegenderpreferences',
    )
)
def _common_set_gender_pref_of_all_male_sims(output: CommonConsoleCommandOutput, gender: CommonGender, percentage_amount: int):
    if gender is None:
        return
    if percentage_amount is None:
        return
    if percentage_amount > 100 or percentage_amount < 0:
        output('ERROR: Please specify a percentage between 0 and 100.')
        return
    gender_name = gender.name
    sim_count = 0
    output(f'Setting gender preference of all Male Sims for gender {gender_name} to {percentage_amount}%')
    from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonGenderUtils.is_male):
        try:
            if CommonSimGenderPreferenceUtils.set_gender_preference_amount(sim_info, gender, percentage_amount):
                sim_count += 1
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Failed to set gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%.', exception=ex)
            output(f'Failed to set gender preference of Sim {sim_info} for gender {gender_name} to {percentage_amount}%. Exception: {ex}')
    output(f'Updated Gender Preferences of {sim_count} Sims.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_gender_pref',
    'Print the gender preference amount a Sim has towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preference of the Sim for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printgenderpref',
        's4clib.print_gender_preference',
        's4clib.printgenderpreference',
    )
)
def _common_get_gender_pref(output: CommonConsoleCommandOutput, gender: CommonGender, sim_info: SimInfo=None):
    if gender is None:
        return
    if sim_info is None:
        return
    gender_name = gender.name
    preference_percentage_amount = CommonSimGenderPreferenceUtils.get_gender_preference_amount(sim_info, gender)
    output(f'{sim_info} has a {preference_percentage_amount}% preference for gender {gender_name}')
