"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator

from sims.sim_info import SimInfo
from sims.sim_info_types import Species, SpeciesExtended
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSpecies(CommonInt):
    """Custom Species enum containing all species (including extended species).

    """
    INVALID: 'CommonSpecies' = ...
    HUMAN: 'CommonSpecies' = ...
    SMALL_DOG: 'CommonSpecies' = ...
    LARGE_DOG: 'CommonSpecies' = ...
    CAT: 'CommonSpecies' = ...
    FOX: 'CommonSpecies' = ...
    HORSE: 'CommonSpecies' = ...

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
        elif CommonSpeciesUtils.is_horse(sim_info):
            return CommonSpecies.HORSE
        return CommonSpecies.INVALID

    @staticmethod
    def convert_to_vanilla(value: 'CommonSpecies') -> Union[SpeciesExtended, None]:
        """convert_to_vanilla(value)

        Convert a value into the vanilla SpeciesExtended enum.

        :param value: An instance of CommonSpecies
        :type value: CommonSpecies
        :return: The specified value translated to SpeciesExtended or INVALID if the value could not be translated.
        :rtype: Union[SpeciesExtended, None]
        """
        if value is None or value == CommonSpecies.INVALID:
            return None
        if isinstance(value, SpeciesExtended) or isinstance(value, Species):
            # noinspection PyTypeChecker
            return value
        mapping = {
            CommonSpecies.HUMAN: SpeciesExtended.HUMAN,
        }
        if hasattr(SpeciesExtended, 'SMALLDOG'):
            mapping[CommonSpecies.SMALL_DOG] = SpeciesExtended.SMALLDOG
        if hasattr(SpeciesExtended, 'DOG'):
            mapping[CommonSpecies.LARGE_DOG] = SpeciesExtended.DOG
        if hasattr(SpeciesExtended, 'CAT'):
            mapping[CommonSpecies.CAT] = SpeciesExtended.CAT
        if hasattr(SpeciesExtended, 'FOX'):
            mapping[CommonSpecies.FOX] = SpeciesExtended.FOX
        if hasattr(SpeciesExtended, 'HORSE'):
            mapping[CommonSpecies.HORSE] = SpeciesExtended.HORSE
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: SpeciesExtended) -> 'CommonSpecies':
        """convert_from_vanilla(value)

        Convert a value into a CommonSpecies enum.

        :param value: An instance of SpeciesExtended
        :type value: SpeciesExtended
        :return: The specified value translated to CommonSpecies or INVALID if the value could not be translated.
        :rtype: CommonSpecies
        """
        if value is None or value == CommonSpecies.INVALID:
            return SpeciesExtended.INVALID
        if isinstance(value, CommonSpecies):
            # noinspection PyTypeChecker
            return value
        mapping = {
            Species.HUMAN: CommonSpecies.HUMAN,
        }
        if hasattr(SpeciesExtended, 'SMALLDOG'):
            mapping[SpeciesExtended.SMALLDOG] = CommonSpecies.SMALL_DOG
        if hasattr(Species, 'DOG'):
            mapping[Species.DOG] = CommonSpecies.LARGE_DOG
        if hasattr(Species, 'CAT'):
            mapping[Species.CAT] = CommonSpecies.CAT
        if hasattr(Species, 'FOX'):
            mapping[Species.FOX] = CommonSpecies.FOX
        if hasattr(Species, 'HORSE'):
            mapping[Species.HORSE] = CommonSpecies.HORSE
        return mapping.get(value, CommonSpecies.INVALID)

    @staticmethod
    def convert_to_localized_string_id(value: 'CommonSpecies') -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a value into a Localized String identifier.

        :param value: An instance of a CommonSpecies
        :type value: CommonSpecies
        :return: The specified value translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        from sims4communitylib.enums.strings_enum import CommonStringId
        display_name_mapping = {
            CommonSpecies.HUMAN: CommonStringId.HUMAN,
            CommonSpecies.LARGE_DOG: CommonStringId.LARGE_DOG,
            CommonSpecies.SMALL_DOG: CommonStringId.SMALL_DOG,
            CommonSpecies.CAT: CommonStringId.CAT,
            CommonSpecies.FOX: CommonStringId.FOX,
            CommonSpecies.HORSE: CommonStringId.HORSE,
        }
        if isinstance(value, int) and not isinstance(value, CommonSpecies):
            from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
            # noinspection PyTypeChecker
            converted_value = CommonResourceUtils.get_enum_by_int_value(value, SpeciesExtended, default_value=None)
            if converted_value is None:
                return str(value)
            value = CommonSpecies.convert_from_vanilla(converted_value)
        if not isinstance(value, CommonSpecies):
            # noinspection PyTypeChecker
            value = CommonSpecies.convert_from_vanilla(value)
        return display_name_mapping.get(value, value.name if hasattr(value, 'name') else str(value))
