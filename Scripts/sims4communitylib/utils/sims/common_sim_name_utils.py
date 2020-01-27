"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims.sim_info import SimInfo


class CommonSimNameUtils:
    """Utilities for manipulating the name of Sims.

    """
    @staticmethod
    def get_first_name(sim_info: SimInfo) -> str:
        """get_first_name(sim_info)

        Retrieve the First Name of a Sim.

        :param sim_info: The Sim to retrieve the first name of.
        :type sim_info: SimInfo
        :return: The first name of the specified Sim.
        :rtype: str
        """
        if sim_info is None or not hasattr(sim_info, 'first_name'):
            return ''
        return getattr(sim_info, 'first_name')

    @staticmethod
    def get_last_name(sim_info: SimInfo) -> str:
        """get_last_name(sim_info)

        Retrieve the Last Name of a Sim.

        :param sim_info: The Sim to retrieve the last name of.
        :type sim_info: SimInfo
        :return: The last name of the specified Sim.
        :rtype: str
        """
        if sim_info is None or not hasattr(sim_info, 'last_name'):
            return ''
        return getattr(sim_info, 'last_name')

    @staticmethod
    def get_full_name(sim_info: SimInfo) -> str:
        """get_full_name(sim_info)

        Retrieve the full name of a Sim.

        .. note:: Resulting Full Name: '{First} {Last}'

        :param sim_info: The Sim to retrieve the full name of.
        :type sim_info: SimInfo
        :return: The full name of the specified Sim.
        :rtype: str
        """
        return '{} {}'.format(CommonSimNameUtils.get_first_name(sim_info), CommonSimNameUtils.get_last_name(sim_info))

    @staticmethod
    def get_full_names(sim_info_list: Tuple[SimInfo]) -> Tuple[str]:
        """get_full_names(sim_info_list)

        Retrieve a collection of full names for the specified Sims.

        .. note:: Resulting Full Names: ('{First} {Last}', '{First} {Last}', '{First} {Last}', ...)

        :param sim_info_list: A collection of Sims
        :type sim_info_list: Tuple[SimInfo]
        :return: A collection of full names of the specified Sims.
        :rtype: Tuple[str]
        """
        result: Tuple[str] = tuple([CommonSimNameUtils.get_full_name(sim_info) for sim_info in sim_info_list])
        return result
