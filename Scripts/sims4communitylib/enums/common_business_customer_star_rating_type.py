"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from business.business_enums import BusinessCustomerStarRatingBuffBuckets
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonBusinessCustomerStarRatingType(CommonInt):
    """Customer star rating types"""
    INVALID: 'CommonBusinessCustomerStarRatingType' = ...
    SERVICE: 'CommonBusinessCustomerStarRatingType' = ...
    AMBIANCE: 'CommonBusinessCustomerStarRatingType' = ...
    FOOD_QUALITY: 'CommonBusinessCustomerStarRatingType' = ...
    FOOD_VALUE: 'CommonBusinessCustomerStarRatingType' = ...
    PERSONAL_TOUCH: 'CommonBusinessCustomerStarRatingType' = ...
    WAIT_TIME: 'CommonBusinessCustomerStarRatingType' = ...
    MISC: 'CommonBusinessCustomerStarRatingType' = ...
    STRESS_LEVEL: 'CommonBusinessCustomerStarRatingType' = ...
    SERVICE_VALUE: 'CommonBusinessCustomerStarRatingType' = ...
    SERVICE_QUALITY: 'CommonBusinessCustomerStarRatingType' = ...
    CUSTOMER_RELATIONSHIP: 'CommonBusinessCustomerStarRatingType' = ...
    ACTIVITIES_COMPLETED: 'CommonBusinessCustomerStarRatingType' = ...
    PRICING: 'CommonBusinessCustomerStarRatingType' = ...
    QUALITY: 'CommonBusinessCustomerStarRatingType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonBusinessCustomerStarRatingType'] = None) -> Tuple['CommonBusinessCustomerStarRatingType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessCustomerStarRatingType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonBusinessCustomerStarRatingType]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonBusinessCustomerStarRatingType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonBusinessCustomerStarRatingType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessCustomerStarRatingType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonBusinessCustomerStarRatingType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBusinessCustomerStarRatingType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonBusinessCustomerStarRatingType') -> BusinessCustomerStarRatingBuffBuckets:
        """convert_to_vanilla(value)

        Convert a value into the vanilla BusinessCustomerStarRatingBuffBuckets enum.

        :param value: An instance of CommonBusinessCustomerStarRatingType
        :type value: CommonBusinessCustomerStarRatingType
        :return: The specified value translated to BusinessCustomerStarRatingBuffBuckets or INVALID if the value could not be translated.
        :rtype: BusinessCustomerStarRatingBuffBuckets
        """
        if value is None or value == CommonBusinessCustomerStarRatingType.INVALID:
            return BusinessCustomerStarRatingBuffBuckets.INVALID
        if isinstance(value, BusinessCustomerStarRatingBuffBuckets):
            return value
        mapping = dict()
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'SERVICE'):
            mapping[CommonBusinessCustomerStarRatingType.SERVICE] = BusinessCustomerStarRatingBuffBuckets.SERVICE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'AMBIANCE'):
            mapping[CommonBusinessCustomerStarRatingType.AMBIANCE] = BusinessCustomerStarRatingBuffBuckets.AMBIANCE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'FOOD_QUALITY'):
            mapping[CommonBusinessCustomerStarRatingType.FOOD_QUALITY] = BusinessCustomerStarRatingBuffBuckets.FOOD_QUALITY
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'FOOD_VALUE'):
            mapping[CommonBusinessCustomerStarRatingType.FOOD_VALUE] = BusinessCustomerStarRatingBuffBuckets.FOOD_VALUE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'PERSONAL_TOUCH'):
            mapping[CommonBusinessCustomerStarRatingType.PERSONAL_TOUCH] = BusinessCustomerStarRatingBuffBuckets.PERSONAL_TOUCH
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'WAIT_TIME'):
            mapping[CommonBusinessCustomerStarRatingType.WAIT_TIME] = BusinessCustomerStarRatingBuffBuckets.WAIT_TIME
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'MISC'):
            mapping[CommonBusinessCustomerStarRatingType.MISC] = BusinessCustomerStarRatingBuffBuckets.MISC
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'STRESS_LEVEL'):
            mapping[CommonBusinessCustomerStarRatingType.STRESS_LEVEL] = BusinessCustomerStarRatingBuffBuckets.STRESS_LEVEL
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'SERVICE_VALUE'):
            mapping[CommonBusinessCustomerStarRatingType.SERVICE_VALUE] = BusinessCustomerStarRatingBuffBuckets.SERVICE_VALUE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'SERVICE_QUALITY'):
            mapping[CommonBusinessCustomerStarRatingType.SERVICE_QUALITY] = BusinessCustomerStarRatingBuffBuckets.SERVICE_QUALITY
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'CUSTOMER_RELATIONSHIP'):
            mapping[CommonBusinessCustomerStarRatingType.CUSTOMER_RELATIONSHIP] = BusinessCustomerStarRatingBuffBuckets.CUSTOMER_RELATIONSHIP
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'ACTIVITIES_COMPLETED'):
            mapping[CommonBusinessCustomerStarRatingType.ACTIVITIES_COMPLETED] = BusinessCustomerStarRatingBuffBuckets.ACTIVITIES_COMPLETED
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'PRICING'):
            mapping[CommonBusinessCustomerStarRatingType.PRICING] = BusinessCustomerStarRatingBuffBuckets.PRICING
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'QUALITY'):
            mapping[CommonBusinessCustomerStarRatingType.QUALITY] = BusinessCustomerStarRatingBuffBuckets.QUALITY
        return mapping.get(value, BusinessCustomerStarRatingBuffBuckets.INVALID)

    @staticmethod
    def convert_from_vanilla(value: Union[int, BusinessCustomerStarRatingBuffBuckets]) -> 'CommonBusinessCustomerStarRatingType':
        """convert_from_vanilla(value)

        Convert a value into a CommonBusinessCustomerStarRatingType enum.

        :param value: An instance of BusinessCustomerStarRatingBuffBuckets
        :type value: BusinessCustomerStarRatingBuffBuckets
        :return: The specified value translated to CommonBusinessCustomerStarRatingType or INVALID if the value could not be translated.
        :rtype: CommonBusinessCustomerStarRatingType
        """
        if value is None or value == BusinessCustomerStarRatingBuffBuckets.INVALID:
            return CommonBusinessCustomerStarRatingType.INVALID
        if isinstance(value, CommonBusinessCustomerStarRatingType):
            return value
        mapping = dict()
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'SERVICE'):
            mapping[BusinessCustomerStarRatingBuffBuckets.SERVICE] = CommonBusinessCustomerStarRatingType.SERVICE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'AMBIANCE'):
            mapping[BusinessCustomerStarRatingBuffBuckets.AMBIANCE] = CommonBusinessCustomerStarRatingType.AMBIANCE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'FOOD_QUALITY'):
            mapping[BusinessCustomerStarRatingBuffBuckets.FOOD_QUALITY] = CommonBusinessCustomerStarRatingType.FOOD_QUALITY
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'FOOD_VALUE'):
            mapping[BusinessCustomerStarRatingBuffBuckets.FOOD_VALUE] = CommonBusinessCustomerStarRatingType.FOOD_VALUE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'PERSONAL_TOUCH'):
            mapping[BusinessCustomerStarRatingBuffBuckets.PERSONAL_TOUCH] = CommonBusinessCustomerStarRatingType.PERSONAL_TOUCH
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'WAIT_TIME'):
            mapping[BusinessCustomerStarRatingBuffBuckets.WAIT_TIME] = CommonBusinessCustomerStarRatingType.WAIT_TIME
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'MISC'):
            mapping[BusinessCustomerStarRatingBuffBuckets.MISC] = CommonBusinessCustomerStarRatingType.MISC
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'STRESS_LEVEL'):
            mapping[BusinessCustomerStarRatingBuffBuckets.STRESS_LEVEL] = CommonBusinessCustomerStarRatingType.STRESS_LEVEL
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'SERVICE_VALUE'):
            mapping[BusinessCustomerStarRatingBuffBuckets.SERVICE_VALUE] = CommonBusinessCustomerStarRatingType.SERVICE_VALUE
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'SERVICE_QUALITY'):
            mapping[BusinessCustomerStarRatingBuffBuckets.SERVICE_QUALITY] = CommonBusinessCustomerStarRatingType.SERVICE_QUALITY
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'CUSTOMER_RELATIONSHIP'):
            mapping[BusinessCustomerStarRatingBuffBuckets.CUSTOMER_RELATIONSHIP] = CommonBusinessCustomerStarRatingType.CUSTOMER_RELATIONSHIP
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'ACTIVITIES_COMPLETED'):
            mapping[BusinessCustomerStarRatingBuffBuckets.ACTIVITIES_COMPLETED] = CommonBusinessCustomerStarRatingType.ACTIVITIES_COMPLETED
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'PRICING'):
            mapping[BusinessCustomerStarRatingBuffBuckets.PRICING] = CommonBusinessCustomerStarRatingType.PRICING
        if hasattr(BusinessCustomerStarRatingBuffBuckets, 'QUALITY'):
            mapping[BusinessCustomerStarRatingBuffBuckets.QUALITY] = CommonBusinessCustomerStarRatingType.QUALITY
        return mapping.get(value, CommonBusinessCustomerStarRatingType.INVALID)


