"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.terrain import Terrain
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3


class CommonTerrainLocationUtils:
    """Utilities for manipulating the locational data of Terrain."""

    @staticmethod
    def get_water_depth_at(x: float, z: float, surface_level: int=0) -> float:
        """get_water_depth_at(x, z, surface_level=0)

        Determine the water depth at the specified coordinates.

        :param x: The X coordinate.
        :type x: float
        :param z: The Z coordinate.
        :type z: float
        :param surface_level: The surface level. Default is 0.
        :type surface_level: int, optional
        :return: The depth of the water at the specified coordinates.
        :rtype: float
        """
        from terrain import get_water_depth
        return get_water_depth(x, z, level=surface_level)

    @staticmethod
    def get_position(terrain_object: Terrain) -> Union[CommonVector3, None]:
        """get_position(terrain_object)

        Retrieve the position of a Terrain Object.

        :param terrain_object: An instance of a Terrain object.
        :type terrain_object: Terrain
        :return: The position of the Object or None if the Object does not have a position.
        :rtype: CommonVector3
        """
        if terrain_object is None:
            return None
        # noinspection PyBroadException
        try:
            return CommonVector3.from_vector3(terrain_object.position)
        except:
            return None

    @staticmethod
    def get_routing_surface(terrain_object: Terrain) -> Union[CommonSurfaceIdentifier, None]:
        """get_routing_surface(game_object)

        Retrieve the routing surface of a Terrain Object.

        :param terrain_object: An instance of a Terrain Object.
        :type terrain_object: Terrain
        :return: The routing surface of the object or None if a problem occurs.
        :rtype: Union[CommonSurfaceIdentifier, None]
        """
        if terrain_object is None:
            return None
        return CommonSurfaceIdentifier.from_surface_identifier(terrain_object.routing_surface)
