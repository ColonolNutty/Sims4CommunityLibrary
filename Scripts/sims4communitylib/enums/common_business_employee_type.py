"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from business.business_enums import BusinessEmployeeType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonBusinessEmployeeType(CommonInt):
    """Employee types of various businesses."""
    INVALID: 'CommonBusinessEmployeeType' = ...
    RETAIL: 'CommonBusinessEmployeeType' = ...
    RESTAURANT_CHEF: 'CommonBusinessEmployeeType' = ...
    RESTAURANT_WAITSTAFF: 'CommonBusinessEmployeeType' = ...
    RESTAURANT_HOST: 'CommonBusinessEmployeeType' = ...
    VET: 'CommonBusinessEmployeeType' = ...
    SMALL_BUSINESS_HELP: 'CommonBusinessEmployeeType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonBusinessEmployeeType'] = None) -> Tuple['CommonBusinessEmployeeType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessEmployeeType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonBusinessEmployeeType]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonBusinessEmployeeType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonBusinessEmployeeType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessEmployeeType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonBusinessEmployeeType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessEmployeeType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonBusinessEmployeeType') -> BusinessEmployeeType:
        """convert_to_vanilla(value)

        Convert a value into the vanilla BusinessEmployeeType enum.

        :param value: An instance of CommonBusinessEmployeeType
        :type value: CommonBusinessEmployeeType
        :return: The specified value translated to BusinessEmployeeType or INVALID if the value could not be translated.
        :rtype: BusinessEmployeeType
        """
        if value is None or value == CommonBusinessEmployeeType.INVALID:
            return BusinessEmployeeType.INVALID
        if isinstance(value, BusinessEmployeeType):
            return value
        mapping = dict()
        if hasattr(BusinessEmployeeType, 'RETAIL'):
            mapping[CommonBusinessEmployeeType.RETAIL] = BusinessEmployeeType.RETAIL
        if hasattr(BusinessEmployeeType, 'RESTAURANT_CHEF'):
            mapping[CommonBusinessEmployeeType.RESTAURANT_CHEF] = BusinessEmployeeType.RESTAURANT_CHEF
        if hasattr(BusinessEmployeeType, 'RESTAURANT_WAITSTAFF'):
            mapping[CommonBusinessEmployeeType.RESTAURANT_WAITSTAFF] = BusinessEmployeeType.RESTAURANT_WAITSTAFF
        if hasattr(BusinessEmployeeType, 'RESTAURANT_HOST'):
            mapping[CommonBusinessEmployeeType.RESTAURANT_HOST] = BusinessEmployeeType.RESTAURANT_HOST
        if hasattr(BusinessEmployeeType, 'VET'):
            mapping[CommonBusinessEmployeeType.VET] = BusinessEmployeeType.VET
        if hasattr(BusinessEmployeeType, 'SMALL_BUSINESS_HELP'):
            mapping[CommonBusinessEmployeeType.SMALL_BUSINESS_HELP] = BusinessEmployeeType.SMALL_BUSINESS_HELP
        return mapping.get(value, BusinessEmployeeType.INVALID)

    @staticmethod
    def convert_from_vanilla(value: Union[int, BusinessEmployeeType]) -> 'CommonBusinessEmployeeType':
        """convert_from_vanilla(value)

        Convert a value into a CommonBusinessEmployeeType enum.

        :param value: An instance of BusinessEmployeeType
        :type value: BusinessEmployeeType
        :return: The specified value translated to CommonBusinessEmployeeType or INVALID if the value could not be translated.
        :rtype: CommonBusinessEmployeeType
        """
        if value is None or value == BusinessEmployeeType.INVALID:
            return CommonBusinessEmployeeType.INVALID
        if isinstance(value, CommonBusinessEmployeeType):
            return value
        mapping = dict()
        if hasattr(BusinessEmployeeType, 'RETAIL'):
            mapping[BusinessEmployeeType.RETAIL] = CommonBusinessEmployeeType.RETAIL
        if hasattr(BusinessEmployeeType, 'RESTAURANT_CHEF'):
            mapping[BusinessEmployeeType.RESTAURANT_CHEF] = CommonBusinessEmployeeType.RESTAURANT_CHEF
        if hasattr(BusinessEmployeeType, 'RESTAURANT_WAITSTAFF'):
            mapping[BusinessEmployeeType.RESTAURANT_WAITSTAFF] = CommonBusinessEmployeeType.RESTAURANT_WAITSTAFF
        if hasattr(BusinessEmployeeType, 'RESTAURANT_HOST'):
            mapping[BusinessEmployeeType.RESTAURANT_HOST] = CommonBusinessEmployeeType.RESTAURANT_HOST
        if hasattr(BusinessEmployeeType, 'VET'):
            mapping[BusinessEmployeeType.VET] = CommonBusinessEmployeeType.VET
        if hasattr(BusinessEmployeeType, 'SMALL_BUSINESS_HELP'):
            mapping[BusinessEmployeeType.SMALL_BUSINESS_HELP] = CommonBusinessEmployeeType.SMALL_BUSINESS_HELP
        return mapping.get(value, CommonBusinessEmployeeType.INVALID)

