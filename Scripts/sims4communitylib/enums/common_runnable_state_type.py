"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonRunnableStateType(CommonInt):
    """ States that a runnable can be in. """
    STOPPED = ...
    STOPPING = ...
    RUNNING = ...
    STARTING = ...
    WAITING_TO_START = ...
