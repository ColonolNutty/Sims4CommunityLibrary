"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from sims.global_gender_preference_tuning import GlobalGenderPreferenceTuning, GenderPreferenceType
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_gender_preference_type import CommonGenderPreferenceType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CommonSimGenderPreferenceUtils:
    """ Utilities for Sim gender preferences. """
    LOW_PREFERENCE_THRESHOLD = 20
    HIGH_PREFERENCE_THRESHOLD = 80

    @classmethod
    def set_preference_for_gender(cls, sim_info: SimInfo, gender: CommonGender, is_attracted_to_gender: Union[bool, None], preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType] = CommonGenderPreferenceType.ROMANTIC) -> CommonExecutionResult:
        """set_preference_for_gender(sim_info, gender, is_attracted_to_gender, preference_type=CommonGenderPreferenceType.ROMANTIC)

        Set the preference a Sim has for a gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a gender.
        :type gender: CommonGender
        :param is_attracted_to_gender: True, if you want the Sim to be attracted to the gender. False, if you want the Sim to NOT be attracted to the gender. None, if you want the Sim to have no preferences.
        :type is_attracted_to_gender: Union[bool, None]
        :param preference_type: The type of preference to use. Default is CommonGenderPreferenceType.ROMANTIC.
        :type preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType], optional
        :return: True, if successfully set. False, it not.
        :rtype: CommonExecutionResult
        """
        if preference_type == CommonGenderPreferenceType.ROMANTIC or preference_type == GenderPreferenceType.ROMANTIC:
            attraction_traits_map = GlobalGenderPreferenceTuning.ROMANTIC_PREFERENCE_TRAITS_MAPPING
        else:
            attraction_traits_map = GlobalGenderPreferenceTuning.WOOHOO_PREFERENCE_TRAITS_MAPPING
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        if preference_type == CommonGenderPreferenceType.ROMANTIC or preference_type == GenderPreferenceType.ROMANTIC:
            gender_preference_stat_type = GlobalGenderPreferenceTuning.GENDER_PREFERENCE.get(vanilla_gender)
            if is_attracted_to_gender:
                new_value = gender_preference_stat_type.max_value
            else:
                new_value = gender_preference_stat_type.min_value
            sim_info.set_stat_value(gender_preference_stat_type, new_value)

        if is_attracted_to_gender is None:
            traits_to_remove = (
                attraction_traits_map[vanilla_gender].not_attracted_trait,
                attraction_traits_map[vanilla_gender].is_attracted_trait
            )
            return CommonTraitUtils.remove_traits(sim_info, traits_to_remove)

        if is_attracted_to_gender:
            trait_to_remove = attraction_traits_map[vanilla_gender].not_attracted_trait
            trait_to_add = attraction_traits_map[vanilla_gender].is_attracted_trait
        else:
            trait_to_remove = attraction_traits_map[vanilla_gender].is_attracted_trait
            trait_to_add = attraction_traits_map[vanilla_gender].not_attracted_trait
        remove_result = CommonTraitUtils.remove_trait(sim_info, trait_to_remove)
        if not remove_result:
            return remove_result
        add_result = CommonTraitUtils.add_trait(sim_info, trait_to_add)
        if not add_result:
            return add_result
        return CommonExecutionResult.TRUE

    @classmethod
    def set_gender_preference_amount(cls, sim_info: SimInfo, gender: CommonGender, amount: int, preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType] = CommonGenderPreferenceType.ROMANTIC) -> bool:
        """set_gender_preference_amount(sim_info, gender, amount, preference_type=CommonGenderPreferenceType.ROMANTIC)

        Set the amount a Sim prefers the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a gender.
        :type gender: CommonGender
        :param amount: The amount the Sim prefers the specified gender.
        :type amount: int
        :param preference_type: The type of preference to use. Default is CommonGenderPreferenceType.ROMANTIC.
        :type preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType], optional
        :return: True, if successfully set. False, it not.
        :rtype: bool
        """
        if amount > 0:
            is_attracted_to_gender = True
        elif amount < 0:
            is_attracted_to_gender = False
        else:
            is_attracted_to_gender = None
        if cls.set_preference_for_gender(sim_info, gender, is_attracted_to_gender, preference_type=preference_type):
            return True
        return False

    @classmethod
    def get_gender_preference_amount(cls, sim_info: SimInfo, gender: CommonGender, preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType] = CommonGenderPreferenceType.ROMANTIC) -> int:
        """get_gender_preference_value(sim_info, gender, preference_type=CommonGenderPreferenceType.ROMANTIC)

        Retrieve the amount a Sim prefers the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a gender.
        :type gender: CommonGender
        :param preference_type: The type of preference to use. Default is CommonGenderPreferenceType.ROMANTIC.
        :type preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType], optional
        :return: The amount the Sim prefers the specified gender.
        :rtype: int
        """
        if cls.has_preference_for_gender(sim_info, gender, preference_type=preference_type):
            return 100
        return 0

    @classmethod
    def get_default_preferred_genders(cls, sim_info: SimInfo) -> Tuple[CommonGender]:
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

    @classmethod
    def has_preference_for_gender(cls, sim_info: SimInfo, gender: CommonGender, like_threshold: int = None, love_threshold: int = None, preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType] = CommonGenderPreferenceType.ROMANTIC) -> bool:
        """has_preference_for_gender(sim_info, gender, like_threshold=None, love_threshold=None, preference_type=CommonGenderPreferenceType.ROMANTIC)

        Determine if a Sim has a preference for the specified gender.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param gender: An instance of a CommonGender.
        :type gender: CommonGender
        :param like_threshold: A value indicating a low amount of preference. Default is CommonSimGenderPreferenceUtils.LOW_PREFERENCE_THRESHOLD. (This argument is obsolete, do not use)
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is CommonSimGenderPreferenceUtils.HIGH_PREFERENCE_THRESHOLD. (This argument is obsolete, do not use)
        :type love_threshold: int, optional
        :param preference_type: The type of preference to use. Default is CommonGenderPreferenceType.ROMANTIC.
        :type preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType], optional
        :return: True, if the Sim has a preference for the specified gender. False, if not.
        :rtype: bool
        """
        preferences = cls.determine_preferred_genders(
            sim_info,
            like_threshold=like_threshold,
            love_threshold=love_threshold,
            preference_type=preference_type,
        )
        return gender in preferences

    @classmethod
    def has_preference_for(cls, sim_info: SimInfo, target_sim_info: SimInfo, like_threshold: int = None, love_threshold: int = None, preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType] = CommonGenderPreferenceType.ROMANTIC) -> bool:
        """has_preference_for(sim_info, target_sim_info, like_threshold=None, love_threshold=None, preference_type=CommonGenderPreferenceType.ROMANTIC)

        Determine if a Sim has a preference for another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param target_sim_info: An instance of a Sim.
        :type target_sim_info: SimInfo
        :param like_threshold: A value indicating a low amount of preference. Default is CommonSimGenderPreferenceUtils.LOW_PREFERENCE_THRESHOLD. (This argument is obsolete, do not use)
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is CommonSimGenderPreferenceUtils.HIGH_PREFERENCE_THRESHOLD. (This argument is obsolete, do not use)
        :type love_threshold: int, optional
        :param preference_type: The type of preference to use. Default is CommonGenderPreferenceType.ROMANTIC.
        :type preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType], optional
        :return: True, if the Source Sim has a preference for the Target Sim. False, if not.
        :rtype: bool
        """
        return cls.has_preference_for_gender(
            sim_info,
            CommonGender.get_gender(target_sim_info),
            like_threshold=like_threshold,
            love_threshold=love_threshold,
            preference_type=preference_type,
        )

    # noinspection PyUnusedLocal
    @classmethod
    def determine_preferred_genders(cls, sim_info: SimInfo, like_threshold: int = None, love_threshold: int = None, preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType] = CommonGenderPreferenceType.ROMANTIC) -> Tuple[CommonGender]:
        """determine_preferred_genders(sim_info, like_threshold=None, love_threshold=None, preference_type=CommonGenderPreferenceType.ROMANTIC)

        Determine which genders a Sim prefers.

        .. note::

            The math is as follows (The first match will return):

            - Default Gender Preferences = MALE_PREF < like_threshold and FEMALE_PREF < like_threshold
            - Prefers both Genders = absolute(MALE_PREF - FEMALE_PREF) <= love_threshold
            - Prefers Male = MALE_PREF > FEMALE_PREF
            - Prefers Female = FEMALE_PREF > MALE_PREF

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param like_threshold: A value indicating a low amount of preference. Default is cls.LOW_PREFERENCE_THRESHOLD. (This argument is obsolete, do not use)
        :type like_threshold: int, optional
        :param love_threshold: A value indicating a high amount of preference. Default is cls.HIGH_PREFERENCE_THRESHOLD. (This argument is obsolete, do not use)
        :type love_threshold: int, optional
        :param preference_type: The type of preference to use. Default is CommonGenderPreferenceType.ROMANTIC.
        :type preference_type: Union[CommonGenderPreferenceType, GenderPreferenceType], optional
        :return: A collection of CommonGenders the specified Sim prefers.
        :rtype: Tuple[CommonGender]
        """
        preferred_genders = list()
        vanilla_preference_type = CommonGenderPreferenceType.convert_to_vanilla(preference_type)
        for gender in sim_info.get_attracted_genders(vanilla_preference_type):
            preferred_genders.append(CommonGender.convert_from_vanilla(gender))
        return tuple(preferred_genders)

    @classmethod
    def set_to_default_gender_preferences(cls, sim_info: SimInfo) -> None:
        """set_to_default_gender_preferences(sim_info)

        Set a Sim to the default gender preferences.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        default_attracted_to_genders = cls.get_default_preferred_genders(sim_info)
        for gender in CommonGender.get_all():
            if gender in default_attracted_to_genders:
                cls.set_preference_for_gender(sim_info, gender, True, preference_type=CommonGenderPreferenceType.ROMANTIC)
                cls.set_preference_for_gender(sim_info, gender, True, preference_type=CommonGenderPreferenceType.WOOHOO)
            else:
                cls.set_preference_for_gender(sim_info, gender, False, preference_type=CommonGenderPreferenceType.ROMANTIC)
                cls.set_preference_for_gender(sim_info, gender, False, preference_type=CommonGenderPreferenceType.WOOHOO)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_world_sexually_exploring',
    'Set all Sims to be sexually exploring in their Sexual Orientation.',
    command_arguments=(
        CommonConsoleCommandArgument('is_sexually_exploring', 'True or False', 'If True, all Sims will be sexually exploring. If False, all Sims will NOT be sexually exploring.'),
    )
)
def _common_set_world_sexually_exploring(output: CommonConsoleCommandOutput, is_sexually_exploring: bool):
    if is_sexually_exploring:
        output('Attempting to set all Sims to be Sexually Exporing in their Sexual Orientation.')
    else:
        output('Attempting to set all Sims to be Not Sexually Exporing in their Sexual Orientation.')
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        CommonSimGenderOptionUtils.set_is_exploring_sexuality(sim_info, is_sexually_exploring)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref',
    'Set the gender preference amount of a Sim towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preference of the Sim for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('is_attracted_to_gender', 'True or False', 'If True, the Sim will be attracted to the specified Gender. If False, the Sim will no longer be attracted to the gender.'),
        CommonConsoleCommandArgument('preference_type', 'ROMANTIC or WOOHOO', 'The type of preference being updated.', is_optional=True, default_value='ROMANTIC'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.setgenderpref',
        's4clib.set_gender_preference',
        's4clib.setgenderpreference',
    )
)
def _common_set_gender_pref(output: CommonConsoleCommandOutput, gender: CommonGender, is_attracted_to_gender: bool, preference_type: CommonGenderPreferenceType = CommonGenderPreferenceType.ROMANTIC, sim_info: SimInfo = None):
    if gender is None:
        return
    if sim_info is None:
        return
    gender_name = gender.name
    output(f'Attempting to set the {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}')
    if CommonSimGenderPreferenceUtils.set_preference_for_gender(sim_info, gender, is_attracted_to_gender, preference_type=preference_type):
        output(f'SUCCESS: Successfully set the {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}')
    else:
        output(f'FAILED: Failed to set the {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref_of_all_sims',
    'Set the gender preference amount of all Sims towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preferences of the Sims for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('is_attracted_to_gender', 'True or False', 'If True, all Female Sims will be attracted to the specified Gender. If False, all Female Sims will no longer be attracted to the gender.'),
        CommonConsoleCommandArgument('preference_type', 'ROMANTIC or WOOHOO', 'The type of preference being updated.', is_optional=True, default_value='ROMANTIC')
    ),
    command_aliases=(
        's4clib.setgenderprefofallsims',
        's4clib.setgenderpreferenceofallsims',
        's4clib.set_gender_preference_of_all_sims',
        's4clib.set_all_gender_preferences',
        's4clib.setallgenderpreferences',
    )
)
def _common_set_gender_pref_of_all_sims(output: CommonConsoleCommandOutput, gender: CommonGender, is_attracted_to_gender: bool, preference_type: CommonGenderPreferenceType = CommonGenderPreferenceType.ROMANTIC):
    if gender is None:
        return
    gender_name = gender.name
    count_of_sims_changed = 0
    output(f'Setting {preference_type.name} gender preference of all Sims for gender {gender_name} to {is_attracted_to_gender}')
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        try:
            if CommonSimGenderPreferenceUtils.set_preference_for_gender(sim_info, gender, is_attracted_to_gender, preference_type=preference_type):
                count_of_sims_changed += 1
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Failed to set {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}', exception=ex)
            output(f'ERROR: Failed to set {preference_type.name} gender preference of Sim {sim_info} for gender {gender} to {is_attracted_to_gender}. Exception: {ex}')
    output(f'Updated the Gender Preferences of {count_of_sims_changed} Sims.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref_of_all_female_sims',
    'Set the gender preference amount of all Female Sims towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preferences of the Sims for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('is_attracted_to_gender', 'True or False', 'If True, all Female Sims will be attracted to the specified Gender. If False, all Female Sims will no longer be attracted to the gender.'),
        CommonConsoleCommandArgument('preference_type', 'ROMANTIC or WOOHOO', 'The type of preference being updated.', is_optional=True, default_value='ROMANTIC')
    ),
    command_aliases=(
        's4clib.setgenderprefofallfemalesims',
        's4clib.setgenderpreferenceofallfemalesims',
        's4clib.set_gender_preference_of_all_female_sims',
        's4clib.set_all_female_gender_preferences',
        's4clib.setallfemalegenderpreferences',
    )
)
def _common_set_gender_pref_of_all_female_sims(output: CommonConsoleCommandOutput, gender: CommonGender, is_attracted_to_gender: bool, preference_type: CommonGenderPreferenceType = CommonGenderPreferenceType.ROMANTIC):
    if gender is None:
        return
    gender_name = gender.name
    sim_count = 0
    output(f'Setting {preference_type.name} gender preference of all Female Sims for gender {gender_name} to {is_attracted_to_gender}')
    from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonGenderUtils.is_female):
        try:
            if CommonSimGenderPreferenceUtils.set_preference_for_gender(sim_info, gender, is_attracted_to_gender, preference_type=preference_type):
                sim_count += 1
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Failed to set {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}.', exception=ex)
            output(f'Failed to set {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}. Exception: {ex}')
    output(f'Updated Gender Preferences of {sim_count} Sims.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_gender_pref_of_all_male_sims',
    'Set the gender preference of all Male Sims towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preferences of the Sims for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('is_attracted_to_gender', 'True or False', 'If True, all Male Sims will be attracted to the specified Gender. If False, all Male Sims will no longer be attracted to the gender.'),
        CommonConsoleCommandArgument('preference_type', 'ROMANTIC or WOOHOO', 'The type of preference being updated.', is_optional=True, default_value='ROMANTIC')
    ),
    command_aliases=(
        's4clib.setgenderprefofallmalesims',
        's4clib.setgenderpreferenceofallmalesims',
        's4clib.set_gender_preference_of_all_male_sims',
        's4clib.set_all_male_gender_preferences',
        's4clib.setallmalegenderpreferences',
    )
)
def _common_set_gender_pref_of_all_male_sims(output: CommonConsoleCommandOutput, gender: CommonGender, is_attracted_to_gender: bool, preference_type: CommonGenderPreferenceType = CommonGenderPreferenceType.ROMANTIC):
    if gender is None:
        return
    gender_name = gender.name
    sim_count = 0
    output(f'Setting {preference_type.name} gender preference of all Male Sims for gender {gender_name} to {is_attracted_to_gender}')
    from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonGenderUtils.is_male):
        try:
            if CommonSimGenderPreferenceUtils.set_preference_for_gender(sim_info, gender, is_attracted_to_gender, preference_type=preference_type):
                sim_count += 1
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Failed to set {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}.', exception=ex)
            output(f'Failed to set {preference_type.name} gender preference of Sim {sim_info} for gender {gender_name} to {is_attracted_to_gender}. Exception: {ex}')
    output(f'Updated Gender Preferences of {sim_count} Sims.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_gender_pref',
    'Print the gender preference amount a Sim has towards a Gender.',
    command_arguments=(
        CommonConsoleCommandArgument('gender', 'CommonGender', f'The gender to change the preference of the Sim for. Valid Values: {CommonGender.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('preference_type', 'ROMANTIC or WOOHOO', 'The type of preference being checked.', is_optional=True, default_value='ROMANTIC'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printgenderpref',
        's4clib.print_gender_preference',
        's4clib.printgenderpreference',
    )
)
def _common_get_gender_pref(output: CommonConsoleCommandOutput, gender: CommonGender, preference_type: CommonGenderPreferenceType = CommonGenderPreferenceType.ROMANTIC, sim_info: SimInfo = None):
    if gender is None:
        return
    if sim_info is None:
        return
    gender_name = gender.name
    preference_percentage_amount = CommonSimGenderPreferenceUtils.get_gender_preference_amount(sim_info, gender, preference_type=preference_type)
    output(f'{sim_info} has a {preference_percentage_amount}% preference for gender {gender_name}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_preferred_genders',
    'Print preferred genders a Sim is attracted to.',
    command_arguments=(
        CommonConsoleCommandArgument('preference_type', 'ROMANTIC or WOOHOO', 'The type of preference being checked.', is_optional=True, default_value='ROMANTIC'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printpreferredgenders',
    )
)
def _common_get_gender_pref(output: CommonConsoleCommandOutput, preference_type: CommonGenderPreferenceType = CommonGenderPreferenceType.ROMANTIC, sim_info: SimInfo = None):
    if sim_info is None:
        return
    preferred_genders = CommonSimGenderPreferenceUtils.determine_preferred_genders(sim_info, preference_type=preference_type)
    output(f'{sim_info} has a {preference_type.name} gender preference for genders {preferred_genders}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.apply_default_gender_pref',
    'Apply the default Gender preferences for ROMANTIC and WOOHOO preference types to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
)
def _s4clib_apply_default_gender_pref_to_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to update the gender preferences to their default values for {sim_info}.')
    # noinspection PyBroadException
    try:
        CommonSimGenderPreferenceUtils.set_to_default_gender_preferences(sim_info)
    except:
        output(f'Failed to update Sim {sim_info}. They were most likely culled out or unavailable.')
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.apply_default_gender_pref_to_all_sims',
    'Apply the default Gender preference for ROMANTIC and WOOHOO preference types to all Sims using their Gender.'
)
def _s4clib_apply_default_gender_pref_to_all_sims(output: CommonConsoleCommandOutput):
    output('Attempting to update the gender preferences to their default values for all Sims.')
    sim_count = 0
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        # noinspection PyBroadException
        try:
            if sim_info is None:
                continue
            CommonSimGenderPreferenceUtils.set_to_default_gender_preferences(sim_info)
            sim_count += 1
        except:
            output(f'Failed to update Sim {sim_info}. They were most likely culled out or unavailable.')
    output(f'Updated Gender Preferences of {sim_count} Sim(s).')
    return True
