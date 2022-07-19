"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonQueryMethodType(CommonInt):
    """ Various methods to query for items. """
    ALL_PLUS_ANY: 'CommonQueryMethodType' = ...
    ALL_INTERSECT_ANY: 'CommonQueryMethodType' = ...
    ALL_PLUS_ANY_MUST_HAVE_ONE: 'CommonQueryMethodType' = ...
    ALL_INTERSECT_ANY_MUST_HAVE_ONE: 'CommonQueryMethodType' = ...
