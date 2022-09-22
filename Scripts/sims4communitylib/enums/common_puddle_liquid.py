"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.puddles import PuddleLiquid
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonPuddleLiquid(CommonInt):
    """ Various types of liquids a puddle may have. """
    INVALID: 'CommonPuddleLiquid' = ...
    ACID: 'CommonPuddleLiquid' = ...
    DARK_MATTER: 'CommonPuddleLiquid' = ...
    GREEN_GOO: 'CommonPuddleLiquid' = ...
    MUD: 'CommonPuddleLiquid' = ...
    VOMIT: 'CommonPuddleLiquid' = ...
    WATER: 'CommonPuddleLiquid' = ...

    @staticmethod
    def convert_to_vanilla(value: 'CommonPuddleLiquid') -> Union[PuddleLiquid, None]:
        """convert_to_vanilla(value)

        Convert a value into the vanilla PuddleLiquid enum.

        :param value: An instance of a CommonPuddleLiquid
        :type value: CommonPuddleLiquid
        :return: The specified value translated to a PuddleLiquid or INVALID if the value could not be translated.
        :rtype: Union[PuddleLiquid, None]
        """
        if value is None or value == CommonPuddleLiquid.INVALID:
            return PuddleLiquid.INVALID
        if isinstance(value, PuddleLiquid):
            return value
        mapping = dict()
        if hasattr(PuddleLiquid, 'WATER'):
            mapping[CommonPuddleLiquid.WATER] = PuddleLiquid.WATER
        if hasattr(PuddleLiquid, 'Dark Matter'):
            mapping[CommonPuddleLiquid.DARK_MATTER] = getattr(PuddleLiquid, 'Dark Matter')
        if hasattr(PuddleLiquid, 'GreenGoo'):
            mapping[CommonPuddleLiquid.GREEN_GOO] = PuddleLiquid.GreenGoo
        if hasattr(PuddleLiquid, 'Vomit'):
            mapping[CommonPuddleLiquid.VOMIT] = PuddleLiquid.Vomit
        if hasattr(PuddleLiquid, 'Mud'):
            mapping[CommonPuddleLiquid.MUD] = PuddleLiquid.Mud
        if hasattr(PuddleLiquid, 'Acid'):
            mapping[CommonPuddleLiquid.ACID] = PuddleLiquid.Acid
        return mapping.get(value, PuddleLiquid.INVALID)

    @staticmethod
    def convert_from_vanilla(value: PuddleLiquid) -> Union['CommonPuddleLiquid', None]:
        """convert_from_vanilla(value)

        Convert a value into a CommonPuddleLiquid enum.

        :param value: An instance of a PuddleLiquid
        :type value: PuddleLiquid
        :return: The specified value translated to a CommonPuddleLiquid or INVALID if the value could not be translated.
        :rtype: Union['CommonPuddleLiquid', None]
        """
        if value is None or value == CommonPuddleLiquid.INVALID:
            return PuddleLiquid.INVALID
        if isinstance(value, CommonPuddleLiquid):
            return value
        mapping = dict()
        if hasattr(PuddleLiquid, 'WATER'):
            mapping[PuddleLiquid.WATER] = CommonPuddleLiquid.WATER
        if hasattr(PuddleLiquid, 'Dark Matter'):
            mapping[getattr(PuddleLiquid, 'Dark Matter')] = CommonPuddleLiquid.DARK_MATTER
        if hasattr(PuddleLiquid, 'GreenGoo'):
            mapping[PuddleLiquid.GreenGoo] = CommonPuddleLiquid.GREEN_GOO
        if hasattr(PuddleLiquid, 'Vomit'):
            mapping[PuddleLiquid.Vomit] = CommonPuddleLiquid.VOMIT
        if hasattr(PuddleLiquid, 'Mud'):
            mapping[PuddleLiquid.Mud] = CommonPuddleLiquid.MUD
        if hasattr(PuddleLiquid, 'Acid'):
            mapping[PuddleLiquid.Acid] = CommonPuddleLiquid.ACID
        return mapping.get(value, PuddleLiquid.INVALID)
