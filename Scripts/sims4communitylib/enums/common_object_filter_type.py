"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonObjectFilterType(CommonInt):
    """The type of an object filter."""
    OBJECT_DEFINITION_FILTER = 0
    OBJECT_TAG_FILTER = 1
    CUSTOM = 5000
