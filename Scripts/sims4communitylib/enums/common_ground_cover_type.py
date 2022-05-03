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
    from weather.weather_enums import GroundCoverType
except:
    class GroundCoverType(CommonInt):
        """Mock class."""
        pass


class CommonGroundCoverType(CommonInt):
    """Identifiers for ground cover types."""
    RAIN_ACCUMULATION = 1002
    SNOW_ACCUMULATION = 1003

    @classmethod
    def get_all(cls) -> Tuple['CommonGroundCoverType']:
        """get_all()

        Retrieve a collection of all CommonGroundCoverType

        :return: A collection of all CommonGroundCoverType
        :rtype: Tuple[CommonGroundCoverType]
        """
        # noinspection PyTypeChecker
        value_list: Tuple[CommonGroundCoverType, ...] = tuple([value for value in cls.values])
        return value_list

    @staticmethod
    def convert_to_vanilla(value: 'CommonGroundCoverType') -> Union[GroundCoverType, None]:
        """convert_to_vanilla(value)

        Convert a CommonGroundCoverType into the vanilla GroundCoverType enum.

        :param value: An instance of a CommonGroundCoverType
        :type value: CommonGroundCoverType
        :return: The specified CommonGroundCoverType translated to a GroundCoverType or None if a vanilla GroundCoverType is not found.
        :rtype: Union[GroundCoverType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), GroundCoverType, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: GroundCoverType) -> Union['CommonGroundCoverType', None]:
        """convert_from_vanilla(value)

        Convert a vanilla GroundCoverType into a CommonGroundCoverType enum.

        :param value: An instance of a CommonGroundCoverType
        :type value: CommonGroundCoverType
        :return: The specified GroundCoverType translated to a GroundCoverType or None if a CommonGroundCoverType is not found.
        :rtype: Union[GroundCoverType, None]
        """
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonGroundCoverType, default_value=None)
