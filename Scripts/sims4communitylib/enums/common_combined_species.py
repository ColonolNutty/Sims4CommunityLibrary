"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
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
