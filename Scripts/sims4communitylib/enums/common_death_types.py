"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from interactions.utils.death import DeathType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonDeathType(CommonInt):
    """Various types of deaths Sims can have."""
    NONE: 'CommonDeathType' = ...
    ANGER: 'CommonDeathType' = ...
    BEETLES: 'CommonDeathType' = ...
    BROKEN_HEART: 'CommonDeathType' = ...
    CLIMBING_ROUTE: 'CommonDeathType' = ...
    COW_PLANT: 'CommonDeathType' = ...
    CROW: 'CommonDeathType' = ...
    DEATH_FLOWER_ARRANGEMENT: 'CommonDeathType' = ...
    DROWN: 'CommonDeathType' = ...
    ELDER_EXHAUSTION: 'CommonDeathType' = ...
    ELECTROCUTION: 'CommonDeathType' = ...
    EMBARRASSMENT: 'CommonDeathType' = ...
    EMOTIONAL_STARVATION: 'CommonDeathType' = ...
    FIRE: 'CommonDeathType' = ...
    FLIES: 'CommonDeathType' = ...
    FROZEN: 'CommonDeathType' = ...
    HUNGER: 'CommonDeathType' = ...
    KILLER_CHICKEN: 'CommonDeathType' = ...
    KILLER_RABBIT: 'CommonDeathType' = ...
    LAUGHTER: 'CommonDeathType' = ...
    LIGHTNING: 'CommonDeathType' = ...
    METEORITE: 'CommonDeathType' = ...
    MOLD_SYSTEM: 'CommonDeathType' = ...
    MOTHER_PLANT: 'CommonDeathType' = ...
    MURPHY_BED: 'CommonDeathType' = ...
    OLD_AGE: 'CommonDeathType' = ...
    OVERHEAT: 'CommonDeathType' = ...
    POISON: 'CommonDeathType' = ...
    PUFFERFISH: 'CommonDeathType' = ...
    RODENT_DISEASE: 'CommonDeathType' = ...
    STEAM: 'CommonDeathType' = ...
    STINK_BOMB: 'CommonDeathType' = ...
    SUN: 'CommonDeathType' = ...
    URBAN_MYTH: 'CommonDeathType' = ...
    VENDING_MACHINE: 'CommonDeathType' = ...
    WITCH_OVERLOAD: 'CommonDeathType' = ...

    @classmethod
    def get_random(cls) -> 'CommonDeathType':
        """get_random()

        Retrieve a random death type.

        :return: A death type.
        :rtype: CommonDeathType
        """
        return CommonDeathType.convert_from_vanilla(DeathType.get_random_death_type())

    @classmethod
    def convert_to_vanilla(cls, value: Union['CommonDeathType', int, DeathType]) -> Union[DeathType, 'CommonDeathType', int]:
        """convert_to_vanilla(value)

        Convert a CommonDeathType into the vanilla DeathType enum.

        :param value: An instance of a CommonDeathType
        :type value: CommonDeathType
        :return: The specified value translated to a DeathType or the value itself if it could not be translated.
        :rtype: DeathType
        """
        if value is None or value == CommonDeathType.NONE:
            return DeathType.NONE
        if isinstance(value, DeathType):
            return value
        mapping = dict()
        if hasattr(DeathType, 'Hunger'):
            mapping[CommonDeathType.HUNGER] = DeathType.Hunger
        if hasattr(DeathType, 'Old Age'):
            mapping[CommonDeathType.OLD_AGE] = getattr(DeathType, 'Old Age')
        if hasattr(DeathType, 'Cowplant'):
            mapping[CommonDeathType.COW_PLANT] = DeathType.Cowplant
        if hasattr(DeathType, 'Electrocution'):
            mapping[CommonDeathType.ELECTROCUTION] = DeathType.Electrocution
        if hasattr(DeathType, 'Anger'):
            mapping[CommonDeathType.ANGER] = DeathType.Anger
        if hasattr(DeathType, 'Laughter'):
            mapping[CommonDeathType.LAUGHTER] = DeathType.Laughter
        if hasattr(DeathType, 'ElderExhaustion'):
            mapping[CommonDeathType.ELDER_EXHAUSTION] = DeathType.ElderExhaustion
        if hasattr(DeathType, 'Embarrassment'):
            mapping[CommonDeathType.EMBARRASSMENT] = DeathType.Embarrassment
        if hasattr(DeathType, 'EmotionalStarvation'):
            mapping[CommonDeathType.EMOTIONAL_STARVATION] = DeathType.EmotionalStarvation
        if hasattr(DeathType, 'Fire'):
            mapping[CommonDeathType.FIRE] = DeathType.Fire
        if hasattr(DeathType, 'Drown'):
            mapping[CommonDeathType.DROWN] = DeathType.Drown
        if hasattr(DeathType, 'Steam'):
            mapping[CommonDeathType.STEAM] = DeathType.Steam
        if hasattr(DeathType, 'Pufferfish'):
            mapping[CommonDeathType.PUFFERFISH] = DeathType.Pufferfish
        if hasattr(DeathType, 'Sun'):
            mapping[CommonDeathType.SUN] = DeathType.Sun
        if hasattr(DeathType, 'Poison'):
            mapping[CommonDeathType.POISON] = DeathType.Poison
        if hasattr(DeathType, 'RodentDisease'):
            mapping[CommonDeathType.RODENT_DISEASE] = DeathType.RodentDisease
        if hasattr(DeathType, 'Frozen'):
            mapping[CommonDeathType.FROZEN] = DeathType.Frozen
        if hasattr(DeathType, 'Overheat'):
            mapping[CommonDeathType.OVERHEAT] = DeathType.Overheat
        if hasattr(DeathType, 'Lightning'):
            mapping[CommonDeathType.LIGHTNING] = DeathType.Lightning
        if hasattr(DeathType, 'DeathFlowerArrangement'):
            mapping[CommonDeathType.DEATH_FLOWER_ARRANGEMENT] = DeathType.DeathFlowerArrangement
        if hasattr(DeathType, 'MotherPlant'):
            mapping[CommonDeathType.MOTHER_PLANT] = DeathType.MotherPlant
        if hasattr(DeathType, 'WitchOverload'):
            mapping[CommonDeathType.WITCH_OVERLOAD] = DeathType.WitchOverload
        if hasattr(DeathType, 'MurphyBed'):
            mapping[CommonDeathType.MURPHY_BED] = DeathType.MurphyBed
        if hasattr(DeathType, 'Flies'):
            mapping[CommonDeathType.FLIES] = DeathType.Flies
        if hasattr(DeathType, 'VendingMachine'):
            mapping[CommonDeathType.VENDING_MACHINE] = DeathType.VendingMachine
        if hasattr(DeathType, 'ClimbingRoute'):
            mapping[CommonDeathType.CLIMBING_ROUTE] = DeathType.ClimbingRoute
        if hasattr(DeathType, 'KillerRabbit'):
            mapping[CommonDeathType.KILLER_RABBIT] = DeathType.KillerRabbit
        if hasattr(DeathType, 'KillerChicken'):
            mapping[CommonDeathType.KILLER_CHICKEN] = DeathType.KillerChicken
        if hasattr(DeathType, 'Meteorite'):
            mapping[CommonDeathType.METEORITE] = DeathType.Meteorite
        if hasattr(DeathType, 'StinkBomb'):
            mapping[CommonDeathType.STINK_BOMB] = DeathType.StinkBomb
        if hasattr(DeathType, 'UrbanMyth'):
            mapping[CommonDeathType.URBAN_MYTH] = DeathType.UrbanMyth
        if hasattr(DeathType, 'MoldSystem'):
            mapping[CommonDeathType.MOLD_SYSTEM] = DeathType.MoldSystem
        if hasattr(DeathType, 'BrokenHeart'):
            mapping[CommonDeathType.BROKEN_HEART] = DeathType.BrokenHeart
        if hasattr(DeathType, 'Crow'):
            mapping[CommonDeathType.CROW] = DeathType.Crow
        if hasattr(DeathType, 'Beetles'):
            mapping[CommonDeathType.BEETLES] = DeathType.Beetles

        return mapping.get(value, DeathType.NONE)

    @classmethod
    def convert_from_vanilla(cls, value: Union[DeathType, int, 'CommonDeathType']) -> Union['CommonDeathType', DeathType, int]:
        """convert_from_vanilla(value)

        Convert a DeathType into a CommonDeathType enum.

        :param value: An instance of a DeathType
        :type value: DeathType
        :return: The specified value translated to a CommonDeathType or NONE if it could not be translated.
        :rtype: CommonDeathType
        """
        if value is None or value == DeathType.NONE:
            return CommonDeathType.NONE
        if isinstance(value, CommonDeathType):
            return value
        mapping = dict()
        if hasattr(DeathType, 'Hunger'):
            mapping[DeathType.Hunger] = CommonDeathType.HUNGER
        if hasattr(DeathType, 'Old Age'):
            mapping[getattr(DeathType, 'Old Age')] = CommonDeathType.OLD_AGE
        if hasattr(DeathType, 'Cowplant'):
            mapping[DeathType.Cowplant] = CommonDeathType.COW_PLANT
        if hasattr(DeathType, 'Electrocution'):
            mapping[DeathType.Electrocution] = CommonDeathType.ELECTROCUTION
        if hasattr(DeathType, 'Anger'):
            mapping[DeathType.Anger] = CommonDeathType.ANGER
        if hasattr(DeathType, 'Laughter'):
            mapping[DeathType.Laughter] = CommonDeathType.LAUGHTER
        if hasattr(DeathType, 'ElderExhaustion'):
            mapping[DeathType.ElderExhaustion] = CommonDeathType.ELDER_EXHAUSTION
        if hasattr(DeathType, 'Embarrassment'):
            mapping[DeathType.Embarrassment] = CommonDeathType.EMBARRASSMENT
        if hasattr(DeathType, 'EmotionalStarvation'):
            mapping[DeathType.EmotionalStarvation] = CommonDeathType.EMOTIONAL_STARVATION
        if hasattr(DeathType, 'Fire'):
            mapping[DeathType.Fire] = CommonDeathType.FIRE
        if hasattr(DeathType, 'Drown'):
            mapping[DeathType.Drown] = CommonDeathType.DROWN
        if hasattr(DeathType, 'Steam'):
            mapping[DeathType.Steam] = CommonDeathType.STEAM
        if hasattr(DeathType, 'Pufferfish'):
            mapping[DeathType.Pufferfish] = CommonDeathType.PUFFERFISH
        if hasattr(DeathType, 'Sun'):
            mapping[DeathType.Sun] = CommonDeathType.SUN
        if hasattr(DeathType, 'Poison'):
            mapping[DeathType.Poison] = CommonDeathType.POISON
        if hasattr(DeathType, 'RodentDisease'):
            mapping[DeathType.RodentDisease] = CommonDeathType.RODENT_DISEASE
        if hasattr(DeathType, 'Frozen'):
            mapping[DeathType.Frozen] = CommonDeathType.FROZEN
        if hasattr(DeathType, 'Overheat'):
            mapping[DeathType.Overheat] = CommonDeathType.OVERHEAT
        if hasattr(DeathType, 'Lightning'):
            mapping[DeathType.Lightning] = CommonDeathType.LIGHTNING
        if hasattr(DeathType, 'DeathFlowerArrangement'):
            mapping[DeathType.DeathFlowerArrangement] = CommonDeathType.DEATH_FLOWER_ARRANGEMENT
        if hasattr(DeathType, 'MotherPlant'):
            mapping[DeathType.MotherPlant] = CommonDeathType.MOTHER_PLANT
        if hasattr(DeathType, 'WitchOverload'):
            mapping[DeathType.WitchOverload] = CommonDeathType.WITCH_OVERLOAD
        if hasattr(DeathType, 'MurphyBed'):
            mapping[DeathType.MurphyBed] = CommonDeathType.MURPHY_BED
        if hasattr(DeathType, 'Flies'):
            mapping[DeathType.Flies] = CommonDeathType.FLIES
        if hasattr(DeathType, 'VendingMachine'):
            mapping[DeathType.VendingMachine] = CommonDeathType.VENDING_MACHINE
        if hasattr(DeathType, 'ClimbingRoute'):
            mapping[DeathType.ClimbingRoute] = CommonDeathType.CLIMBING_ROUTE
        if hasattr(DeathType, 'KillerRabbit'):
            mapping[DeathType.KillerRabbit] = CommonDeathType.KILLER_RABBIT
        if hasattr(DeathType, 'KillerChicken'):
            mapping[DeathType.KillerChicken] = CommonDeathType.KILLER_CHICKEN
        if hasattr(DeathType, 'Meteorite'):
            mapping[DeathType.Meteorite] = CommonDeathType.METEORITE
        if hasattr(DeathType, 'StinkBomb'):
            mapping[DeathType.StinkBomb] = CommonDeathType.STINK_BOMB
        if hasattr(DeathType, 'UrbanMyth'):
            mapping[DeathType.UrbanMyth] = CommonDeathType.URBAN_MYTH
        if hasattr(DeathType, 'MoldSystem'):
            mapping[DeathType.MoldSystem] = CommonDeathType.MOLD_SYSTEM
        if hasattr(DeathType, 'BrokenHeart'):
            mapping[DeathType.BrokenHeart] = CommonDeathType.BROKEN_HEART
        if hasattr(DeathType, 'Crow'):
            mapping[DeathType.Crow] = CommonDeathType.CROW
        if hasattr(DeathType, 'Beetles'):
            mapping[DeathType.Beetles] = CommonDeathType.BEETLES
        return mapping.get(value, CommonDeathType.NONE)
