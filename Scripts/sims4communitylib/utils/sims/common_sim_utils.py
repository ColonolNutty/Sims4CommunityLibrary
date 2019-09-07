"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from sims.sim import Sim
from sims.sim_info import SimInfo


class CommonSimUtils:
    """ Utilities for retrieving sims in different ways. """
    @staticmethod
    def get_active_sim() -> Sim:
        """
            Retrieve a Sim object of the Currently Active Sim.
        :return: The Sim object of the currently active sim.
        """
        client = services.client_manager().get_first_client()
        return client.active_sim

    @staticmethod
    def get_active_sim_info() -> SimInfo:
        """
            Retrieve a SimInfo object of the Currently Active Sim.
        :return: The SimInfo object of the currently active sim.
        """
        return CommonSimUtils.get_active_sim().sim_info
