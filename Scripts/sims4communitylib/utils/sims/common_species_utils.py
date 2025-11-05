"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Species, SpeciesExtended
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'common_species_utils')


class CommonSpeciesUtils:
    """Utilities for manipulating and checking the Species of Sims.

    """
    @classmethod
    def get_species(cls, sim_info: SimInfo) -> Union[Species, SpeciesExtended, None]:
        """get_species(sim_info)

        Retrieve the Species of a sim.

        :param sim_info: The Sim to get the Species of.
        :type sim_info: SimInfo
        :return: The Species of the Sim or None if the Sim does not have a Species.
        :rtype: Union[Species, SpeciesExtended, None]
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, 'species'):
            return sim_info.species
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'species'):
            return sim_info.sim_info.species
        return None

    @classmethod
    def set_species(cls, sim_info: SimInfo, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """set_species(sim_info, species)

        Set the Species of a sim.

        :param sim_info: The Sim to set the Species of.
        :type sim_info: SimInfo
        :param species: The Species to set the Sim to.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        sim_info.species = species
        return True

    @classmethod
    def are_same_species(cls, sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
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

    @classmethod
    def is_human_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_human_species(species)

        Determine if a Species is a Human.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is Human. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'HUMAN'):
            return False
        species = CommonSpecies.convert_to_vanilla(species)
        return species in (Species.HUMAN, SpeciesExtended.HUMAN)

    @classmethod
    def is_pet_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_pet_species(species)

        Determine if a Species is a Pet.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Pet Species (Large Dog, Small Dog, Cat). False, if not.
        :rtype: bool
        """
        return cls.is_dog_species(species) or cls.is_cat_species(species) or cls.is_horse_species(species)

    @classmethod
    def is_animal_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_animal_species(species)

        Determine if a Species is an Animal.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is an Animal Species (Large Dog, Small Dog, Cat, or Fox). False, if not.
        :rtype: bool
        """
        return cls.is_pet_species(species) or cls.is_fox_species(species)

    @classmethod
    def is_dog_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_dog_species(species)

        Determine if a Species is a Dog.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Dog Species (Large Dog, Small Dog). False, if not.
        :rtype: bool
        """
        return cls.is_large_dog_species(species) or cls.is_small_dog_species(species)

    @classmethod
    def is_large_dog_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_large_dog_species(species)

        Determine if a Species is a Large Dog.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Large Dog Species. False, if not.
        :rtype: bool
        """
        if hasattr(Species, 'DOG'):
            species = CommonSpecies.convert_to_vanilla(species)
            if species in (Species.DOG, SpeciesExtended.DOG):
                return True
        return False

    @classmethod
    def is_small_dog_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_small_dog_species(species)

        Determine if a Species is a Small Dog.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Small Dog Species. False, if not.
        :rtype: bool
        """
        if hasattr(SpeciesExtended, 'SMALLDOG'):
            species = CommonSpecies.convert_to_vanilla(species)
            if species == SpeciesExtended.SMALLDOG:
                return True
        return False

    @classmethod
    def is_cat_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_cat_species(species)

        Determine if a Species is a Cat.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Cat Species. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'CAT'):
            return False
        species = CommonSpecies.convert_to_vanilla(species)
        return species in (Species.CAT, SpeciesExtended.CAT)

    @classmethod
    def is_fox_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_fox_species(species)

        Determine if a Species is a Fox.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Fox Species. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'FOX'):
            return False
        species = CommonSpecies.convert_to_vanilla(species)
        return species in (Species.FOX, SpeciesExtended.FOX)

    @classmethod
    def is_horse_species(cls, species: Union[CommonSpecies, Species, SpeciesExtended, int]) -> bool:
        """is_horse_species(species)

        Determine if a Species is a Horse.

        :param species: The Species to check.
        :type species: Union[CommonSpecies, Species, SpeciesExtended, int]
        :return: True, if the Species is a Horse Species. False, if not.
        :rtype: bool
        """
        if not hasattr(Species, 'HORSE'):
            return False
        species = CommonSpecies.convert_to_vanilla(species)
        return species in (Species.HORSE, SpeciesExtended.HORSE)

    @classmethod
    def is_dog(cls, sim_info: SimInfo) -> bool:
        """is_dog(sim_info)

        Determine if a Sim is a Dog.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Dog (Large Dog, Small Dog). False, if not.
        :rtype: bool
        """
        return cls.is_dog_species(cls.get_species(sim_info))

    @classmethod
    def is_human(cls, sim_info: SimInfo) -> bool:
        """is_human(sim_info)

        Determine if a Sim is a Human.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Human. False, if not.
        :rtype: bool
        """
        return cls.is_human_species(cls.get_species(sim_info))

    @classmethod
    def is_pet(cls, sim_info: SimInfo) -> bool:
        """is_pet(sim_info)

        Determine if a Sim is a Pet.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Pet (Large Dog, Small Dog, Cat). False, if not.
        :rtype: bool
        """
        return cls.is_pet_species(cls.get_species(sim_info))

    @classmethod
    def is_animal(cls, sim_info: SimInfo) -> bool:
        """is_animal(sim_info)

        Determine if a Sim is an Animal.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Animal (Large Dog, Small Dog, Cat, Fox). False, if not.
        :rtype: bool
        """
        return cls.is_animal_species(cls.get_species(sim_info))

    @classmethod
    def is_large_dog(cls, sim_info: SimInfo) -> bool:
        """is_large_dog(sim_info)

        Determine if a Sim is a Large Dog.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Large Dog. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return cls.is_dog_species(cls.get_species(sim_info)) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_EXTENDED_LARGE_DOGS)

    @classmethod
    def is_small_dog(cls, sim_info: SimInfo) -> bool:
        """is_small_dog(sim_info)

        Determine if a Sim is a Small Dog.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Small Dog. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return cls.is_dog_species(cls.get_species(sim_info)) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_EXTENDED_SMALL_DOGS)

    @classmethod
    def is_cat(cls, sim_info: SimInfo) -> bool:
        """is_cat(sim_info)

        Determine if a Sim is a Cat.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Cat. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return cls.is_cat_species(cls.get_species(sim_info)) or CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_CAT)

    @classmethod
    def is_fox(cls, sim_info: SimInfo) -> bool:
        """is_fox(sim_info)

        Determine if a Sim is a Fox.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Fox. False, if not.
        :rtype: bool
        """
        return cls.is_fox_species(cls.get_species(sim_info)) or CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_FOX)

    @classmethod
    def is_horse(cls, sim_info: SimInfo) -> bool:
        """is_horse(sim_info)

        Determine if a Sim is a Horse.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Horse. False, if not.
        :rtype: bool
        """
        return cls.is_horse_species(cls.get_species(sim_info)) or CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_HORSE)
