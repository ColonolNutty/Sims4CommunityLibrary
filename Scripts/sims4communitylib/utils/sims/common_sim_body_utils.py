"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimBodyUtils:
    """Utilities for manipulating the body of Sims.

    """

    @staticmethod
    def get_wading_size(sim_info: SimInfo) -> Tuple[int, int]:
        """get_wading_size(sim_info)

        Retrieve the size of a Sim if they were to wade in a pool of water.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A tuple indicating the x and y wading size of a Sim from their origin point.
        :rtype: Tuple[int, int]
        """
        # noinspection PyBroadException
        try:
            from world.ocean_tuning import OceanTuning
        except:
            return 0, 0
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return 0, 0
        wading_interval = OceanTuning.get_actor_wading_interval(sim)
        if wading_interval is None:
            return 0, 0
        return wading_interval.lower_bound, wading_interval.upper_bound
