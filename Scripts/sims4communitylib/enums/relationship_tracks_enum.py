"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonRelationshipTrackId(CommonInt):
    """Identifiers for vanilla sim relationship tracks.

    """
    INVALID: 'CommonRelationshipTrackId' = 0
    AUTHORITY: 'CommonRelationshipTrackId' = 161998
    FEUD: 'CommonRelationshipTrackId' = 193901
    FRIENDSHIP: 'CommonRelationshipTrackId' = 16650
    MISCHIEF: 'CommonRelationshipTrackId' = 26920
    RIVALRY: 'CommonRelationshipTrackId' = 161999
    ROMANCE: 'CommonRelationshipTrackId' = 16651
    ROMANCE_SATISFACTION: 'CommonRelationshipTrackId' = 362100
    SIM_TO_PET_FRIENDSHIP: 'CommonRelationshipTrackId' = 159228
    SMART_HUB_FRIENDSHIP: 'CommonRelationshipTrackId' = 203686
