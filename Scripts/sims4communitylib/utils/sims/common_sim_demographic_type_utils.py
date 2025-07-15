"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, TYPE_CHECKING, Dict, List, Callable, Union, Iterator

from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.utils.math.common_bitwise_utils import CommonBitwiseUtils
from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

if TYPE_CHECKING:
    from sims4communitylib.enums.common_age import CommonAge
    from sims4communitylib.enums.common_gender import CommonGender
    from sims4communitylib.enums.common_species import CommonSpecies
    from sims4communitylib.enums.common_occult_type import CommonOccultType
    from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType


class CommonSimDemographicTypeUtils(_HasS4CLClassLog):
    """ Utilities for Sim Demographic types. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_demographic_type_utils'

    @classmethod
    def determine_sim_demographic_flags(cls, sim_info: SimInfo) -> 'CommonSimDemographicType':
        """Determine the demographics of a Sim as flags."""
        from sims4communitylib.enums.common_age import CommonAge
        from sims4communitylib.enums.common_gender import CommonGender
        from sims4communitylib.enums.common_species import CommonSpecies
        value: 'CommonSimDemographicType' = cls.convert_from_age(CommonAge.get_age(sim_info))
        value = CommonBitwiseUtils.add_flags(value, cls.convert_from_species(CommonSpecies.get_species(sim_info)))
        value = CommonBitwiseUtils.add_flags(value, cls.convert_from_gender(CommonGender.get_gender(sim_info)))
        value = CommonBitwiseUtils.add_flags(value, cls.convert_from_occult_type(CommonSimOccultTypeUtils.determine_current_occult_type(sim_info)))
        return value

    @classmethod
    def determine_sim_demographics(cls, sim_info: SimInfo) -> Tuple['CommonSimDemographicType']:
        """Determine the demographics of a Sim as a collection."""
        from sims4communitylib.enums.common_age import CommonAge
        from sims4communitylib.enums.common_gender import CommonGender
        from sims4communitylib.enums.common_species import CommonSpecies
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        values: List['CommonSimDemographicType'] = list()
        values.append(cls.convert_from_species(CommonSpecies.get_species(sim_info)))
        values.append(cls.convert_from_age(CommonAge.get_age(sim_info)))
        values.append(cls.convert_from_gender(CommonGender.get_gender(sim_info)))
        values.append(cls.convert_from_occult_type(CommonSimOccultTypeUtils.determine_current_occult_type(sim_info)))
        if CommonSimUtils.is_active_sim(sim_info):
            values.append(CommonSimDemographicType.CURRENTLY_CONTROLLED)
        if CommonSimTypeUtils.is_non_player_sim(sim_info):
            values.append(CommonSimDemographicType.NON_HOUSEHOLD)
        if CommonSimTypeUtils.is_player_sim(sim_info):
            values.append(CommonSimDemographicType.HOUSEHOLD)
        return tuple(values)

    @classmethod
    def is_sim_contained_in_demographic_flags(cls, sim_info: SimInfo, demographic_flags: 'CommonSimDemographicType', match_all: bool = True) -> bool:
        """is_sim_contained_in_demographic_flags(sim_info, demographic_flags, match_all=True)

        Determine if a Sim is contained in demographic flags.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param demographic_flags: The flags of Sim Demographics to match.
        :type demographic_flags: CommonSimDemographicType
        :param match_all: If True, the Sim must be a match for all specified demographic flags. If False, the Sim can match any of the demographic flags. Default is True.
        :type match_all: bool, optional
        :return: True, if the Sim matches all (or any) of the Demographic Flags. False, if not.
        :rtype: bool
        """
        sim_demographic_flags = cls.determine_sim_demographic_flags(sim_info)
        # from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        # if CommonBitwiseUtils.contains_any_flags(demographic_flags, CommonSimDemographicType.get_all_flags(exclude_values=(CommonSimDemographicType.CURRENTLY_CONTROLLED, CommonSimDemographicType.CONTROLLED, CommonSimDemographicType.HOUSEHOLD, CommonSimDemographicType.NON_HOUSEHOLD))):
        # demographic_flags must contain all the values from sim_demographic_flags. If WEREWOLF was not in demographic_flags but was in sim_demographic_flags, then this would return False.
        if match_all:
            if not CommonBitwiseUtils.contains_all_flags(demographic_flags, sim_demographic_flags):
                cls.get_log().format_with_message('Sim failed to match all flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
                return False
        else:
            if not CommonBitwiseUtils.contains_any_flags(demographic_flags, sim_demographic_flags):
                cls.get_log().format_with_message('Sim failed to match any flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
                return False

        # # Handle the non mutually exclusive flags.
        # from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        # if CommonBitwiseUtils.contains_all_flags(demographic_flags, CommonSimDemographicType.CURRENTLY_CONTROLLED) and CommonSimUtils.is_active_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed controlled flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
        #     return True
        # if CommonBitwiseUtils.contains_all_flags(demographic_flags, CommonSimDemographicType.CONTROLLED) and CommonSimUtils.is_active_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed controlled flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
        #     return True
        # if CommonBitwiseUtils.contains_all_flags(demographic_flags, CommonSimDemographicType.HOUSEHOLD) and CommonSimTypeUtils.is_player_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed household flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
        #     return True
        # if CommonBitwiseUtils.contains_all_flags(demographic_flags, CommonSimDemographicType.NON_HOUSEHOLD) and CommonSimTypeUtils.is_non_player_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed non household flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
        #     return True
        cls.get_log().format_with_message('Sim passed all flags', sim=sim_info, demographic_flags=demographic_flags, sim_demographic_flags=sim_demographic_flags)
        return True

    @classmethod
    def is_sim_contained_in_demographics(cls, sim_info: SimInfo, demographics: Tuple['CommonSimDemographicType'], match_all: bool = True) -> bool:
        """is_sim_contained_in_demographic_flags(sim_info, demographics, match_all=True)

        Determine if a Sim is contained in a collection of Sim demographics.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param demographics: A collection of Sim Demographics to match.
        :type demographics: Tuple[CommonSimDemographicType]
        :param match_all: If True, the Sim must be a match for all specified demographics. If False, the Sim can match any of the demographics. Default is True.
        :type match_all: bool, optional
        :return: True, if the Sim matches all (or any) of the Demographics. False, if not.
        :rtype: bool
        """
        sim_demographics = cls.determine_sim_demographics(sim_info)

        # # Handle the non mutually exclusive flags.
        # from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        # from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        # if CommonSimDemographicType.CURRENTLY_CONTROLLED in demographics and CommonSimUtils.is_active_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed controlled flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics)
        #     return True
        # if CommonSimDemographicType.CONTROLLED in demographics and CommonSimUtils.is_active_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed controlled flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics)
        #     return True
        # if CommonSimDemographicType.NON_HOUSEHOLD in demographics and CommonSimTypeUtils.is_non_player_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed non household flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics)
        #     return True
        # if CommonSimDemographicType.HOUSEHOLD in demographics and CommonSimTypeUtils.is_player_sim(sim_info):
        #     cls.get_log().format_with_message('Sim passed household flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics)
        #     return True

        # demographics must contain all the values from sim_demographics. If WEREWOLF was not in demographics but was in sim_demographics, then this would return False.
        if match_all:
            for sim_demographic in sim_demographics:
                if sim_demographic not in demographics:
                    cls.get_log().format_with_message('Sim failed all flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics, missing_sim_demographic=sim_demographic)
                    return False
            cls.get_log().format_with_message('Sim passed all flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics)
            return True
        else:
            for sim_demographic in sim_demographics:
                if sim_demographic in demographics:
                    cls.get_log().format_with_message('Sim passed flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics, matching_sim_demographic=sim_demographic)
                    return True
            cls.get_log().format_with_message('Sim failed all flags', sim=sim_info, demographics=demographics, sim_demographics=sim_demographics)
            return False

    @classmethod
    def convert_to_age(cls, value: 'CommonSimDemographicType') -> 'CommonAge':
        """Convert a value to an Age value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_age import CommonAge
        mapping: Dict[CommonSimDemographicType, CommonAge] = {
            CommonSimDemographicType.BABY: CommonAge.BABY,
            CommonSimDemographicType.INFANT: CommonAge.INFANT,
            CommonSimDemographicType.TODDLER: CommonAge.TODDLER,
            CommonSimDemographicType.CHILD: CommonAge.CHILD,
            CommonSimDemographicType.TEEN: CommonAge.TEEN,
            CommonSimDemographicType.YOUNG_ADULT: CommonAge.YOUNGADULT,
            CommonSimDemographicType.ADULT: CommonAge.ADULT,
            CommonSimDemographicType.ELDER: CommonAge.ELDER
        }
        return mapping.get(value, CommonAge.INVALID)

    @classmethod
    def convert_from_age(cls, value: 'CommonAge') -> 'CommonSimDemographicType':
        """Convert a value to a Sim demographic value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_age import CommonAge
        mapping: Dict[CommonAge, CommonSimDemographicType] = {
            CommonAge.BABY: CommonSimDemographicType.BABY,
            CommonAge.INFANT: CommonSimDemographicType.INFANT,
            CommonAge.TODDLER: CommonSimDemographicType.TODDLER,
            CommonAge.CHILD: CommonSimDemographicType.CHILD,
            CommonAge.TEEN: CommonSimDemographicType.TEEN,
            CommonAge.YOUNGADULT: CommonSimDemographicType.YOUNG_ADULT,
            CommonAge.ADULT: CommonSimDemographicType.ADULT,
            CommonAge.ELDER: CommonSimDemographicType.ELDER
        }
        return mapping.get(value, CommonSimDemographicType.NONE)

    @classmethod
    def convert_to_gender(cls, value: 'CommonSimDemographicType') -> 'CommonGender':
        """Convert a value to a Gender value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_gender import CommonGender
        mapping: Dict[CommonSimDemographicType, CommonGender] = {
            CommonSimDemographicType.MALE: CommonGender.MALE,
            CommonSimDemographicType.FEMALE: CommonGender.FEMALE
        }
        return mapping.get(value, CommonGender.INVALID)

    @classmethod
    def convert_from_gender(cls, value: 'CommonGender') -> 'CommonSimDemographicType':
        """Convert a value to a Sim demographic value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_gender import CommonGender
        mapping: Dict[CommonGender, CommonSimDemographicType] = {
            CommonGender.MALE: CommonSimDemographicType.MALE,
            CommonGender.FEMALE: CommonSimDemographicType.FEMALE
        }
        return mapping.get(value, CommonSimDemographicType.NONE)

    @classmethod
    def convert_to_species(cls, value: 'CommonSimDemographicType') -> 'CommonSpecies':
        """Convert a value to a Species value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_species import CommonSpecies
        mapping: Dict[CommonSimDemographicType, CommonSpecies] = {
            CommonSimDemographicType.HUMAN: CommonSpecies.HUMAN,
            CommonSimDemographicType.SMALL_DOG: CommonSpecies.SMALL_DOG,
            CommonSimDemographicType.LARGE_DOG: CommonSpecies.LARGE_DOG,
            CommonSimDemographicType.CAT: CommonSpecies.CAT,
            CommonSimDemographicType.FOX: CommonSpecies.FOX,
            CommonSimDemographicType.HORSE: CommonSpecies.HORSE,
        }
        return mapping.get(value, CommonSpecies.INVALID)

    @classmethod
    def convert_from_species(cls, value: 'CommonSpecies') -> 'CommonSimDemographicType':
        """Convert a value to a Sim demographic value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_species import CommonSpecies
        mapping: Dict[CommonSpecies, CommonSimDemographicType] = {
            CommonSpecies.HUMAN: CommonSimDemographicType.HUMAN,
            CommonSpecies.SMALL_DOG: CommonSimDemographicType.SMALL_DOG,
            CommonSpecies.LARGE_DOG: CommonSimDemographicType.LARGE_DOG,
            CommonSpecies.CAT: CommonSimDemographicType.CAT,
            CommonSpecies.FOX: CommonSimDemographicType.FOX,
            CommonSpecies.HORSE: CommonSimDemographicType.HORSE,
        }
        return mapping.get(value, CommonSimDemographicType.NONE)

    @classmethod
    def convert_to_occult_type(cls, value: 'CommonSimDemographicType') -> 'CommonOccultType':
        """Convert a value to an Occult Type value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_occult_type import CommonOccultType
        mapping: Dict[CommonSimDemographicType, CommonOccultType] = {
            CommonSimDemographicType.ALIEN: CommonOccultType.ALIEN,
            CommonSimDemographicType.FAIRY: CommonOccultType.FAIRY,
            CommonSimDemographicType.MERMAID: CommonOccultType.MERMAID,
            CommonSimDemographicType.ROBOT: CommonOccultType.ROBOT,
            CommonSimDemographicType.SKELETON: CommonOccultType.SKELETON,
            CommonSimDemographicType.VAMPIRE: CommonOccultType.VAMPIRE,
            CommonSimDemographicType.WITCH: CommonOccultType.WITCH,
            CommonSimDemographicType.PLANT: CommonOccultType.PLANT_SIM,
            CommonSimDemographicType.GHOST: CommonOccultType.GHOST,
            CommonSimDemographicType.WEREWOLF: CommonOccultType.WEREWOLF,
            CommonSimDemographicType.NON_OCCULT: CommonOccultType.NON_OCCULT,
        }
        return mapping.get(value, CommonOccultType.NONE)

    @classmethod
    def convert_from_occult_type(cls, value: 'CommonOccultType') -> 'CommonSimDemographicType':
        """Convert a value to a Sim demographic value."""
        from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
        from sims4communitylib.enums.common_occult_type import CommonOccultType
        mapping: Dict[CommonOccultType, CommonSimDemographicType] = {
            CommonOccultType.ALIEN: CommonSimDemographicType.ALIEN,
            CommonOccultType.FAIRY: CommonSimDemographicType.FAIRY,
            CommonOccultType.MERMAID: CommonSimDemographicType.MERMAID,
            CommonOccultType.ROBOT: CommonSimDemographicType.ROBOT,
            CommonOccultType.SKELETON: CommonSimDemographicType.SKELETON,
            CommonOccultType.VAMPIRE: CommonSimDemographicType.VAMPIRE,
            CommonOccultType.WITCH: CommonSimDemographicType.WITCH,
            CommonOccultType.PLANT_SIM: CommonSimDemographicType.PLANT,
            CommonOccultType.GHOST: CommonSimDemographicType.GHOST,
            CommonOccultType.WEREWOLF: CommonSimDemographicType.WEREWOLF,
            CommonOccultType.NON_OCCULT: CommonSimDemographicType.NON_OCCULT,
        }
        return mapping.get(value, CommonSimDemographicType.NONE)

    @classmethod
    def get_all_sims_matching_demographics(
        cls,
        sim_demographics: Tuple['CommonSimDemographicType'],
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None,
        instanced_only: bool = True
    ) -> Iterator[SimInfo]:
        """get_all_sims_matching_demographics(\
            sim_demographics,\
            include_sim_callback=None,\
            instanced_only=True\
        )

        Get all Sims matching a collection of Sim Demographics.

        :param sim_demographics: A collection of Sim demographics to match on.
        :type sim_demographics: Tuple[CommonSimDemographicType]
        :param include_sim_callback: If the result of this callback is True, the Sim will be available in the results. If set to None, All Sims will be available in the results.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :param instanced_only: If True, only Sims that are currently loaded will be available in the results. Default is True.
        :type instanced_only: bool, optional
        :return: A generator of Sims matching the specified demographics.
        :rtype: Iterator[SimInfo]
        """
        if instanced_only:
            sim_info_gen = CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback)
        else:
            sim_info_gen = CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback)
        for sim_info in sim_info_gen:
            if cls.is_sim_contained_in_demographics(sim_info, sim_demographics):
                yield sim_info

    @classmethod
    def get_all_sims_matching_demographic_flags(
        cls,
        sim_demographic_flags: 'CommonSimDemographicType',
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None,
        instanced_only: bool = True
    ) -> Iterator[SimInfo]:
        """get_all_sims_matching_demographic_flags(\
            sim_demographic_flags,\
            include_sim_callback=None,\
            instanced_only=True\
        )

        Get all Sims matching Sim Demographics Flags.

        :param sim_demographic_flags: Flags of Sim Demographics to match on.
        :type sim_demographic_flags: CommonSimDemographicType
        :param include_sim_callback: If the result of this callback is True, the Sim will be available in the results. If set to None, All Sims will be available in the results.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :param instanced_only: If True, only Sims that are currently loaded will be available in the results. Default is True.
        :type instanced_only: bool, optional
        :return: A generator of Sims matching the specified demographics.
        :rtype: Iterator[SimInfo]
        """
        if instanced_only:
            sim_info_gen = CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback)
        else:
            sim_info_gen = CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback)
        for sim_info in sim_info_gen:
            if cls.is_sim_contained_in_demographic_flags(sim_info, sim_demographic_flags):
                yield sim_info

    @classmethod
    def perform_action_on_sims_matching_demographics(
        cls,
        sim_demographics: Tuple['CommonSimDemographicType'],
        action: Callable[[SimInfo], None],
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None,
        instanced_only: bool = True
    ):
        """perform_action_on_sims_matching_demographics(\
            sim_demographics,\
            action,\
            include_sim_callback=None,\
            instanced_only=True\
        )

        Perform an action on all Sims matching a collection of Sim Demographics.

        :param sim_demographics: A collection of Sim demographics to match on.
        :type sim_demographics: Tuple[CommonSimDemographicType]
        :param action: A function invoked on each matching Sim.
        :type action: Callable[[SimInfo], None]
        :param include_sim_callback: If the result of this callback is True, the Sim will be available to have the action performed on them. If set to None, All Sims will be available to have the action performed on them.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :param instanced_only: If True, only Sims that are currently loaded will be available. Default is True.
        :type instanced_only: bool, optional
        """
        for sim_info in cls.get_all_sims_matching_demographics(sim_demographics, include_sim_callback=include_sim_callback, instanced_only=instanced_only):
            if cls.is_sim_contained_in_demographics(sim_info, sim_demographics):
                action(sim_info)

    @classmethod
    def perform_action_on_sims_matching_demographic_flags(
        cls,
        sim_demographic_flags: 'CommonSimDemographicType',
        action: Callable[[SimInfo], None],
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None,
        instanced_only: bool = True
    ):
        """perform_action_on_sims_matching_demographic_flags(\
            sim_demographic_flags,\
            action,\
            include_sim_callback=None,\
            instanced_only=True\
        )

        Perform an action on all Sims matching Sim Demographics Flags.

        :param sim_demographic_flags: Flags of Sim Demographics to match on.
        :type sim_demographic_flags: CommonSimDemographicType
        :param action: A function invoked on each matching Sim.
        :type action: Callable[[SimInfo], None]
        :param include_sim_callback: If the result of this callback is True, the Sim will be available to have the action performed on them. If set to None, All Sims will be available to have the action performed on them.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :param instanced_only: If True, only Sims that are currently loaded will be available to have the action performed on them. Default is True.
        :type instanced_only: bool, optional
        """
        for sim_info in cls.get_all_sims_matching_demographic_flags(sim_demographic_flags, include_sim_callback=include_sim_callback, instanced_only=instanced_only):
            if cls.is_sim_contained_in_demographic_flags(sim_info, sim_demographic_flags):
                action(sim_info)
