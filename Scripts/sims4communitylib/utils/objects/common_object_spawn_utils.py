"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import objects.system
from objects.game_object import GameObject
from objects.object_enums import ItemLocation
from sims4.commands import Command, CommandType, CheatOutput
from typing import Any, Callable, Union
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonObjectSpawnUtils:
    """Utilities for creating, spawning, and despawning Objects.

    """
    @staticmethod
    def spawn_object_on_lot(
        object_definition_id: int,
        location: CommonLocation,
        on_object_initialize_callback: Callable[[GameObject], Any]=None,
        post_object_spawned_callback: Callable[[GameObject], Any]=None
    ) -> Union[GameObject, None]:
        """spawn_object_on_lot(\
            object_definition_id,\
            location,\
            on_object_initialize_callback=None,\
            post_object_spawned_callback=None\
        )

        Spawn an Object on the current lot.

        :param object_definition_id: The decimal identifier of an Object.
        :type object_definition_id: int
        :param location: The location to spawn the Object at.
        :type location: CommonLocation
        :param on_object_initialize_callback: Called when initializing the Object.
        :type on_object_initialize_callback: Callable[[GameObject], Any], optional
        :param post_object_spawned_callback: Called after the Object was added to the lot.
        :type post_object_spawned_callback: Callable[[GameObject], Any], optional
        :return: An instance of the spawned Object or None if not successfully spawned.
        :rtype: GameObject
        """
        from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
        game_object = objects.system.create_object(
            object_definition_id,
            init=on_object_initialize_callback,
            post_add=post_object_spawned_callback,
            loc_type=ItemLocation.ON_LOT
        )
        if game_object is None:
            return None
        CommonObjectLocationUtils.set_location(game_object, location)
        return game_object

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def destroy_object(game_object: GameObject, source: str=None, cause: str=None, **kwargs) -> bool:
        """destroy_object(game_object, source=None, cause=None, **kwargs)

        Destroy an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param source: The source of the destruction.
        :type source: str, optional
        :param cause: The cause of the destruction.
        :type cause: str, optional
        :return: True, if the Object was successfully destroyed. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        game_object.destroy(source=source, cause=cause, **kwargs)
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def schedule_object_for_destroy(game_object: GameObject, source: str=None, cause: str=None, on_destroyed: Callable[[], None]=None, **kwargs) -> bool:
        """schedule_object_for_destroy(game_object, source=None, cause=None, on_destroyed=None, **kwargs)

        Schedule an Object to be destroyed.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param source: The source of the destruction. Default is None.
        :type source: str, optional
        :param cause: The cause of the destruction. Default is None.
        :type cause: str, optional
        :param on_destroyed: A callback that occurs after the Object is destroyed. Default is None.
        :type on_destroyed: Callable[[], None], optional
        :return: True, if the Object was successfully scheduled for destruction. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        game_object.schedule_destroy_asap(post_delete_func=on_destroyed, source=source, cause=cause, **kwargs)
        return True


@Command('s4clib_testing.spawn_object_on_lot', command_type=CommandType.Live)
def _common_testing_spawn_object_on_lot(object_id: str='20359', _connection: Any=None):
    output = CheatOutput(_connection)
    # noinspection PyBroadException
    try:
        object_id = int(object_id)
    except Exception:
        output('object_id must be an number.')
    output('Attempting to spawn object on the current lot with id \'{}\'.'.format(object_id))
    from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
    active_sim_info = CommonSimUtils.get_active_sim_info()
    location = CommonSimLocationUtils.get_location(active_sim_info)
    try:
        game_object = CommonObjectSpawnUtils.spawn_object_on_lot(object_id, location)
        if game_object is None:
            output('Failed to spawn object.')
        else:
            output('Object spawned successfully. Can you see it? Object Id: {}'.format(CommonObjectUtils.get_object_id(game_object)))
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred trying to spawn object.', exception=ex)
    output('Done spawning object.')
