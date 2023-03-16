"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union, Tuple, Iterator

from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonAge(CommonInt):
    """Custom Age enum containing all ages, because there have been too many problems when referencing the vanilla Age in various places.

    """
    INVALID: 'CommonAge' = 0
    BABY: 'CommonAge' = 1
    INFANT: 'CommonAge' = 2
    TODDLER: 'CommonAge' = 4
    CHILD: 'CommonAge' = 8
    TEEN: 'CommonAge' = 16
    YOUNGADULT: 'CommonAge' = 32
    ADULT: 'CommonAge' = 64
    ELDER: 'CommonAge' = 128

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonAge'] = None) -> Tuple['CommonAge']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonAge], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonAge]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonAge, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonAge'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonAge], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonAge'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonAge], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def get_age(sim_info: SimInfo) -> 'CommonAge':
        """get_age(sim_info)

        Retrieve the CommonAge of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonAge that represents what age a Sim is or INVALID if their age cannot be determined.
        :rtype: CommonAge
        """
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeUtils.is_baby(sim_info):
            return CommonAge.BABY
        elif CommonAgeUtils.is_infant(sim_info):
            return CommonAge.INFANT
        elif CommonAgeUtils.is_toddler(sim_info):
            return CommonAge.TODDLER
        elif CommonAgeUtils.is_child(sim_info):
            return CommonAge.CHILD
        elif CommonAgeUtils.is_teen(sim_info):
            return CommonAge.TEEN
        elif CommonAgeUtils.is_young_adult(sim_info):
            return CommonAge.YOUNGADULT
        elif CommonAgeUtils.is_adult(sim_info):
            return CommonAge.ADULT
        elif CommonAgeUtils.is_elder(sim_info):
            return CommonAge.ELDER
        return CommonAge.INVALID

    @staticmethod
    def convert_to_vanilla(value: 'CommonAge') -> Union[Age, None]:
        """convert_to_vanilla(value)

        Convert a CommonAge into the vanilla Age enum.

        :param value: An instance of CommonAge
        :type value: CommonAge
        :return: The specified CommonAge translated to Age or None if the value could not be translated.
        :rtype: Union[Age, None]
        """
        if value is None or value == CommonAge.INVALID:
            return None
        if isinstance(value, Age):
            return value
        age_conversion_mapping: Dict[CommonAge, Age] = {
            CommonAge.BABY: Age.BABY,
            CommonAge.INFANT: Age.INFANT,
            CommonAge.TODDLER: Age.TODDLER,
            CommonAge.CHILD: Age.CHILD,
            CommonAge.TEEN: Age.TEEN,
            CommonAge.YOUNGADULT: Age.YOUNGADULT,
            CommonAge.ADULT: Age.ADULT,
            CommonAge.ELDER: Age.ELDER
        }
        return age_conversion_mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: Union[int, Age]) -> 'CommonAge':
        """convert_from_vanilla(value)

        Convert a vanilla Age to a CommonAge.

        :param value: An instance of Age
        :type value: Age
        :return: The specified Age translated to CommonAge or INVALID if the value could not be translated.
        :rtype: CommonAge
        """
        if value is None:
            return CommonAge.INVALID
        if isinstance(value, CommonAge):
            return value
        age_conversion_mapping: Dict[int, CommonAge] = {
            int(Age.BABY): CommonAge.BABY,
            int(Age.INFANT): CommonAge.INFANT,
            int(Age.TODDLER): CommonAge.TODDLER,
            int(Age.CHILD): CommonAge.CHILD,
            int(Age.TEEN): CommonAge.TEEN,
            int(Age.YOUNGADULT): CommonAge.YOUNGADULT,
            int(Age.ADULT): CommonAge.ADULT,
            int(Age.ELDER): CommonAge.ELDER
        }
        value = int(value)
        if value not in age_conversion_mapping:
            return CommonAge.INVALID
        return age_conversion_mapping[value]

    @staticmethod
    def convert_to_localized_string_id(value: Union[int, 'CommonAge']) -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a CommonAge into a Localized String identifier.

        :param value: An instance of a CommonAge
        :type value: CommonAge
        :return: The specified CommonAge translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        display_name_mapping = {
            CommonAge.BABY: CommonStringId.BABY,
            CommonAge.INFANT: CommonStringId.INFANT,
            CommonAge.TODDLER: CommonStringId.TODDLER,
            CommonAge.CHILD: CommonStringId.CHILD,
            CommonAge.TEEN: CommonStringId.TEEN,
            CommonAge.YOUNGADULT: CommonStringId.YOUNG_ADULT,
            CommonAge.ADULT: CommonStringId.ADULT,
            CommonAge.ELDER: CommonStringId.ELDER
        }
        if isinstance(value, int) and not isinstance(value, CommonAge):
            value = CommonAge.convert_from_vanilla(value)
        return display_name_mapping.get(value, value.name if hasattr(value, 'name') else str(value))
