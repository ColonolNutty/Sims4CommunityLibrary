"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Callable

import services
from clubs.club import Club
from clubs.club_tuning import ClubRule
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonClubUtils:
    """ Utilities for manipulating Clubs. """

    @staticmethod
    def get_clubs_currently_gathering_gen(include_club_callback: Callable[[Club], bool] = CommonFunctionUtils.noop_true) -> Iterator[Club]:
        """get_clubs_currently_gathering_gen(include_club_callback=CommonFunctionUtils.noop_true)

        Retrieve all Clubs that are currently hosting a gathering.

        :param include_club_callback: If the result of this callback is True, the Club will be included in the results. The default callback will allow all.
        :type include_club_callback: Callable[[Club], bool], optional
        :return: An iterator of all Clubs that are currently gathering and that pass the include callback filter.
        :rtype: Iterator[Club]
        """
        from clubs.club_service import ClubService
        club_service: ClubService = services.get_club_service()
        if club_service is None:
            return tuple()
        for club in club_service.clubs_to_gatherings_map.keys():
            if club is None or not include_club_callback(club):
                continue
            yield club

    @staticmethod
    def get_club_members_gen(club: Club, include_club_member_callback: Callable[[SimInfo], bool] = CommonFunctionUtils.noop_true) -> Iterator[SimInfo]:
        """get_club_members_gen(club, include_club_member_callback=CommonFunctionUtils.noop_true)

        Retrieve the SimInfo of all members who are a part of a Club.

        :param club: An instance of a Club.
        :type club: Club
        :param include_club_member_callback: If the result of this callback is True, the Club Member will be included in the results. The default callback will allow all.
        :type include_club_member_callback: Callable[[SimInfo], bool], optional
        :return: An iterator of all Sims in a Club that pass the include callback filter.
        :rtype: Iterator[SimInfo]
        """
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        for member_sim in club.members:
            sim_info = CommonSimUtils.get_sim_info(member_sim)
            if not include_club_member_callback(sim_info):
                continue
            yield sim_info

    @staticmethod
    def get_club_rules_gen(club: Club, include_club_rule_callback: Callable[[SimInfo], bool] = CommonFunctionUtils.noop_true) -> Iterator[ClubRule]:
        """get_club_rules_gen(club, include_club_rule_callback=CommonFunctionUtils.noop_true)

        Retrieve all Club Rules of a Club.

        :param club: An instance of a Club.
        :type club: Club
        :param include_club_rule_callback: If the result of this callback is True, the Club Rule will be included in the results. The default callback will allow all.
        :type include_club_rule_callback: Callable[[ClubRule], bool], optional
        :return: An iterator of all Club Rules for the specified Club that pass the include callback filter.
        :rtype: Iterator[ClubRule]
        """
        if club is None:
            return tuple()
        for club_rule in club.rules:
            if club_rule is None or not include_club_rule_callback(club_rule):
                continue
            yield club_rule
