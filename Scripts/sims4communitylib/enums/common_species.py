"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import enum

from sims.sim_info import SimInfo


# noinspection PyUnresolvedReferences
class CommonSpecies(enum.Int):
    """ Custom Species enum containing all species (including extended species). """
    INVALID = 0
    HUMAN = 1
    SMALL_DOG = 2
    LARGE_DOG = 3
    CAT = 4

    @staticmethod
    def get_species(sim_info: SimInfo) -> int:
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
