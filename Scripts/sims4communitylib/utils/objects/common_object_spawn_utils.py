"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from objects.object_enums import ItemLocation
from sims.sim_info import SimInfo
from typing import Any, Callable, Union, Tuple, Iterator
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_transform import CommonTransform
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from carry.carry_postures import CarryingObject
from objects.game_object import GameObject
from objects.object_enums import ResetReason
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.objects.common_object_ownership_utils import CommonObjectOwnershipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonObjectSpawnUtils(_HasS4CLClassLog):
    """Utilities for creating, spawning, and despawning Objects.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_object_spawn_utils'

    @classmethod
    def create_object(
        cls,
        object_definition_id: int,
        on_object_initialize_callback: Callable[[GameObject], Any] = None,
        post_object_spawned_callback: Callable[[GameObject], Any] = None,
        location_type: ItemLocation = ItemLocation.ON_LOT,
        **kwargs
    ) -> Union[GameObject, None]:
        """create_object(\
            object_definition_id,\
            on_object_initialize_callback=None,\
            post_object_spawned_callback=None,\
            location_type=ItemLocation.ON_LOT,\
            **kwargs\
        )

        Create an Object.

        :param object_definition_id: The decimal identifier of the definition of an Object.
        :type object_definition_id: int
        :param on_object_initialize_callback: Called when initializing the Object.
        :type on_object_initialize_callback: Callable[[GameObject], Any], optional
        :param post_object_spawned_callback: Called after the Object was added.
        :type post_object_spawned_callback: Callable[[GameObject], Any], optional
        :param location_type: The location the object is intended to be spawned at. Default is on the lot.
        :type location_type: ItemLocation, optional
        :return: An instance of the created Object or None if not successfully created.
        :rtype: GameObject
        """
        from objects.system import create_object
        return create_object(
            object_definition_id,
            init=on_object_initialize_callback,
            post_add=post_object_spawned_callback,
            loc_type=location_type,
            **kwargs
        )

    @classmethod
    def spawn_object_on_lot(
        cls,
        object_definition_id: int,
        location: CommonLocation,
        on_object_initialize_callback: Callable[[GameObject], Any] = None,
        post_object_spawned_callback: Callable[[GameObject], Any] = None,
        **kwargs
    ) -> Union[GameObject, None]:
        """spawn_object_on_lot(\
            object_definition_id,\
            location,\
            on_object_initialize_callback=None,\
            post_object_spawned_callback=None,\
            **kwargs\
        )

        Spawn an Object on the current lot.

        :param object_definition_id: The decimal identifier of the definition of an Object.
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
        game_object = cls.create_object(
            object_definition_id,
            on_object_initialize_callback=on_object_initialize_callback,
            post_object_spawned_callback=post_object_spawned_callback,
            location_type=ItemLocation.ON_LOT,
            **kwargs
        )
        if game_object is None:
            return None
        CommonObjectLocationUtils.set_location(game_object, location)
        return game_object

    @classmethod
    def spawn_object_near_location(
        cls,
        object_definition_id: int,
        location: CommonLocation,
        radius: int = 1,
        on_object_initialize_callback: Callable[[GameObject], Any] = None,
        post_object_spawned_callback: Callable[[GameObject], Any] = None,
        **kwargs
    ) -> GameObject:
        """spawn_object_near_location(\
            object_definition_id,\
            location,\
            radius=1,\
            on_object_initialize_callback=None,\
            post_object_spawned_callback=None,\
            **kwargs
        )

        Spawn an Object near a location.

        :param object_definition_id: The decimal identifier of the definition of an Object.
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
        if location is None:
            raise AssertionError('location was found to be None!')
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
        parent_ref = None
        if location.parent_ref is not None and hasattr(location.parent_ref, 'provided_routing_surface'):
            parent_ref = location.parent_ref
        new_location = CommonLocation(
            new_transform,
            location.routing_surface,
            parent_ref=parent_ref,
            joint_name_or_hash=location.joint_name_or_hash,
            slot_hash=location.slot_hash
        )
        return CommonObjectSpawnUtils.spawn_object_on_lot(
            object_definition_id,
            new_location,
            on_object_initialize_callback=on_object_initialize_callback,
            post_object_spawned_callback=post_object_spawned_callback,
            **kwargs
        )

    @classmethod
    def destroy_object(cls, game_object: GameObject, source: Any = None, cause: str = None, **kwargs) -> bool:
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
        if game_object.is_in_inventory():
            inventory = game_object.get_inventory()
            if inventory is None or inventory.owner is None:
                game_object.destroy(source=source, cause=cause, **kwargs)
            else:
                from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
                object_id = CommonObjectUtils.get_object_id(game_object)
                if game_object.is_in_sim_inventory():
                    sim_info = CommonSimUtils.get_sim_info(inventory.owner)
                    from sims4communitylib.utils.sims.common_sim_inventory_utils import CommonSimInventoryUtils
                    CommonSimInventoryUtils.remove_from_inventory(sim_info, object_id, count=1)
                else:
                    inventory_game_object = CommonObjectUtils.get_game_object(inventory.owner)
                    from sims4communitylib.utils.objects.common_object_inventory_utils import CommonObjectInventoryUtils
                    CommonObjectInventoryUtils.remove_from_inventory_by_id(inventory_game_object, object_id, count=1)
        else:
            game_object.destroy(source=source, cause=cause, **kwargs)
        return True

    @classmethod
    def schedule_object_for_destroy(cls, game_object: GameObject, source: Any = None, cause: str = None, on_destroyed: Callable[[], None] = None, **kwargs) -> bool:
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
        if game_object.is_in_inventory():
            inventory = game_object.get_inventory()
            if inventory is None or inventory.owner is None:
                game_object.schedule_destroy_asap(post_delete_func=on_destroyed, source=source, cause=cause, **kwargs)
            else:
                from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
                object_id = CommonObjectUtils.get_object_id(game_object)
                if game_object.is_in_sim_inventory():
                    sim_info = CommonSimUtils.get_sim_info(inventory.owner)
                    from sims4communitylib.utils.sims.common_sim_inventory_utils import CommonSimInventoryUtils
                    CommonSimInventoryUtils.remove_from_inventory(sim_info, object_id, count=1)
                else:
                    inventory_game_object = CommonObjectUtils.get_game_object(inventory.owner)
                    from sims4communitylib.utils.objects.common_object_inventory_utils import CommonObjectInventoryUtils
                    CommonObjectInventoryUtils.remove_from_inventory_by_id(inventory_game_object, object_id, count=1)
        else:
            game_object.schedule_destroy_asap(post_delete_func=on_destroyed, source=source, cause=cause, **kwargs)
        return True

    @classmethod
    def soft_reset(
        cls,
        game_object: GameObject,
        reset_reason: ResetReason = ResetReason.RESET_EXPECTED,
        hard_reset_on_exception: bool = False,
        source: Any = None,
        cause: str = 'S4CL Soft Reset'
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

    @classmethod
    def hard_reset(cls, game_object: GameObject, reset_reason: ResetReason = ResetReason.RESET_EXPECTED, source: Any = None, cause: str = 'S4CL Hard Reset') -> bool:
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

    @classmethod
    def fade_in(cls, game_object: GameObject, fade_duration: float = 1.0, immediate: bool = False, additional_channels: Iterator[Tuple[int, int, int]] = None):
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

    @classmethod
    def fade_out(cls, game_object: GameObject, fade_duration: float = 1.0, immediate: bool = False, additional_channels: Iterator[Tuple[int, int, int]] = None):
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


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.spawn_object',
    'Spawn a Game Object at the feet of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('object_definition_id', 'Decimal Identifier', 'The decimal identifier of the Object Definition for the object to spawn.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to spawn the object at.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.spawnobject',
    )
)
def _common_spawn_object(output: CommonConsoleCommandOutput, object_definition_id: int, sim_info: SimInfo = None):
    if object_definition_id <= 0:
        output('ERROR: object_definition_id must be a positive number above zero.')
        return
    output('Attempting to spawn object on the current lot with id \'{}\'.'.format(object_definition_id))
    from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
    from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
    sim_location = CommonSimLocationUtils.get_location(sim_info)
    game_object = CommonObjectSpawnUtils.spawn_object_on_lot(object_definition_id, sim_location)
    if game_object is not None:
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        CommonObjectSpawnUtils.get_log().enable()
        CommonObjectSpawnUtils.get_log().debug(f'Object {game_object} spawned successfully. Can you see it? Object Id: {game_object_id}')
        CommonObjectSpawnUtils.get_log().disable()
        output(f'SUCCESS: Object {game_object} spawned successfully. Can you see it? Object Id: {game_object_id}')
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        CommonObjectOwnershipUtils.set_owning_household_id(game_object, CommonHouseholdUtils.get_household_id(sim_info))
    else:
        output(f'ERROR: Failed to spawn object with definition id {object_definition_id}.')
    output(f'Done spawning object {game_object}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.fade_in_object',
    'Fade In an object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Instance Id', 'The instance id of a game object to fade in.'),
    ),
    command_aliases=(
        's4clib.fadeinobject',
    )
)
def _common_fade_in_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    if game_object is None:
        return
    game_object_str = str(game_object)
    output(f'Attempting to fade in object \'{game_object_str}\'.')

    if CommonObjectSpawnUtils.fade_in(game_object, immediate=True):
        output('Successfully faded in object.')
    else:
        output('Failed to fade in object.')
    return True


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.destroy_object',
    'Destroy/Delete a game object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Instance Id', 'The instance id of a game object to destroy/delete.'),
    ),
    command_aliases=(
        's4clib.destroyobject',
    )
)
def _common_destroy_object(output: CommonConsoleCommandOutput, game_object: GameObject):
    if game_object is None:
        return
    game_object_str = str(game_object)
    output(f'Attempting to destroy object \'{game_object_str}\'.')

    def _on_destroyed() -> None:
        output(f'SUCCESS: Object {game_object_str} successfully destroyed.')

    if CommonObjectSpawnUtils.schedule_object_for_destroy(game_object, source='S4CL Command', cause='S4CL Command', on_destroyed=_on_destroyed):
        output(f'Successfully scheduled object {game_object} for destruction. Please wait.')
    else:
        output(f'FAILED: Failed to schedule object {game_object} for destruction.')
    output(f'Done destroying or scheduling the destruction of object {game_object}.')

