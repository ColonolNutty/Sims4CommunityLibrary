"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_voice_utils import CommonSimVoiceUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CommonSimGenderOptionUtils:
    """Utilities for manipulating the Gender Options of Sims.

    """

    @staticmethod
    def has_masculine_frame(sim_info: SimInfo) -> bool:
        """has_masculine_frame(sim_info)

        Determine if a sim has a Masculine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)

    @staticmethod
    def has_feminine_frame(sim_info: SimInfo) -> bool:
        """has_feminine_frame(sim_info)

        Determine if a sim has a Feminine Body Frame.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)

    @staticmethod
    def prefers_menswear(sim_info: SimInfo) -> bool:
        """prefers_menswear(sim_info)

        Determine if a sim prefers Mens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)

    @staticmethod
    def prefers_womenswear(sim_info: SimInfo) -> bool:
        """prefers_womenswear(sim_info)

        Determine if a sim prefers Womens Clothing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim does. False, if the Sim does not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)

    @staticmethod
    def can_impregnate(sim_info: SimInfo) -> bool:
        """can_impregnate(sim_info)

        Determine if a sim Can Impregnate.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can impregnate other Sims. False, if the Sim can not impregnate other Sims.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
        return CommonSimPregnancyUtils.can_impregnate(sim_info)

    @staticmethod
    def can_not_impregnate(sim_info: SimInfo) -> bool:
        """can_not_impregnate(sim_info)

        Determine if a sim Can Not Impregnate.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: This will check for a sim to not also have the GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not impregnate other Sims. False, if the Sim can impregnate other Sims.
        :rtype: bool
        """
        return not CommonSimGenderOptionUtils.can_impregnate(sim_info)

    @staticmethod
    def can_be_impregnated(sim_info: SimInfo) -> bool:
        """can_be_impregnated(sim_info)

        Determine if a sim Can Be Impregnated.

        .. note:: Use :func:`~can_reproduce` for Pet Sims.
        .. note:: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can be impregnated. False, if the Sim can not be impregnated.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
        return CommonSimPregnancyUtils.can_be_impregnated(sim_info)

    @staticmethod
    def can_not_be_impregnated(sim_info: SimInfo) -> bool:
        """can_not_be_impregnated(sim_info)

        Determine if a sim Can Not Be Impregnated.

        .. note:: Use :func:`~can_not_reproduce` for Pet Sims.
        .. note:: Will return False if the sim has the GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not be impregnated. False, if the Sim can be impregnated.
        :rtype: bool
        """
        return not CommonSimGenderOptionUtils.can_be_impregnated(sim_info)

    @staticmethod
    def can_create_pregnancy(sim_info: SimInfo) -> bool:
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
        return CommonTraitUtils.can_impregnate(sim_info) or CommonTraitUtils.can_be_impregnated(sim_info) or CommonTraitUtils.can_reproduce(sim_info)

    @staticmethod
    def can_reproduce(sim_info: SimInfo) -> bool:
        """can_reproduce(sim_info)

        Determine if a Pet Sim can reproduce.

        .. note:: Use :func:`~can_impregnate` and :func:`~can_be_impregnated` for Human Sims.
        .. note:: Will return False if the Pet Sim has the PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can reproduce. False, if the Sim can not reproduce.
        :rtype: bool
        """
        return CommonSimGenderOptionUtils.can_impregnate(sim_info) or CommonSimGenderOptionUtils.can_be_impregnated(sim_info)

    @staticmethod
    def can_not_reproduce(sim_info: SimInfo) -> bool:
        """can_not_reproduce(sim_info)

        Determine if a pet sim can reproduce.

        ..note:: Use :func:`~can_not_impregnate` and :func:`~can_not_be_impregnated` for Human Sims.
        .. note:: Will return False if the pet sim has the PREGNANCY_OPTIONS_PET_CAN_REPRODUCE trait.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can not reproduce. False, if the Sim can reproduce.
        :rtype: bool
        """
        return not CommonSimGenderOptionUtils.can_reproduce(sim_info)

    @staticmethod
    def uses_toilet_standing(sim_info: SimInfo) -> bool:
        """uses_toilet_standing(sim_info)

        Determine if a sim uses the toilet while standing.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim uses toilets while standing. False, if the Sim does not use toilets while standing.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)

    @staticmethod
    def uses_toilet_sitting(sim_info: SimInfo) -> bool:
        """uses_toilet_sitting(sim_info)

        Determine if a sim uses the toilet while sitting.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim uses toilets while sitting. False, if the Sim does not use toilets while sitting.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)

    @staticmethod
    def has_breasts(sim_info: SimInfo) -> bool:
        """has_breasts(sim_info)

        Determine if a Sim has breasts.

        .. note:: This will True if breasts are being forced on the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has breasts. False, if not.
        :rtype: bool
        """
        if CommonGenderUtils.is_female(sim_info) and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF):
            return True
        if CommonGenderUtils.is_male(sim_info) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON):
            return True
        return False

    @staticmethod
    def update_gender_options_to_vanilla_male(sim_info: SimInfo) -> bool:
        """update_gender_options_to_vanilla_male(sim_info)

        Update a Sim to the vanilla Sims 4 default gender options for Male Sims. (Masculine, Menswear Preference, etc.)

        .. note:: This will change the following things: Body Frame (Masculine), Clothing Preference (Masculine), Can Be Impregnated (False), Can Impregnate (True), Can Reproduce (True), Toilet Usage Posture (Standing), Voice Actor (MALE).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        CommonSimGenderOptionUtils.update_body_frame(sim_info, True)
        CommonSimGenderOptionUtils.update_clothing_preference(sim_info, True)
        CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, False)
        CommonSimGenderOptionUtils.update_can_impregnate(sim_info, True)
        CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
        CommonSimGenderOptionUtils.update_toilet_usage(sim_info, True)
        CommonSimVoiceUtils.set_to_default_male_voice(sim_info)
        return True

    @staticmethod
    def update_gender_options_to_vanilla_female(sim_info: SimInfo) -> bool:
        """update_gender_options_to_vanilla_female(sim_info)

        Update a Sim to the vanilla Sims 4 default gender options for Female Sims. (Feminine, Womenswear Preference, etc.)

        .. note:: This will change the following things: Body Frame (Feminine), Clothing Preference (Feminine), Can Be Impregnated (True), Can Impregnate (False), Can Reproduce (True), Toilet Usage Posture (Sitting), Voice Actor (FEMALE).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        CommonSimGenderOptionUtils.update_body_frame(sim_info, False)
        CommonSimGenderOptionUtils.update_clothing_preference(sim_info, False)
        CommonSimGenderOptionUtils.update_can_be_impregnated(sim_info, True)
        CommonSimGenderOptionUtils.update_can_impregnate(sim_info, False)
        CommonSimGenderOptionUtils.update_can_reproduce(sim_info, True)
        CommonSimGenderOptionUtils.update_toilet_usage(sim_info, False)
        CommonSimVoiceUtils.set_to_default_female_voice(sim_info)
        return True

    @staticmethod
    def update_has_breasts(sim_info: SimInfo, has_breasts: bool) -> bool:
        """update_has_breasts(sim_info, has_breasts)

        Give or Take Away the breasts of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param has_breasts: If True, the Sim will be given breasts.\
        If False, the Sim will not longer have breasts.
        :type has_breasts: bool
        :return: True, if the state of a Sim having breasts or not was changed. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
        CommonTraitUtils.remove_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
        if has_breasts:
            if CommonGenderUtils.is_male(sim_info):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_ON)
                CommonSimEventDispatcherService()._on_sim_change_gender_options_breasts(sim_info)
                return True
        else:
            if CommonGenderUtils.is_female(sim_info):
                CommonTraitUtils.add_trait(sim_info, CommonTraitId.BREASTS_FORCE_OFF)
                CommonSimEventDispatcherService()._on_sim_change_gender_options_breasts(sim_info)
                return True
        return False

    @staticmethod
    def update_body_frame(sim_info: SimInfo, masculine: bool) -> bool:
        """update_body_frame(sim_info, masculine)

        Update the Body Frame of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param masculine: If True, the Sim will get a Masculine frame.\
        If False, the Sim will get a Feminine frame.
        :type masculine: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if masculine:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_body_frame(sim_info)
        return True

    @staticmethod
    def update_clothing_preference(sim_info: SimInfo, prefer_menswear: bool) -> bool:
        """update_clothing_preference(sim_info, prefer_menswear)

        Update the Clothing Preference of a Sim.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param prefer_menswear: If True, the Sim will prefer Menswear.\
        If False, the Sim will prefer Womenswear.
        :type prefer_menswear: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if prefer_menswear:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_clothing_preference(sim_info)
        return True

    @staticmethod
    def update_can_be_impregnated(sim_info: SimInfo, can_be_impregnated: bool) -> bool:
        """update_can_be_impregnated(sim_info, can_be_impregnated)

        Update a Sims ability to be impregnated by other Sims.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_be_impregnated: If True, the Sim will have the ability to be impregnated.\
        If False, the Sim will not have the ability to be impregnated.
        :type can_be_impregnated: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if can_be_impregnated:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_can_be_impregnated(sim_info)
        return True

    @staticmethod
    def update_can_impregnate(sim_info: SimInfo, can_impregnate: bool) -> bool:
        """update_can_impregnate(sim_info, can_impregnate)

        Update a Sims ability to impregnate other Sims.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_impregnate: If True, the Sim will have the ability to impregnate other Sims.\
        If False, the Sim will not have the ability to impregnate other Sims.
        :type can_impregnate: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if can_impregnate:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_can_impregnate(sim_info)
        return True

    @staticmethod
    def update_can_reproduce(sim_info: SimInfo, can_reproduce: bool) -> bool:
        """update_can_reproduce(sim_info, can_reproduce)

        Update a Sims ability to reproduce.

        .. note:: Will only update Pet Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_reproduce: If True, the Sim will have the ability to reproduce.\
        If False, the Sim will not have the ability to reproduce.
        :type can_reproduce: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_pet(sim_info):
            return False
        if can_reproduce:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_can_reproduce(sim_info)
        return True

    @staticmethod
    def update_toilet_usage(sim_info: SimInfo, uses_toilet_standing: bool) -> bool:
        """update_toilet_usage(sim_info, uses_toilet_standing)

        Update how a Sim uses the toilet. i.e. Toilet Standing or Toilet Sitting.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param uses_toilet_standing: If True, the Sim will use toilets while standing and will not use toilets while sitting.\
        If False, the Sim will use toilets while sitting and will not use toilets while standing.
        :type uses_toilet_standing: bool
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if uses_toilet_standing:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
        else:
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return True

    @staticmethod
    def set_can_use_toilet_standing(sim_info: SimInfo, can_use_toilet_standing: bool) -> bool:
        """set_can_use_toilet_standing(sim_info, can_use_toilet_standing)

        Set whether a Sim can use a toilet while standing or not.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_use_toilet_standing: Whether or not the Sim will be able to use a toilet while standing.
        :type can_use_toilet_standing: bool
        :return: True, if successful set. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if can_use_toilet_standing and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING):
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
        elif CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING):
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_STANDING)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return True

    @staticmethod
    def set_can_use_toilet_sitting(sim_info: SimInfo, can_use_toilet_sitting: bool) -> bool:
        """set_can_use_toilet_sitting(sim_info, can_use_toilet_sitting)

        Set whether a Sim can use a toilet while sitting or not.

        .. note:: Will only update Human Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param can_use_toilet_sitting: Whether or not the Sim will be able to use a toilet while sitting.
        :type can_use_toilet_sitting: bool
        :return: True, if successful set. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not CommonSpeciesUtils.is_human(sim_info):
            return False
        if can_use_toilet_sitting and not CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING):
            CommonTraitUtils.add_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
        elif CommonTraitUtils.has_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING):
            CommonTraitUtils.remove_trait(sim_info, CommonTraitId.GENDER_OPTIONS_TOILET_SITTING)
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender_options_toilet_usage(sim_info)
        return True
