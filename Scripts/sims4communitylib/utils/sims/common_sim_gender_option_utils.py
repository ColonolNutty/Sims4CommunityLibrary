"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.global_gender_preference_tuning import SexualityStatus, GlobalGenderPreferenceTuning
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_voice_utils import CommonSimVoiceUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from traits.traits import Trait


class CommonSimGenderOptionUtils:
    """Utilities for manipulating the Gender Options of Sims.

    """

    @staticmethod
    def has_masculine_frame(sim_info: SimInfo) -> CommonTestResult:
        """has_masculine_frame(sim_info)

        Determine if a sim has a Masculine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim does. False, if the Sim does not.
        :rtype: CommonTestResult
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)

    @staticmethod
    def has_feminine_frame(sim_info: SimInfo) -> CommonTestResult:
        """has_feminine_frame(sim_info)

        Determine if a sim has a Feminine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim does. False, if the Sim does not.
        :rtype: CommonTestResult
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)

    @staticmethod
    def prefers_menswear(sim_info: SimInfo) -> CommonTestResult:
        """prefers_menswear(sim_info)

        Determine if a sim prefers Mens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim does. False, if the Sim does not.
        :rtype: CommonTestResult
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)

    @staticmethod
    def prefers_womenswear(sim_info: SimInfo) -> CommonTestResult:
        """prefers_womenswear(sim_info)

        Determine if a sim prefers Womens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim does. False, if the Sim does not.
        :rtype: CommonTestResult
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)

    @staticmethod
    def can_impregnate(sim_info: SimInfo) -> CommonTestResult:
        """can_impregnate(sim_info)

        Determine if a sim Can Impregnate.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can impregnate other Sims. False, if the Sim can not impregnate other Sims.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
        return CommonSimPregnancyUtils.can_impregnate(sim_info)

    @staticmethod
    def can_not_impregnate(sim_info: SimInfo) -> CommonTestResult:
        """can_not_impregnate(sim_info)

        Determine if a sim Can Not Impregnate.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can not impregnate other Sims. False, if the Sim can impregnate other Sims.
        :rtype: CommonTestResult
        """
        can_impregnate_result = CommonSimGenderOptionUtils.can_impregnate(sim_info)
        return can_impregnate_result.reverse_result()

    @staticmethod
    def can_be_impregnated(sim_info: SimInfo) -> CommonTestResult:
        """can_be_impregnated(sim_info)

        Determine if a sim Can Be Impregnated.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can be impregnated. False, if the Sim can not be impregnated.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
        return CommonSimPregnancyUtils.can_be_impregnated(sim_info)

    @staticmethod
    def can_not_be_impregnated(sim_info: SimInfo) -> CommonTestResult:
        """can_not_be_impregnated(sim_info)

        Determine if a sim Can Not Be Impregnated.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can not be impregnated. False, if the Sim can be impregnated.
        :rtype: CommonTestResult
        """
        can_be_impregnated_result = CommonSimGenderOptionUtils.can_be_impregnated(sim_info)
        return can_be_impregnated_result.reverse_result()

    @staticmethod
    def can_create_pregnancy(sim_info: SimInfo) -> CommonTestResult:
        """can_create_pregnancy(sim_info)

        Determine if a Sim can either impregnate, be impregnated, or can reproduce.

        .. note:: Will return False if the Sim can both impregnate and not impregnate,\
            if the Sim can both be impregnated and not be impregnated\
            or if the Sim can both reproduce and not reproduce.

        .. note:: A Sim can impregnate when they can either impregnate other Sims, can be impregnated by other Sims, or if they are a Pet, can reproduce.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can create pregnancies. False, if the Sim can not create pregnancies.
        :rtype: CommonTestResult
        """
        return CommonTraitUtils.can_impregnate(sim_info) or CommonTraitUtils.can_be_impregnated(sim_info) or CommonTraitUtils.can_reproduce(sim_info)

    @staticmethod
    def can_reproduce(sim_info: SimInfo) -> CommonTestResult:
        """can_reproduce(sim_info)

        Determine if a Pet Sim can reproduce.

        .. note:: Use :func:`~can_impregnate` and :func:`~can_be_impregnated` for Human Sims.
        .. note:: Will return False if the Pet Sim has the PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can reproduce. False, if the Sim can not reproduce.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
            return CommonTestResult(False, reason=f'Sim has the Cannot Reproduce trait.')
        if CommonSimGenderOptionUtils.can_not_impregnate(sim_info) and CommonSimGenderOptionUtils.can_not_be_impregnated(sim_info):
            return CommonTestResult(False, reason=f'Sim can neither impregnate nor be impregnated.')
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
            return CommonTestResult(True, reason=f'Sim has the Can Reproduce trait.')
        can_impregnate_result = CommonSimGenderOptionUtils.can_impregnate(sim_info)
        if can_impregnate_result:
            return can_impregnate_result
        can_be_impregnated_result = CommonSimGenderOptionUtils.can_be_impregnated(sim_info)
        if can_be_impregnated_result:
            return can_be_impregnated_result
        return CommonTestResult(False, reason=f'Sim can neither impregnate nor be impregnated.')

    @staticmethod
    def can_not_reproduce(sim_info: SimInfo) -> CommonTestResult:
        """can_not_reproduce(sim_info)

        Determine if a pet sim can reproduce.

        ..note:: Use :func:`~can_not_impregnate` and :func:`~can_not_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet sim has the PREGNANCY_OPTIONS_PET_CAN_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim can not reproduce. False, if the Sim can reproduce.
        :rtype: CommonTestResult
        """
        can_reproduce_result = CommonSimGenderOptionUtils.can_reproduce(sim_info)
        return can_reproduce_result.reverse_result()

    @staticmethod
    def uses_toilet_standing(sim_info: SimInfo) -> CommonTestResult:
        """uses_toilet_standing(sim_info)

        Determine if a sim uses the toilet while standing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim uses toilets while standing. False, if the Sim does not use toilets while standing.
        :rtype: CommonTestResult
        """
        toilet_standing_trait = CommonSimGenderOptionUtils.determine_toilet_standing_trait(sim_info)
        if toilet_standing_trait is None:
            return CommonTestResult(False, reason='No toilet standing trait was found for Sim.')
        return CommonTraitUtils.has_trait(sim_info, toilet_standing_trait)

    @staticmethod
    def uses_toilet_sitting(sim_info: SimInfo) -> CommonTestResult:
        """uses_toilet_sitting(sim_info)

        Determine if a sim uses the toilet while sitting.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim uses toilets while sitting. False, if the Sim does not use toilets while sitting.
        :rtype: CommonTestResult
        """
        toilet_sitting_trait = CommonSimGenderOptionUtils.determine_toilet_sitting_trait(sim_info)
        if toilet_sitting_trait is None:
            return CommonTestResult(False, reason='No toilet sitting trait was found for Sim.')
        return CommonTraitUtils.has_trait(sim_info, toilet_sitting_trait)

    @staticmethod
    def has_breasts(sim_info: SimInfo) -> CommonTestResult:
        """has_breasts(sim_info)

        Determine if a Sim has breasts.

        .. note:: This will True if breasts are being forced on the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has breasts. False, if not.
        :rtype: CommonTestResult
        """
        if CommonGenderUtils.is_female(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF):
                return CommonTestResult(False, reason=f'Sim does not have breasts. They are Female and have the Breasts Force Off trait.')
            else:
                return CommonTestResult(True, reason=f'Sim has breasts. They are Female and they do not have the Breasts Force Off trait.')
        if CommonGenderUtils.is_male(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON):
                return CommonTestResult(True, reason=f'Sim has breasts. They are Male and they have the Breasts Force On trait.')
            else:
                return CommonTestResult(False, reason=f'Sim does not have breasts. They are Male and they do not have the Breasts Force On trait.')
        return CommonTestResult(False, reason=f'Sim does not have breasts. They are neither Male nor Female.')

    @staticmethod
    def update_gender_options_to_vanilla_male(sim_info: SimInfo, return_on_failure: bool = False) -> CommonExecutionResult:
        """update_gender_options_to_vanilla_male(sim_info, return_on_failure=False)

        Update a Sim to the vanilla Sims 4 default gender options for Male Sims. (Masculine, Menswear Preference, etc.)

        .. note:: This will change the following things: Body Frame (Masculine), Clothing Preference (Masculine), Can Be Impregnated (False), Can Impregnate (True), Can Reproduce (True), Toilet Usage Posture (Standing), Voice Actor (MALE).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param return_on_failure: If True, if any update attempt fails, the function will return that result. If False, any failures will be ignored. Default is False.
        :type return_on_failure: bool, optional
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        update_body_frame_result = CommonSimGenderOptionUtils.update_body_frame(sim_info, True)
        if return_on_failure and not update_body_frame_result:
            return update_body_frame_result
        update_clothing_preference_result = CommonSimGenderOptionUtils.update_clothing_preference(sim_info, True)
        if return_on_failure and not update_clothing_preference_result:
            return update_clothing_preference_result
        update_can_be_impregnated_result = CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
        if return_on_failure and not update_can_be_impregnated_result:
            return update_can_be_impregnated_result
        update_can_impregnate_result = CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
        if return_on_failure and not update_can_impregnate_result:
            return update_can_impregnate_result
        update_can_reproduce_result = CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
        if return_on_failure and not update_can_reproduce_result:
            return update_can_reproduce_result
        update_toilet_usage_result = CommonSimGenderOptionUtils.update_toilet_usage(sim_info, True)
        if return_on_failure and not update_toilet_usage_result:
            return update_toilet_usage_result
        set_male_voice_result = CommonSimVoiceUtils.set_to_default_male_voice(sim_info)
        if return_on_failure and not set_male_voice_result:
            return set_male_voice_result
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_gender_options_to_vanilla_female(sim_info: SimInfo, return_on_failure: bool = False) -> CommonExecutionResult:
        """update_gender_options_to_vanilla_female(sim_info, return_on_failure=False)

        Update a Sim to the vanilla Sims 4 default gender options for Female Sims. (Feminine, Womenswear Preference, etc.)

        .. note:: This will change the following things: Body Frame (Feminine), Clothing Preference (Feminine), Can Be Impregnated (True), Can Impregnate (False), Can Reproduce (True), Toilet Usage Posture (Sitting), Voice Actor (FEMALE).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param return_on_failure: If True, if any update attempt fails, the function will return that result. If False, any failures will be ignored. Default is False.
        :type return_on_failure: bool, optional
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        update_body_frame_result = CommonSimGenderOptionUtils.update_body_frame(sim_info, False)
        if return_on_failure and not update_body_frame_result:
            return update_body_frame_result
        update_clothing_preference_result = CommonSimGenderOptionUtils.update_clothing_preference(sim_info, False)
        if return_on_failure and not update_clothing_preference_result:
            return update_clothing_preference_result
        update_can_be_impregnated_result = CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
        if return_on_failure and not update_can_be_impregnated_result:
            return update_can_be_impregnated_result
        update_can_impregnate_result = CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
        if return_on_failure and not update_can_impregnate_result:
            return update_can_impregnate_result
        update_can_reproduce_result = CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
        if return_on_failure and not update_can_reproduce_result:
            return update_can_reproduce_result
        update_toilet_usage_result = CommonSimGenderOptionUtils.update_toilet_usage(sim_info, False)
        if return_on_failure and not update_toilet_usage_result:
            return update_toilet_usage_result
        set_female_voice_result = CommonSimVoiceUtils.set_to_default_female_voice(sim_info)
        if return_on_failure and not set_female_voice_result:
            return set_female_voice_result
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_has_breasts(sim_info: SimInfo, has_breasts: bool) -> CommonExecutionResult:
        """update_has_breasts(sim_info, has_breasts)

        Give or Take Away the breasts of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param has_breasts: If True, the Sim will be given breasts.\
        If False, the Sim will not longer have breasts.
        :type has_breasts: bool
        :return: The result of updating. True, if the state of a Sim having breasts or not was changed. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
        if has_breasts:
            if CommonGenderUtils.is_male(sim_info):
                add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
                if not add_trait_result:
                    return add_trait_result
                CommonSimEventDispatcherService()._on_sim_change_gender_options_breasts(sim_info)
        else:
            if CommonGenderUtils.is_female(sim_info):
                add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
                if not add_trait_result:
                    return add_trait_result
                CommonSimEventDispatcherService()._on_sim_change_gender_options_breasts(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_body_frame(sim_info: SimInfo, masculine: bool) -> CommonExecutionResult:
        """update_body_frame(sim_info, masculine)

        Update the Body Frame of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param masculine: If True, the Sim will get a Masculine frame.\
        If False, the Sim will get a Feminine frame.
        :type masculine: bool
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonSpeciesUtils.is_human(sim_info):
            return CommonExecutionResult(False, reason=f'Sim is not Human.')
        if masculine:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)
            if not add_trait_result:
                return add_trait_result
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)
            if not add_trait_result:
                return add_trait_result
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_body_frame(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_clothing_preference(sim_info: SimInfo, prefer_menswear: bool) -> CommonExecutionResult:
        """update_clothing_preference(sim_info, prefer_menswear)

        Update the Clothing Preference of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param prefer_menswear: If True, the Sim will prefer Menswear.\
        If False, the Sim will prefer Womenswear.
        :type prefer_menswear: bool
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonSpeciesUtils.is_human(sim_info):
            return CommonExecutionResult(False, reason=f'Sim is not Human.')
        if prefer_menswear:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)
            if not add_trait_result:
                return add_trait_result
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)
            if not add_trait_result:
                return add_trait_result
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_clothing_preference(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_can_be_impregnated(sim_info: SimInfo, can_be_impregnated: bool) -> CommonExecutionResult:
        """update_can_be_impregnated(sim_info, can_be_impregnated)

        Update a Sims ability to be impregnated by other Sims.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_be_impregnated: If True, the Sim will have the ability to be impregnated.\
        If False, the Sim will not have the ability to be impregnated.
        :type can_be_impregnated: bool
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
        can_be_impregnated_trait = CommonSimPregnancyUtils.determine_can_be_impregnated_trait(sim_info)
        can_not_be_impregnated_trait = CommonSimPregnancyUtils.determine_can_not_be_impregnated_trait(sim_info)
        if can_be_impregnated_trait is None:
            return CommonExecutionResult(False, reason=f'No Can Be Impregnated trait was found for Sim {sim_info}')
        if can_not_be_impregnated_trait is None:
            return CommonExecutionResult(False, reason=f'No Can Not Be Impregnated trait was found for Sim {sim_info}')
        if can_be_impregnated:
            CommonTraitUtils.remove_trait(sim_info, can_not_be_impregnated_trait)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, can_be_impregnated_trait)
            if not add_trait_result:
                return add_trait_result
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
            if not add_trait_result:
                return add_trait_result
        else:
            CommonTraitUtils.remove_trait(sim_info, can_be_impregnated_trait)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, can_not_be_impregnated_trait)
            if not add_trait_result:
                return add_trait_result
            if not CommonSimPregnancyUtils.can_impregnate(sim_info):
                CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
                add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
                if not add_trait_result:
                    return add_trait_result
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_can_be_impregnated(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_can_impregnate(sim_info: SimInfo, can_impregnate: bool) -> CommonExecutionResult:
        """update_can_impregnate(sim_info, can_impregnate)

        Update a Sims ability to impregnate other Sims.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_impregnate: If True, the Sim will have the ability to impregnate other Sims.\
        If False, the Sim will not have the ability to impregnate other Sims.
        :type can_impregnate: bool
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
        can_impregnate_trait = CommonSimPregnancyUtils.determine_can_impregnate_trait(sim_info)
        can_not_impregnate_trait = CommonSimPregnancyUtils.determine_can_not_impregnate_trait(sim_info)
        if can_impregnate_trait is None:
            return CommonExecutionResult(False, reason=f'No Can Impregnate trait was found for Sim {sim_info}')
        if can_not_impregnate_trait is None:
            return CommonExecutionResult(False, reason=f'No Can Not Impregnate trait was found for Sim {sim_info}')
        if can_impregnate:
            CommonTraitUtils.remove_trait(sim_info, can_not_impregnate_trait)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, can_impregnate_trait)
            if not add_trait_result:
                return add_trait_result
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
            if not add_trait_result:
                return add_trait_result
        else:
            CommonTraitUtils.remove_trait(sim_info, can_impregnate_trait)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, can_not_impregnate_trait)
            if not add_trait_result:
                return add_trait_result
            if not CommonSimPregnancyUtils.can_be_impregnated(sim_info):
                CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
                add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
                if not add_trait_result:
                    return add_trait_result
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_can_impregnate(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_can_reproduce(sim_info: SimInfo, can_reproduce: bool) -> CommonExecutionResult:
        """update_can_reproduce(sim_info, can_reproduce)

        Update a Sims ability to reproduce.

        .. note:: Will only update Pet Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_reproduce: If True, the Sim will have the ability to reproduce.\
        If False, the Sim will not have the ability to reproduce.
        :type can_reproduce: bool
        :return: The result of updating. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not CommonSpeciesUtils.is_animal(sim_info):
            return CommonExecutionResult(False, reason=f'Sim is not an Animal.')
        if can_reproduce:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
            if not add_trait_result:
                return add_trait_result
            if CommonGenderUtils.is_male(sim_info):
                update_can_impregnate_result = CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
                if not update_can_impregnate_result:
                    return update_can_impregnate_result
                update_can_be_impregnated_result = CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
                if not update_can_be_impregnated_result:
                    return update_can_be_impregnated_result
            else:
                update_can_impregnate_result = CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
                if not update_can_impregnate_result:
                    return update_can_impregnate_result
                update_can_be_impregnated_result = CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
                if not update_can_be_impregnated_result:
                    return update_can_be_impregnated_result
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
            if not add_trait_result:
                return add_trait_result
            if CommonGenderUtils.is_male(sim_info):
                update_can_impregnate_result = CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
                if not update_can_impregnate_result:
                    return update_can_impregnate_result
                update_can_be_impregnated_result = CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
                if not update_can_be_impregnated_result:
                    return update_can_be_impregnated_result
            else:
                update_can_impregnate_result = CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
                if not update_can_impregnate_result:
                    return update_can_impregnate_result
                update_can_be_impregnated_result = CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
                if not update_can_be_impregnated_result:
                    return update_can_be_impregnated_result
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_can_reproduce(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def update_toilet_usage(sim_info: SimInfo, uses_toilet_standing: bool) -> CommonExecutionResult:
        """update_toilet_usage(sim_info, uses_toilet_standing)

        Update how a Sim uses the toilet. i.e. Toilet Standing or Toilet Sitting.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param uses_toilet_standing: If True, the Sim will use toilets while standing and will not use toilets while sitting.\
        If False, the Sim will use toilets while sitting and will not use toilets while standing.
        :type uses_toilet_standing: bool
        :return: The result of updating toilet use posture. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        toilet_standing = CommonSimGenderOptionUtils.determine_toilet_standing_trait(sim_info)
        toilet_sitting = CommonSimGenderOptionUtils.determine_toilet_sitting_trait(sim_info)

        if toilet_standing is None:
            return CommonExecutionResult(False, reason='No toilet standing trait was found for Sim.')

        if toilet_sitting is None:
            return CommonExecutionResult(False, reason='No toilet sitting trait was found for Sim.')

        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN)
        if uses_toilet_standing:
            CommonTraitUtils.remove_trait(sim_info, toilet_sitting)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, toilet_standing)
            if not add_trait_result:
                return add_trait_result
        else:
            CommonTraitUtils.remove_trait(sim_info, toilet_standing)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, toilet_sitting)
            if not add_trait_result:
                return add_trait_result
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def set_can_use_toilet_standing(sim_info: SimInfo, can_use_toilet_standing: bool) -> CommonExecutionResult:
        """set_can_use_toilet_standing(sim_info, can_use_toilet_standing)

        Set whether a Sim can use a toilet while standing or not.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_use_toilet_standing: Whether or not the Sim will be able to use a toilet while standing.
        :type can_use_toilet_standing: bool
        :return: The result of setting toilet use posture. True, if successful set. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        toilet_standing = CommonSimGenderOptionUtils.determine_toilet_standing_trait(sim_info)

        if toilet_standing is None:
            return CommonExecutionResult(False, reason='No toilet standing trait was found for Sim.')

        if can_use_toilet_standing and not CommonTraitUtils.has_trait(sim_info, toilet_standing):
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, toilet_standing)
            if not add_trait_result:
                return add_trait_result
        elif CommonTraitUtils.has_trait(sim_info, toilet_standing):
            CommonTraitUtils.remove_trait(sim_info, toilet_standing)
            if not CommonSimGenderOptionUtils.uses_toilet_sitting(sim_info):
                add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN)
                if not add_trait_result:
                    return add_trait_result

        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def set_can_use_toilet_sitting(sim_info: SimInfo, can_use_toilet_sitting: bool) -> CommonExecutionResult:
        """set_can_use_toilet_sitting(sim_info, can_use_toilet_sitting)

        Set whether a Sim can use a toilet while sitting or not.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_use_toilet_sitting: Whether or not the Sim will be able to use a toilet while sitting.
        :type can_use_toilet_sitting: bool
        :return: The result of setting toilet use posture. True, if successful set. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        toilet_sitting = CommonSimGenderOptionUtils.determine_toilet_sitting_trait(sim_info)

        if toilet_sitting is None:
            return CommonExecutionResult(False, reason='No toilet sitting trait was found for Sim.')

        if can_use_toilet_sitting and not CommonTraitUtils.has_trait(sim_info, toilet_sitting):
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN)
            add_trait_result = CommonTraitUtils.add_trait(sim_info, toilet_sitting)
            if not add_trait_result:
                return add_trait_result
        elif CommonTraitUtils.has_trait(sim_info, toilet_sitting):
            CommonTraitUtils.remove_trait(sim_info, toilet_sitting)
            if not CommonSimGenderOptionUtils.uses_toilet_standing(sim_info):
                add_trait_result = CommonTraitUtils.add_trait(sim_info, CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_UNKNOWN)
                if not add_trait_result:
                    return add_trait_result

        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return CommonExecutionResult.TRUE

    @staticmethod
    def determine_toilet_standing_trait(sim_info: SimInfo) -> Union[CommonTraitId, None]:
        """determine_toilet_standing_trait(sim_info)

        Determine the trait that would indicate a Sim uses the toilet while standing.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The trait that would indicate the Sim uses the toilet while standing or None if no trait is found.
        :rtype: Union[CommonTraitId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonTraitId.GENDER_OPTIONS_TOILET_STANDING
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_LARGE_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_SMALL_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_STANDING_FOX
        return None

    @staticmethod
    def determine_toilet_sitting_trait(sim_info: SimInfo) -> Union[CommonTraitId, None]:
        """determine_toilet_sitting_trait(sim_info)

        Determine the trait that would indicate a Sim uses the toilet while sitting.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The trait that would indicate the Sim uses the toilet while sitting or None if no trait is found.
        :rtype: Union[CommonTraitId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonTraitId.GENDER_OPTIONS_TOILET_SITTING
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_LARGE_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_SMALL_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_TOILET_SITTING_FOX
        return None

    @classmethod
    def is_exploring_sexuality(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_exploring_sexuality(sim_info)

        Determine if a Sim is open to exploring their sexuality.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_sexuality_exploration_status(sim_info, SexualityStatus.EXPLORING)

    @classmethod
    def is_not_exploring_sexuality(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_not_exploring_sexuality(sim_info)

        Determine if a Sim is not open to exploring their sexuality.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        return cls.has_sexuality_exploration_status(sim_info, SexualityStatus.NOT_EXPLORING)

    @classmethod
    def has_sexuality_exploration_status(cls, sim_info: SimInfo, sexuality_status: SexualityStatus) -> CommonTestResult:
        """has_sexuality_exploration_status(sim_info, sexuality_status)

        Determine if a Sim has the specified exploration status for their sexuality.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param sexuality_status: The exploration status to check for.
        :type sexuality_status: SexualityStatus
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            return CommonTestResult(False, reason=f'{sim_info} is None!')
        exploring_sexuality_trait = cls.get_sexuality_status_trait(sim_info, sexuality_status)
        if CommonTraitUtils.has_trait(sim_info, exploring_sexuality_trait):
            if sexuality_status == SexualityStatus.EXPLORING:
                return CommonTestResult(True, reason=f'{sim_info} is open to exploring their sexuality.')
            else:
                return CommonTestResult(True, reason=f'{sim_info} is not open to exploring their sexuality.')
        if sexuality_status == SexualityStatus.EXPLORING:
            return CommonTestResult(False, reason=f'{sim_info} is not open to exploring their sexuality.')
        else:
            return CommonTestResult(False, reason=f'{sim_info} is open to exploring their sexuality.')

    @classmethod
    def set_is_exploring_sexuality(cls, sim_info: SimInfo, is_exploring: bool) -> CommonExecutionResult:
        """set_is_exploring_sexuality(sim_info, is_exploring)

        Set whether a Sim is open to explore their sexuality or not.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param is_exploring: Set True if the Sim should be set to Exploring. Set False if the Sim should be set to Not Exploring.
        :type is_exploring: bool
        """
        if sim_info is None:
            return CommonTestResult(False, reason=f'{sim_info} is None!')
        if is_exploring:
            sexuality_status = SexualityStatus.EXPLORING
            opposite_sexuality_status = SexualityStatus.NOT_EXPLORING
        else:
            sexuality_status = SexualityStatus.NOT_EXPLORING
            opposite_sexuality_status = SexualityStatus.EXPLORING
        to_remove_trait = cls.get_sexuality_status_trait(sim_info, opposite_sexuality_status)
        to_add_trait = cls.get_sexuality_status_trait(sim_info, sexuality_status)
        remove_result = CommonTraitUtils.remove_trait(sim_info, to_remove_trait)
        if not remove_result:
            return remove_result
        return CommonTraitUtils.add_trait(sim_info, to_add_trait)

    # noinspection PyUnusedLocal
    @classmethod
    def get_sexuality_status_trait(cls, sim_info: SimInfo, sexuality_status: SexualityStatus) -> Union[Trait, None]:
        """get_sexuality_status_trait(sim_info, sexuality_status)

        Retrieve the trait associated with a sexuality status.

        :param sim_info: An instance of the Sim to receive or be checked for the trait.
        :type sim_info: SimInfo
        :param sexuality_status: The sexuality status to look for.
        :type sexuality_status: SexualityStatus
        :return: The trait associated with the specified sexuality status or None if not found.
        :rtype: Union[Trait, None]
        """
        return GlobalGenderPreferenceTuning.EXPLORING_SEXUALITY_TRAITS_MAPPING.get(sexuality_status, None)
