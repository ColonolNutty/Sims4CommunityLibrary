"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.components.state import StateComponent
from server_commands.argument_helpers import OptionalTargetParam
from sims.pregnancy.pregnancy_enums import PregnancyOrigin
from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4.resources import Types
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_pregnancy')


class CommonSimPregnancyUtils:
    """Utilities for manipulating the pregnancy status of Sims.

    """
    @staticmethod
    def is_pregnant(sim_info: SimInfo) -> bool:
        """is_pregnant(sim_info)

        Determine if the a Sim is pregnant.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the specified Sim is pregnant. False, if not.
        :rtype: bool
        """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        return pregnancy_tracker.is_pregnant

    @staticmethod
    def start_pregnancy(sim_info: SimInfo, partner_sim_info: SimInfo, pregnancy_origin: PregnancyOrigin=PregnancyOrigin.DEFAULT) -> bool:
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
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        pregnancy_tracker.start_pregnancy(sim_info, partner_sim_info, pregnancy_origin=pregnancy_origin)
        pregnancy_tracker.clear_pregnancy_visuals()
        CommonSimStatisticUtils.set_statistic_value(sim_info, CommonStatisticId.PREGNANCY, 1.0)
        return True

    @staticmethod
    def induce_labor_in_sim(sim_info: SimInfo) -> bool:
        """induce_labor(sim_info)

        Induce Labor in a pregnant Sim.

        :param sim_info: The Sim to go into labor.
        :type sim_info: SimInfo
        :return: True, if labor was induced successfully. False, if not.
        """
        if sim_info is None or not CommonSimPregnancyUtils.is_pregnant(sim_info):
            return False
        # Pregnant_InLabor
        state = CommonResourceUtils.load_instance(Types.OBJECT_STATE, 75273)
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        state_component: StateComponent = sim.state_component
        state_component.set_state(state.state, state)
        return True

    @staticmethod
    def clear_pregnancy(sim_info: SimInfo) -> bool:
        """clear_pregnancy(sim_info)

        Clear the pregnancy status of a Sim.

        :param sim_info: The Sim being cleared.
        :type sim_info: SimInfo
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return False
        sim_info.pregnancy_tracker.clear_pregnancy()
        CommonSimStatisticUtils.remove_statistic(sim_info, CommonStatisticId.PREGNANCY)
        return True

    @staticmethod
    def can_be_impregnated(sim_info: SimInfo) -> bool:
        """can_be_impregnated(sim_info)

        Determine if a Sim can be impregnated.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: True, if they can. False, if they cannot.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        can_be_impregnated_trait = CommonSimPregnancyUtils.determine_can_be_impregnated_trait(sim_info)
        can_not_be_impregnated_trait = CommonSimPregnancyUtils.determine_can_not_be_impregnated_trait(sim_info)
        if can_be_impregnated_trait is None or can_not_be_impregnated_trait is None:
            return False
        if CommonSpeciesUtils.is_pet(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
                return False
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                return False

        if CommonTraitUtils.has_trait(sim_info, can_not_be_impregnated_trait):
            return False
        return CommonTraitUtils.has_trait(sim_info, can_be_impregnated_trait)

    @staticmethod
    def can_impregnate(sim_info: SimInfo) -> bool:
        """can_impregnate(sim_info)

        Determine if a Sim can impregnate other sims.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: True, if they can. False, if they cannot.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        can_impregnate_trait = CommonSimPregnancyUtils.determine_can_impregnate_trait(sim_info)
        can_not_impregnate_trait = CommonSimPregnancyUtils.determine_can_not_impregnate_trait(sim_info)
        if can_impregnate_trait is None or can_not_impregnate_trait is None:
            return False
        if CommonSpeciesUtils.is_pet(sim_info):
            if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_NOT_REPRODUCE):
                return False
            if not CommonTraitUtils.has_trait(sim_info, CommonTraitId.PREGNANCY_OPTIONS_PET_CAN_REPRODUCE):
                return False

        if CommonTraitUtils.has_trait(sim_info, can_not_impregnate_trait):
            return False
        return CommonTraitUtils.has_trait(sim_info, can_impregnate_trait)

    @staticmethod
    def get_partner_of_pregnant_sim(sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_partner_of_pregnant_sim(sim_info)

        Retrieve a SimInfo object of the Sim that impregnated the specified Sim.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The Sim that has impregnated the specified Sim or None if the Sim does not have a partner.
        :rtype: Union[SimInfo, None]
        """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return None
        return pregnancy_tracker.get_partner()

    @staticmethod
    def get_pregnancy_progress(sim_info: SimInfo) -> float:
        """get_pregnancy_progress(sim_info)

        Retrieve the pregnancy progress of a Sim.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The current progress of the pregnancy of a Sim.
        :rtype: float
        """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None or not CommonSimPregnancyUtils.is_pregnant(sim_info):
            return 0.0
        pregnancy_commodity_type = pregnancy_tracker.PREGNANCY_COMMODITY_MAP.get(CommonSpeciesUtils.get_species(sim_info))
        statistic_tracker = sim_info.get_tracker(pregnancy_commodity_type)
        pregnancy_commodity = statistic_tracker.get_statistic(pregnancy_commodity_type, add=False)
        if not pregnancy_commodity:
            return 0.0
        return pregnancy_commodity.get_value()

    @staticmethod
    def get_pregnancy_rate(sim_info: SimInfo) -> float:
        """get_pregnancy_rate(sim_info)

        Retrieve the rate at which pregnancy progresses.

        :param sim_info: The Sim being checked.
        :type sim_info: SimInfo
        :return: The rate at which the pregnancy state of a Sim is progressing.
        :rtype: float
        """
        pregnancy_tracker = CommonSimPregnancyUtils._get_pregnancy_tracker(sim_info)
        if pregnancy_tracker is None:
            return 0.0
        return pregnancy_tracker.PREGNANCY_RATE

    @staticmethod
    def get_in_labor_buff(sim_info: SimInfo) -> Union[int, CommonBuffId]:
        """get_in_labor_buff(sim_info)

        Retrieve an In Labor buff appropriate for causing the Sim to go into labor (Give Birth).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The decimal identifier of a Buff that will cause the specified Sim to go into labor. If no appropriate Buff is found, -1 will be returned.
        :rtype: Union[int, CommonBuffId]
        """
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
        log.debug('No appropriate Buff located to induce labor in \'{}\'.'.format(sim_name))
        return -1

    @staticmethod
    def _get_pregnancy_tracker(sim_info: SimInfo) -> Union[PregnancyTracker, None]:
        if sim_info is None:
            return None
        return sim_info.pregnancy_tracker

    @staticmethod
    def determine_can_impregnate_trait(sim_info: SimInfo) -> Union[CommonTraitId, None]:
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
        return None

    @staticmethod
    def determine_can_not_impregnate_trait(sim_info: SimInfo) -> Union[CommonTraitId, None]:
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
        return None

    @staticmethod
    def determine_can_be_impregnated_trait(sim_info: SimInfo) -> Union[CommonTraitId, None]:
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
        return None

    @staticmethod
    def determine_can_not_be_impregnated_trait(sim_info: SimInfo) -> Union[CommonTraitId, None]:
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
        return None


@Command('s4clib.stop_pregnancy', command_type=CommandType.Live)
def _common_command_stop_pregnancy(opt_sim: OptionalTargetParam=None, _connection: int=None):
    output = CheatOutput(_connection)
    from server_commands.argument_helpers import get_optional_target
    sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    sim_name = CommonSimNameUtils.get_full_name(sim_info)
    output('Attempting to stop the pregnancy of {}.'.format(sim_name))
    result = CommonSimPregnancyUtils.clear_pregnancy(sim_info)
    if result:
        output('Successfully stopped the pregnancy of {}.'.format(sim_name))
    else:
        output('Failed to stop the pregnancy of {}.'.format(sim_name))


@Command('s4clib.stop_all_pregnancies', command_type=CommandType.Live)
def _common_command_stop_all_pregnancies(_connection: int=None):
    output = CheatOutput(_connection)
    output('Attempting to stop the pregnancies of all available Sims. This may take awhile.')
    for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=CommonSimPregnancyUtils.is_pregnant):
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        if not CommonSimPregnancyUtils.clear_pregnancy(sim_info):
            output('Failed to stop pregnancy of {}'.format(sim_name))
            continue
        output('Successfully stopped pregnancy of {}'.format(sim_name))
    output('Stopped all pregnancies of all Sims')
