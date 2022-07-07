"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.puddles import PuddleSize
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonPuddleSize(CommonInt):
    """ Various sizes of puddles. """
    NONE: 'CommonPuddleSize' = 0
    SMALL: 'CommonPuddleSize' = 1
    MEDIUM: 'CommonPuddleSize' = 2
    LARGE: 'CommonPuddleSize' = 3

    @staticmethod
    def convert_to_vanilla(value: 'CommonPuddleSize') -> PuddleSize:
        """convert_to_vanilla(value)

        Convert a CommonPuddleSize into the vanilla PuddleSize enum.

        :param value: An instance of a CommonPuddleSize
        :type value: CommonPuddleSize
        :return: The specified CommonPuddleSize translated to a PuddleSize or NoPuddle if the CommonPuddleSize could not be translated.
        :rtype: PuddleSize
        """
        if value is None or value == CommonPuddleSize.NONE:
            return PuddleSize.NoPuddle
        if isinstance(value, PuddleSize):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), PuddleSize, default_value=PuddleSize.NoPuddle)

    @staticmethod
    def convert_from_vanilla(value: PuddleSize) -> 'CommonPuddleSize':
        """convert_from_vanilla(value)

        Convert a PuddleSize into a CommonPuddleSize enum.

        :param value: An instance of a PuddleSize
        :type value: PuddleSize
        :return: The specified PuddleSize translated to a CommonPuddleSize or NONE if the PuddleSize could not be translated.
        :rtype: CommonPuddleSize
        """
        if value is None or value == CommonPuddleSize.NONE:
            return PuddleSize.NoPuddle
        if isinstance(value, CommonPuddleSize):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonPuddleSize, default_value=CommonPuddleSize.NONE)
