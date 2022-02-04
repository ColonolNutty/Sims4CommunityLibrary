"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_spawner_enums import SimNameType
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonSimNameType(CommonInt):
    """Types of names."""
    DEFAULT = 0
    JAPANESE = 1
    MOROCCAN = 2
    INDIAN = 3
    CAT = 4
    DOG = 5
    SKELETON = 6
    LATIN = 7
    ISLANDER = 8
    CHINESE = 9
    FAMILIAR_DRAGON = 10
    FAMILIAR_BUNNERFLY = 11
    FAMILIAR_FAIRY = 12
    FAMILIAR_FROG = 13
    FAMILIAR_OWL = 14
    FAMILIAR_PHOENIX = 15
    FAMILIAR_RAVEN = 16
    FAMILIAR_SKULL = 17
    FAMILIAR_VOID_CRITTER = 18
    FAMILIAR_VOODOO_DOLL = 19
    FAMILIAR_BAT = 20
    HUMANOID_ROBOT = 21
    HUMANOID_ROBOT_GENERIC = 22
    MARKETPLACE_NAME = 23
    STAR_WARS_GENERAL = 24
    STAR_WARS_FIRST_ORDER = 25
    STAR_WARS_STORM_TROOPER = 26
    FOX = 27

    @classmethod
    def get_all(cls) -> Tuple['CommonSimNameType']:
        """get_all()

        Retrieve a collection of all CommonSimNameType, excluding CommonSimNameType.DEFAULT.

        :return: A collection of all CommonSimNameType, without CommonSimNameType.DEFAULT.
        :rtype: Tuple[CommonSimNameType]
        """
        value_list: Tuple[CommonSimNameType] = tuple([value for value in cls.values if value != cls.DEFAULT])
        return value_list

    @classmethod
    def get_all_names(cls) -> Tuple[str]:
        """get_all_names()

        Retrieve a collection of the names of all CommonSimNameType, excluding CommonSimNameType.DEFAULT.

        :return: A collection of the names of all CommonSimNameType, without CommonSimNameType.DEFAULT.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all()])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls) -> str:
        """get_comma_separated_names_string()

        Create a string containing all names of all CommonSimNameType values (excluding CommonSimNameType.DEFAULT), separated by a comma.

        :return: A string containing all names of all CommonSimNameType values (excluding CommonSimNameType.DEFAULT), separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names())

    @staticmethod
    def convert_to_vanilla(sim_name_type: 'CommonSimNameType') -> SimNameType:
        """convert_to_vanilla(sim_name_type)

        Convert a CommonSimNameType into the vanilla SimNameType enum.

        :param sim_name_type: An instance of a CommonSimNameType.
        :type sim_name_type: CommonSimNameType
        :return: The specified CommonSimNameType translated to a SimNameType or SimNameType.DEFAULT if the CommonSimNameType could not be translated.
        :rtype: SimNameType
        """
        return CommonResourceUtils.get_enum_by_int_value(int(sim_name_type), SimNameType, default_value=SimNameType.DEFAULT)

    @staticmethod
    def convert_from_vanilla(sim_name_type: SimNameType) -> 'CommonSimNameType':
        """convert_from_vanilla(sim_name_type)

        Convert a vanilla SimNameType into a CommonSimNameType enum.

        :param sim_name_type: An instance of a SimNameType.
        :type sim_name_type: SimNameType
        :return: The specified SimNameType translated to a CommonSimNameType or CommonSimNameType.DEFAULT if the SimNameType could not be translated.
        :rtype: CommonSimNameType
        """
        return CommonResourceUtils.get_enum_by_int_value(int(sim_name_type), CommonSimNameType, default_value=CommonSimNameType.DEFAULT)
