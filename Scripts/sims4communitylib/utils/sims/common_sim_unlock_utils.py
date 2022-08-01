"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from sims.sim_info import SimInfo
from sims.unlock_tracker import UnlockTracker


class CommonSimUnlockUtils:
    """Utilities for unlocks. """
    @classmethod
    def get_unlock_tracker(cls, sim_info: SimInfo) -> Union[UnlockTracker, None]:
        """get_unlock_tracker(sim_info)

        Retrieve tracker for unlocks for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The tracker for unlocks for the Sim or None if not found.
        :rtype: Union[UnlockTracker, None]
        """
        if sim_info is None:
            return None
        return sim_info.unlock_tracker
