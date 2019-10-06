"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_info_types import Species
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.MOD_NAME, 'common_species_utils')


class CommonSpeciesUtils:
    """ Utilities for handling sim species. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def get_species(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> Union[Species, None]:
        """
            Retrieve the Species of a sim.
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, 'species'):
            return sim_info.species
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'species'):
            return sim_info.sim_info.species
        return None
    
    @staticmethod
    def set_species(sim_info: Union[SimInfo, SimInfoBaseWrapper], species: Union[Species, int]) -> bool:
        """
            Set the Species of a sim.
        """
        try:
            sim_info.species = species
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.MOD_NAME, 'Failed to set species of sim {} to {}.'.format(pformat(sim_info), species), exception=ex)
            return False
    
    @staticmethod
    def are_same_species(sim_info: Union[SimInfo, SimInfoBaseWrapper], other_sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if two sims are of the same species.
    
            Note: Also checks Extended Species (Large Dog, Small Dog, etc.)
        """
        if sim_info is None or other_sim_info is None:
            log.debug('Either sim info or target is None')
            return False
    
        species_one = CommonSpeciesUtils.get_species(sim_info)
        species_two = CommonSpeciesUtils.get_species(other_sim_info)
        if species_one != species_two:
            log.format_with_message('Sims not the same species.', species_one=species_one, species_two=species_two)
            return False
    
        if CommonSpeciesUtils.is_human(sim_info):
            log.debug('Both are human.')
            return True
    
        if CommonSpeciesUtils.is_cat(sim_info):
            log.debug('Both are cats.')
            return True
    
        if CommonSpeciesUtils.is_large_dog(sim_info) and CommonSpeciesUtils.is_large_dog(other_sim_info):
            log.debug('Both are large dogs.')
            return True
    
        if CommonSpeciesUtils.is_small_dog(sim_info) and CommonSpeciesUtils.is_small_dog(other_sim_info):
            log.debug('Both are small dogs.')
            return True
    
        log.debug('Sims are not the same species.')
        return False
    
    @staticmethod
    def is_human_species(species: Union[Species, int]) -> bool:
        """
            Determine if a Species is a Human.
        """
        return species == Species.HUMAN
    
    @staticmethod
    def is_pet_species(species: Union[Species, int]) -> bool:
        """
            Determine if a Species is a Pet.
        """
        return CommonSpeciesUtils.is_dog_species(species) or CommonSpeciesUtils.is_cat_species(species)
    
    @staticmethod
    def is_dog_species(species: Union[Species, int]) -> bool:
        """
            Determine if a Species is a Dog.
        """
        return species == Species.DOG
    
    @staticmethod
    def is_cat_species(species: Union[Species, int]) -> bool:
        """
            Determine if a Species is a Cat.
        """
        return species == Species.CAT
    
    @staticmethod
    def is_dog(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Dog.
        """
        return CommonSpeciesUtils.get_species(sim_info) == Species.DOG
    
    @staticmethod
    def is_human(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Human.
        """
        return CommonSpeciesUtils.is_human_species(CommonSpeciesUtils.get_species(sim_info))
    
    @staticmethod
    def is_pet(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Pet.
        """
        return CommonSpeciesUtils.is_pet_species(CommonSpeciesUtils.get_species(sim_info))
    
    @staticmethod
    def is_large_dog(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Large Dog.
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return CommonSpeciesUtils.is_dog_species(CommonSpeciesUtils.get_species(sim_info)) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_EXTENDED_LARGE_DOGS)
    
    @staticmethod
    def is_small_dog(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Small Dog.
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return CommonSpeciesUtils.is_dog_species(CommonSpeciesUtils.get_species(sim_info)) and CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_EXTENDED_SMALL_DOGS)
    
    @staticmethod
    def is_cat(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Cat.
        """
        from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
        from sims4communitylib.enums.traits_enum import CommonTraitId
        return CommonSpeciesUtils.is_cat_species(CommonSpeciesUtils.get_species(sim_info)) or CommonTraitUtils.has_trait(sim_info, CommonTraitId.SPECIES_CAT)
