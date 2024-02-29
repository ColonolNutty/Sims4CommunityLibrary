"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.puddles import PuddleSize
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonPuddleSize(CommonInt):
    """ Various sizes of puddles. """
    NONE: 'CommonPuddleSize' = ...
    SMALL: 'CommonPuddleSize' = ...
    MEDIUM: 'CommonPuddleSize' = ...
    LARGE: 'CommonPuddleSize' = ...

    @staticmethod
    def convert_to_vanilla(value: 'CommonPuddleSize') -> PuddleSize:
        """convert_to_vanilla(value)

        Convert a value into the vanilla PuddleSize enum.

        :param value: An instance of a CommonPuddleSize
        :type value: CommonPuddleSize
        :return: The specified value translated to a PuddleSize or NoPuddle if the value could not be translated.
        :rtype: PuddleSize
        """
        if value is None or value == CommonPuddleSize.NONE:
            return PuddleSize.NoPuddle
        if isinstance(value, PuddleSize):
            return value
        mapping = {
            CommonPuddleSize.SMALL: PuddleSize.SmallPuddle,
            CommonPuddleSize.MEDIUM: PuddleSize.MediumPuddle,
            CommonPuddleSize.LARGE: PuddleSize.LargePuddle,
        }
        return mapping.get(value, PuddleSize.NoPuddle)

    @staticmethod
    def convert_from_vanilla(value: PuddleSize) -> 'CommonPuddleSize':
        """convert_from_vanilla(value)

        Convert a value into a CommonPuddleSize enum.

        :param value: An instance of a PuddleSize
        :type value: PuddleSize
        :return: The specified value translated to a CommonPuddleSize or NONE if the value could not be translated.
        :rtype: CommonPuddleSize
        """
        if value is None or value == PuddleSize.NoPuddle:
            return CommonPuddleSize.NONE
        if isinstance(value, CommonPuddleSize):
            return value
        mapping = {
            PuddleSize.SmallPuddle: CommonPuddleSize.SMALL,
            PuddleSize.MediumPuddle: CommonPuddleSize.MEDIUM,
            PuddleSize.LargePuddle: CommonPuddleSize.LARGE,
        }
        return mapping.get(value, CommonPuddleSize.NONE)
