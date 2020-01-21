"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, List

from sims.sim_info import SimInfo
from whims.whim_set import WhimSetBaseMixin


class CommonWhimUtils:
    """Utilities for manipulating the Whims of Sims.

    """
    @staticmethod
    def get_current_whims(sim_info: SimInfo) -> Tuple[WhimSetBaseMixin]:
        """Retrieve the current Whims of the specified Sim.

        """
        whims_tracker = sim_info.whim_tracker
        if whims_tracker is None:
            return tuple()
        goal_instances: List[WhimSetBaseMixin] = []
        for whim_data in whims_tracker.get_active_whim_data():
            if whim_data.whim is not None:
                goal_instances.append(whim_data.whim)
        return tuple(goal_instances)
