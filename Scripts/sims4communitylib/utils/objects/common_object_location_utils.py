"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from typing import Union
from objects.components.live_drag_component import LiveDragComponent
from objects.script_object import ScriptObject
from protocolbuffers.Math_pb2 import Vector3
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils


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
    def set_location(game_object: GameObject, location: Vector3) -> bool:
        """set_location(game_object, location)

        Set the location of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param location: The location to put the Object.
        :type location: Vector3
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if game_object is None or location is None:
            return False
        game_object.location = location
        return True

    @staticmethod
    def get_location(game_object: GameObject) -> Union[Vector3, None]:
        """get_location(game_object)

        Retrieve the location of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The location of the Object or None if the Object does not have a location.
        :rtype: Vector3
        """
        if game_object is None:
            return None
        return game_object.location

    @staticmethod
    def get_position(script_object: ScriptObject) -> Union[Vector3, None]:
        """get_position(game_object)

        Retrieve the position of an Object.

        :param script_object: An instance of an Object.
        :type script_object: ScriptObject
        :return: The position of the Object or None if the Object does not have a position.
        :rtype: Vector3
        """
        if script_object is None:
            return None
        return script_object.position
