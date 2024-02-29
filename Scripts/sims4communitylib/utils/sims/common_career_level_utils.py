"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from careers.career_tuning import CareerLevel


class CommonCareerLevelUtils:
    """ Utilities for manipulating Career Levels. """

    @staticmethod
    def load_career_level_by_guid(career_level_identifier: Union[int, CareerLevel]) -> Union[CareerLevel, None]:
        """load_career_level_by_guid(career_level_identifier)

        Load an instance of a CareerLevel by its identifier.

        :param career_level_identifier: The identifier of a CareerLevel.
        :type career_level_identifier: Union[int, CareerLevel]
        :return: An instance of a CareerLevel matching the decimal identifier or None if not found.
        :rtype: Union[CareerLevel, None]
        """
        if career_level_identifier is None:
            return None
        if isinstance(career_level_identifier, CareerLevel):
            return career_level_identifier
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            career_level_instance = career_level_identifier()
            if isinstance(career_level_instance, CareerLevel):
                # noinspection PyTypeChecker
                return career_level_identifier
        except:
            pass
        # noinspection PyBroadException
        try:
            career_level_identifier: int = int(career_level_identifier)
        except:
            # noinspection PyTypeChecker
            career_level_identifier: CareerLevel = career_level_identifier
            return career_level_identifier

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.CAREER_LEVEL, career_level_identifier)
