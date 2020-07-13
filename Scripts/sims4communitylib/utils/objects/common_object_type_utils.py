"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject


class CommonObjectTypeUtils:
    """ Utilities for determining the type of an object. """
    @staticmethod
    def is_window(game_object: GameObject) -> bool:
        """is_window(game_object)

        Determine if an Object is a window.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Window. False, if not.
        :rtype: bool
        """
        from sims4communitylib.enums.tags_enum import CommonGameTag
        from sims4communitylib.utils.objects.common_object_tag_utils import CommonObjectTagUtils
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.BUILD_WINDOW, ))
