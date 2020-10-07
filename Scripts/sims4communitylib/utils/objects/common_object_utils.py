"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.base_object import BaseObject
from typing import Callable, Iterator, Union
import services
from objects.definition import Definition
from objects.game_object import GameObject
from objects.script_object import ScriptObject
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonObjectUtils:
    """Utilities for retrieving Objects in various ways.

    """
    @staticmethod
    def create_unique_identifier(game_object: GameObject) -> int:
        """create_unique_identifier(game_object)

        Create a unique identifier for an Object.

        .. note:: The unique identifier will be the same for all objects of the same type. For Example, with two The Ambassador toilets they will have the same unique identifier.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: An identifier that uniquely identifies a specific Object.
        :rtype: int
        """
        guid64 = CommonObjectUtils.get_object_guid(game_object)
        catalog_name = CommonObjectUtils.get_catalog_name(game_object)
        if guid64 > catalog_name:
            identifier_data = [int(catalog_name), int(guid64)]
        else:
            identifier_data = [int(guid64), int(catalog_name)]
        hash_value = 3430008
        for item in identifier_data:
            hash_value = eval(hex(1000003 * hash_value & 4294967295)[:-1]) ^ item
        hash_value ^= len(identifier_data)
        return abs(hash_value)

    @staticmethod
    def get_object_id(object_instance: BaseObject) -> int:
        """get_object_id(object_instance)

        Retrieve the decimal identifier of an Object.

        :param object_instance: An instance of an Object.
        :type object_instance: BaseObject
        :return: The decimal identifier of the BaseObject or -1 if the id could not be gained.
        :rtype: int
        """
        if object_instance is None:
            return -1
        return object_instance.id or getattr(object_instance, 'id', -1)

    @staticmethod
    def get_object_guid(game_object: GameObject) -> int:
        """get_object_guid(game_object)

        Retrieve the GUID of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The GUID of the specified Object or -1 if it does not have one.
        :rtype: int
        """
        if game_object is None or not hasattr(game_object, 'guid64'):
            return -1
        return getattr(game_object, 'guid64', -1)

    @staticmethod
    def get_object_definition(object_id: int, pack_safe: bool=False, get_fallback_definition_id: bool=True) -> Definition:
        """get_definition(object_id)

        Retrieve the definition for an Object.

        :param object_id: The decimal identifier of an Object.
        :type object_id: int
        :param pack_safe: If true, objects will be searched for keeping package safety in mind. Default is False.
        :type pack_safe: bool, optional
        :param get_fallback_definition_id: Whether or not to locate a fallback definition id. Default is True.
        :type get_fallback_definition_id: bool, optional
        :return: The definition of the object with the id.
        :rtype: Definition
        """
        return services.definition_manager().get(object_id, pack_safe=pack_safe, get_fallback_definition_id=get_fallback_definition_id)

    @staticmethod
    def get_catalog_name(game_object: GameObject) -> int:
        """get_catalog_name(game_object)

        Retrieve the catalog name identifier of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The decimal identifier of the catalog name of an Object or -1 if no catalog name is found.
        :rtype: int
        """
        if game_object is None:
            return -1
        return game_object.catalog_name

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
    def has_root_parent(object_instance: ScriptObject) -> bool:
        """has_root_parent(object_instance)

        Determine if an Object has a root parent.

        :param object_instance: An instance of an Object.
        :type object_instance: ScriptObject
        :return: True, if the Object has a root parent. False, if not.
        :rtype: bool
        """
        if object_instance is None:
            return False
        return object_instance.parent is not None

    @staticmethod
    def get_root_parent(object_instance: ScriptObject) -> Union[ScriptObject, None]:
        """get_root_parent(object_instance)

        Retrieve the root parent of an Object.

        :param object_instance: An instance of an Object.
        :type object_instance: ScriptObject
        :return: The root parent of the Object or None if a problem occurs.
        :rtype: Union[ScriptObject, None]
        """
        if object_instance is None or object_instance.parent is None:
            return object_instance
        return CommonObjectUtils.get_root_parent(object_instance.parent) or object_instance

    @staticmethod
    def get_instance_for_all_game_objects_generator(
        include_object_callback: Callable[[GameObject], bool]=None
    ) -> Iterator[GameObject]:
        """get_instance_for_all_objects_generator(include_object_callback=None)

        Retrieve an instance for each and every Object in the game world.

        :param include_object_callback: If the result of this callback is True, the Object will be included in the\
         results. If set to None, All Objects will be included.
        :type include_object_callback: Callable[[GameObject], bool], optional
        :return: An iterable of all Objects matching the `include_object_callback` filter.
        :rtype: Iterator[GameObject]
        """
        game_object_list = tuple(services.object_manager().get_all())
        for game_object in game_object_list:
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
        :return: An iterable of all Objects matching the `include_object_callback` filter.
        :rtype: Iterator[GameObject]
        """
        def _is_visible(_game_object: GameObject) -> bool:
            return not _game_object.is_hidden()

        include_object_callback = CommonFunctionUtils.run_predicates_as_one((_is_visible, include_object_callback))

        for game_object in CommonObjectUtils.get_instance_for_all_game_objects_generator(
            include_object_callback=include_object_callback
        ):
            yield game_object
