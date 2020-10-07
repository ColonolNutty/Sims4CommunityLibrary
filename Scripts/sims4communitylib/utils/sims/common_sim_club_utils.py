"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimClubUtils:
    """ Utilities for manipulating the Clubs of Sims. """

    @staticmethod
    def is_engaged_in_club_gathering(sim_info: SimInfo) -> bool:
        """is_engaged_in_club_gathering(sim_info)

        Determine if a Sim is engaged in a Club Gathering.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is engaged in a Club Gathering. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        club_service = services.get_club_service()
        if club_service is None:
            return False
        return sim in club_service.sims_to_gatherings_map
