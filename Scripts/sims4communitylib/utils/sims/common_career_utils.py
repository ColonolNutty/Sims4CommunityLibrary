"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Callable, Tuple, List

from careers.career_location import CareerLocation
from careers.career_tuning import Career, TunableCareerTrack, CareerLevel


class CommonCareerUtils:
    """ Utilities for manipulating Careers. """
    @classmethod
    def get_career_levels(cls, career: Career, include_branches: bool=False) -> Tuple[CareerLevel]:
        """get_career_levels(career, include_branches=False)

        Retrieve Career Levels available for a Career.

        :param career: A career.
        :type career: Career
        :param include_branches: If True, all career levels from Career Tracks the starting track branches into will be included in the result. If False, only the career levels available for the starting Track will be included in the result. Default is False.
        :rtype: include_branches: bool, optional
        :return: A collection of Career Levels available for the specified Career.
        :rtype: Tuple[CareerLevel]
        """
        if career is None:
            return tuple()

        from sims4communitylib.utils.sims.common_career_track_utils import CommonCareerTrackUtils
        return CommonCareerTrackUtils.get_career_levels(career.start_track, include_branches=include_branches)

    @classmethod
    def get_starting_career_track(cls, career: Career) -> Union[TunableCareerTrack, None]:
        """get_starting_career_track(career)

        Retrieve the starting Career Track of a Career.

        :param career: A career.
        :type career: Career
        :return: The starting Career Track of the Career or None if not found.
        :rtype: Union[TunableCareerTrack, None]
        """
        if career is None:
            return None
        return career.start_track

    @classmethod
    def get_all_career_tracks(cls, career: Career) -> Tuple[TunableCareerTrack]:
        """get_all_career_tracks(career)

        Retrieve all Career Tracks available for a Career, including all branching Career Tracks.

        :param career: A career.
        :type career: Career
        :return: A collection of Career Levels available for the specified Career.
        :rtype: Tuple[CareerLevel]
        """
        if career is None:
            return tuple()

        career_tracks: List[TunableCareerTrack] = list()
        career_tracks.append(career.start_track)
        from sims4communitylib.utils.sims.common_career_track_utils import CommonCareerTrackUtils
        branch_career_tracks = CommonCareerTrackUtils.get_branches(career.start_track, include_sub_branches=True)
        if branch_career_tracks:
            career_tracks.extend(branch_career_tracks)
        return tuple(career_tracks)

    @classmethod
    def get_career_id(cls, career: Career) -> int:
        """get_career_id(career)

        Retrieve the instance identifier of a Career.

        :param career: An instance of a Career.
        :type career: Career
        :return: The instance identifier of the specified Career or -1 if a problem occurs.
        :rtype: int
        """
        if career is None:
            return -1
        if not hasattr(career, 'id') or not isinstance(career, Career):
            return -1
        return career.id or getattr(career, 'id', -1)

    @classmethod
    def get_career_guid(cls, career: Career) -> Union[int, None]:
        """get_career_guid(career)

        Retrieve the Guid64 identifier of a career.

        :param career: An instance of a Career.
        :type career: Career
        :return: The Guid64 identifier of the specified Career.
        :rtype: Union[int, None]
        """
        if career is None:
            return None
        return getattr(career, 'guid64', None)

    @classmethod
    def get_career_location(cls, career: Career) -> Union[CareerLocation, None]:
        """get_career_location(career)

        Retrieve the workplace location of a career.

        :param career: An instance of a Career.
        :type career: Career
        :return: The location the Career is set to occur at.
        :rtype: Union[CareerLocation, None]
        """
        if career is None:
            return None
        return career.get_career_location()

    @classmethod
    def get_career_location_zone_id(cls, career: Career) -> int:
        """get_career_location_zone_id(career)

        Retrieve the zone id of a Career where it is set to occur at.

        :param career: An instance of a Career.
        :type career: Career
        :return: The instance identifier of the zone the career is set to occur at.
        :rtype: int
        """
        if career is None:
            return 0
        career_location = cls.get_career_location(career)
        if career_location is None:
            return 0
        return career_location.get_zone_id()

    @staticmethod
    def load_career_by_guid(career_identifier: Union[int, Career]) -> Union[Career, None]:
        """load_career_by_guid(career_identifier)

        Load an instance of a Career by its identifier.

        :param career_identifier: The identifier of a Career.
        :type career_identifier: Union[int, Career]
        :return: An instance of a Career matching the decimal identifier or None if not found.
        :rtype: Union[Career, None]
        """
        if career_identifier is None:
            return None
        if isinstance(career_identifier, Career):
            return career_identifier
        # noinspection PyBroadException
        try:
            career_identifier: int = int(career_identifier)
        except:
            career_identifier: Career = career_identifier
            return career_identifier

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.CAREER, career_identifier)

    @staticmethod
    def get_all_careers_generator(include_career_callback: Callable[[Career], bool]=None) -> Iterator[Career]:
        """get_all_careers_generator(include_career_callback=None)

        Retrieve all Careers.

        :param include_career_callback: If the result of this callback is True, the Career will be included in the results. If set to None, All Careers will be included. Default is None.
        :type include_career_callback: Callable[[Career], bool], optional
        :return: An iterable of Careers matching `include_career_callback`
        :rtype: Iterator[Career]
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        for (career_guid, career) in CommonResourceUtils.load_all_instances(Types.CAREER):
            if include_career_callback is not None and include_career_callback(career) is False:
                continue
            yield career

    @staticmethod
    def determine_entry_level_into_career_from_user_level(career: Career, desired_user_level: int) -> Tuple[Union[int, None], Union[int, None], Union[TunableCareerTrack, None]]:
        """get_career_entry_level_from_user_level(career, desired_user_level)

        Pick a career level and career track from a user level.

        :param career: The career to retrieve a career track from.
        :type career: Career
        :param desired_user_level: The user level desired to be given to a Sim.
        :type desired_user_level: int
        :return: The career level for the career track (or branch career track) used, the level of the user in that career track, and the career track itself.
        :rtype: Tuple[int, int, TunableCareerTrack]
        """
        if career is None:
            return None, None, None
        track = CommonCareerUtils.get_starting_career_track(career)
        from sims4communitylib.utils.sims.common_career_track_utils import CommonCareerTrackUtils
        return CommonCareerTrackUtils.determine_entry_level_into_career_track_by_user_level(track, desired_user_level)
