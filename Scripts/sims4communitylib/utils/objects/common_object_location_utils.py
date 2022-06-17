"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from typing import Union
from objects.components.live_drag_component import LiveDragComponent
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.objects.common_object_type_utils import CommonObjectTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from world.lot import Lot


class CommonObjectLocationUtils:
    """Utilities for manipulating the location and draggability of Objects.

    """

    @staticmethod
    def enable_object_drag_in_live_mode(game_object: GameObject) -> bool:
        """enable_object_drag_in_live_mode(game_object)

        Enable the draggability of an Object in Live Mode.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        live_drag_component: LiveDragComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.LIVE_DRAG)
        if live_drag_component is None:
            return False
        live_drag_component._set_can_live_drag(True)
        return True

    @staticmethod
    def disable_object_drag_in_live_mode(game_object: GameObject) -> bool:
        """disable_object_drag_in_live_mode(game_object)

        Disable the draggability an Object in Live Mode.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        live_drag_component: LiveDragComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.LIVE_DRAG)
        if live_drag_component is None:
            return False
        live_drag_component._set_can_live_drag(False)
        return True

    @staticmethod
    def is_within_range_of_position(game_object: GameObject, position: CommonVector3, distance_in_squares: float) -> bool:
        """is_within_range_of_position(game_object, position, distance_in_squares)

        Determine if a Game Object is within a certain distance of a Position.

        :param game_object: The object to check.
        :type game_object: GameObject
        :param position: A position.
        :type position: CommonVector3
        :param distance_in_squares: A unit measured in squares. 1 square is the size of 1 square in the Build/Buy mode visual grid. For comparison, a dining chair would be 1 square by 1 square. 0.5 would be half a square, or half a dining chair.
        :type distance_in_squares: float
        :return: True, if the distance between the Object and the Position is less than or equal to the specified distance in squares. False, if not.
        :return: bool
        """
        object_position = CommonObjectLocationUtils.get_position(game_object)
        if object_position is None:
            return False
        return CommonLocationUtils.is_position_within_range_of_position(object_position, position, distance_in_squares)

    @staticmethod
    def is_within_range_of_location(game_object: GameObject, location: CommonLocation, distance_in_squares: float) -> bool:
        """is_within_range_of_location(game_object, location, distance_in_squares)

        Determine if a Game Object is within a certain distance of a Location.

        :param game_object: The object to check.
        :type game_object: GameObject
        :param location: A location.
        :type location: CommonLocation
        :param distance_in_squares: A unit measured in squares. 1 square is the size of 1 square in the Build/Buy mode visual grid. For comparison, a dining chair would be 1 square by 1 square. 0.5 would be half a square, or half a dining chair.
        :type distance_in_squares: float
        :return: True, if the distance between the Object and the Location is less than or equal to the specified distance in squares. False, if not.
        :return: bool
        """
        object_location = CommonObjectLocationUtils.get_location(game_object)
        if object_location is None:
            return False
        return CommonLocationUtils.is_location_within_range_of_location(object_location, location, distance_in_squares)

    @staticmethod
    def is_on_current_lot(game_object: GameObject) -> bool:
        """is_on_current_lot(game_object)

        Determine if a Sim is on the active Lot.

        :param game_object: The object to check.
        :type game_object: GameObject
        :return: True, if the Object is on the active Lot. False, if not.
        :rtype: bool
        """
        active_lot = CommonLocationUtils.get_current_lot()
        return CommonObjectLocationUtils.is_on_lot(game_object, active_lot)

    @staticmethod
    def is_on_lot(game_object: GameObject, lot: Lot) -> bool:
        """is_on_lot(sim_info, lot)

        Determine if a Game Object is on a Lot.

        :param game_object: The object to check.
        :type game_object: GameObject
        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: True, if the Object is on the specified Lot. False, if not.
        :rtype: bool
        """
        object_position = CommonObjectLocationUtils.get_position(game_object)
        if object_position is None:
            return False
        return CommonLocationUtils.is_position_on_lot(object_position, lot)

    @staticmethod
    def can_drag_object_in_live_mode(game_object: GameObject) -> bool:
        """can_live_drag(game_object)

        Determine if an Object can be dragged in Live Mode.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object can be dragged in Live Mode. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        live_drag_component: LiveDragComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.LIVE_DRAG)
        if live_drag_component is None:
            return False
        return live_drag_component.can_live_drag

    @staticmethod
    def set_location(game_object: GameObject, location: CommonLocation) -> bool:
        """set_location(game_object, location)

        Set the location of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param location: The location to put the Object.
        :type location: CommonLocation
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if game_object is None or location is None:
            return False
        game_object.location = location
        return True

    @staticmethod
    def get_location(game_object: GameObject) -> Union[CommonLocation, None]:
        """get_location(game_object)

        Retrieve the location of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The location of the Object or None if the Object does not have a location.
        :rtype: Union[CommonLocation, None]
        """
        if game_object is None:
            return None
        return CommonLocation.from_location(game_object.location)

    @staticmethod
    def get_position(game_object: GameObject) -> Union[CommonVector3, None]:
        """get_position(game_object)

        Retrieve the position of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The position of the Object or None if the Object does not have a position.
        :rtype: CommonVector3
        """
        if game_object is None:
            return None
        # noinspection PyBroadException
        try:
            return CommonVector3.from_vector3(game_object.position)
        except:
            return None

    @staticmethod
    def get_bone_position(game_object: GameObject, bone_name: str) -> Union[CommonVector3, None]:
        """get_bone_position(game_object, bone_name)

        Retrieve the position of a joint bone on an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param bone_name: The name of the bone to retrieve the position of.
        :type bone_name: str
        :return: The position of the Object or None if the Object does not have the specified bone.
        :rtype: Union[CommonVector3, None]
        """
        # noinspection PyBroadException
        try:
            return CommonVector3.from_vector3(game_object.get_joint_transform_for_joint(bone_name).translation)
        except:
            return None

    @staticmethod
    def get_root_position(game_object: GameObject) -> CommonVector3:
        """get_root_position(game_object)

        Calculate the position of an Object based off of the position of it's Root bone.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The position of the Object based off of the position of it's Root bone.
        :rtype: CommonVector3
        """
        object_position = CommonObjectLocationUtils.get_bone_position(game_object, bone_name='b__ROOT__') or CommonObjectLocationUtils.get_position(game_object)
        if object_position is not None and CommonObjectTypeUtils.is_window(game_object):
            # For whatever reason, windows have a Y coordinate of -0.0. We fix it here.
            object_position = CommonVector3(object_position.x, CommonLocationUtils.get_surface_height_at(object_position.x, object_position.z, CommonObjectLocationUtils.get_routing_surface(game_object)), object_position.z)
        return object_position

    @staticmethod
    def get_forward_vector(game_object: GameObject) -> CommonVector3:
        """get_forward_vector(game_object)

        Retrieve the forward vector of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The forward vector of the Object.
        :rtype: CommonVector3
        """
        return CommonVector3.from_vector3(game_object.forward)

    @staticmethod
    def get_orientation(game_object: GameObject) -> CommonQuaternion:
        """get_orientation(game_object)

        Retrieve the orientation of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The orientation of the Object.
        :rtype: CommonQuaternion
        """
        return CommonQuaternion.from_quaternion(game_object.orientation)

    @staticmethod
    def get_orientation_degrees(game_object: GameObject) -> float:
        """get_orientation_in_degrees(game_object)

        Retrieve the orientation of an Object in degrees.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The orientation of the Object represented in degrees.
        :rtype: float
        """
        return CommonQuaternion.to_degrees(CommonObjectLocationUtils.get_orientation(game_object))

    @staticmethod
    def get_routing_surface(game_object: GameObject) -> Union[CommonSurfaceIdentifier, None]:
        """get_routing_surface(game_object)

        Retrieve the routing surface of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The routing surface of the object or None if a problem occurs.
        :rtype: Union[CommonSurfaceIdentifier, None]
        """
        if game_object is None:
            return None
        return CommonSurfaceIdentifier.from_surface_identifier(game_object.routing_surface)

    @staticmethod
    def get_surface_level(game_object: GameObject) -> int:
        """get_surface_level(game_object)

        Retrieve the surface level of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The surface level of the object.
        :rtype: int
        """
        if game_object is None:
            return 0
        routing_surface = CommonObjectLocationUtils.get_routing_surface(game_object)
        if not routing_surface:
            return 0
        return routing_surface.secondary_id

    @staticmethod
    def can_be_routed_to(game_object: GameObject) -> bool:
        """can_be_routed_to(game_object)

        Determine if an Object can be routed to by Sims.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object can be routed to by Sims. False, it not.
        :rtype: bool
        """
        position = CommonObjectLocationUtils.get_position(game_object) + CommonObjectLocationUtils.get_forward_vector(game_object)
        routing_surface = CommonObjectLocationUtils.get_routing_surface(game_object)
        return CommonLocationUtils.can_position_be_routed_to(position, routing_surface)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.move_object_to_sim',
    'Move a game object to the current location of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Instance Id', 'The instance id of a game object to move.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to move the object to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.moveobjecttosim',
    )
)
def _common_move_object_to_sim(output: CommonConsoleCommandOutput, game_object: GameObject, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    if game_object is None:
        output('ERROR: No object was specified or the specified Game Object was not found.')
        return
    output(f'Attempting to move object {game_object} to Sim {sim_info}.')
    from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
    if CommonObjectLocationUtils.set_location(game_object, CommonSimLocationUtils.get_location(sim_info)):
        output(f'SUCCESS: Object {game_object} was moved successfully to Sim {sim_info}.')
    else:
        output(f'FAILED: Object {game_object} failed to move to Sim {sim_info}')
    output(f'Done moving object {game_object}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_bone_position_on_sim',
    'Print the position of a bone on a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('bone_name', 'Text', 'The name of a bone on the rig.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of a Sim.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printbonepositiononsim',
    )
)
def _common_print_bone_position(output: CommonConsoleCommandOutput, bone_name: str, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    if bone_name is None:
        output('ERROR: No bone name was specified.')
        return
    sim = CommonSimUtils.get_sim_instance(sim_info)
    bone_position = CommonObjectLocationUtils.get_bone_position(sim, bone_name)
    if bone_position is None:
        output(f'Bone {bone_name} not found on Sim {sim_info}.')
    else:
        output(f'Got bone position. X: {bone_position.x} Y: {bone_position.y} Z: {bone_position.z}')
