"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.base_object import BaseObject
from typing import Callable, Iterator
import services
from objects.game_object import GameObject
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonObjectUtils:
    """Utilities for retrieving Objects in various ways.

    """

    @staticmethod
    def get_object_id(object_instance: BaseObject) -> int:
        """get_object_id(object_instance)

        Retrieve the decimal identifier of an Object.

        :param object_instance: An instance of an Object.
        :type object_instance: BaseObject
        :return: The decimal identifier of the BaseObject.
        :rtype: int
        """
        if object_instance is None:
            return -1
        return object_instance.id or getattr(object_instance, 'id', None)

    @staticmethod
    def get_game_object(game_object_id: int) -> GameObject:
        """get_game_object(game_object_id)

        Retrieve an instance of an Object in the game world.

        :param game_object_id: The decimal identifier of an Object.
        :type game_object_id: int
        :return: An instance of an Object or None if not found.
        :rtype: GameObject
        """
        return services.object_manager().get(game_object_id)

    @staticmethod
    def get_instance_for_all_game_objects_generator(
        include_object_callback: Callable[[GameObject], bool]=None
    ) -> Iterator[GameObject]:
        """get_instance_for_all_objects_generator(include_object_callback=None)

        Retrieve an instance for each and every Object in the game world.

        :param include_object_callback: If the result of this callback is True, the Object will be included in the\
         results. If set to None, All Objects will be included.
        :type include_object_callback: Callable[[GameObject], bool], optional
        :return: An iterable of all Sims matching the `include_object_callback` filter.
        :rtype: Iterator[GameObject]
        """
        for game_object in services.object_manager().get_all():
            if game_object is None:
                continue
            if include_object_callback is not None and not include_object_callback(game_object):
                continue
            yield game_object

    @staticmethod
    def get_instance_for_all_visible_game_objects_generator(
        include_object_callback: Callable[[GameObject], bool]=None
    ) -> Iterator[GameObject]:
        """get_instance_for_all_visible_objects_generator(include_object_callback=None)

        Retrieve an instance for each and every visible Object in the game world.

        :param include_object_callback: If the result of this callback is True, the Object will be included in the results. If set to None, All Objects will be included.
        :type include_object_callback: Callable[[GameObject], bool], optional
        :return: An iterable of all Sims matching the `include_object_callback` filter.
        :rtype: Iterator[GameObject]
        """
        def _is_visible(_game_object: GameObject) -> bool:
            return not _game_object.is_hidden()

        include_object_callback = CommonFunctionUtils.run_predicates_as_one((_is_visible, include_object_callback))

        for game_object in CommonObjectUtils.get_instance_for_all_game_objects_generator(
            include_object_callback=include_object_callback
        ):
            yield game_object
