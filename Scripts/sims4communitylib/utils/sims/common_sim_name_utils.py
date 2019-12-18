"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo


class CommonSimNameUtils:
    """ Utilities for manipulating the name of Sims. """
    @staticmethod
    def get_first_name(sim_info: SimInfo) -> str:
        """
            Retrieve the First Name of a Sim.
        """
        if sim_info is None or not hasattr(sim_info, 'first_name'):
            return ''
        return getattr(sim_info, 'first_name')

    @staticmethod
    def get_last_name(sim_info: SimInfo) -> str:
        """
            Retrieve the Last Name of a Sim.
        """
        if sim_info is None or not hasattr(sim_info, 'last_name'):
            return ''
        return getattr(sim_info, 'last_name')

    @staticmethod
    def get_full_name(sim_info: SimInfo) -> str:
        """
            Retrieve the full name of a Sim.

            Format:
            '{First} {Last}'
        """
        return '{} {}'.format(CommonSimNameUtils.get_first_name(sim_info), CommonSimNameUtils.get_last_name(sim_info))

    @staticmethod
    def get_full_names(sim_info_list: Tuple[SimInfo]) -> Tuple[str]:
        """
            Retrieve a collection of full names for the specified Sims.

            Format:
            ('{First} {Last}', '{First} {Last}', '{First} {Last}', ...)
        """
        result: Tuple[str] = tuple([CommonSimNameUtils.get_full_name(sim_info) for sim_info in sim_info_list])
        return result
