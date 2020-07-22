"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from typing import Tuple, Set, Union, Iterator

from sims4communitylib.enums.tags_enum import CommonGameTag


class CommonObjectTagUtils:
    """Utilities for manipulating the tags of objects.

    """

    @staticmethod
    def has_game_tags(game_object: GameObject, tags: Iterator[Union[int, CommonGameTag]]) -> bool:
        """has_game_tags(game_object, tags)

        Determine if an Object has any of the specified tags.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param tags: A collection of tags to locate.
        :type tags: Iterator[Union[int, CommonGameTag]]
        :return: True, if the Object has any of the specified tags. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        return game_object.has_any_tag(tuple(tags))

    @staticmethod
    def get_game_tags(game_object: GameObject) -> Set[int]:
        """get_game_tags(game_object)

        Retrieve the tags of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: A collection of tags the Object has.
        :rtype: Set[int]
        """
        if game_object is None:
            return set()
        return game_object.get_tags()

    @staticmethod
    def add_game_tags(game_object: GameObject, tags: Tuple[int], persist: bool=False) -> bool:
        """add_game_tags(game_object, tags, persist=False)

        Add tags to an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param tags: A collection of Game Tags to add.
        :type tags: Tuple[int]
        :param persist: If True, the Tags will persist to all instances of the Object. If False, the Tags will persist only to the specified Object. Default is False.
        :type persist: bool, optional
        :return: True, if the Tags were successfully added. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        game_object.append_tags(set(tags), persist=persist)
        return True
