"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Union, Iterator, Callable, Tuple, List

from careers.career_tuning import TunableCareerTrack, CareerLevel


class CommonCareerTrackUtils:
    """ Utilities for manipulating Career Tracks. """
    @classmethod
    def get_branches(cls, career_track: TunableCareerTrack, include_sub_branches: bool=False) -> Tuple[TunableCareerTrack]:
        """get_branches(career_track, include_sub_branches=True)

        Retrieve a collection of all Career Tracks that branch off of a Career Track and if specified, the branches those branches branch off to.

        :param career_track: A Career Track.
        :type career_track: TunableCareerTrack
        :param include_sub_branches: If True, all branches will be checked for their own branches and those branches will be included recursively. If False, only the top level branches will be included. Default is False.
        :type include_sub_branches: bool, optional
        :return: A collection of all Career Tracks that branch off from the specified Career Track.
        :rtype: Tuple[TunableCareerTrack]
        """
        if career_track is None:
            return tuple()
        if include_sub_branches:
            # noinspection PyUnresolvedReferences
            if hasattr(career_track, 'branches') and career_track.branches is not None:
                career_track_branches: List[TunableCareerTrack] = list(career_track.branches)
                for sub_career_track in career_track_branches:
                    sub_branches = cls.get_branches(sub_career_track, include_sub_branches=include_sub_branches)
                    if not sub_branches:
                        continue
                    career_track_branches.extend(sub_branches)
                return tuple(career_track_branches)
        else:
            # noinspection PyUnresolvedReferences
            if hasattr(career_track, 'branches') and career_track.branches is not None:
                return tuple(career_track.branches)
        return tuple()

    @classmethod
    def get_career_levels(cls, career_track: TunableCareerTrack, include_branches: bool=False) -> Tuple[CareerLevel]:
        """get_career_levels(career_track, include_branches=False)

        Retrieve a collection of all career levels under a Career Track.

        :param career_track: A Career Track.
        :type career_track: TunableCareerTrack
        :param include_branches: If True, all career levels from Career Track branches will be included in the result. If False, only the career levels available for the specified Career Track will be included in the result. Default is False.
        :rtype: include_branches: bool, optional
        :return: A collection of all Career Levels under the Career Track.
        :rtype: Tuple[CareerLevel]
        """
        if career_track is None:
            return tuple()
        if include_branches:
            # noinspection PyUnresolvedReferences
            if hasattr(career_track, 'career_levels') and career_track.career_levels is not None:
                career_levels: List[CareerLevel] = list(career_track.career_levels)
                branches = cls.get_branches(career_track)
                for branch_career_track in branches:
                    sub_career_levels = cls.get_career_levels(branch_career_track, include_branches=include_branches)
                    if not sub_career_levels:
                        continue
                    career_levels.extend(sub_career_levels)
                return tuple(career_levels)
        else:
            # noinspection PyUnresolvedReferences
            if hasattr(career_track, 'career_levels') and career_track.career_levels is not None:
                return tuple(career_track.career_levels)
        return tuple()

    @classmethod
    def get_career_level_by_index(cls, career_track: TunableCareerTrack, index: int) -> Union[CareerLevel, None]:
        """get_career_level_by_index(career_track, index)

        Retrieve a Career Level within a Career Track by its index.

        :param career_track: A Career Track.
        :type career_track: TunableCareerTrack
        :param index: The index of the career level to retrieve. (Career Levels start at 1 instead of zero!)
        :type index: int
        :return: The career level found at the specified index or None if not found.
        :rtype: Union[CareerLevel, None]
        """
        career_levels = cls.get_career_levels(career_track)
        if index > len(career_levels):
            return None
        return career_levels[index]

    @classmethod
    def get_career_track_guid(cls, career_track: TunableCareerTrack) -> Union[int, None]:
        """get_career_track_guid(career_track)

        Retrieve the Guid64 identifier of a career_track.

        :param career_track: An instance of a Career Track.
        :type career_track: TunableCareerTrack
        :return: The Guid64 identifier of the specified Career Track.
        :rtype: Union[int, None]
        """
        if career_track is None:
            return None
        return getattr(career_track, 'guid64', None)

    @staticmethod
    def load_career_track_by_guid(career_track_identifier: Union[int, TunableCareerTrack]) -> Union[TunableCareerTrack, None]:
        """load_career_track_by_guid(career_track_identifier)

        Load an instance of a CareerTrack by its identifier.

        :param career_track_identifier: The identifier of a CareerTrack.
        :type career_track_identifier: Union[int, TunableCareerTrack]
        :return: An instance of a Career Track matching the decimal identifier or None if not found.
        :rtype: Union[TunableCareerTrack, None]
        """
        if career_track_identifier is None:
            return None
        if isinstance(career_track_identifier, TunableCareerTrack):
            return career_track_identifier
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            career_track_instance = career_track_identifier()
            if isinstance(career_track_instance, TunableCareerTrack):
                # noinspection PyTypeChecker
                return career_track_identifier
        except:
            pass
        # noinspection PyBroadException
        try:
            career_track_identifier: int = int(career_track_identifier)
        except:
            # noinspection PyTypeChecker
            career_track_identifier: TunableCareerTrack = career_track_identifier
            return career_track_identifier

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.CAREER_TRACK, career_track_identifier)

    @staticmethod
    def get_all_career_tracks_generator(include_career_track_callback: Callable[[TunableCareerTrack], bool]=None) -> Iterator[TunableCareerTrack]:
        """get_all_career_tracks_generator(include_career_callback=None)

        Retrieve all Career Tracks.

        :param include_career_track_callback: If the result of this callback is True, the Career will be included in the results. If set to None, All Careers will be included. Default is None.
        :type include_career_track_callback: Callable[[TunableCareerTrack], bool], optional
        :return: An iterator of Careers matching `include_career_track_callback`
        :rtype: Iterator[TunableCareerTrack]
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        for (_, career_track) in CommonResourceUtils.load_all_instances(Types.CAREER_TRACK):
            if include_career_track_callback is not None and not include_career_track_callback(career_track):
                continue
            yield career_track

    @classmethod
    def determine_entry_level_into_career_track_by_user_level(cls, career_track: TunableCareerTrack, desired_user_level: int) -> Tuple[Union[int, None], Union[int, None], Union[TunableCareerTrack, None]]:
        """determine_entry_level_into_career_track_by_user_level(career_track, desired_user_level)

        Pick a Career Track level and Career Track from a user level.

        :param career_track: The Career Track to locate a Career Level in.
        :type career_track: TunableCareerTrack
        :param desired_user_level: The desired user level within the Career Track.
        :type desired_user_level: int
        :return: The index of the Career Level for the Career Track (or branch Career Track) used, the level of the user in that Career Track, and the Career Track itself.
        :rtype: Tuple[int, int, TunableCareerTrack]
        """
        if career_track is None:
            return None, None, None
        track = career_track
        track_start_level = 1

        while True:
            track_length = len(cls.get_career_levels(track))
            level = desired_user_level - track_start_level
            if level < track_length:
                user_level = track_start_level + level
                return level, user_level, track

            branches = cls.get_branches(track)
            if not branches:
                # The exit path. When we run out of branches to check we'll just return the last info found.
                level = track_length - 1
                user_level = track_start_level + level
                return level, user_level, track

            track_start_level += track_length
            track = random.choice(branches)
