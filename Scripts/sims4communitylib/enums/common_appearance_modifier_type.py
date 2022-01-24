"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonAppearanceModifierType(CommonInt):
    """Types for appearance modifiers."""
    SET_CAS_PART: 'CommonAppearanceModifierType' = 0
    RANDOMIZE_BODY_TYPE_COLOR: 'CommonAppearanceModifierType' = 1
    RANDOMIZE_SKIN_TONE_FROM_TAGS: 'CommonAppearanceModifierType' = 2
    GENERATE_OUTFIT: 'CommonAppearanceModifierType' = 3
    RANDOMIZE_CAS_PART: 'CommonAppearanceModifierType' = 4
    CUSTOM: 'CommonAppearanceModifierType' = 5000
