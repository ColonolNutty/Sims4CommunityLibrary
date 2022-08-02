"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.utils.death import DeathType
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonDeathType(CommonInt):
    """Various types of deaths Sims can have."""
    NONE: 'CommonDeathType' = 0
    ANGER: 'CommonDeathType' = 68
    CLIMBING_ROUTE: 'CommonDeathType' = 88
    COW_PLANT: 'CommonDeathType' = 66
    DEATH_FLOWER_ARRANGEMENT: 'CommonDeathType' = 82
    DROWN: 'CommonDeathType' = 73
    ELDER_EXHAUSTION: 'CommonDeathType' = 70
    ELECTROCUTION: 'CommonDeathType' = 67
    EMBARRASSMENT: 'CommonDeathType' = 71
    FIRE: 'CommonDeathType' = 72
    FLIES: 'CommonDeathType' = 86
    FROZEN: 'CommonDeathType' = 79
    HUNGER: 'CommonDeathType' = 64
    KILLER_CHICKEN: 'CommonDeathType' = 90
    KILLER_RABBIT: 'CommonDeathType' = 89
    LAUGHTER: 'CommonDeathType' = 69
    LIGHTNING: 'CommonDeathType' = 81
    METEORITE: 'CommonDeathType' = 91
    MOTHER_PLANT: 'CommonDeathType' = 83
    MURPHY_BED: 'CommonDeathType' = 85
    OLD_AGE: 'CommonDeathType' = 65
    OVERHEAT: 'CommonDeathType' = 80
    POISON: 'CommonDeathType' = 77
    PUFFERFISH: 'CommonDeathType' = 75
    RODENT_DISEASE: 'CommonDeathType' = 78
    STEAM: 'CommonDeathType' = 74
    STINK_BOMB: 'CommonDeathType' = 92
    SUN: 'CommonDeathType' = 76
    URBAN_MYTH: 'CommonDeathType' = 93
    VENDING_MACHINE: 'CommonDeathType' = 87
    WITCH_OVERLOAD: 'CommonDeathType' = 84

    @staticmethod
    def get_random() -> 'CommonDeathType':
        """get_random()

        Retrieve a random death type.

        :return: A death type.
        :rtype: CommonDeathType
        """
        return CommonDeathType.convert_from_vanilla(DeathType.get_random_death_type())

    @staticmethod
    def convert_to_vanilla(value: 'CommonDeathType') -> DeathType:
        """convert_to_vanilla(value)

        Convert a CommonDeathType into the vanilla DeathType enum.

        :param value: An instance of a CommonDeathType
        :type value: CommonDeathType
        :return: The specified CommonDeathType translated to a DeathType or NoPuddle if the CommonDeathType could not be translated.
        :rtype: DeathType
        """
        if value is None or value == CommonDeathType.NONE:
            return DeathType.NONE
        if isinstance(value, DeathType):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), DeathType, default_value=DeathType.NONE)

    @staticmethod
    def convert_from_vanilla(value: DeathType) -> 'CommonDeathType':
        """convert_from_vanilla(value)

        Convert a DeathType into a CommonDeathType enum.

        :param value: An instance of a DeathType
        :type value: DeathType
        :return: The specified DeathType translated to a CommonDeathType or NONE if the DeathType could not be translated.
        :rtype: CommonDeathType
        """
        if value is None or value == DeathType.NONE:
            return CommonDeathType.NONE
        if isinstance(value, CommonDeathType):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonDeathType, default_value=CommonDeathType.NONE)
