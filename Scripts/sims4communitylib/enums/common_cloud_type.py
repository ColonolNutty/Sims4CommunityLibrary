"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Iterator

from sims4communitylib.enums.enumtypes.common_int import CommonInt

# noinspection PyBroadException
try:
    from weather.weather_enums import CloudType
except:
    class CloudType(CommonInt):
        """Mock class."""
        PARTLY_CLOUDY = 2000
        CLEAR = 2001
        LIGHT_RAINCLOUDS = 2002
        DARK_RAINCLOUDS = 2003
        # noinspection SpellCheckingInspection
        LIGHT_SNOWCLOUDS = 2004
        # noinspection SpellCheckingInspection
        DARK_SNOWCLOUDS = 2005
        CLOUDY = 2006
        HEATWAVE = 2007
        STRANGE = 2008
        VERY_STRANGE = 2009
        SKYBOX_INDUSTRIAL = 2010


class CommonCloudType(CommonInt):
    """Identifiers for cloud types."""
    PARTLY_CLOUDY: 'CommonCloudType' = ...
    CLEAR: 'CommonCloudType' = ...
    LIGHT_RAIN_CLOUDS: 'CommonCloudType' = ...
    DARK_RAIN_CLOUDS: 'CommonCloudType' = ...
    LIGHT_SNOW_CLOUDS: 'CommonCloudType' = ...
    DARK_SNOW_CLOUDS: 'CommonCloudType' = ...
    CLOUDY: 'CommonCloudType' = ...
    HEATWAVE: 'CommonCloudType' = ...
    STRANGE: 'CommonCloudType' = ...
    VERY_STRANGE: 'CommonCloudType' = ...
    SKY_BOX_INDUSTRIAL: 'CommonCloudType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonCloudType'] = ()) -> Tuple['CommonCloudType']:
        """get_all(exclude_values=())

        Get a collection of all values.

        :param exclude_values: These values will be excluded. Default is an empty collection.
        :type exclude_values: Iterator[CommonCloudType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonCloudType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonCloudType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonCloudType') -> Union[CloudType, None]:
        """convert_to_vanilla(value)

        Convert a CommonCloudType into the vanilla CloudType enum.

        :param value: An instance of CommonCloudType
        :type value: CommonCloudType
        :return: The specified CommonCloudType translated to CloudType or None if a vanilla CloudType is not found.
        :rtype: Union[CloudType, None]
        """
        if isinstance(value, CloudType):
            return value
        mapping = {
            CommonCloudType.PARTLY_CLOUDY: CloudType.PARTLY_CLOUDY,
            CommonCloudType.CLEAR: CloudType.CLEAR,
            CommonCloudType.LIGHT_RAIN_CLOUDS: CloudType.LIGHT_RAINCLOUDS,
            CommonCloudType.DARK_RAIN_CLOUDS: CloudType.DARK_RAINCLOUDS,
            CommonCloudType.LIGHT_SNOW_CLOUDS: CloudType.LIGHT_SNOWCLOUDS,
            CommonCloudType.DARK_SNOW_CLOUDS: CloudType.DARK_SNOWCLOUDS,
            CommonCloudType.CLOUDY: CloudType.CLOUDY,
            CommonCloudType.HEATWAVE: CloudType.HEATWAVE,
            CommonCloudType.STRANGE: CloudType.STRANGE,
            CommonCloudType.VERY_STRANGE: CloudType.VERY_STRANGE,
            CommonCloudType.SKY_BOX_INDUSTRIAL: CloudType.SKYBOX_INDUSTRIAL,
        }
        return mapping.get(value, value)

    @staticmethod
    def convert_from_vanilla(value: CloudType) -> Union['CommonCloudType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla CloudType into a CommonCloudType enum.

        :param value: An instance of CommonCloudType
        :type value: CommonCloudType
        :return: The specified CloudType translated to CloudType or None if the value could not be translated.
        :rtype: Union[CloudType, None]
        """
        if isinstance(value, CommonCloudType):
            return value
        mapping = {
            CloudType.PARTLY_CLOUDY: CommonCloudType.PARTLY_CLOUDY,
            CloudType.CLEAR: CommonCloudType.CLEAR,
            CloudType.LIGHT_RAINCLOUDS: CommonCloudType.LIGHT_RAIN_CLOUDS,
            CloudType.DARK_RAINCLOUDS: CommonCloudType.DARK_RAIN_CLOUDS,
            CloudType.LIGHT_SNOWCLOUDS: CommonCloudType.LIGHT_SNOW_CLOUDS,
            CloudType.DARK_SNOWCLOUDS: CommonCloudType.DARK_SNOW_CLOUDS,
            CloudType.CLOUDY: CommonCloudType.CLOUDY,
            CloudType.HEATWAVE: CommonCloudType.HEATWAVE,
            CloudType.STRANGE: CommonCloudType.STRANGE,
            CloudType.VERY_STRANGE: CommonCloudType.VERY_STRANGE,
            CloudType.SKYBOX_INDUSTRIAL: CommonCloudType.SKY_BOX_INDUSTRIAL,
        }
        return mapping.get(value, value)
