"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from sims4communitylib.enums.enumtypes.common_int import CommonInt

# noinspection PyBroadException
try:
    from weather.weather_enums import PrecipitationType
except:
    class PrecipitationType(CommonInt):
        """Mock class."""
        pass


class CommonPrecipitationType(CommonInt):
    """Identifiers for precipitation types."""
    RAIN: 'CommonPrecipitationType' = 1000
    SNOW: 'CommonPrecipitationType' = 1001

    @classmethod
    def get_all(cls) -> Tuple['CommonPrecipitationType']:
        """get_all()

        Retrieve a collection of all CommonPrecipitationType

        :return: A collection of all CommonPrecipitationType
        :rtype: Tuple[CommonPrecipitationType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonPrecipitationType, ...] = tuple([value for value in cls.values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonPrecipitationType') -> Union[PrecipitationType, None]:
        """convert_to_vanilla(value)

        Convert a CommonPrecipitationType into the vanilla PrecipitationType enum.

        :param value: An instance of a CommonPrecipitationType
        :type value: CommonPrecipitationType
        :return: The specified CommonPrecipitationType translated to a PrecipitationType or None if a vanilla PrecipitationType is not found.
        :rtype: Union[PrecipitationType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), PrecipitationType, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: PrecipitationType) -> Union['CommonPrecipitationType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla PrecipitationType into a CommonPrecipitationType enum.

        :param value: An instance of a CommonPrecipitationType
        :type value: CommonPrecipitationType
        :return: The specified PrecipitationType translated to a PrecipitationType or None if a CommonPrecipitationType is not found.
        :rtype: Union[PrecipitationType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonPrecipitationType, default_value=None)
