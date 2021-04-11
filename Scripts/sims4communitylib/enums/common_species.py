"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict

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

    @staticmethod
    def get_species(sim_info: SimInfo) -> 'CommonSpecies':
        """Retrieve the CommonSpecies of a sim. Use this instead of CommonSpeciesUtils.get_species to determine a more specific species.

        """
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        if CommonSpeciesUtils.is_human(sim_info):
            return CommonSpecies.HUMAN
        elif CommonSpeciesUtils.is_small_dog(sim_info):
            return CommonSpecies.SMALL_DOG
        elif CommonSpeciesUtils.is_large_dog(sim_info):
            return CommonSpecies.LARGE_DOG
        elif CommonSpeciesUtils.is_cat(sim_info):
            return CommonSpecies.CAT
        return CommonSpecies.INVALID

    @staticmethod
    def convert_to_vanilla(species: 'CommonSpecies') -> Union[Species, None]:
        """convert_to_vanilla(species)

        Convert a CommonSpecies into the vanilla Species enum.

        :param species: An instance of a CommonSpecies
        :type species: CommonSpecies
        :return: The specified CommonSpecies translated to a Species or SpeciesExtended or None if the CommonSpecies could not be translated.
        :rtype: Union[Species, None]
        """
        if species is None or species == CommonSpecies.INVALID:
            return None
        if isinstance(species, Species):
            return species
        conversion_mapping: Dict[CommonSpecies, Species] = {
            CommonSpecies.HUMAN: Species.HUMAN,
            CommonSpecies.SMALL_DOG: SpeciesExtended.SMALLDOG,
            CommonSpecies.LARGE_DOG: Species.DOG,
            CommonSpecies.CAT: Species.CAT
        }
        return conversion_mapping.get(species, None)
