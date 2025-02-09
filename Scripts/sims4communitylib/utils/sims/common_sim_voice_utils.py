"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, List, Tuple
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.common_voice_actor_type import CommonVoiceActorType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimVoiceUtils:
    """Utilities for manipulating the Voice of Sims.

    """

    @staticmethod
    def has_voice_actor(sim_info: SimInfo, voice_actor: Union[int, CommonVoiceActorType]) -> CommonTestResult:
        """has_voice_actor(sim_info, voice_actor)

        Determine if a Sim has a specified voice actor.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param voice_actor: The voice actor to check.
        :type voice_actor: Union[int, CommonVoiceActorType]
        :return: The result of testing. True, if the Sim has the specified voice actor. False, if not.
        :rtype: CommonTestResult
        """
        current_voice_actor = CommonSimVoiceUtils.get_voice_actor(sim_info)
        if current_voice_actor is None:
            current_voice_actor_str = 'None'
        else:
            current_voice_actor_str = current_voice_actor.name if hasattr(current_voice_actor, 'name') else str(current_voice_actor)
        if int(current_voice_actor) == int(voice_actor):
            return CommonTestResult(True, reason=f'{sim_info} has voice actor {current_voice_actor_str}', tooltip_text=CommonStringId.S4CL_SIM_HAS_VOICE_ACTOR, tooltip_tokens=(sim_info, current_voice_actor_str))
        voice_actor_str = voice_actor.name if hasattr(voice_actor, 'name') else str(voice_actor)
        return CommonTestResult(False, reason=f'{sim_info} does not have voice actor {voice_actor_str}. It was {current_voice_actor_str}', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_VOICE_ACTOR_IT_WAS_ACTOR, tooltip_tokens=(sim_info, voice_actor_str, current_voice_actor_str))

    @staticmethod
    def has_voice_pitch(sim_info: SimInfo, voice_pitch: float) -> CommonTestResult:
        """has_voice_pitch(sim_info, voice_pitch)

        Determine if a Sim has a specified voice pitch.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param voice_pitch: The voice pitch to check.
        :type voice_pitch: float
        :return: The result of testing. True, if the Sim has the specified voice pitch. False, if not.
        :rtype: CommonTestResult
        """
        current_voice_pitch = CommonSimVoiceUtils.get_voice_pitch(sim_info)
        if current_voice_pitch == voice_pitch:
            return CommonTestResult(True, reason=f'{sim_info} has voice pitch {voice_pitch}', tooltip_text=CommonStringId.S4CL_SIM_HAS_VOICE_PITCH, tooltip_tokens=(sim_info, str(voice_pitch)))
        return CommonTestResult(False, reason=f'{sim_info} did not have voice pitch {voice_pitch}', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_VOICE_PITCH_IT_WAS_PITCH, tooltip_tokens=(sim_info, str(voice_pitch), str(current_voice_pitch)))

    @staticmethod
    def get_voice_pitch(sim_info: SimInfo) -> float:
        """get_voice_pitch(sim_info)
        
        Retrieve the Pitch of the Voice of a Sim.
        
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A value that represents the pitch of the voice of a Sim. The value can range from -1.0 to 1.0
        :rtype: float
        """
        # noinspection PyPropertyAccess
        return sim_info.voice_pitch

    @staticmethod
    def set_voice_pitch(sim_info: SimInfo, voice_pitch: float) -> CommonExecutionResult:
        """set_voice_pitch(sim_info, voice_pitch)
        
        Set the Pitch of the Voice of a Sim.
        
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param voice_pitch: The value to set the voice pitch to, from -1.0 to 1.0.
        :type voice_pitch: float
        :return: The result of setting the voice pitch of the Sim. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim_info.voice_pitch = voice_pitch
        return CommonExecutionResult.TRUE

    @staticmethod
    def get_voice_actor(sim_info: SimInfo) -> Union[int, CommonVoiceActorType]:
        """get_voice_actor(sim_info)
        
        Retrieve the Actor of the Voice of a Sim.
        
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A value that represents the voice actor of a Sim.
        :rtype: int
        """
        # noinspection PyPropertyAccess
        voice_actor = sim_info.voice_actor
        if voice_actor not in CommonVoiceActorType.value_to_name:
            return voice_actor

        return CommonResourceUtils.get_enum_by_name(CommonVoiceActorType.value_to_name[voice_actor].upper(), CommonVoiceActorType, default_value=voice_actor)

    @staticmethod
    def set_voice_actor(sim_info: SimInfo, voice_actor: Union[int, CommonVoiceActorType]) -> CommonExecutionResult:
        """set_voice_actor(sim_info, voice_actor)

        Set the Voice Actor of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param voice_actor: The voice actor to set the Sim to have.
        :type voice_actor: Union[int, CommonVoiceActorType]
        :return: The result of setting the voice actor. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        sim_info.voice_actor = int(voice_actor)
        return CommonExecutionResult.TRUE

    @staticmethod
    def set_to_default_voice(sim_info: SimInfo) -> CommonExecutionResult:
        """set_to_default_voice(sim_info)

        Set the voice of a Sim to the default for their Age, Gender, and Species.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of setting the voice of the Sim to their default voice. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
        if CommonGenderUtils.is_male(sim_info):
            return CommonSimVoiceUtils.set_to_default_male_voice(sim_info)
        else:
            return CommonSimVoiceUtils.set_to_default_female_voice(sim_info)

    @staticmethod
    def set_to_default_male_voice(sim_info: SimInfo) -> CommonExecutionResult:
        """set_to_default_male_voice(sim_info)

        Set the voice of a Sim to the default male voice for their Age and Species.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of setting the voice of the Sim to the default male voice. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_HUMAN_MASCULINE_1)
        elif CommonAgeSpeciesUtils.is_child_human(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_HUMAN_AMBIGUOUS_1)
        elif CommonAgeSpeciesUtils.is_toddler_human(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.TODDLER_HUMAN_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_large_dog(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_large_dog(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_small_dog(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_small_dog(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_cat(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_CAT_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_cat(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_CAT_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_fox(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_FOX_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_horse(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_HORSE_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_horse(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_HORSE_AMBIGUOUS_1)
        return CommonExecutionResult(False, reason=f'Failed to locate a default male voice actor for Sim {sim_info}', tooltip_text=CommonStringId.S4CL_FAILED_TO_LOCATE_DEFAULT_MALE_VOICE_ACTOR_FOR_SIM, tooltip_tokens=(sim_info,))

    @staticmethod
    def set_to_default_female_voice(sim_info: SimInfo) -> CommonExecutionResult:
        """set_to_default_female_voice(sim_info)

        Set the voice of a Sim to the default female voice for their Age and Species.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of setting the voice of the Sim to the default female voice. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_HUMAN_FEMININE_1)
        elif CommonAgeSpeciesUtils.is_child_human(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_HUMAN_AMBIGUOUS_1)
        elif CommonAgeSpeciesUtils.is_toddler_human(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.TODDLER_HUMAN_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_large_dog(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_large_dog(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_small_dog(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_small_dog(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_DOG_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_cat(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_CAT_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_cat(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_CAT_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_fox(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_FOX_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_horse(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.ADULT_HORSE_AMBIGUOUS_1)
        elif CommonSpeciesUtils.is_horse(sim_info) and CommonAgeUtils.is_child(sim_info):
            return CommonSimVoiceUtils.set_voice_actor(sim_info, CommonVoiceActorType.CHILD_HORSE_AMBIGUOUS_1)
        return CommonExecutionResult(False, reason=f'Failed to locate a default female voice actor for Sim {sim_info}', tooltip_text=CommonStringId.S4CL_FAILED_TO_LOCATE_DEFAULT_FEMALE_VOICE_ACTOR_FOR_SIM, tooltip_tokens=(sim_info,))

    @staticmethod
    def determine_available_voice_types(sim_info: SimInfo) -> Tuple[CommonVoiceActorType]:
        """determine_available_voice_types(sim_info)

        Retrieve a collection of Voice Actor Types that are available for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A collection of voice actor types available for the Sim.
        :rtype: Tuple[CommonVoiceActorType]
        """
        from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.ADULT_HUMAN_AMBIGUOUS_1,
                CommonVoiceActorType.ADULT_HUMAN_FEMININE_1,
                CommonVoiceActorType.ADULT_HUMAN_FEMININE_2,
                CommonVoiceActorType.ADULT_HUMAN_MASCULINE_1,
                CommonVoiceActorType.ADULT_HUMAN_MASCULINE_2,
                CommonVoiceActorType.ADULT_HUMAN_MASCULINE_3,
                CommonVoiceActorType.KYLO_REN_1,
                CommonVoiceActorType.REY_1,
                CommonVoiceActorType.HONDO_OHNAKA_1,
            )
        elif CommonAgeSpeciesUtils.is_child_human(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.CHILD_HUMAN_AMBIGUOUS_1,
                CommonVoiceActorType.CHILD_HUMAN_AMBIGUOUS_2,
                CommonVoiceActorType.KYLO_REN_1,
                CommonVoiceActorType.REY_1,
                CommonVoiceActorType.HONDO_OHNAKA_1,
            )
        elif CommonAgeSpeciesUtils.is_toddler_human(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.TODDLER_HUMAN_AMBIGUOUS_1,
            )
        elif CommonSpeciesUtils.is_large_dog(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_1,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_2,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_3,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_4
            )
        elif CommonSpeciesUtils.is_large_dog(sim_info) and CommonAgeUtils.is_child(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.CHILD_DOG_AMBIGUOUS_1,
            )
        elif CommonSpeciesUtils.is_small_dog(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_1,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_2,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_3,
                CommonVoiceActorType.ADULT_DOG_AMBIGUOUS_4
            )
        elif CommonSpeciesUtils.is_small_dog(sim_info) and CommonAgeUtils.is_child(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.CHILD_DOG_AMBIGUOUS_1,
            )
        elif CommonSpeciesUtils.is_cat(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.ADULT_CAT_AMBIGUOUS_1,
                CommonVoiceActorType.ADULT_CAT_AMBIGUOUS_2,
            )
        elif CommonSpeciesUtils.is_cat(sim_info) and CommonAgeUtils.is_child(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.CHILD_CAT_AMBIGUOUS_1,
            )
        elif CommonSpeciesUtils.is_fox(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.ADULT_FOX_AMBIGUOUS_1,
            )
        elif CommonSpeciesUtils.is_horse(sim_info) and CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.ADULT_HORSE_AMBIGUOUS_1,
            )
        elif CommonSpeciesUtils.is_horse(sim_info) and CommonAgeUtils.is_child(sim_info):
            # noinspection PyTypeChecker
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
                CommonVoiceActorType.CHILD_HORSE_AMBIGUOUS_1,
            )
        else:
            result: Tuple[CommonVoiceActorType] = (
                CommonVoiceActorType.MUTE,
            )
        return result


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'common_voice_actor_log')
log.enable()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_voice',
    'Print information about the voice of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
)
def _common_print_voice_pitch(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    voice_pitch = CommonSimVoiceUtils.get_voice_pitch(sim_info)
    voice_actor = CommonSimVoiceUtils.get_voice_actor(sim_info)
    voice_actor_name = voice_actor.name if hasattr(voice_actor, 'name') else voice_actor
    log.debug(f'Voice info about {sim_info}')
    log.debug(f'Voice Pitch: {voice_pitch}')
    log.debug(f'Voice Actor: {voice_actor_name}')
    output(f'Voice info about {sim_info}')
    output(f'Voice Pitch: {voice_pitch}')
    output(f'Voice Actor: {voice_actor_name}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_voice_pitch',
    'Set the pitch of a Sims voice.',
    command_arguments=(
        CommonConsoleCommandArgument('voice_pitch', 'Decimal Identifier', 'The voice pitch to set the voice of the Sim to.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_set_voice_pitch(output: CommonConsoleCommandOutput, voice_pitch: float, sim_info: SimInfo=None):
    if sim_info is None:
        return
    if voice_pitch is None:
        return
    result = CommonSimVoiceUtils.set_voice_pitch(sim_info, voice_pitch)
    if result:
        log.format_with_message('Set voice pitch', sim=sim_info, voice_pitch=voice_pitch, result=result)
        output(f'SUCCESS: Successfully set the voice pitch of Sim {sim_info} to {voice_pitch}: {result}')
    else:
        log.format_with_message('Set voice pitch', sim=sim_info, voice_pitch=voice_pitch, result=result)
        output(f'FAILED: Failed to set the voice pitch of Sim {sim_info} to {voice_pitch}: {result}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_voice_actor',
    'Set the voice actor of a Sims voice.',
    command_arguments=(
        CommonConsoleCommandArgument('voice_actor', 'CommonVoiceActorType', f'The voice actor to change the Sim to. Valid Voice Actors: ({CommonVoiceActorType.get_comma_separated_names_string()})'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_set_voice_actor(output: CommonConsoleCommandOutput, voice_actor: CommonVoiceActorType, sim_info: SimInfo=None):
    if voice_actor is None:
        return
    if sim_info is None:
        return
    voice_actor_name = voice_actor.name
    output(f'Attempting to set the voice actor of {sim_info} to {voice_actor_name}.')
    result = CommonSimVoiceUtils.set_voice_actor(sim_info, voice_actor)
    if result:
        output(f'SUCCESS: Successfully set the voice actor of {sim_info} to {voice_actor_name}: {result}')
    else:
        output(f'FAILED: Failed to set the voice actor of {sim_info} to {voice_actor_name}: {result}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_voice_actor_custom',
    'Set the voice actor of a Sims voice to a custom voice. NOTE: Success does not mean that it truly succeeded, much of the time the Sim will become Mute instead.',
    command_arguments=(
        CommonConsoleCommandArgument('voice_actor_id', 'int', 'The id of the voice actor to change the Sim to.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_set_voice_actor_custom(output: CommonConsoleCommandOutput, voice_actor_id: int, sim_info: SimInfo=None):
    if voice_actor_id is None:
        return
    if sim_info is None:
        return
    output(f'Attempting to set the voice actor of {sim_info} to {voice_actor_id}.')
    result = CommonSimVoiceUtils.set_voice_actor(sim_info, voice_actor_id)
    if result:
        output(f'SUCCESS: Successfully set the voice actor of {sim_info} to {voice_actor_id}: {result}')
    else:
        output(f'FAILED: Failed to set the voice actor of {sim_info} to {voice_actor_id}: {result}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_dev.print_all_voice_actors',
    'Print a list of all available Voice Actors (It entirely depends on all of the Sims available in the game though)',
    show_with_help_command=False
)
def _common_get_all_voice_actors(output: CommonConsoleCommandOutput):
    output('Printing all voice actors.')
    sim_count = 0
    duplicate_count = 0
    voice_actor_by_age: Dict[(CommonAge, CommonSpecies, CommonGender), List[Union[int, CommonVoiceActorType]]] = dict()
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        sim_type = CommonSimTypeUtils.determine_sim_type(sim_info)
        gender = CommonGender.get_gender(sim_info)
        key = (sim_type.name, gender.name)
        if key not in voice_actor_by_age:
            voice_actor_by_age[key] = list()
        voice_actor_list = voice_actor_by_age[key]
        voice_actor = CommonSimVoiceUtils.get_voice_actor(sim_info)
        sim_count += 1
        if voice_actor in voice_actor_list:
            duplicate_count += 1
            continue
        log.format_with_message('Adding voice actor from Sim', sim=sim_info, voice_actor=voice_actor.name if isinstance(voice_actor, CommonVoiceActorType) else voice_actor)
        voice_actor_list.append(voice_actor)
        voice_actor_by_age[key] = voice_actor_list
    log.format_with_message('Voice Actor', voice_actors=voice_actor_by_age, sim_count=sim_count, duplicate_count=duplicate_count)
    for (_key, _voice_actor) in voice_actor_by_age.items():
        voice_actor_name = _voice_actor.name if isinstance(_voice_actor, CommonVoiceActorType) else _voice_actor
        output(f'Voice Actor {_key} = {voice_actor_name}')
