"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonAppearanceModifierPriority(CommonInt):
    """Priorities for appearance modifiers. These priorities determine the order in which appearance modifiers are applied, which ones override which."""
    INVALID: 'CommonAppearanceModifierPriority' = 0
    MANNEQUIN: 'CommonAppearanceModifierPriority' = 1
    SICKNESS: 'CommonAppearanceModifierPriority' = 2
    PATIENT: 'CommonAppearanceModifierPriority' = 3
    TRANSFORMED: 'CommonAppearanceModifierPriority' = 4
    FROZEN: 'CommonAppearanceModifierPriority' = 5
