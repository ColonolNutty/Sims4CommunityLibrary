"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union, Tuple

from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonAge(CommonInt):
    """Custom Age enum containing all ages, because there have been too many problems when referencing the vanilla Age in various places.

    """
    INVALID: 'CommonAge' = 0
    BABY: 'CommonAge' = 1
    TODDLER: 'CommonAge' = 2
    CHILD: 'CommonAge' = 4
    TEEN: 'CommonAge' = 8
    YOUNGADULT: 'CommonAge' = 16
    ADULT: 'CommonAge' = 32
    ELDER: 'CommonAge' = 64

    @classmethod
    def get_all(cls) -> Tuple['CommonAge']:
        """get_all()

        Retrieve a collection of all CommonAge, excluding CommonAge.INVALID.

        :return: A collection of all CommonAge, without CommonAge.INVALID.
        :rtype: Tuple[CommonAge]
        """
        value_list: Tuple[CommonAge] = tuple([value for value in cls.values if value != cls.INVALID])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonAge, excluding CommonAge.INVALID.

        :return: A collection of the names of all CommonAge, without CommonAge.INVALID.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list

    @staticmethod
    def get_age(sim_info: SimInfo) -> 'CommonAge':
        """get_age(sim_info)

        Retrieve the CommonAge of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonAge that represents what age a Sim is or CommonAge.INVALID if their age cannot be determined.
        :rtype: CommonAge
        """
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeUtils.is_baby(sim_info):
            return CommonAge.BABY
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
    def convert_to_vanilla(age: 'CommonAge') -> Union[Age, None]:
        """convert_to_vanilla(age)

        Convert a CommonAge into the vanilla Age enum.

        :param age: An instance of a CommonAge
        :type age: CommonAge
        :return: The specified CommonAge translated to an Age or None if the CommonAge could not be translated.
        :rtype: Union[Age, None]
        """
        if age is None or age == CommonAge.INVALID:
            return None
        if isinstance(age, Age):
            return age
        age_conversion_mapping: Dict[CommonAge, Age] = {
            CommonAge.BABY: Age.BABY,
            CommonAge.TODDLER: Age.TODDLER,
            CommonAge.CHILD: Age.CHILD,
            CommonAge.TEEN: Age.TEEN,
            CommonAge.YOUNGADULT: Age.YOUNGADULT,
            CommonAge.ADULT: Age.ADULT,
            CommonAge.ELDER: Age.ELDER
        }
        return age_conversion_mapping.get(age, None)

    @staticmethod
    def convert_from_vanilla(age: Age) -> 'CommonAge':
        """convert_from_age(age)

        Convert a vanilla Age to a CommonAge.

        :param age: An instance of an Age
        :type age: Age
        :return: The specified Age translated to a CommonAge or CommonAge.INVALID if the Age could not be translated.
        :rtype: CommonAge
        """
        if age is None:
            return CommonAge.INVALID
        if isinstance(age, CommonAge):
            return age
        age_conversion_mapping: Dict[int, CommonAge] = {
            int(Age.BABY): CommonAge.BABY,
            int(Age.TODDLER): CommonAge.TODDLER,
            int(Age.CHILD): CommonAge.CHILD,
            int(Age.TEEN): CommonAge.TEEN,
            int(Age.YOUNGADULT): CommonAge.YOUNGADULT,
            int(Age.ADULT): CommonAge.ADULT,
            int(Age.ELDER): CommonAge.ELDER
        }
        age = int(age)
        if age not in age_conversion_mapping:
            return CommonAge.INVALID
        return age_conversion_mapping[age]

    @staticmethod
    def convert_to_localized_string_id(age: 'CommonAge') -> Union[int, str]:
        """convert_to_localized_string_id(age)

        Convert a CommonAge into a Localized String identifier.

        :param age: An instance of a CommonAge
        :type age: CommonAge
        :return: The specified CommonAge translated to a localized string identifier or the name property of the value, if no localized string id is found.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        display_name_mapping = {
            CommonAge.BABY: CommonStringId.BABY,
            CommonAge.TODDLER: CommonStringId.TODDLER,
            CommonAge.CHILD: CommonStringId.CHILD,
            CommonAge.TEEN: CommonStringId.TEEN,
            CommonAge.YOUNGADULT: CommonStringId.YOUNG_ADULT,
            CommonAge.ADULT: CommonStringId.ADULT,
            CommonAge.ELDER: CommonStringId.ELDER
        }
        return display_name_mapping.get(age, age.name)

