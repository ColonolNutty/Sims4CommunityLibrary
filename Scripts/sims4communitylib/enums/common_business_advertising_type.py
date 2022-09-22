"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from business.business_enums import BusinessAdvertisingType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonBusinessAdvertisingType(CommonInt):
    """Advertising types for businesses."""
    INVALID: 'CommonBusinessAdvertisingType' = ...
    BUSINESS_NONE: 'CommonBusinessAdvertisingType' = ...
    BUSINESS_RADIO: 'CommonBusinessAdvertisingType' = ...
    RETAIL_TV_LONG: 'CommonBusinessAdvertisingType' = ...
    RETAIL_TV_SHORT: 'CommonBusinessAdvertisingType' = ...
    RETAIL_WEB_LONG: 'CommonBusinessAdvertisingType' = ...
    RETAIL_WEB_SHORT: 'CommonBusinessAdvertisingType' = ...
    BUSINESS_WEB: 'CommonBusinessAdvertisingType' = ...
    BUSINESS_NEWSPAPER: 'CommonBusinessAdvertisingType' = ...
    BUSINESS_TV: 'CommonBusinessAdvertisingType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonBusinessAdvertisingType'] = None) -> Tuple['CommonBusinessAdvertisingType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessAdvertisingType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonBusinessAdvertisingType]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonBusinessAdvertisingType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonBusinessAdvertisingType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessAdvertisingType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonBusinessAdvertisingType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessAdvertisingType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonBusinessAdvertisingType') -> BusinessAdvertisingType:
        """convert_to_vanilla(value)

        Convert a value into the vanilla BusinessAdvertisingType enum.

        :param value: An instance of CommonBusinessAdvertisingType
        :type value: CommonBusinessAdvertisingType
        :return: The specified value translated to BusinessAdvertisingType or INVALID if the value could not be translated.
        :rtype: BusinessAdvertisingType
        """
        if value is None or value == CommonBusinessAdvertisingType.INVALID:
            return BusinessAdvertisingType.INVALID
        if isinstance(value, BusinessAdvertisingType):
            return value
        mapping = dict()
        if hasattr(BusinessAdvertisingType, 'Business_None'):
            mapping[CommonBusinessAdvertisingType.BUSINESS_NONE] = BusinessAdvertisingType.Business_None
        if hasattr(BusinessAdvertisingType, 'Business_Radio'):
            mapping[CommonBusinessAdvertisingType.BUSINESS_RADIO] = BusinessAdvertisingType.Business_Radio
        if hasattr(BusinessAdvertisingType, 'Retail_TV_Long'):
            mapping[CommonBusinessAdvertisingType.RETAIL_TV_LONG] = BusinessAdvertisingType.Retail_TV_Long
        if hasattr(BusinessAdvertisingType, 'Retail_TV_Short'):
            mapping[CommonBusinessAdvertisingType.RETAIL_TV_SHORT] = BusinessAdvertisingType.Retail_TV_Short
        if hasattr(BusinessAdvertisingType, 'Retail_Web_Long'):
            mapping[CommonBusinessAdvertisingType.RETAIL_WEB_LONG] = BusinessAdvertisingType.Retail_Web_Long
        if hasattr(BusinessAdvertisingType, 'Retail_Web_Short'):
            mapping[CommonBusinessAdvertisingType.RETAIL_WEB_SHORT] = BusinessAdvertisingType.Retail_Web_Short
        if hasattr(BusinessAdvertisingType, 'Business_Web'):
            mapping[CommonBusinessAdvertisingType.BUSINESS_WEB] = BusinessAdvertisingType.Business_Web
        if hasattr(BusinessAdvertisingType, 'Business_Newspaper'):
            mapping[CommonBusinessAdvertisingType.BUSINESS_NEWSPAPER] = BusinessAdvertisingType.Business_Newspaper
        if hasattr(BusinessAdvertisingType, 'Business_TV'):
            mapping[CommonBusinessAdvertisingType.BUSINESS_TV] = BusinessAdvertisingType.Business_TV
        return mapping.get(value, BusinessAdvertisingType.INVALID)

    @staticmethod
    def convert_from_vanilla(value: Union[int, BusinessAdvertisingType]) -> 'CommonBusinessAdvertisingType':
        """convert_from_vanilla(value)

        Convert a value into a CommonBusinessAdvertisingType enum.

        :param value: An instance of BusinessAdvertisingType
        :type value: BusinessAdvertisingType
        :return: The specified value translated to CommonBusinessAdvertisingType or INVALID if the value could not be translated.
        :rtype: CommonBusinessAdvertisingType
        """
        if value is None or value == BusinessAdvertisingType.INVALID:
            return CommonBusinessAdvertisingType.INVALID
        if isinstance(value, CommonBusinessAdvertisingType):
            return value
        mapping = dict()
        if hasattr(BusinessAdvertisingType, 'Business_None'):
            mapping[BusinessAdvertisingType.Business_None] = CommonBusinessAdvertisingType.BUSINESS_NONE
        if hasattr(BusinessAdvertisingType, 'Business_Radio'):
            mapping[BusinessAdvertisingType.Business_Radio] = CommonBusinessAdvertisingType.BUSINESS_RADIO
        if hasattr(BusinessAdvertisingType, 'Retail_TV_Long'):
            mapping[BusinessAdvertisingType.Retail_TV_Long] = CommonBusinessAdvertisingType.RETAIL_TV_LONG
        if hasattr(BusinessAdvertisingType, 'Retail_TV_Short'):
            mapping[BusinessAdvertisingType.Retail_TV_Short] = CommonBusinessAdvertisingType.RETAIL_TV_SHORT
        if hasattr(BusinessAdvertisingType, 'Retail_Web_Long'):
            mapping[BusinessAdvertisingType.Retail_Web_Long] = CommonBusinessAdvertisingType.RETAIL_WEB_LONG
        if hasattr(BusinessAdvertisingType, 'Retail_Web_Short'):
            mapping[BusinessAdvertisingType.Retail_Web_Short] = CommonBusinessAdvertisingType.RETAIL_WEB_SHORT
        if hasattr(BusinessAdvertisingType, 'Business_Web'):
            mapping[BusinessAdvertisingType.Business_Web] = CommonBusinessAdvertisingType.BUSINESS_WEB
        if hasattr(BusinessAdvertisingType, 'Business_Newspaper'):
            mapping[BusinessAdvertisingType.Business_Newspaper] = CommonBusinessAdvertisingType.BUSINESS_NEWSPAPER
        if hasattr(BusinessAdvertisingType, 'Business_TV'):
            mapping[BusinessAdvertisingType.Business_TV] = CommonBusinessAdvertisingType.BUSINESS_TV
        return mapping.get(value, CommonBusinessAdvertisingType.INVALID)
