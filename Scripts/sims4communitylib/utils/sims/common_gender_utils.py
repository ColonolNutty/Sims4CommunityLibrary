"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_sim_voice_utils import CommonSimVoiceUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CommonGenderUtils:
    """Utilities for manipulating Genders of Sims.

    """
    @staticmethod
    def get_gender(sim_info: SimInfo) -> Union[Gender, None]:
        """get_gender(sim_info)

        Retrieve the Gender of a Sim.

        :param sim_info: The Sim to retrieve the gender of.
        :type sim_info: SimInfo
        :return: The Gender of the Sim or None if a problem occurs.
        :rtype: Union[Gender, None]
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, 'gender'):
            # noinspection PyPropertyAccess
            return sim_info.gender
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'gender'):
            return sim_info.sim_info.gender
        return None

    @staticmethod
    def set_gender(sim_info: SimInfo, gender: Union[Gender, CommonGender, int]) -> bool:
        """set_gender(sim_info, gender)

        Set the Gender of a Sim.

        :param sim_info: The Sim to set the Gender of.
        :type sim_info: SimInfo
        :param gender: The Gender to set the Sim to.
        :type gender: Union[Gender, CommonGender, int]
        :return: True, if the Gender of the Sim was set successfully. False, if not.
        :rtype: bool
        """
        gender = CommonGender.convert_to_vanilla(gender)
        if gender is None:
            return False
        sim_info.gender = gender
        if gender == Gender.MALE:
            new_trait_id = CommonTraitId.GENDER_MALE
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_FEMALE)
        else:
            new_trait_id = CommonTraitId.GENDER_FEMALE
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_MALE)
        CommonTraitUtils.add_trait(sim_info, new_trait_id)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender(sim_info)
        return True

    @staticmethod
    def swap_gender(sim_info: SimInfo, update_gender_options: bool=True, update_voice: bool=True, update_outfits: bool=True) -> bool:
        """swap_gender(sim_info, update_gender_options=True, update_voice=True, update_outfits=True)

        Swap the Gender of a Sim to it's opposite. i.e. Change a Sim from Male to Female or from Female to Male.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param update_gender_options: If True, gender option traits such as Toilet Usage, Clothing Preference, Pregnancy, and Body Frame will be updated to reflect the vanilla settings for each gender\
        For example, if a Human Sim is swapping from Female to Male, their gender options will be updated to Toilet Standing, Cannot Be Impregnated, Can Impregnate, Mens Wear clothing preference, and Masculine Frame.\
        If False, gender option traits will not be updated.\
        Default is True.
        :type update_gender_options: bool, optional
        :param update_voice: If True, the voice of the Sim will be updated to a default voice for the gender being swapped to. If False, the voice of the Sim will remain unchanged. Default is True.
        :type update_voice: bool, optional
        :param update_outfits: If True, the outfits of the Sim will be regenerated to match the gender options of the Sim. If False, the outfits of the Sim will not be regenerated. Default is True.
        :param update_outfits: bool, optional
        :return: True, if the Gender of the Sim was swapped successfully. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        result = False
        frame = CommonSimGenderOptionUtils.has_masculine_frame(sim_info).result
        prefers_menswear = CommonSimGenderOptionUtils.prefers_menswear(sim_info).result
        can_impregnate = CommonSimGenderOptionUtils.can_impregnate(sim_info).result
        can_be_impregnated = CommonSimGenderOptionUtils.can_be_impregnated(sim_info).result
        can_reproduce = CommonSimGenderOptionUtils.can_reproduce(sim_info).result
        voice_pitch = CommonSimVoiceUtils.get_voice_pitch(sim_info)
        voice_actor = CommonSimVoiceUtils.get_voice_actor(sim_info)
        uses_toilet_standing = CommonSimGenderOptionUtils.uses_toilet_standing(sim_info).result
        has_breasts = CommonSimGenderOptionUtils.has_breasts(sim_info).result
        saved_outfits = sim_info.save_outfits()
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        if CommonGenderUtils.is_male(sim_info):
            result = CommonGenderUtils.set_gender(sim_info, CommonGender.FEMALE)
            if update_voice:
                CommonSimVoiceUtils.set_to_default_female_voice(sim_info)
            if update_gender_options:
                CommonSimGenderOptionUtils.update_gender_options_to_vanilla_female(sim_info)
            if update_outfits:
                CommonOutfitUtils.regenerate_all_outfits(sim_info)
        elif CommonGenderUtils.is_female(sim_info):
            result = CommonGenderUtils.set_gender(sim_info, CommonGender.MALE)
            if update_voice:
                CommonSimVoiceUtils.set_to_default_male_voice(sim_info)
            if update_gender_options:
                CommonSimGenderOptionUtils.update_gender_options_to_vanilla_male(sim_info)
            if update_outfits:
                CommonOutfitUtils.regenerate_all_outfits(sim_info)

        if not update_voice:
            CommonSimVoiceUtils.set_voice_pitch(sim_info, voice_pitch)
            CommonSimVoiceUtils.set_voice_actor(sim_info, voice_actor)

        if not update_gender_options:
            CommonSimGenderOptionUtils.update_body_frame(sim_info, frame)
            CommonSimGenderOptionUtils.update_clothing_preference(sim_info, prefers_menswear)
            CommonSimGenderOptionUtils.update_can_impregnate(sim_info, can_impregnate)
            CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, can_be_impregnated)
            CommonSimGenderOptionUtils.update_can_reproduce(sim_info, can_reproduce)
            CommonSimGenderOptionUtils.update_toilet_usage(sim_info, uses_toilet_standing)
            CommonSimGenderOptionUtils.update_has_breasts(sim_info, has_breasts)

        if not update_outfits:
            sim_info.load_outfits(saved_outfits)
            CommonOutfitUtils.resend_outfits(sim_info)
            CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)
        return result

    @staticmethod
    def are_same_gender(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_gender(sim_info, other_sim_info)

        Determine if two Sims are the same Gender.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Gender. False, if not.
        :rtype: bool
        """
        gender_a = CommonGenderUtils.get_gender(sim_info)
        if gender_a is None:
            return False
        gender_b = CommonGenderUtils.get_gender(other_sim_info)
        if gender_b is None:
            return False
        return int(gender_a) == int(gender_b)

    @staticmethod
    def is_female_gender(gender: Union[Gender, CommonGender, int]) -> bool:
        """is_female_gender(gender)

        Determine if a Gender is Female.

        :param gender: The gender to check.
        :type gender: Union[Gender, CommonGender, int]
        :return: True, if the gender is female. False, if the gender is not female.
        :rtype: bool
        """
        if gender is None:
            return False
        return int(gender) == int(Gender.FEMALE)

    @staticmethod
    def is_male_gender(gender: Union[Gender, CommonGender, int]) -> bool:
        """is_male_gender(gender)

        Determine if a Gender is Male.

        :param gender: The gender to check.
        :type gender: Union[Gender, CommonGender, int]
        :return: True, if the gender is male. False, if the gender is not male.
        :rtype: bool
        """
        if gender is None:
            return False
        return int(gender) == int(Gender.MALE)

    @staticmethod
    def is_female(sim_info: SimInfo) -> bool:
        """is_female(sim_info)

        Determine if a Sim is Female.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is female. False, if the Sim is not female.
        :rtype: bool
        """
        return CommonGenderUtils.is_female_gender(CommonGenderUtils.get_gender(sim_info))

    @staticmethod
    def is_male(sim_info: SimInfo) -> bool:
        """is_male(sim_info)

        Determine if a Sim is Male.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is male. False, if the Sim is not male.
        :rtype: bool
        """
        return CommonGenderUtils.is_male_gender(CommonGenderUtils.get_gender(sim_info))


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.swap_gender',
    'Swap the gender of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('update_gender_options', 'True or False', 'If True, gender options will be updated to vanilla gender options for the gender they are swapping to.', is_optional=True, default_value='True'),
        CommonConsoleCommandArgument('update_voice', 'True or False', 'If True, voice of the Sim will be updated to a default voice for the gender they are swapping to.', is_optional=True, default_value='True'),
        CommonConsoleCommandArgument('update_outfits', 'True or False', 'If True, outfits of the Sim will be regenerated to reflect the gender they are swapping to.', is_optional=True, default_value='True'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or decimal identifier of the Sim to use.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_swap_gender(output: CommonConsoleCommandOutput, sim_info: SimInfo = None, update_gender_options: bool = True, update_voice: bool = True, update_outfits: bool = True) -> bool:
    output(f'Swapping the gender of Sim {sim_info}.')
    result = CommonGenderUtils.swap_gender(sim_info, update_gender_options=update_gender_options, update_voice=update_voice, update_outfits=update_outfits)
    if result:
        output('Success!')
    else:
        output('Failed!')
    return True
