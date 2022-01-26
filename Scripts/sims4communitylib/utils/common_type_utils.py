"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4.math import Location
from objects.game_object import GameObject
from objects.script_object import ScriptObject


class CommonTypeUtils:
    """Utilities for determining the type of an object.

    """
    @staticmethod
    def is_sim_or_sim_info(obj: Any) -> bool:
        """is_sim_or_sim_info(obj)

        Determine if an object is either of type Sim or type SimInfo

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonTypeUtils.is_sim_instance(obj) or CommonTypeUtils.is_sim_info(obj)

    @staticmethod
    def is_sim_instance(obj: Any) -> bool:
        """is_sim_instance(obj)

        Determine if an object is of type Sim

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return isinstance(obj, Sim)

    @staticmethod
    def is_sim_info(obj: Any) -> bool:
        """is_sim_info(obj)

        Determine if an object is of type SimInfo

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return isinstance(obj, SimInfo)

    @staticmethod
    def is_sim_info_base_wrapper(obj: Any) -> bool:
        """is_sim_info_base_wrapper(obj)

        Determine if an object is of type SimInfo

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return isinstance(obj, SimInfoBaseWrapper)

    @staticmethod
    def is_script_object(obj: Any) -> bool:
        """is_script_object(obj)

        Determine if an object is of type ScriptObject

        .. note:: GameObjects, Terrain, and Sims are all ScriptObjects. Try also :func:`~is_game_object`, :func:`~is_terrain`, and :func:`~is_sim_instance`

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return isinstance(obj, ScriptObject)

    @staticmethod
    def is_game_object(obj: Any) -> bool:
        """is_game_object(obj)

        Determine if an object is of type GameObject

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return isinstance(obj, GameObject)

    @staticmethod
    def is_terrain(obj: Any) -> bool:
        """is_terrain(obj)

        Determine if an object is of type Terrain

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from objects.terrain import Terrain
        return isinstance(obj, Terrain)

    @staticmethod
    def is_land(obj: Any) -> bool:
        """is_land(obj)

        Determine if an object is of type Terrain or TerrainPoint.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonTypeUtils.is_terrain(obj) or CommonTypeUtils.is_terrain_point(obj)

    @staticmethod
    def is_water(obj: Any) -> bool:
        """is_water(obj)

        Determine if an object is of type Ocean, OceanPoint, SwimmingPool, or PoolPoint.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        return CommonTypeUtils.is_ocean(obj) or CommonTypeUtils.is_ocean_point(obj) or CommonTypeUtils.is_swimming_pool(obj) or CommonTypeUtils.is_pool_point(obj)

    @staticmethod
    def is_ocean(obj: Any) -> bool:
        """is_ocean(obj)

        Determine if an object is of type Ocean.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        try:
            from objects.pools.ocean import Ocean
        except ModuleNotFoundError:
            return False
        return isinstance(obj, Ocean)

    @staticmethod
    def is_swimming_pool(obj: Any) -> bool:
        """is_swimming_pool(obj)

        Determine if an object is of type SwimmingPool.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from sims4communitylib.utils.objects.common_object_type_utils import CommonObjectTypeUtils
        return CommonObjectTypeUtils.is_swimming_pool(obj)

    @staticmethod
    def is_door(obj: Any) -> bool:
        """is_door(obj)

        Determine if an Object is of type Door

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from sims4communitylib.utils.objects.common_object_type_utils import CommonObjectTypeUtils
        return CommonObjectTypeUtils.is_door(obj)

    @staticmethod
    def is_location(obj: Any) -> bool:
        """is_location(obj)

        Determine if an object is of type Location.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from sims4communitylib.classes.math.common_location import CommonLocation
        return isinstance(obj, Location) or isinstance(obj, CommonLocation)

    @staticmethod
    def is_location_point(obj: Any) -> bool:
        """is_location_point(obj)

        Determine if an object is of type _LocationPoint.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from objects.terrain import _LocationPoint
        return isinstance(obj, _LocationPoint)

    @staticmethod
    def is_terrain_point(obj: Any) -> bool:
        """is_terrain_point(obj)

        Determine if an object is of type TerrainPoint.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from objects.terrain import TerrainPoint
        return isinstance(obj, TerrainPoint)

    @staticmethod
    def is_ocean_point(obj: Any) -> bool:
        """is_ocean_point(obj)

        Determine if an object is of type OceanPoint.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        try:
            from objects.terrain import OceanPoint
        except ModuleNotFoundError:
            return False
        return isinstance(obj, OceanPoint)

    @staticmethod
    def is_pool_point(obj: Any) -> bool:
        """is_pool_point(obj)

        Determine if an object is of type PoolPoint.

        :param obj: The object to check.
        :type obj: Any
        :return: True, if it is. False, if it is not.
        :rtype: bool
        """
        from objects.terrain import PoolPoint
        return isinstance(obj, PoolPoint)

    @staticmethod
    def is_pool_seat(obj: Any) -> bool:
        """is_pool_seat(obj)

        Determine if an Object is a Pool Seat.

        :param obj: An instance of an Object.
        :type: Any
        :return: True, if the Object is a Pool Seat. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.objects.common_object_type_utils import CommonObjectTypeUtils
        return CommonObjectTypeUtils.is_swimming_pool_seat(obj)
