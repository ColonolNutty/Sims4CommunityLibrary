"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from business.business_enums import BusinessQualityType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonBusinessQualityType(CommonInt):
    """Different quality types of a Business."""
    INVALID: 'CommonBusinessQualityType' = ...
    LOW: 'CommonBusinessQualityType' = ...
    MEDIUM: 'CommonBusinessQualityType' = ...
    HIGH: 'CommonBusinessQualityType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonBusinessQualityType'] = None) -> Tuple['CommonBusinessQualityType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessQualityType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonBusinessQualityType]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonBusinessQualityType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonBusinessQualityType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessQualityType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonBusinessQualityType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessQualityType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonBusinessQualityType') -> BusinessQualityType:
        """convert_to_vanilla(value)

        Convert a value into the vanilla BusinessQualityType enum.

        :param value: An instance of CommonBusinessQualityType
        :type value: CommonBusinessQualityType
        :return: The specified value translated to BusinessQualityType or INVALID if the value could not be translated.
        :rtype: BusinessQualityType
        """
        if value is None or value == CommonBusinessQualityType.INVALID:
            return BusinessQualityType.INVALID
        if isinstance(value, BusinessQualityType):
            return value
        mapping = dict()
        if hasattr(BusinessQualityType, 'LOW'):
            mapping[CommonBusinessQualityType.LOW] = BusinessQualityType.LOW
        if hasattr(BusinessQualityType, 'MEDIUM'):
            mapping[CommonBusinessQualityType.MEDIUM] = BusinessQualityType.MEDIUM
        if hasattr(BusinessQualityType, 'HIGH'):
            mapping[CommonBusinessQualityType.HIGH] = BusinessQualityType.HIGH
        return mapping.get(value, BusinessQualityType.INVALID)

    @staticmethod
    def convert_from_vanilla(value: Union[int, BusinessQualityType]) -> 'CommonBusinessQualityType':
        """convert_from_vanilla(value)

        Convert a value into a CommonBusinessQualityType enum.

        :param value: An instance of BusinessQualityType
        :type value: BusinessQualityType
        :return: The specified value translated to CommonBusinessQualityType or INVALID if the value could not be translated.
        :rtype: CommonBusinessQualityType
        """
        if value is None or value == BusinessQualityType.INVALID:
            return CommonBusinessQualityType.INVALID
        if isinstance(value, CommonBusinessQualityType):
            return value
        mapping = dict()
        if hasattr(BusinessQualityType, 'LOW'):
            mapping[BusinessQualityType.LOW] = CommonBusinessQualityType.LOW
        if hasattr(BusinessQualityType, 'MEDIUM'):
            mapping[BusinessQualityType.MEDIUM] = CommonBusinessQualityType.MEDIUM
        if hasattr(BusinessQualityType, 'HIGH'):
            mapping[BusinessQualityType.HIGH] = CommonBusinessQualityType.HIGH
        return mapping.get(value, CommonBusinessQualityType.INVALID)
