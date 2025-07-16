"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator

from sims.sim_spawner_enums import SimNameType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSimNameType(CommonInt):
    """Types of names."""
    DEFAULT: 'CommonSimNameType' = ...
    JAPANESE: 'CommonSimNameType' = ...
    MOROCCAN: 'CommonSimNameType' = ...
    INDIAN: 'CommonSimNameType' = ...
    CAT: 'CommonSimNameType' = ...
    DOG: 'CommonSimNameType' = ...
    SKELETON: 'CommonSimNameType' = ...
    LATIN: 'CommonSimNameType' = ...
    ISLANDER: 'CommonSimNameType' = ...
    CHINESE: 'CommonSimNameType' = ...
    FAMILIAR_DRAGON: 'CommonSimNameType' = ...
    FAMILIAR_BUNNERFLY: 'CommonSimNameType' = ...
    FAMILIAR_FAIRY: 'CommonSimNameType' = ...
    FAMILIAR_FROG: 'CommonSimNameType' = ...
    FAMILIAR_OWL: 'CommonSimNameType' = ...
    FAMILIAR_PHOENIX: 'CommonSimNameType' = ...
    FAMILIAR_RAVEN: 'CommonSimNameType' = ...
    FAMILIAR_SKULL: 'CommonSimNameType' = ...
    FAMILIAR_VOID_CRITTER: 'CommonSimNameType' = ...
    FAMILIAR_VOODOO_DOLL: 'CommonSimNameType' = ...
    FAMILIAR_BAT: 'CommonSimNameType' = ...
    HUMANOID_ROBOT: 'CommonSimNameType' = ...
    HUMANOID_ROBOT_GENERIC: 'CommonSimNameType' = ...
    MARKETPLACE_NAME: 'CommonSimNameType' = ...
    MARKETPLACE_FASHION_NAME: 'CommonSimNameType' = ...
    STAR_WARS_GENERAL: 'CommonSimNameType' = ...
    STAR_WARS_FIRST_ORDER: 'CommonSimNameType' = ...
    STAR_WARS_STORM_TROOPER: 'CommonSimNameType' = ...
    FOX: 'CommonSimNameType' = ...
    HORSE: 'CommonSimNameType' = ...
    SOUTH_EAST_ASIAN: 'CommonSimNameType' = ...
    NATIVE_AMERICAN: 'CommonSimNameType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonSimNameType'] = None) -> Tuple['CommonSimNameType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, DEFAULT will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSimNameType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonSimNameType]
        """
        if exclude_values is None:
            exclude_values = (cls.DEFAULT,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonSimNameType] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonSimNameType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, DEFAULT will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSimNameType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonSimNameType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, DEFAULT will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSimNameType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @classmethod
    def convert_to_vanilla(cls, value: 'CommonSimNameType') -> SimNameType:
        """convert_to_vanilla(value)

        Convert a value into the vanilla SimNameType enum.

        :param value: An instance of CommonSimNameType.
        :type value: CommonSimNameType
        :return: The specified value translated to SimNameType or DEFAULT if the value could not be translated.
        :rtype: SimNameType
        """
        if value is None or value == CommonSimNameType.DEFAULT:
            return SimNameType.DEFAULT
        if isinstance(value, SimNameType):
            return value
        mapping = dict()
        if hasattr(SimNameType, 'Japanese'):
            mapping[CommonSimNameType.JAPANESE] = SimNameType.Japanese
        if hasattr(SimNameType, 'Moroccan'):
            mapping[CommonSimNameType.MOROCCAN] = SimNameType.Moroccan
        if hasattr(SimNameType, 'Indian'):
            mapping[CommonSimNameType.INDIAN] = SimNameType.Indian
        if hasattr(SimNameType, 'Cat'):
            mapping[CommonSimNameType.CAT] = SimNameType.Cat
        if hasattr(SimNameType, 'Dog'):
            mapping[CommonSimNameType.DOG] = SimNameType.Dog
        if hasattr(SimNameType, 'Skeleton'):
            mapping[CommonSimNameType.SKELETON] = SimNameType.Skeleton
        if hasattr(SimNameType, 'Latin'):
            mapping[CommonSimNameType.LATIN] = SimNameType.Latin
        if hasattr(SimNameType, 'Islander'):
            mapping[CommonSimNameType.ISLANDER] = SimNameType.Islander
        if hasattr(SimNameType, 'Chinese'):
            mapping[CommonSimNameType.CHINESE] = SimNameType.Chinese
        if hasattr(SimNameType, 'FamiliarDragon'):
            mapping[CommonSimNameType.FAMILIAR_DRAGON] = SimNameType.FamiliarDragon
        if hasattr(SimNameType, 'FamiliarBunnerfly'):
            mapping[CommonSimNameType.FAMILIAR_BUNNERFLY] = SimNameType.FamiliarBunnerfly
        if hasattr(SimNameType, 'FamiliarFairy'):
            mapping[CommonSimNameType.FAMILIAR_FAIRY] = SimNameType.FamiliarFairy
        if hasattr(SimNameType, 'FamiliarFrog'):
            mapping[CommonSimNameType.FAMILIAR_FROG] = SimNameType.FamiliarFrog
        if hasattr(SimNameType, 'FamiliarOwl'):
            mapping[CommonSimNameType.FAMILIAR_OWL] = SimNameType.FamiliarOwl
        if hasattr(SimNameType, 'FamiliarPhoenix'):
            mapping[CommonSimNameType.FAMILIAR_PHOENIX] = SimNameType.FamiliarPhoenix
        if hasattr(SimNameType, 'FamiliarRaven'):
            mapping[CommonSimNameType.FAMILIAR_RAVEN] = SimNameType.FamiliarRaven
        if hasattr(SimNameType, 'FamiliarSkull'):
            mapping[CommonSimNameType.FAMILIAR_SKULL] = SimNameType.FamiliarSkull
        if hasattr(SimNameType, 'FamiliarVoidcritter'):
            mapping[CommonSimNameType.FAMILIAR_VOID_CRITTER] = SimNameType.FamiliarVoidcritter
        if hasattr(SimNameType, 'FamiliarVoodooDoll'):
            mapping[CommonSimNameType.FAMILIAR_VOODOO_DOLL] = SimNameType.FamiliarVoodooDoll
        if hasattr(SimNameType, 'FamiliarBat'):
            mapping[CommonSimNameType.FAMILIAR_BAT] = SimNameType.FamiliarBat
        if hasattr(SimNameType, 'HumanoidRobot'):
            mapping[CommonSimNameType.HUMANOID_ROBOT] = SimNameType.HumanoidRobot
        if hasattr(SimNameType, 'HumanoidRobot_Generic'):
            mapping[CommonSimNameType.HUMANOID_ROBOT_GENERIC] = SimNameType.HumanoidRobot_Generic
        if hasattr(SimNameType, 'Marketplace_Name'):
            mapping[CommonSimNameType.MARKETPLACE_NAME] = SimNameType.Marketplace_Name
        if hasattr(SimNameType, 'StarWars_General'):
            mapping[CommonSimNameType.STAR_WARS_GENERAL] = SimNameType.StarWars_General
        if hasattr(SimNameType, 'StarWars_FirstOrder'):
            mapping[CommonSimNameType.STAR_WARS_FIRST_ORDER] = SimNameType.StarWars_FirstOrder
        if hasattr(SimNameType, 'StarWars_Stormtrooper'):
            mapping[CommonSimNameType.STAR_WARS_STORM_TROOPER] = SimNameType.StarWars_Stormtrooper
        if hasattr(SimNameType, 'Fox'):
            mapping[CommonSimNameType.FOX] = SimNameType.Fox
        if hasattr(SimNameType, 'FashionMarketplace_Name'):
            mapping[CommonSimNameType.MARKETPLACE_FASHION_NAME] = SimNameType.FashionMarketplace_Name
        if hasattr(SimNameType, 'Horse'):
            mapping[CommonSimNameType.HORSE] = SimNameType.Horse
        if hasattr(SimNameType, 'SoutheastAsian'):
            mapping[CommonSimNameType.SOUTH_EAST_ASIAN] = SimNameType.SoutheastAsian
        if hasattr(SimNameType, 'NativeAmerican'):
            mapping[CommonSimNameType.NATIVE_AMERICAN] = SimNameType.NativeAmerican
        return mapping.get(value, SimNameType.DEFAULT)

    @classmethod
    def convert_from_vanilla(cls, value: SimNameType) -> 'CommonSimNameType':
        """convert_from_vanilla(value)

        Convert a vanilla value into a CommonSimNameType enum.

        :param value: An instance of SimNameType.
        :type value: SimNameType
        :return: The specified value translated to CommonSimNameType or DEFAULT if the value could not be translated.
        :rtype: CommonSimNameType
        """
        if value is None or value == SimNameType.DEFAULT:
            return CommonSimNameType.DEFAULT
        if isinstance(value, CommonSimNameType):
            return value
        mapping = dict()
        if hasattr(SimNameType, 'Japanese'):
            mapping[SimNameType.Japanese] = CommonSimNameType.JAPANESE
        if hasattr(SimNameType, 'Moroccan'):
            mapping[SimNameType.Moroccan] = CommonSimNameType.MOROCCAN
        if hasattr(SimNameType, 'Indian'):
            mapping[SimNameType.Indian] = CommonSimNameType.INDIAN
        if hasattr(SimNameType, 'Cat'):
            mapping[SimNameType.Cat] = CommonSimNameType.CAT
        if hasattr(SimNameType, 'Dog'):
            mapping[SimNameType.Dog] = CommonSimNameType.DOG
        if hasattr(SimNameType, 'Skeleton'):
            mapping[SimNameType.Skeleton] = CommonSimNameType.SKELETON
        if hasattr(SimNameType, 'Latin'):
            mapping[SimNameType.Latin] = CommonSimNameType.LATIN
        if hasattr(SimNameType, 'Islander'):
            mapping[SimNameType.Islander] = CommonSimNameType.ISLANDER
        if hasattr(SimNameType, 'Chinese'):
            mapping[SimNameType.Chinese] = CommonSimNameType.CHINESE
        if hasattr(SimNameType, 'FamiliarDragon'):
            mapping[SimNameType.FamiliarDragon] = CommonSimNameType.FAMILIAR_DRAGON
        if hasattr(SimNameType, 'FamiliarBunnerfly'):
            mapping[SimNameType.FamiliarBunnerfly] = CommonSimNameType.FAMILIAR_BUNNERFLY
        if hasattr(SimNameType, 'FamiliarFairy'):
            mapping[SimNameType.FamiliarFairy] = CommonSimNameType.FAMILIAR_FAIRY
        if hasattr(SimNameType, 'FamiliarFrog'):
            mapping[SimNameType.FamiliarFrog] = CommonSimNameType.FAMILIAR_FROG
        if hasattr(SimNameType, 'FamiliarOwl'):
            mapping[SimNameType.FamiliarOwl] = CommonSimNameType.FAMILIAR_OWL
        if hasattr(SimNameType, 'FamiliarPhoenix'):
            mapping[SimNameType.FamiliarPhoenix] = CommonSimNameType.FAMILIAR_PHOENIX
        if hasattr(SimNameType, 'FamiliarRaven'):
            mapping[SimNameType.FamiliarRaven] = CommonSimNameType.FAMILIAR_RAVEN
        if hasattr(SimNameType, 'FamiliarSkull'):
            mapping[SimNameType.FamiliarSkull] = CommonSimNameType.FAMILIAR_SKULL
        if hasattr(SimNameType, 'FamiliarVoidcritter'):
            mapping[SimNameType.FamiliarVoidcritter] = CommonSimNameType.FAMILIAR_VOID_CRITTER
        if hasattr(SimNameType, 'FamiliarVoodooDoll'):
            mapping[SimNameType.FamiliarVoodooDoll] = CommonSimNameType.FAMILIAR_VOODOO_DOLL
        if hasattr(SimNameType, 'FamiliarBat'):
            mapping[SimNameType.FamiliarBat] = CommonSimNameType.FAMILIAR_BAT
        if hasattr(SimNameType, 'HumanoidRobot'):
            mapping[SimNameType.HumanoidRobot] = CommonSimNameType.HUMANOID_ROBOT
        if hasattr(SimNameType, 'HumanoidRobot_Generic'):
            mapping[SimNameType.HumanoidRobot_Generic] = CommonSimNameType.HUMANOID_ROBOT_GENERIC
        if hasattr(SimNameType, 'Marketplace_Name'):
            mapping[SimNameType.Marketplace_Name] = CommonSimNameType.MARKETPLACE_NAME
        if hasattr(SimNameType, 'StarWars_General'):
            mapping[SimNameType.StarWars_General] = CommonSimNameType.STAR_WARS_GENERAL
        if hasattr(SimNameType, 'StarWars_FirstOrder'):
            mapping[SimNameType.StarWars_FirstOrder] = CommonSimNameType.STAR_WARS_FIRST_ORDER
        if hasattr(SimNameType, 'StarWars_Stormtrooper'):
            mapping[SimNameType.StarWars_Stormtrooper] = CommonSimNameType.STAR_WARS_STORM_TROOPER
        if hasattr(SimNameType, 'Fox'):
            mapping[SimNameType.Fox] = CommonSimNameType.FOX
        if hasattr(SimNameType, 'FashionMarketplace_Name'):
            mapping[SimNameType.FashionMarketplace_Name] = CommonSimNameType.MARKETPLACE_FASHION_NAME
        if hasattr(SimNameType, 'Horse'):
            mapping[SimNameType.Horse] = CommonSimNameType.HORSE
        if hasattr(SimNameType, 'SoutheastAsian'):
            mapping[SimNameType.SoutheastAsian] = CommonSimNameType.SOUTH_EAST_ASIAN
        if hasattr(SimNameType, 'NativeAmerican'):
            mapping[SimNameType.NativeAmerican] = CommonSimNameType.NATIVE_AMERICAN
        return mapping.get(value, CommonSimNameType.DEFAULT)
