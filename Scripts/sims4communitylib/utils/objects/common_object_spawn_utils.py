"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random

import objects.system
from objects.object_enums import ItemLocation
from sims4.commands import Command, CommandType, CheatOutput
from typing import Any, Callable, Union, Tuple, Iterator
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_transform import CommonTransform
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from carry.carry_postures import CarryingObject
from objects.game_object import GameObject
from objects.object_enums import ResetReason


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
    def spawn_object_near_location(
        object_definition_id: int,
        location: CommonLocation,
        radius: int=1,
        on_object_initialize_callback: Callable[[GameObject], Any]=None,
        post_object_spawned_callback: Callable[[GameObject], Any]=None
    ) -> GameObject:
        """spawn_object_on_lot(\
            object_definition_id,\
            location,\
            radius=1,\
            on_object_initialize_callback=None,\
            post_object_spawned_callback=None\
        )

        Spawn an Object near a location.

        :param object_definition_id: The decimal identifier of an Object.
        :type object_definition_id: int
        :param location: The location to spawn the Object at.
        :type location: CommonLocation
        :param radius: The radius at which the object may spawn in with the location at the center. Default is 1 square out.
        :type radius: int, optional
        :param on_object_initialize_callback: Called when initializing the Object.
        :type on_object_initialize_callback: Callable[[GameObject], Any], optional
        :param post_object_spawned_callback: Called after the Object was added to the lot.
        :type post_object_spawned_callback: Callable[[GameObject], Any], optional
        :return: An instance of the spawned Object or None if not successfully spawned.
        :rtype: GameObject
        """
        current_translation = location.transform.translation
        x = int(current_translation.x)
        min_x = x - radius
        max_x = x + radius
        new_x = random.randint(min_x, max_x)
        z = int(current_translation.z)
        min_z = z - radius
        max_z = z + radius
        new_z = random.randint(min_z, max_z)
        new_translation = CommonVector3(new_x, current_translation.y, new_z)
        new_transform = CommonTransform(
            new_translation,
            location.transform.orientation
        )
        new_location = CommonLocation(
            new_transform,
            location.routing_surface,
            parent_ref=location.parent_ref,
            joint_name_or_hash=location.joint_name_or_hash,
            slot_hash=location.slot_hash
        )
        return CommonObjectSpawnUtils.spawn_object_on_lot(
            object_definition_id,
            new_location,
            on_object_initialize_callback=on_object_initialize_callback,
            post_object_spawned_callback=post_object_spawned_callback
        )

    @staticmethod
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

    @staticmethod
    def soft_reset(
        game_object: GameObject,
        reset_reason: ResetReason=ResetReason.RESET_EXPECTED,
        hard_reset_on_exception: bool=False,
        source: Any=None,
        cause: Any='S4CL Soft Reset'
    ) -> bool:
        """soft_reset(game_object, reset_reason=ResetReason.RESET_EXPECTED, hard_reset_on_exception=False, source=None, cause=None)

        Perform a soft reset on an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param reset_reason: The reason for the reset. Default is ResetReason.RESET_EXPECTED.
        :type reset_reason: ResetReason, optional
        :param hard_reset_on_exception: If set to True, a hard reset of the Object will be attempted upon an error occurring. If set to False, nothing will occur if the reset failed. Default is False.
        :type hard_reset_on_exception: bool, optional
        :param source: The source of the reset. Default is the GameObject.
        :type source: Any, optional
        :param cause: The cause of the reset. Default is 'S4CL Soft Reset'.
        :type cause: Any, optional
        :return: True, if the reset was successful. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return True
        # noinspection PyBroadException
        try:
            if game_object.parent is not None and game_object.parent.is_sim and not game_object.parent.posture_state.is_carrying(game_object):
                CarryingObject.snap_to_good_location_on_floor(
                    game_object,
                    starting_transform=game_object.parent.transform,
                    starting_routing_surface=game_object.parent.routing_surface
                )
            location = game_object.location
            game_object.on_reset_send_op(reset_reason)
            game_object.location = location
            game_object.resend_location()
            if game_object.routing_component is not None:
                game_object.routing_component.on_reset_internal_state(reset_reason)
            if game_object.idle_component is not None:
                game_object.idle_component._refresh_active_idle()
            if game_object.linked_object_component is not None:
                game_object.linked_object_component._relink(update_others=True)
            return True
        except:
            if hard_reset_on_exception:
                return CommonObjectSpawnUtils.hard_reset(game_object, reset_reason=reset_reason, source=source, cause=cause)
        return False

    @staticmethod
    def hard_reset(game_object: GameObject, reset_reason: ResetReason=ResetReason.RESET_EXPECTED, source: Any=None, cause: Any='S4CL Hard Reset') -> bool:
        """hard_reset(game_object, reset_reason=ResetReason.RESET_EXPECTED, source=None, cause=None)

        Perform a hard reset on an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param reset_reason: The reason for the reset. Default is ResetReason.RESET_EXPECTED.
        :type reset_reason: ResetReason, optional
        :param source: The source of the reset. Default is the GameObject.
        :type source: Any, optional
        :param cause: The cause of the reset. Default is 'S4CL Hard Reset'.
        :type cause: Any, optional
        :return: True, if the reset was successful. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return True
        # noinspection PyBroadException
        try:
            game_object.reset(reset_reason, source=source or game_object, cause=cause)
            return True
        except:
            return False

    @staticmethod
    def fade_in(game_object: GameObject, fade_duration: float=1.0, immediate: bool=False, additional_channels: Iterator[Tuple[int, int, int]]=None):
        """fade_in(game_object, fade_duration=1.0, immediate=False, additional_channels=None)

        Change the opacity of an Object from invisible to visible.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param fade_duration: The number of milliseconds the fade effect should take to complete. Default is 1.0.
        :type fade_duration: float, optional
        :param immediate: If set to True, fade in will occur immediately. Default is False.
        :type immediate: bool, optional
        :param additional_channels: A collection of additional channels. The order of the inner tuple is Manager Id, Object Id, and Mask. Default is None.
        :type additional_channels: Iterator[Tuple[int, int, int]], optional
        """
        if game_object is None:
            return
        game_object.fade_in(fade_duration=fade_duration, immediate=immediate, additional_channels=additional_channels)

    @staticmethod
    def fade_out(game_object: GameObject, fade_duration: float=1.0, immediate: bool=False, additional_channels: Iterator[Tuple[int, int, int]]=None):
        """fade_out(game_object, fade_duration=1.0, immediate=False, additional_channels=None)

        Change the opacity of an Object from visible to invisible.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param fade_duration: The number of milliseconds the fade effect should take to complete. Default is 1.0.
        :type fade_duration: float, optional
        :param immediate: If set to True, fade out will occur immediately. Default is False.
        :type immediate: bool, optional
        :param additional_channels: A collection of additional channels. The order of the inner tuple is Manager Id, Object Id, and Mask. Default is None.
        :type additional_channels: Iterator[Tuple[int, int, int]], optional
        """
        if game_object is None:
            return
        game_object.fade_out(fade_duration=fade_duration, immediate=immediate, additional_channels=additional_channels)


@Command('s4clib.spawn_object', command_type=CommandType.Live)
def _common_spawn_object(object_id: str='20359', _connection: Any=None):
    output = CheatOutput(_connection)
    # noinspection PyBroadException
    try:
        object_id = int(object_id)
    except Exception:
        output('ERROR: object_id must be a number.')
        return
    if object_id < 0:
        output('ERROR: object_id must be a positive number.')
        return
    output('Attempting to spawn object on the current lot with id \'{}\'.'.format(object_id))
    from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
    active_sim_info = CommonSimUtils.get_active_sim_info()
    location = CommonSimLocationUtils.get_location(active_sim_info)
    try:
        game_object = CommonObjectSpawnUtils.spawn_object_on_lot(object_id, location)
        if game_object is None:
            output('ERROR: Failed to spawn object.')
        else:
            output('Object spawned successfully. Can you see it? Object Id: {}'.format(CommonObjectUtils.get_object_id(game_object)))
    except Exception as ex:
        output('ERROR: A problem occurred while attempting to spawn the object.')
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred trying to spawn object.', exception=ex)
    output('Done spawning object.')
