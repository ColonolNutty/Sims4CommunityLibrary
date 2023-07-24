"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonCombinedSpecies(CommonInt):
    """Various combined species types to reduce code ugliness"""
    NONE: 'CommonCombinedSpecies' = ...
    HUMAN: 'CommonCombinedSpecies' = ...  # Human
    ANIMAL: 'CommonCombinedSpecies' = ...  # Large Dog, Small Dog, Cat, Fox
    PET: 'CommonCombinedSpecies' = ...  # Large Dog, Small Dog, Cat
    NON_PET: 'CommonCombinedSpecies' = ...  # Fox
    DOG: 'CommonCombinedSpecies' = ...  # Large Dog, Small Dog
    CAT: 'CommonCombinedSpecies' = ...  # Cat
    FOX: 'CommonCombinedSpecies' = ...  # Fox
    HORSE: 'CommonCombinedSpecies' = ...  # Horse

    @classmethod
    def convert_to_signature(cls, combined_species: 'CommonCombinedSpecies') -> str:
        """convert_to_signature(combined_species)

        Convert a CommonCombinedSpecies to a unique signature.

        :param combined_species: The value to convert.
        :type combined_species: CommonCombinedSpecies
        :return: A string signature that uniquely represents the CommonCombinedSpecies or the name of the CommonCombinedSpecies, if no unique signature is found.
        :rtype: str
        """
        mapping = {
            CommonCombinedSpecies.HUMAN: 'Human',
            CommonCombinedSpecies.ANIMAL: 'Animal',
            CommonCombinedSpecies.PET: 'Pet',
            CommonCombinedSpecies.NON_PET: 'Non_Pet',
            CommonCombinedSpecies.DOG: 'Dog',
            CommonCombinedSpecies.CAT: 'Cat',
            CommonCombinedSpecies.FOX: 'Fox',
            CommonCombinedSpecies.HORSE: 'Horse',
        }
        return mapping.get(combined_species, combined_species.name)

    @classmethod
    def convert_to_enum_xml(cls, combined_species: 'CommonCombinedSpecies') -> Tuple[str]:
        """convert_to_species_xml(combined_species)

        Convert a CommonCombinedSpecies to the xml representations of species. i.e. (<E>(species)</E>,)

        :param combined_species: The value to convert.
        :type combined_species: CommonCombinedSpecies
        :return: A collection of strings that represent the xml associated with the value.
        :rtype: Tuple[str]
        """
        if combined_species == CommonCombinedSpecies.ANIMAL:
            result: Tuple[str, ...] = (*cls.convert_to_enum_xml(CommonCombinedSpecies.DOG), *cls.convert_to_enum_xml(CommonCombinedSpecies.CAT), *cls.convert_to_enum_xml(CommonCombinedSpecies.FOX), *cls.convert_to_enum_xml(CommonCombinedSpecies.HORSE))
            return result
        if combined_species == CommonCombinedSpecies.PET:
            result: Tuple[str, ...] = (*cls.convert_to_enum_xml(CommonCombinedSpecies.DOG), *cls.convert_to_enum_xml(CommonCombinedSpecies.CAT), *cls.convert_to_enum_xml(CommonCombinedSpecies.HORSE))
            return result
        if combined_species == CommonCombinedSpecies.NON_PET:
            result: Tuple[str, ...] = (*cls.convert_to_enum_xml(CommonCombinedSpecies.HUMAN),)
            return result

        mapping = {
            CommonCombinedSpecies.HUMAN: ('<E>HUMAN</E>',),
            CommonCombinedSpecies.DOG: ('<E>DOG</E>',),
            CommonCombinedSpecies.CAT: ('<E>CAT</E>',),
            CommonCombinedSpecies.FOX: ('<E>FOX</E>',),
            CommonCombinedSpecies.HORSE: ('<E>HORSE</E>',),
        }
        return mapping.get(combined_species, tuple())

    @classmethod
    def is_animal(cls, combined_species: 'CommonCombinedSpecies') -> bool:
        """is_animal(combined_species)

        Determine if a value represents an animal.

        :param combined_species: The value to check.
        :type combined_species: CommonCombinedSpecies
        :return: True, if the value represents an Animal. False, if not.
        :rtype: bool
        """
        return combined_species in (
            CommonCombinedSpecies.ANIMAL,
            CommonCombinedSpecies.PET,
            CommonCombinedSpecies.DOG,
            CommonCombinedSpecies.CAT,
            CommonCombinedSpecies.FOX,
            CommonCombinedSpecies.HORSE
        )
