"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

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
        """get_current_whims(sim_info)

        Retrieve the current Whims of the specified Sim.

        :param sim_info: The Sim to get the Whim Sets of.
        :type sim_info: SimInfo
        :return: A collection of Whims Sets for the specified Sim.
        :rtype: Tuple[WhimSetBaseMixin]
        """
        whims_tracker = sim_info.whim_tracker
        if whims_tracker is None:
            return tuple()
        goal_instances: List[WhimSetBaseMixin] = []
        for whim_data in whims_tracker.get_active_whim_data():
            if whim_data.whim is not None:
                goal_instances.append(whim_data.whim)
        return tuple(goal_instances)
