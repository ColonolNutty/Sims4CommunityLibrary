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
try:
    from objects.pools.ocean import Ocean
except ModuleNotFoundError:
    # Those without the Island Paradise expansion pack won't have an Ocean object
    Ocean = None
from objects.doors.door import Door
from objects.game_object import GameObject
from objects.pools.pool import SwimmingPool
from objects.script_object import ScriptObject
from objects.terrain import Terrain


class CommonTypeUtils:
    """Utilities for determining the type of an object.

    """
    @staticmethod
    def is_sim_or_sim_info(obj: Any) -> bool:
        """Determine if an object is either of type Sim or type SimInfo

        """
        return CommonTypeUtils.is_sim_info(obj) or CommonTypeUtils.is_sim_instance(obj)

    @staticmethod
    def is_sim_instance(obj: Any) -> bool:
        """Determine if an object is of type Sim

        """
        return isinstance(obj, Sim)

    @staticmethod
    def is_sim_info(obj: Any) -> bool:
        """Determine if an object is of type SimInfo

        """
        return isinstance(obj, SimInfo)

    @staticmethod
    def is_sim_info_base_wrapper(obj: Any) -> bool:
        """Determine if an object is of type SimInfo

        """
        return isinstance(obj, SimInfoBaseWrapper)

    @staticmethod
    def is_script_object(obj: Any) -> bool:
        """Determine if an object is of type ScriptObject

        """
        return isinstance(obj, ScriptObject)

    @staticmethod
    def is_game_object(obj: Any) -> bool:
        """Determine if an object is of type GameObject

        """
        return isinstance(obj, GameObject)

    @staticmethod
    def is_terrain(obj: Any) -> bool:
        """Determine if an object is of type Terrain

        """
        return isinstance(obj, Terrain)

    @staticmethod
    def is_ocean(obj: Any) -> bool:
        """Determine if an object is of type Ocean

        """
        if Ocean is None:
            return False
        return isinstance(obj, Ocean)

    @staticmethod
    def is_swimming_pool(obj: Any) -> bool:
        """Determine if an object is of type SwimmingPool

        """
        return isinstance(obj, SwimmingPool)

    @staticmethod
    def is_door(obj: Any) -> bool:
        """Determine if an object is of type Door

        """
        return isinstance(obj, Door)
