"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.puddles import PuddleLiquid
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonPuddleLiquid(CommonInt):
    """ Various types of liquids a puddle may have. """
    ACID: 'CommonPuddleLiquid' = 67585
    DARK_MATTER: 'CommonPuddleLiquid' = 1
    GREEN_GOO: 'CommonPuddleLiquid' = 2
    INVALID: 'CommonPuddleLiquid' = -1
    MUD: 'CommonPuddleLiquid' = 59393
    VOMIT: 'CommonPuddleLiquid' = 57345
    WATER: 'CommonPuddleLiquid' = 0

    @staticmethod
    def convert_to_vanilla(value: 'CommonPuddleLiquid') -> Union[PuddleLiquid, None]:
        """convert_to_vanilla(value)

        Convert a CommonPuddleLiquid into the vanilla PuddleLiquid enum.

        :param value: An instance of a CommonPuddleLiquid
        :type value: CommonPuddleLiquid
        :return: The specified CommonPuddleLiquid translated to a PuddleLiquid or None if the CommonPuddleLiquid could not be translated.
        :rtype: Union[PuddleLiquid, None]
        """
        if value is None or value == CommonPuddleLiquid.INVALID:
            return None
        if isinstance(value, PuddleLiquid):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), PuddleLiquid, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: PuddleLiquid) -> Union['CommonPuddleLiquid', None]:
        """convert_from_vanilla(value)

        Convert a PuddleLiquid into a CommonPuddleLiquid enum.

        :param value: An instance of a PuddleLiquid
        :type value: PuddleLiquid
        :return: The specified PuddleLiquid translated to a CommonPuddleLiquid or None if the PuddleLiquid could not be translated.
        :rtype: Union['CommonPuddleLiquid', None]
        """
        if value is None or value == CommonPuddleLiquid.INVALID:
            return None
        if isinstance(value, CommonPuddleLiquid):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonPuddleLiquid, default_value=None)
