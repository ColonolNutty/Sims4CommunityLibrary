"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from sims.pregnancy.pregnancy_enums import PregnancyOrigin
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.common_object_state_value_ids import CommonObjectStateValueId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from statistics.commodity import Commodity


class CommonSimPregnancyUtils(HasClassLog):
    """Utilities for manipulating the pregnancy status of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_pregnancy_utils'
    
    @classmethod
    def is_pregnant(cls, sim_info: SimInfo) -> bool:
        """is_pregnant(sim_info)

        Determine if the a Sim is pregnant.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the specified Sim is pregnant. False, if not.
        :rtype: bool
        """
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        return pregnancy_tracker.is_pregnant

    @classmethod
    def has_permission_for_pregnancies(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_permission_for_pregnancies(sim_info)

        Determine if a Sim has the permissions to cause a Pregnancy or to become Pregnant. (Regardless of traits)

        .. note:: In the vanilla game, only Adult and Elder Sims have permission for pregnancies.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if the test fails.
        :rtype: CommonTestResult
        """
        if CommonAgeUtils.is_adult_or_elder(sim_info):
            return CommonTestResult(True, reason=f'{sim_info} has permission for pregnancies. They are either an Adult or an Elder Sim.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERMISSION_FOR_PREGNANCIES_NOT_ADULT_OR_ELDER, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} does not have permission for pregnancies. They are neither an Adult nor an Elder Sim.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERMISSION_FOR_PREGNANCIES_NOT_ADULT_OR_ELDER, tooltip_tokens=(sim_info,))

    @classmethod
    def has_permission_for_pregnancies_with(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> CommonTestResult:
        """has_permission_for_pregnancies_with(sim_info_a, sim_info_b)

        Determine if Sim A has the permissions to cause a Pregnancy with Sim B or to become pregnant from Sim B.

        .. note:: In the vanilla game, only Adult and Elder Sims of the same species have permission for pregnancies with each other.

        :param sim_info_a: An instance of a Sim. (Sim A)
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim. (Sim B)
        :type sim_info_b: SimInfo
        :return: The result of the test. True, if the test passes. False, if the test fails.
        :rtype: CommonTestResult
        """
        sim_a_has_permission = cls.has_permission_for_pregnancies(sim_info_a)
        if not sim_a_has_permission:
            return CommonTestResult(
                False,
                reason=f'{sim_info_a} does not have permission for pregnancies with {sim_info_b}. {sim_a_has_permission.reason}',
                tooltip_text=CommonStringId.STRING_COMMA_SPACE_STRING,
                tooltip_tokens=(
                    CommonLocalizationUtils.create_localized_tooltip(
                        CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERMISSION_FOR_PREGNANCIES_WITH_SIM,
                        tooltip_tokens=(sim_info_a, sim_info_b)
                    ),
                    CommonLocalizationUtils.create_localized_tooltip(
                        sim_a_has_permission.tooltip_text,
                        tooltip_tokens=sim_a_has_permission.tooltip_tokens
                    )
                )
            )
        sim_b_has_permission = cls.has_permission_for_pregnancies(sim_info_b)
        if not sim_b_has_permission:
            return CommonTestResult(
                False,
                reason=f'{sim_info_a} does not have permission for pregnancies with {sim_info_b}. {sim_b_has_permission.reason}',
                tooltip_text=CommonStringId.STRING_COMMA_SPACE_STRING,
                tooltip_tokens=(
                    CommonLocalizationUtils.create_localized_tooltip(
                        CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERMISSION_FOR_PREGNANCIES_WITH_SIM,
                        tooltip_tokens=(sim_info_a, sim_info_b)
                    ),
                    CommonLocalizationUtils.create_localized_tooltip(
                        sim_b_has_permission.tooltip_text,
                        tooltip_tokens=sim_b_has_permission.tooltip_tokens
                    )
                )
            )
        if not CommonSpeciesUtils.are_same_species(sim_info_a, sim_info_b):
            # If both Sims are dogs, that is an ok combination, even though their species do not match.
            if not CommonSpeciesUtils.is_dog(sim_info_a) or not CommonSpeciesUtils.is_dog(sim_info_b):
                return CommonTestResult(
                    False,
                    reason=f'{sim_info_a} does not have permission for pregnancies with {sim_info_b}. {sim_info_a} and {sim_info_b} are not the same species.',
                    tooltip_text=CommonStringId.STRING_COMMA_SPACE_STRING,
                    tooltip_tokens=(
                        CommonLocalizationUtils.create_localized_tooltip(
                            CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERMISSION_FOR_PREGNANCIES_WITH_SIM,
                            tooltip_tokens=(sim_info_a, sim_info_b)
                        ),
                        CommonLocalizationUtils.create_localized_tooltip(
                            CommonStringId.S4CL_SIM_IS_NOT_THE_SAME_SPECIES_AS_SIM,
                            tooltip_tokens=(sim_info_a, sim_info_b)
                        )
                    )
                )
        romantic_relationships_result = CommonRelationshipUtils.has_permission_for_romantic_relationship_with(sim_info_a, sim_info_b)
        if not romantic_relationships_result:
            return CommonTestResult(
                False,
                reason=f'{sim_info_a} does not have permission for pregnancies with {sim_info_b}. {romantic_relationships_result.reason}',
                tooltip_text=CommonStringId.STRING_COMMA_SPACE_STRING,
                tooltip_tokens=(
                    CommonLocalizationUtils.create_localized_tooltip(
                        CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERMISSION_FOR_PREGNANCIES_WITH_SIM,
                        tooltip_tokens=(sim_info_a, sim_info_b)
                    ),
                    CommonLocalizationUtils.create_localized_tooltip(
                        romantic_relationships_result.tooltip_text,
                        tooltip_tokens=romantic_relationships_result.tooltip_tokens
                    )
                )
            )
        return CommonTestResult(True, reason=f'{sim_info_a} has permission for pregnancies with {sim_info_b}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERMISSION_FOR_PREGNANCIES_WITH_SIM, tooltip_tokens=(sim_info_a, sim_info_b))

    @classmethod
    def get_pregnancy_partner(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_pregnancy_partner(sim_info)

        Retrieve the Sim that caused a Sim to become pregnant.

        :param sim_info: The Sim to get the partner of.
        :type sim_info: SimInfo
        :return: The Sim that impregnated the specified Sim or None if not found.
        :rtype: Union[SimInfo, None]
        """
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return None
        partner_sim = pregnancy_tracker.get_partner()
        if partner_sim is None:
            return None
        return CommonSimUtils.get_sim_info(partner_sim)

    @classmethod
    def start_pregnancy(cls, sim_info: SimInfo, partner_sim_info: SimInfo, pregnancy_origin: PregnancyOrigin = PregnancyOrigin.DEFAULT) -> bool:
        """start_pregnancy(sim_info, partner_sim_info, pregnancy_origin=PregnancyOrigin.DEFAULT)

        Start a pregnancy between a Sim and a Partner Sim.

        :param sim_info: The Sim getting pregnant.
        :type sim_info: SimInfo
        :param partner_sim_info: The Sim that is getting the other Sim pregnant.
        :type partner_sim_info: SimInfo
        :param pregnancy_origin: The origin of the pregnancy. Default is PregnancyOrigin.DEFAULT.
        :type pregnancy_origin: PregnancyOrigin, optional
        :return: True, if the Sim is successfully impregnated by the Partner Sim. False, if not.
        :rtype: bool
        """
        if not CommonHouseholdUtils.has_free_household_slots(sim_info):
            return False
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        pregnancy_tracker.start_pregnancy(sim_info, partner_sim_info, pregnancy_origin=pregnancy_origin, single_sim_is_allowed=sim_info is partner_sim_info)
        pregnancy_tracker.clear_pregnancy_visuals()
        pregnancy_stat = cls.determine_pregnancy_statistic(sim_info)
        if pregnancy_stat is not None:
            CommonSimStatisticUtils.set_statistic_value(sim_info, pregnancy_stat, 1.0)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is not None:
            CommonObjectStateUtils.set_object_state(sim, CommonObjectStateValueId.PREGNANT_NOT_SHOWING)
        return True

    @classmethod
    def induce_labor_in_sim(cls, sim_info: SimInfo) -> bool:
        """induce_labor(sim_info)

        Induce Labor in a pregnant Sim.

        :param sim_info: The Sim to go into labor.
        :type sim_info: SimInfo
        :return: True, if labor was induced successfully. False, if not.
        """
        if sim_info is None or not cls.is_pregnant(sim_info):
            return False
        pregnancy_stat = cls.determine_pregnancy_statistic(sim_info)
        if pregnancy_stat is not None:
            CommonSimStatisticUtils.set_statistic_value(sim_info, pregnancy_stat, 100.0)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is not None:
            CommonObjectStateUtils.set_object_state(sim, CommonObjectStateValueId.PREGNANT_IN_LABOR)
        buff_id = cls.get_in_labor_buff(sim_info)
        if buff_id != -1:
            result = CommonBuffUtils.add_buff(sim_info, buff_id, buff_reason=CommonStringId.S4CL_BUFF_REASON_FROM_DEBUG)
            return result.result
        return True

    @classmethod
    def clear_pregnancy(cls, sim_info: SimInfo) -> bool:
        """clear_pregnancy(sim_info)

        Clear the pregnancy status of a Sim.

        :param sim_info: The Sim being cleared.
        :type sim_info: SimInfo
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        sim_info.pregnancy_tracker.clear_pregnancy()
        pregnancy_stat = cls.determine_pregnancy_statistic(sim_info)
        if pregnancy_stat is not None:
            CommonSimStatisticUtils.remove_statistic(sim_info, pregnancy_stat)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is not None:
            CommonObjectStateUtils.set_object_state(sim, CommonObjectStateValueId.PREGNANT_NOT_PREGNANT)
        return True

    @classmethod
    def can_be_impregnated(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_be_impregnated(sim_info)

        Determine if a Sim can be impregnated.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The result of testing. True, if they can. False, if they cannot.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        can_be_impregnated_trait = cls.determine_can_be_impregnated_trait(sim_info)
        can_not_be_impregnated_trait = cls.determine_can_not_be_impregnated_trait(sim_info)
        if can_be_impregnated_trait is None:
            return CommonTestResult(False, reason=f'No Can Be Impregnated trait was found for Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_NO_CAN_BE_IMPREGNATED_TRAIT_FOUND_FOR_SIM, tooltip_tokens=(sim_info,))
        if can_not_be_impregnated_trait is None:
            return CommonTestResult(False, reason=f'No Cannot Be Impregnated trait was found for Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_NO_CANNOT_BE_IMPREGNATED_TRAIT_FOUND_FOR_SIM, tooltip_tokens=(sim_info,))
        if CommonSpeciesUtils.is_animal(sim_info):
            if not CommonSpeciesUtils.is_horse(sim_info):
                if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
                    return CommonTestResult(False, reason=f'Animal Sim {sim_info} had the Cannot Reproduce trait.', tooltip_text=CommonStringId.S4CL_SIM_HAS_THE_CANNOT_REPRODUCE_TRAIT, tooltip_tokens=(sim_info,))
                if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                    return CommonTestResult(False, reason=f'Animal Sim {sim_info} did not have the Can Reproduce trait.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_THE_CAN_REPRODUCE_TRAIT, tooltip_tokens=(sim_info,))

        if CommonTraitUtils.has_trait(sim_info, can_not_be_impregnated_trait):
            return CommonTestResult(False, reason=f'{sim_info} had the Cannot Be Impregnated trait.', tooltip_text=CommonStringId.S4CL_SIM_HAS_THE_CANNOT_BE_IMPREGNATED_TRAIT, tooltip_tokens=(sim_info,))
        if not CommonTraitUtils.has_trait(sim_info, can_be_impregnated_trait):
            return CommonTestResult(False, reason=f'{sim_info} did not have the Can Be Impregnated trait.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_THE_CAN_BE_IMPREGNATED_TRAIT, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} can be impregnated by other Sims.', tooltip_text=CommonStringId.S4CL_SIM_CAN_BE_IMPREGNATED_BY_OTHER_SIMS, tooltip_tokens=(sim_info,))

    @classmethod
    def can_impregnate(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_impregnate(sim_info)

        Determine if a Sim can impregnate other sims.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The result of testing. True, if they can. False, if they cannot.
        :rtype: CommonTestResult
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        can_impregnate_trait = cls.determine_can_impregnate_trait(sim_info)
        can_not_impregnate_trait = cls.determine_can_not_impregnate_trait(sim_info)
        if can_impregnate_trait is None:
            return CommonTestResult(False, reason=f'No Can Impregnate trait was found for Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_NO_CAN_IMPREGNATE_TRAIT_FOUND_FOR_SIM, tooltip_tokens=(sim_info,))
        if can_not_impregnate_trait is None:
            return CommonTestResult(False, reason=f'No Cannot Impregnate trait was found for Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_NO_CANNOT_IMPREGNATE_TRAIT_FOUND_FOR_SIM, tooltip_tokens=(sim_info,))
        if CommonSpeciesUtils.is_animal(sim_info):
            if not CommonSpeciesUtils.is_horse(sim_info):
                if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
                    return CommonTestResult(False, reason=f'{sim_info} had the Cannot Reproduce trait.', tooltip_text=CommonStringId.S4CL_SIM_HAS_THE_CANNOT_REPRODUCE_TRAIT, tooltip_tokens=(sim_info,))
                if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                    return CommonTestResult(False, reason=f'{sim_info} did not have the Can Reproduce trait.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_THE_CAN_REPRODUCE_TRAIT, tooltip_tokens=(sim_info,))

        if CommonTraitUtils.has_trait(sim_info, can_not_impregnate_trait):
            return CommonTestResult(False, reason=f'{sim_info} had the Cannot Impregnate trait.', tooltip_text=CommonStringId.S4CL_SIM_HAS_THE_CANNOT_IMPREGNATE_TRAIT, tooltip_tokens=(sim_info,))
        if not CommonTraitUtils.has_trait(sim_info, can_impregnate_trait):
            return CommonTestResult(False, reason=f'{sim_info} did not have the Can Impregnate trait', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_THE_CAN_IMPREGNATE_TRAIT, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} can impregnate other Sims.', tooltip_text=CommonStringId.S4CL_SIM_CAN_IMPREGNATE_OTHER_SIMS, tooltip_tokens=(sim_info,))

    @classmethod
    def get_partner_of_pregnant_sim(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_partner_of_pregnant_sim(sim_info)

        Retrieve a SimInfo object of the Sim that impregnated the specified Sim.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The Sim that has impregnated the specified Sim or None if the Sim does not have a partner.
        :rtype: Union[SimInfo, None]
        """
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return None
        return pregnancy_tracker.get_partner()

    @classmethod
    def set_pregnancy_progress(cls, sim_info: SimInfo, value: float):
        """set_pregnancy_progress(sim_info, value)

        Set the pregnancy progress of a Sim.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :param value: The value to set the progress to.
        :type value: float
        :return: The current progress of the pregnancy of a Sim.
        :rtype: float
        """
        if value > 100.0:
            value = 100.0
        if value < 0.0:
            value = 0.0
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None or not cls.is_pregnant(sim_info):
            return
        pregnancy_commodity_type = pregnancy_tracker.PREGNANCY_COMMODITY_MAP.get(CommonSpeciesUtils.get_species(sim_info))
        statistic_tracker = sim_info.get_tracker(pregnancy_commodity_type)
        pregnancy_commodity: Commodity = statistic_tracker.get_statistic(pregnancy_commodity_type, add=False)
        if not pregnancy_commodity:
            return
        pregnancy_commodity.set_value(value)

    @classmethod
    def get_pregnancy_progress(cls, sim_info: SimInfo) -> float:
        """get_pregnancy_progress(sim_info)

        Retrieve the pregnancy progress of a Sim.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The current progress of the pregnancy of a Sim.
        :rtype: float
        """
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None or not cls.is_pregnant(sim_info):
            return 0.0
        pregnancy_commodity_type = pregnancy_tracker.PREGNANCY_COMMODITY_MAP.get(CommonSpeciesUtils.get_species(sim_info))
        statistic_tracker = sim_info.get_tracker(pregnancy_commodity_type)
        pregnancy_commodity = statistic_tracker.get_statistic(pregnancy_commodity_type, add=False)
        if not pregnancy_commodity:
            return 0.0
        return pregnancy_commodity.get_value()

    @classmethod
    def get_pregnancy_rate(cls, sim_info: SimInfo) -> float:
        """get_pregnancy_rate(sim_info)

        Retrieve the rate at which pregnancy progresses.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The rate at which the pregnancy state of a Sim is progressing.
        :rtype: float
        """
        pregnancy_tracker = cls._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return 0.0
        return pregnancy_tracker.PREGNANCY_RATE

    @classmethod
    def get_in_labor_buff(cls, sim_info: SimInfo) -> Union[int, CommonBuffId]:
        """get_in_labor_buff(sim_info)

        Retrieve an In Labor buff appropriate for causing the Sim to go into labor (Give Birth).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The decimal identifier of a Buff that will cause the specified Sim to go into labor. If no appropriate Buff is found, -1 will be returned.
        :rtype: Union[int, CommonBuffId]
        """
        log = cls.get_log()
        from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        log.debug('Locating appropriate Buff for inducing labor in \'{}\'.'.format(sim_name))
        is_female = CommonGenderUtils.is_female(sim_info)
        if CommonSpeciesUtils.is_human(sim_info):
            log.debug('\'{}\' is Human.'.format(sim_name))
            if is_female:
                log.debug('\'{}\' is Female.'.format(sim_name))
                return CommonBuffId.PREGNANCY_IN_LABOR
            else:
                log.debug('\'{}\' is Male.'.format(sim_name))
                return CommonBuffId.PREGNANCY_IN_LABOR_MALE
        elif CommonSpeciesUtils.is_dog(sim_info):
            log.debug('\'{}\' is a Dog.'.format(sim_name))
            if is_female:
                log.debug('\'{}\' is Female.'.format(sim_name))
                return CommonBuffId.PREGNANCY_IN_LABOR_PET_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            log.debug('\'{}\' is a Cat.'.format(sim_name))
            if is_female:
                log.debug('\'{}\' is Female.'.format(sim_name))
                return CommonBuffId.PREGNANCY_IN_LABOR_PET_CAT
        elif CommonSpeciesUtils.is_horse(sim_info):
            log.debug('\'{}\' is a Horse.'.format(sim_name))
            if is_female:
                log.debug('\'{}\' is Female.'.format(sim_name))
                return CommonBuffId.PREGNANCY_IN_LABOR_PET_HORSE
        log.debug('No appropriate Buff located to induce labor in \'{}\'.'.format(sim_name))
        return -1

    @classmethod
    def get_pregnancy_tracker(cls, sim_info: SimInfo) -> Union[PregnancyTracker, None]:
        """get_pregnancy_tracker(sim_info)

        Retrieve the tracker for tracking pregnancy of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The pregnancy tracker for the Sim or None if the Sim does not have a pregnancy tracker.
        :rtype: Union[PregnancyTracker, None]
        """
        return cls._get_pregnancy_tracker(sim_info)

    @classmethod
    def _get_pregnancy_tracker(cls, sim_info: SimInfo) -> Union[PregnancyTracker, None]:
        if sim_info is None:
            return None
        return sim_info.pregnancy_tracker

    @classmethod
    def determine_pregnancy_statistic(cls, sim_info: SimInfo) -> Union[CommonStatisticId, None]:
        """determine_pregnancy_statistic(sim_info)

        Determine the statistic that would indicate the pregnancy progress of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The statistic that would indicate the pregnancy progress of the Sim or None if no trait is found.
        :rtype: Union[CommonStatisticId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonStatisticId.PREGNANCY
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonStatisticId.PREGNANCY_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonStatisticId.PREGNANCY_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonStatisticId.PREGNANCY_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonStatisticId.PREGNANCY
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonStatisticId.PREGNANCY_HORSE
        return None

    @classmethod
    def determine_can_impregnate_trait(cls, sim_info: SimInfo) -> Union[CommonTraitId, None]:
        """determine_can_impregnate_trait(sim_info)

        Determine the trait that would indicate a Sim can impregnate other Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The trait that would indicate the Sim can impregnate other Sims or None if no trait is found.
        :rtype: Union[CommonTraitId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_LARGE_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_SMALL_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_FOX
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_IMPREGNATE_HORSE
        return None

    @classmethod
    def determine_can_not_impregnate_trait(cls, sim_info: SimInfo) -> Union[CommonTraitId, None]:
        """determine_can_not_impregnate_trait(sim_info)

        Determine the trait that would indicate a Sim can not impregnate other Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The trait that would indicate the Sim can not impregnate other Sims or None if no trait is found.
        :rtype: Union[CommonTraitId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_LARGE_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_SMALL_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_FOX
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_IMPREGNATE_HORSE
        return None

    @classmethod
    def determine_can_be_impregnated_trait(cls, sim_info: SimInfo) -> Union[CommonTraitId, None]:
        """determine_can_be_impregnated_trait(sim_info)

        Determine the trait that would indicate a Sim can be impregnated by other Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The trait that would indicate the Sim can be impregnated by other Sims or None if no trait is found.
        :rtype: Union[CommonTraitId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_LARGE_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_SMALL_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_FOX
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_BE_IMPREGNATED_HORSE
        return None

    @classmethod
    def determine_can_not_be_impregnated_trait(cls, sim_info: SimInfo) -> Union[CommonTraitId, None]:
        """determine_can_not_be_impregnated_trait(sim_info)

        Determine the trait that would indicate a Sim can not be impregnated by other Sims.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The trait that would indicate the Sim can not be impregnated by other Sims or None if no trait is found.
        :rtype: Union[CommonTraitId, None]
        """
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonTraitId.GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_LARGE_DOG
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_SMALL_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_CAT
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_FOX
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonTraitId.S4CL_GENDER_OPTIONS_PREGNANCY_CAN_NOT_BE_IMPREGNATED_HORSE
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_pregnancy_partner',
    'Print the Sim that got a Sim pregnant. If they are pregnant.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
)
def _common_print_pregnancy_partner(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to print the pregnancy partner of {sim_info}.')
    partner_sim_info = CommonSimPregnancyUtils.get_pregnancy_partner(sim_info)
    if partner_sim_info is None:
        output(f'No Sim found to have impregnated {sim_info}.')
    else:
        output(f'{partner_sim_info} is the Sim that impregnated {sim_info}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.stop_pregnancy',
    'End the pregnancy of a Sim. Does your Sim have trouble with pregnancy? Then Stop It!',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.pregnancy_begone',
    )
)
def _common_command_stop_pregnancy(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to stop the pregnancy of {sim_info}.')
    result = CommonSimPregnancyUtils.clear_pregnancy(sim_info)
    if result:
        output(f'SUCCESS: Successfully stopped the pregnancy of {sim_info}.')
    else:
        output(f'FAILED: Failed to stop the pregnancy of {sim_info}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_pregnancy_progress',
    'Set the progress of a Sims pregnancy.',
    command_arguments=(
        CommonConsoleCommandArgument('value', 'Percentage', 'The percentage of progress.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    ),
)
def _common_command_set_pregnancy_progress(output: CommonConsoleCommandOutput, value: float, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to set pregnancy progress of {sim_info} to {value}.')
    if not CommonSimPregnancyUtils.is_pregnant(sim_info):
        output(f'{sim_info} is not pregnant.')
        return
    CommonSimPregnancyUtils.set_pregnancy_progress(sim_info, value)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.stop_all_pregnancies',
    'End the pregnancy of all Sims. Wipe away those pregnancies like they never happened.',
    command_aliases=(
        's4clib.pregnancies_begone',
    )
)
def _common_command_stop_all_pregnancies(output: CommonConsoleCommandOutput):
    output('Attempting to stop the pregnancies of all available Sims. This may take awhile.')
    sim_count = 0
    for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=CommonSimPregnancyUtils.is_pregnant):
        # noinspection PyBroadException
        try:
            if not CommonSimPregnancyUtils.clear_pregnancy(sim_info):
                output(f'FAILED: Failed to stop pregnancy of {sim_info}')
                continue
            output(f'SUCCESS: Successfully stopped pregnancy of {sim_info}')
            sim_count += 1
        except Exception as ex:
            output(f'ERROR: Failed to stop the pregnancy of {sim_info}. {ex}')
    output(f'Stopped the pregnancies of {sim_count} Sim(s)')
