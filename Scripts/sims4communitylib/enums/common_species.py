"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Tuple, Iterator

from sims.sim_info import SimInfo
from sims.sim_info_types import Species, SpeciesExtended
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSpecies(CommonInt):
    """Custom Species enum containing all species (including extended species).

    """
    INVALID: 'CommonSpecies' = 0
    HUMAN: 'CommonSpecies' = 1
    SMALL_DOG: 'CommonSpecies' = 2
    LARGE_DOG: 'CommonSpecies' = 3
    CAT: 'CommonSpecies' = 4
    FOX: 'CommonSpecies' = 5

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonSpecies'] = None) -> Tuple['CommonSpecies']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSpecies], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonSpecies]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonSpecies, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonSpecies'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSpecies], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonSpecies'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonSpecies], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def get_species(sim_info: SimInfo) -> 'CommonSpecies':
        """get_species(sim_info)

        Retrieve the CommonSpecies of a sim. Use this instead of CommonSpeciesUtils.get_species to determine a more specific species.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A species matching the Sim or INVALID if no matching species is found.
        :rtype: CommonSpecies
        """
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonSpecies.HUMAN
        elif CommonSpeciesUtils.is_fox(sim_info):
            return CommonSpecies.FOX
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonSpecies.SMALL_DOG
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonSpecies.LARGE_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonSpecies.CAT
        return CommonSpecies.INVALID

    @staticmethod
    def convert_to_vanilla(value: 'CommonSpecies') -> Union[Species, None]:
        """convert_to_vanilla(value)

        Convert a CommonSpecies into the vanilla Species enum.

        :param value: An instance of CommonSpecies
        :type value: CommonSpecies
        :return: The specified CommonSpecies translated to Species or SpeciesExtended or None if the CommonSpecies could not be translated.
        :rtype: Union[Species, None]
        """
        if value is None or value == CommonSpecies.INVALID:
            return None
        if isinstance(value, Species):
            return value
        conversion_mapping: Dict[CommonSpecies, Species] = {
            CommonSpecies.HUMAN: Species.HUMAN,
            CommonSpecies.SMALL_DOG: SpeciesExtended.SMALLDOG if hasattr(SpeciesExtended, 'SMALLDOG') else None,
            CommonSpecies.LARGE_DOG: Species.DOG if hasattr(Species, 'DOG') else None,
            CommonSpecies.CAT: Species.CAT if hasattr(Species, 'CAT') else None,
            CommonSpecies.FOX: Species.FOX if hasattr(Species, 'FOX') else None
        }
        return conversion_mapping.get(value, None)

    @staticmethod
    def convert_to_localized_string_id(value: 'CommonSpecies') -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a CommonSpecies into a Localized String identifier.

        :param value: An instance of a CommonSpecies
        :type value: CommonSpecies
        :return: The specified CommonSpecies translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        display_name_mapping = {
            CommonSpecies.HUMAN: CommonStringId.HUMAN,
            CommonSpecies.LARGE_DOG: CommonStringId.LARGE_DOG,
            CommonSpecies.SMALL_DOG: CommonStringId.SMALL_DOG,
            CommonSpecies.CAT: CommonStringId.CAT,
            CommonSpecies.FOX: CommonStringId.FOX
        }
        if isinstance(value, int) and not isinstance(value, CommonSpecies):
            from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
            # noinspection PyTypeChecker
            val = CommonResourceUtils.get_enum_by_int_value(value, SpeciesExtended, default_value=None)
            if val is None:
                return str(value)
            value = val
        return display_name_mapping.get(value, value.name if hasattr(value, 'name') else str(value))
