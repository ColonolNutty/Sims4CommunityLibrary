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
    from weather.weather_enums import CloudType
except:
    class CloudType(CommonInt):
        """Mock class."""
        pass


class CommonCloudType(CommonInt):
    """Identifiers for cloud types."""
    PARTLY_CLOUDY: 'CommonCloudType' = 2000
    CLEAR: 'CommonCloudType' = 2001
    LIGHT_RAIN_CLOUDS: 'CommonCloudType' = 2002
    DARK_RAIN_CLOUDS: 'CommonCloudType' = 2003
    LIGHT_SNOW_CLOUDS: 'CommonCloudType' = 2004
    DARK_SNOW_CLOUDS: 'CommonCloudType' = 2005
    CLOUDY: 'CommonCloudType' = 2006
    HEATWAVE: 'CommonCloudType' = 2007
    STRANGE: 'CommonCloudType' = 2008
    VERY_STRANGE: 'CommonCloudType' = 2009
    SKY_BOX_INDUSTRIAL: 'CommonCloudType' = 2010

    @classmethod
    def get_all(cls) -> Tuple['CommonCloudType']:
        """get_all()

        Retrieve a collection of all CommonCloudType

        :return: A collection of all CommonCloudType
        :rtype: Tuple[CommonCloudType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonCloudType, ...] = tuple([value for value in cls.values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonCloudType') -> Union[CloudType, None]:
        """convert_to_vanilla(value)

        Convert a CommonCloudType into the vanilla CloudType enum.

        :param value: An instance of a CommonCloudType
        :type value: CommonCloudType
        :return: The specified CommonCloudType translated to a CloudType or None if a vanilla CloudType is not found.
        :rtype: Union[CloudType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CloudType, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: CloudType) -> Union['CommonCloudType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla CloudType into a CommonCloudType enum.

        :param value: An instance of a CommonCloudType
        :type value: CommonCloudType
        :return: The specified CloudType translated to a CloudType or None if a CommonCloudType is not found.
        :rtype: Union[CloudType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonCloudType, default_value=None)
