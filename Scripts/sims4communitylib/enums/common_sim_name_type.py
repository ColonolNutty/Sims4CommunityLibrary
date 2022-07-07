"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator

from sims.sim_spawner_enums import SimNameType
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonSimNameType(CommonInt):
    """Types of names."""
    DEFAULT: 'CommonSimNameType' = 0
    JAPANESE: 'CommonSimNameType' = 1
    MOROCCAN: 'CommonSimNameType' = 2
    INDIAN: 'CommonSimNameType' = 3
    CAT: 'CommonSimNameType' = 4
    DOG: 'CommonSimNameType' = 5
    SKELETON: 'CommonSimNameType' = 6
    LATIN: 'CommonSimNameType' = 7
    ISLANDER: 'CommonSimNameType' = 8
    CHINESE: 'CommonSimNameType' = 9
    FAMILIAR_DRAGON: 'CommonSimNameType' = 10
    FAMILIAR_BUNNERFLY: 'CommonSimNameType' = 11
    FAMILIAR_FAIRY: 'CommonSimNameType' = 12
    FAMILIAR_FROG: 'CommonSimNameType' = 13
    FAMILIAR_OWL: 'CommonSimNameType' = 14
    FAMILIAR_PHOENIX: 'CommonSimNameType' = 15
    FAMILIAR_RAVEN: 'CommonSimNameType' = 16
    FAMILIAR_SKULL: 'CommonSimNameType' = 17
    FAMILIAR_VOID_CRITTER: 'CommonSimNameType' = 18
    FAMILIAR_VOODOO_DOLL: 'CommonSimNameType' = 19
    FAMILIAR_BAT: 'CommonSimNameType' = 20
    HUMANOID_ROBOT: 'CommonSimNameType' = 21
    HUMANOID_ROBOT_GENERIC: 'CommonSimNameType' = 22
    MARKETPLACE_NAME: 'CommonSimNameType' = 23
    STAR_WARS_GENERAL: 'CommonSimNameType' = 24
    STAR_WARS_FIRST_ORDER: 'CommonSimNameType' = 25
    STAR_WARS_STORM_TROOPER: 'CommonSimNameType' = 26
    FOX: 'CommonSimNameType' = 27

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

    @staticmethod
    def convert_to_vanilla(sim_name_type: 'CommonSimNameType') -> SimNameType:
        """convert_to_vanilla(sim_name_type)

        Convert a CommonSimNameType into the vanilla SimNameType enum.

        :param sim_name_type: An instance of CommonSimNameType.
        :type sim_name_type: CommonSimNameType
        :return: The specified CommonSimNameType translated to SimNameType or DEFAULT if the CommonSimNameType could not be translated.
        :rtype: SimNameType
        """
        return CommonResourceUtils.get_enum_by_int_value(int(sim_name_type), SimNameType, default_value=SimNameType.DEFAULT)

    @staticmethod
    def convert_from_vanilla(sim_name_type: SimNameType) -> 'CommonSimNameType':
        """convert_from_vanilla(sim_name_type)

        Convert a vanilla SimNameType into a CommonSimNameType enum.

        :param sim_name_type: An instance of SimNameType.
        :type sim_name_type: SimNameType
        :return: The specified SimNameType translated to CommonSimNameType or DEFAULT if the SimNameType could not be translated.
        :rtype: CommonSimNameType
        """
        return CommonResourceUtils.get_enum_by_int_value(int(sim_name_type), CommonSimNameType, default_value=CommonSimNameType.DEFAULT)
