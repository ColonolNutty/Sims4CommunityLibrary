"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from buffs.buff import Buff
from objects.doors.door import Door
from objects.game_object import GameObject
try:
    from objects.pools.ocean import Ocean
except ModuleNotFoundError:
    Ocean = None
from objects.pools.pool import SwimmingPool
from objects.pools.pool_seat import PoolSeat
from objects.script_object import ScriptObject
from objects.terrain import Terrain
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4.math import Location


class CommonTypeUtils:
    """ Utilities for determining the type of an object. """
    @staticmethod
    def is_integer(obj: Any) -> bool:
        """
            Determine if an object is of type int
        """
        return isinstance(obj, int)

    @staticmethod
    def is_sim_or_sim_info(obj: Any) -> bool:
        """
            Determine if an object is either of type Sim or type SimInfo
        """
        return CommonTypeUtils.is_sim_info(obj) or CommonTypeUtils.is_sim_instance(obj)

    @staticmethod
    def is_sim_instance(obj: Any) -> bool:
        """
            Determine if an object is of type Sim
        """
        return isinstance(obj, Sim)

    @staticmethod
    def is_sim_info(obj: Any) -> bool:
        """
            Determine if an object is of type SimInfo
        """
        return isinstance(obj, SimInfo)

    @staticmethod
    def is_script_object(obj: Any) -> bool:
        """
            Determine if an object is of type ScriptObject
        """
        return isinstance(obj, ScriptObject)

    @staticmethod
    def is_game_object(obj: Any) -> bool:
        """
            Determine if an object is of type GameObject
        """
        return isinstance(obj, GameObject)

    @staticmethod
    def is_terrain(obj: Any) -> bool:
        """
            Determine if an object is of type Terrain
        """
        return isinstance(obj, Terrain)

    @staticmethod
    def is_ocean(obj: Any) -> bool:
        """
            Determine if an object is of type Ocean
        """
        if Ocean is None:
            return False
        return isinstance(obj, Ocean)

    @staticmethod
    def is_swimming_pool(obj: Any) -> bool:
        """
            Determine if an object is of type SwimmingPool
        """
        return isinstance(obj, SwimmingPool)

    @staticmethod
    def is_pool_seat(obj: Any) -> bool:
        """
            Determine if an object is of type PoolSeat
        """
        return isinstance(obj, PoolSeat)

    @staticmethod
    def is_door_object(obj: Any) -> bool:
        """
            Determine if an object is of type Door
        """
        return isinstance(obj, Door)

    @staticmethod
    def is_buff(obj: Any) -> bool:
        """
            Determine if an object is of type Buff
        """
        return isinstance(obj, Buff)

    @staticmethod
    def is_location(obj: Any) -> bool:
        """
            Determine if an object is of type Location
        """
        return isinstance(obj, Location)
