"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from typing import Union
from objects.components.live_drag_component import LiveDragComponent
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.objects.common_object_type_utils import CommonObjectTypeUtils


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
