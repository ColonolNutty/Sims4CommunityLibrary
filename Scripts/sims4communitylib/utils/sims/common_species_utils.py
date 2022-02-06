"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Species
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'common_species_utils')


class CommonSpeciesUtils:
    """Utilities for manipulating and checking the Species of Sims.

    """
    @staticmethod
    def get_species(sim_info: SimInfo) -> Union[Species, None]:
        """get_species(sim_info)

        Retrieve the Species of a sim.

        :param sim_info: The Sim to get the Species of.
        :type sim_info: SimInfo
        :return: The Species of the Sim or None if the Sim does not have a Species.
        :rtype: Union[Species, None]
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, 'species'):
            return sim_info.species
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'species'):
            return sim_info.sim_info.species
        return None

    @staticmethod
    def set_species(sim_info: SimInfo, species: Union[Species, int]) -> bool:
        """set_species(sim_info, species)

        Set the Species of a sim.

        :param sim_info: The Sim to set the Species of.
        :type sim_info: SimInfo
        :param species: The Species to set the Sim to.
        :type species: Union[Species, int]
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        sim_info.species = species
        return True

    @staticmethod
    def are_same_species(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_species(sim_info, other_sim_info)

        Determine if two sims are of the same species.

        .. note:: Extended Species are also compared (Large Dog, Small Dog, etc.)

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same species. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if other_sim_info is None:
            raise AssertionError('Argument other_sim_info was None')
        from sims4communitylib.enums.common_species import CommonSpecies
        species_one = CommonSpecies.get_species(sim_info)
        species_two = CommonSpecies.get_species(other_sim_info)
        log.format(species_one=species_one, species_two=species_two, sim_one=sim_info, other_sim_info=other_sim_info)
        return species_one == species_two

    @staticmethod
    def is_human_species(species: Union[Species, int]) -> bool:
        """is_human_species(species)

        Determine if a Species is a Human.

        :param species: The Species to check.
        :type species: Union[Species, int]
        :return: True, if the Species is Human. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'HUMAN'):
            return False
        return species == Species.HUMAN

    @staticmethod
    def is_pet_species(species: Union[Species, int]) -> bool:
        """is_pet_species(species)

        Determine if a Species is a Pet.

        :param species: The Species to check.
        :type species: Union[Species, int]
        :return: True, if the Species is a Pet Species (Large Dog, Small Dog, Cat). False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_dog_species(species) or CommonSpeciesUtils.is_cat_species(species)

    @staticmethod
    def is_animal_species(species: Union[Species, int]) -> bool:
        """is_animal_species(species)

        Determine if a Species is an Animal.

        :param species: The Species to check.
        :type species: Union[Species, int]
        :return: True, if the Species is a Animal Species (Large Dog, Small Dog, Cat, or Fox). False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_pet_species(species) or CommonSpeciesUtils.is_fox_species(species)

    @staticmethod
    def is_dog_species(species: Union[Species, int]) -> bool:
        """is_dog_species(species)

        Determine if a Species is a Dog.

        :param species: The Species to check.
        :type species: Union[Species, int]
        :return: True, if the Species is a Dog Species (Large Dog, Small Dog). False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'DOG'):
            return False
        return species == Species.DOG

    @staticmethod
    def is_cat_species(species: Union[Species, int]) -> bool:
        """is_cat_species(species)

        Determine if a Species is a Cat.

        :param species: The Species to check.
        :type species: Union[Species, int]
        :return: True, if the Species is a Cat Species. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'CAT'):
            return False
        return species == Species.CAT

    @staticmethod
    def is_fox_species(species: Union[Species, int]) -> bool:
        """is_fox_species(species)

        Determine if a Species is a Fox.

        :param species: The Species to check.
        :type species: Union[Species, int]
        :return: True, if the Species is a Fox Species. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'FOX'):
            return False
        return species == Species.FOX

    @staticmethod
    def is_dog(sim_info: SimInfo) -> bool:
        """is_dog(sim_info)

        Determine if a sim is a Dog.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Dog (Large Dog, Small Dog). False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_dog_species(CommonSpeciesUtils.get_species(sim_info))

    @staticmethod
    def is_human(sim_info: SimInfo) -> bool:
        """is_human(sim_info)

        Determine if a sim is a Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Human. False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_human_species(CommonSpeciesUtils.get_species(sim_info))

    @staticmethod
    def is_pet(sim_info: SimInfo) -> bool:
        """is_pet(sim_info)

        Determine if a sim is a Pet.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Pet (Large Dog, Small Dog, Cat). False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_pet_species(CommonSpeciesUtils.get_species(sim_info))

    @staticmethod
    def is_animal(sim_info: SimInfo) -> bool:
        """is_animal(sim_info)

        Determine if a sim is an Animal.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Animal (Large Dog, Small Dog, Cat, Fox). False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_animal_species(CommonSpeciesUtils.get_species(sim_info))

    @staticmethod
    def is_large_dog(sim_info: SimInfo) -> bool:
        """is_large_dog(sim_info)

        Determine if a sim is a Large Dog.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Large Dog. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return CommonSpeciesUtils.is_dog_species(CommonSpeciesUtils.get_species(sim_info)) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_EXTENDED_LARGE_DOGS)

    @staticmethod
    def is_small_dog(sim_info: SimInfo) -> bool:
        """is_small_dog(sim_info)

        Determine if a sim is a Small Dog.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Small Dog. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return CommonSpeciesUtils.is_dog_species(CommonSpeciesUtils.get_species(sim_info)) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_EXTENDED_SMALL_DOGS)

    @staticmethod
    def is_cat(sim_info: SimInfo) -> bool:
        """is_cat(sim_info)

        Determine if a sim is a Cat.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Cat. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return CommonSpeciesUtils.is_cat_species(CommonSpeciesUtils.get_species(sim_info)) or CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_CAT)

    @staticmethod
    def is_fox(sim_info: SimInfo) -> bool:
        """is_fox(sim_info)

        Determine if a sim is a Fox.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Fox. False, if not.
        :rtype: bool
        """
        return CommonSpeciesUtils.is_fox_species(CommonSpeciesUtils.get_species(sim_info)) or CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_FOX)
