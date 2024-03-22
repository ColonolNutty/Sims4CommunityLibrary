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
from objects.object_manager import ObjectManager
from objects.script_object import ScriptObject
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonObjectUtils(_HasS4CLClassLog):
    """Utilities for retrieving Objects in various ways.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_object_utils'

    @classmethod
    def create_unique_identifier(cls, game_object: GameObject) -> int:
        """create_unique_identifier(game_object)

        Create a unique identifier for an Object.

        .. note:: The unique identifier will be the same for all objects of the same type. For Example, with two The Ambassador toilets they will have the same unique identifier.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: An identifier that uniquely identifies a specific type of Object.
        :rtype: int
        """
        guid64 = cls.get_object_guid(game_object)
        catalog_name = cls.get_catalog_name(game_object)
        hash_value = 0x09D05916 ^ min(guid64, catalog_name)
        hash_value = (((0x000F4243 * hash_value) >> 4) & 0x0FFFFFFF) ^ max(guid64, catalog_name)
        hash_value = abs(hash_value ^ 2)
        return hash_value

    @classmethod
    def get_object_id(cls, object_instance: BaseObject) -> int:
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

    @classmethod
    def get_object_guid(cls, game_object: GameObject) -> int:
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

    @classmethod
    def get_object_definition(cls, game_object: Union[int, GameObject], pack_safe: bool = False, get_fallback_definition_id: bool = True) -> Definition:
        """get_object_definition(game_object, pack_safe=False, get_fallback_definition_id=True)

        Retrieve the definition for an Object.

        :param game_object: The decimal identifier of an Object or a Game Object.
        :type game_object: Union[int, GameObject]
        :param pack_safe: If true, objects will be searched for keeping package safety in mind. Default is False.
        :type pack_safe: bool, optional
        :param get_fallback_definition_id: Set True, to locate a fallback definition id. Default is True.
        :type get_fallback_definition_id: bool, optional
        :return: The definition of the object with the id.
        :rtype: Definition
        """
        game_object_instance = cls.get_game_object(game_object)
        if game_object_instance is not None:
            if hasattr(game_object_instance, 'definition') and game_object_instance.definition is not None:
                return game_object_instance.definition
        if hasattr(game_object, 'definition') and game_object.definition is not None:
            return game_object.definition
        return services.definition_manager().get(game_object, pack_safe=pack_safe, get_fallback_definition_id=get_fallback_definition_id)

    @classmethod
    def get_object_definition_id(cls, game_object: Union[int, GameObject], pack_safe: bool = False, get_fallback_definition_id: bool = True) -> Union[int, None]:
        """get_object_definition_id(game_object, pack_safe=False, get_fallback_definition_id=True)

        Retrieve the definition for an Object.

        :param game_object: The decimal identifier of an Object or a Game Object.
        :type game_object: Union[int, GameObject]
        :param pack_safe: If true, objects will be searched for keeping package safety in mind. Default is False.
        :type pack_safe: bool, optional
        :param get_fallback_definition_id: Set True, to locate a fallback definition id. Default is True.
        :type get_fallback_definition_id: bool, optional
        :return: The id of the definition of the object with the id.
        :rtype: Union[int, None]
        """
        definition = cls.get_object_definition(game_object, pack_safe=pack_safe, get_fallback_definition_id=get_fallback_definition_id)
        if definition is None:
            return None
        return definition.id

    @classmethod
    def get_game_object_definition(cls, game_object: GameObject, pack_safe: bool = False, get_fallback_definition_id: bool = True) -> Union[Definition, None]:
        """get_game_object_definition(game_object, pack_safe=False, get_fallback_definition_id=True)

        Retrieve the definition for an Object.

        :param game_object: An instance of a GameObject.
        :type game_object: GameObject
        :param pack_safe: If true, objects will be searched for keeping package safety in mind. Default is False.
        :type pack_safe: bool, optional
        :param get_fallback_definition_id: Set True, to locate a fallback definition id. Default is True.
        :type get_fallback_definition_id: bool, optional
        :return: The definition of the Game Object or None if no definition is found.
        :rtype: Definition
        """
        if game_object is None:
            return None
        if hasattr(game_object, 'definition') and game_object.definition is not None:
            return game_object.definition
        game_object_id = cls.get_object_id(game_object)
        if game_object_id is None or game_object_id == -1:
            return None
        return services.definition_manager().get(game_object_id, pack_safe=pack_safe, get_fallback_definition_id=get_fallback_definition_id)

    @classmethod
    def get_game_object_definition_id(cls, game_object: GameObject, pack_safe: bool = False, get_fallback_definition_id: bool = True) -> Union[int, None]:
        """get_game_object_definition(game_object, pack_safe=False, get_fallback_definition_id=True)

        Retrieve the definition for an Object.

        :param game_object: An instance of a GameObject.
        :type game_object: GameObject
        :param pack_safe: If true, objects will be searched for keeping package safety in mind. Default is False.
        :type pack_safe: bool, optional
        :param get_fallback_definition_id: Set True, to locate a fallback definition id. Default is True.
        :type get_fallback_definition_id: bool, optional
        :return: The id of the definition of the Game Object or None if no definition is found.
        :rtype: Union[int, None]
        """
        definition = cls.get_game_object_definition(game_object, pack_safe=pack_safe, get_fallback_definition_id=get_fallback_definition_id)
        if definition is None:
            return None
        return definition.id

    @classmethod
    def get_catalog_name(cls, game_object: GameObject) -> int:
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

    @classmethod
    def get_game_object(cls, game_object_id: int) -> GameObject:
        """get_game_object(game_object_id)

        Retrieve an instance of an Object in the game world.

        :param game_object_id: The decimal identifier of an Object.
        :type game_object_id: int
        :return: An instance of an Object or None if not found.
        :rtype: GameObject
        """
        return cls.get_game_object_manager().get(game_object_id)

    @classmethod
    def has_root_parent(cls, object_instance: ScriptObject) -> bool:
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

    @classmethod
    def get_root_parent(cls, object_instance: ScriptObject) -> Union[ScriptObject, None]:
        """get_root_parent(object_instance)

        Retrieve the root parent of an Object.

        :param object_instance: An instance of an Object.
        :type object_instance: ScriptObject
        :return: The root parent of the Object or None if a problem occurs.
        :rtype: Union[ScriptObject, None]
        """
        if object_instance is None or object_instance.parent is None:
            return object_instance
        return cls.get_root_parent(object_instance.parent) or object_instance

    @classmethod
    def get_instance_for_all_game_objects_generator(
        cls,
        include_object_callback: Callable[[GameObject], bool] = None
    ) -> Iterator[GameObject]:
        """get_instance_for_all_objects_generator(include_object_callback=None)

        Retrieve an instance for each and every Object in the game world.

        :param include_object_callback: If the result of this callback is True, the Object will be included in the\
         results. If set to None, All Objects will be included.
        :type include_object_callback: Callable[[GameObject], bool], optional
        :return: An iterator of all Objects matching the `include_object_callback` filter.
        :rtype: Iterator[GameObject]
        """
        game_object_list = tuple(cls.get_game_object_manager().get_all())
        for game_object in game_object_list:
            if game_object is None:
                continue
            if include_object_callback is not None and not include_object_callback(game_object):
                continue
            yield game_object

    @classmethod
    def get_instance_for_all_visible_game_objects_generator(
        cls,
        include_object_callback: Callable[[GameObject], bool] = None
    ) -> Iterator[GameObject]:
        """get_instance_for_all_visible_objects_generator(include_object_callback=None)

        Retrieve an instance for each and every visible Object in the game world.

        :param include_object_callback: If the result of this callback is True, the Object will be included in the results. If set to None, All Objects will be included.
        :type include_object_callback: Callable[[GameObject], bool], optional
        :return: An iterator of all Objects matching the `include_object_callback` filter.
        :rtype: Iterator[GameObject]
        """
        def _is_visible(_game_object: GameObject) -> bool:
            return not _game_object.is_hidden()

        include_object_callback = CommonFunctionUtils.run_predicates_as_one((_is_visible, include_object_callback))

        for game_object in cls.get_instance_for_all_game_objects_generator(
            include_object_callback=include_object_callback
        ):
            yield game_object

    @classmethod
    def get_game_object_manager(cls) -> ObjectManager:
        """get_game_object_manager()

        Retrieve the manager that manages all Game Objects in a game world.

        :return: The manager that manages all Game Objects in a game world.
        :rtype: ObjectManager
        """
        return services.object_manager()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_objects',
    'Print a list of all objects.'
)
def _s4cl_testing_log_all_objects(output: CommonConsoleCommandOutput):
    log = CommonObjectUtils.get_log()
    try:
        log.enable()
        output(f'Printing a list of all objects.')
        log.debug(f'Printing a list of all objects.')
        all_objects_str_list = list()
        for game_object in CommonObjectUtils.get_instance_for_all_game_objects_generator():
            object_id = CommonObjectUtils.get_object_id(game_object)
            from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
            object_location = CommonObjectLocationUtils.get_location(game_object)
            from sims4communitylib.utils.common_type_utils import CommonTypeUtils
            if CommonTypeUtils.is_sim_or_sim_info(game_object):
                all_objects_str_list.append(f'Sim {game_object} ({object_id}): Loc: {object_location}')
            else:
                all_objects_str_list.append(f'Object {game_object} ({object_id}): Loc: {object_location}')

        all_objects_str_list = sorted(all_objects_str_list)
        for all_objects_str in all_objects_str_list:
            output(all_objects_str)
            log.debug(all_objects_str)
        log.debug('Done printing a list of all objects.')
    finally:
        log.disable()
