"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonGender(CommonInt):
    """Custom Gender enum containing all genders.

    """
    INVALID: 'CommonGender' = 0
    MALE: 'CommonGender' = 4096
    FEMALE: 'CommonGender' = 8192

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonGender'] = None) -> Tuple['CommonGender']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGender], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonGender]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonGender, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonGender'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGender], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonGender'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGender], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def get_gender(sim_info: SimInfo) -> 'CommonGender':
        """get_gender(sim_info)

        Retrieve the CommonGender of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The CommonGender that represents what gender a Sim is or CommonGender.INVALID if their gender cannot be determined.
        :rtype: CommonGender
        """
        from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
        if CommonGenderUtils.is_male(sim_info):
            return CommonGender.MALE
        elif CommonGenderUtils.is_female(sim_info):
            return CommonGender.FEMALE
        return CommonGender.INVALID

    @staticmethod
    def convert_to_vanilla(value: 'CommonGender') -> Union[Gender, None]:
        """convert_to_vanilla(value)

        Convert a value into the vanilla Gender enum.

        :param value: An instance of CommonGender
        :type value: CommonGender
        :return: The specified value translated to Gender or None if the value could not be translated.
        :rtype: Union[Gender, None]
        """
        if value is None or value == CommonGender.INVALID:
            return None
        if isinstance(value, Gender):
            return value
        mapping = {
            CommonGender.MALE: Gender.MALE,
            CommonGender.FEMALE: Gender.FEMALE
        }
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: Union[int, Gender]) -> 'CommonGender':
        """convert_from_vanilla(value)

        Convert a value into a CommonGender enum.

        :param value: An instance of Gender
        :type value: Gender
        :return: The specified value translated to CommonGender or INVALID if the value could not be translated.
        :rtype: CommonGender
        """
        if value is None:
            return CommonGender.INVALID
        if isinstance(value, CommonGender):
            return value
        mapping = {
            int(Gender.MALE): CommonGender.MALE,
            int(Gender.FEMALE): CommonGender.FEMALE
        }
        value = int(value)
        if value not in mapping:
            return CommonGender.INVALID
        return mapping[value]

    @staticmethod
    def convert_to_localized_string_id(value: 'CommonGender') -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a CommonGender into a Localized String identifier.

        :param value: An instance of a CommonGender
        :type value: CommonGender
        :return: The specified CommonGender translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        mapping = {
            CommonGender.MALE: CommonStringId.MALE,
            CommonGender.FEMALE: CommonStringId.FEMALE
        }
        if isinstance(value, int) and not isinstance(value, CommonGender):
            value = CommonGender.convert_from_vanilla(value)
        return mapping.get(value, value.name if hasattr(value, 'name') else str(value))
