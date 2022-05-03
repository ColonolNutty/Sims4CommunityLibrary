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
    from weather.weather_enums import Temperature
except:
    class Temperature(CommonInt):
        """Mock class."""
        pass


class CommonTemperature(CommonInt):
    """Identifiers for temperatures."""
    FREEZING: 'CommonTemperature' = -3
    COLD: 'CommonTemperature' = -2
    COOL: 'CommonTemperature' = -1
    WARM: 'CommonTemperature' = 0
    HOT: 'CommonTemperature' = 1
    BURNING: 'CommonTemperature' = 2

    @classmethod
    def get_all(cls) -> Tuple['CommonTemperature']:
        """get_all()

        Retrieve a collection of all CommonTemperature

        :return: A collection of all CommonTemperature
        :rtype: Tuple[CommonTemperature]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonTemperature, ...] = tuple([value for value in cls.values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonTemperature') -> Union[Temperature, None]:
        """convert_to_vanilla(value)

        Convert a CommonTemperature into the vanilla Temperature enum.

        :param value: An instance of a CommonTemperature
        :type value: CommonTemperature
        :return: The specified CommonTemperature translated to a Temperature or None if a vanilla Temperature is not found.
        :rtype: Union[Temperature, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), Temperature, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: Temperature) -> Union['CommonTemperature', None]:
        """convert_from_vanilla(value)

        Convert a vanilla Temperature into a CommonTemperature enum.

        :param value: An instance of a CommonTemperature
        :type value: CommonTemperature
        :return: The specified Temperature translated to a Temperature or None if a CommonTemperature is not found.
        :rtype: Union[Temperature, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonTemperature, default_value=None)
