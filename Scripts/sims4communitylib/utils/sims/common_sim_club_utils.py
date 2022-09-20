"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Callable, Union

import services
from clubs.club import Club
from clubs.club_gathering_situation import ClubGatheringSituation
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
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

    @staticmethod
    def get_current_club_gathering(sim_info: SimInfo) -> Union[ClubGatheringSituation, None]:
        """get_current_club_gathering(sim_info)

        Retrieve the Club Gathering a Sim is currently taking part in.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The Club Gathering the specified Sim is a part of or None if the Sim is not a part of any Club Gathering.
        :rtype: Union[ClubGatheringSituation, None]
        """
        if sim_info is None:
            return None
        club_service = services.get_club_service()
        if club_service is None:
            return None
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return club_service.sims_to_gatherings_map.get(sim)

    @staticmethod
    def get_clubs_gen(sim_info: SimInfo, include_club_callback: Callable[[Club], bool] = CommonFunctionUtils.noop_true) -> Iterator[Club]:
        """get_clubs_gen(sim_info, include_club_callback=CommonFunctionUtils.noop_true)

        Retrieve all Clubs a Sim is a part of.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_club_callback: If the result of this callback is True, the Club will be included in the results. The default callback will allow all.
        :type include_club_callback: Callable[[Club], bool], optional
        :return: An iterator of all Clubs the specified Sim is a part of and that pass the include callback filter.
        :rtype: Iterator[Club]
        """
        if sim_info is None:
            return tuple()
        club_service = services.get_club_service()
        if club_service is None:
            return tuple()
        for club in club_service.get_clubs_for_sim_info(sim_info):
            if club is None or not include_club_callback(club):
                continue
            yield club

    @staticmethod
    def get_clubs_currently_gathering_gen(sim_info: SimInfo, include_club_callback: Callable[[Club], bool] = CommonFunctionUtils.noop_true) -> Iterator[Club]:
        """get_clubs_currently_gathering_gen(include_club_callback=CommonFunctionUtils.noop_true)

        Retrieve all Clubs the Sim is in that are currently hosting a gathering.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_club_callback: If the result of this callback is True, the Club will be included in the results. The default callback will allow all.
        :type include_club_callback: Callable[[Club], bool], optional
        :return: An iterator of all Clubs the Sim is in that are currently gathering and that pass the include_club_callback filter.
        :rtype: Iterator[Club]
        """
        if sim_info is None:
            return tuple()
        club_service = services.get_club_service()
        if club_service is None:
            return tuple()
        sim_clubs = club_service.get_clubs_for_sim_info(sim_info)
        for club in sim_clubs:
            club_gathering = club_service.clubs_to_gatherings_map.get(club)
            if club_gathering is None or not include_club_callback(club):
                continue
            yield club

    @staticmethod
    def are_part_of_same_club_gathering(sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """are_part_of_same_club_gathering(sim_info_a, sim_info_b)

        Determine if two Sims are at the same Club Gathering

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is taking part in the same Club Gathering as Sim B. False, if not.
        :rtype: bool
        """
        sim_a_club_gathering = CommonSimClubUtils.get_current_club_gathering(sim_info_a)
        sim_b_club_gathering = CommonSimClubUtils.get_current_club_gathering(sim_info_b)
        if sim_a_club_gathering is None or sim_b_club_gathering is None:
            return False
        return sim_a_club_gathering == sim_b_club_gathering
