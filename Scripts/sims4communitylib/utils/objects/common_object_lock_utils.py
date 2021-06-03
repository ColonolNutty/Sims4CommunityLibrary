"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Callable, Iterator

from objects.components.locking_components import BaseLockingComponent
from objects.components.portal_lock_data import LockResult, IndividualSimDoorLockData
from objects.components.portal_locking_enums import LockPriority, LockSide, ClearLock
from objects.doors.door import Door
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class CommonObjectLockUtils:
    """ Utilities for manipulating the locking component of Objects, such as the ones found on Doors. """

    @staticmethod
    def is_door_locked_for_sim(
        door: Door,
        sim_info: SimInfo
    ) -> bool:
        """is_door_locked_for_sim(door, sim_info)

        Determine if a Door is locked for a Sim.

        :param door: An instance of a Door.
        :type door: Door
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Door is locked for the specified Sim. False, if not.
        :rtype: bool
        """
        return bool(CommonObjectLockUtils.test_door_lock_for_sim(door, sim_info))

    @staticmethod
    def test_door_lock_for_sim(
        door: Door,
        sim_info: SimInfo
    ) -> LockResult:
        """test_door_lock_for_sim(door, sim_info)

        Determine if a door is locked for a Sim.

        :param door: An instance of a Door.
        :type door: Door
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the door being locked and which side it is on.
        :rtype: bool
        """
        if not CommonTypeUtils.is_door(door):
            return LockResult(False)
        if not CommonComponentUtils.has_component(door, CommonComponentType.PORTAL_LOCKING):
            return LockResult(False)
        return door.test_lock(sim_info)

    @staticmethod
    def lock_door(
        door: Door,
        sim_info_list: Iterator[SimInfo],
        lock_sides: LockSide=LockSide.LOCK_BOTH,
        lock_priority: LockPriority=LockPriority.PLAYER_LOCK,
        clear_existing_locks: ClearLock=ClearLock.CLEAR_OTHER_LOCK_TYPES,
        replace_same_lock_type: bool=False
    ) -> bool:
        """lock_door(\
            door,\
            sim_info_list,\
            lock_priority=LockPriority.PLAYER_LOCK,\
            lock_sides=LockSide.LOCK_BOTH,\
            clear_existing_locks=ClearLock.CLEAR_OTHER_LOCK_TYPES,\
            replace_same_lock_type=False\
        )

        Lock a Door for Sims.

        :param door: An instance of a Door.
        :type door: Door
        :param sim_info_list: A collection of Sims to lock the door for.
        :type sim_info_list: Iterator[SimInfo]
        :param lock_priority: The priority of the lock being locked. Default is LockPriority.PLAYER_LOCK.
        :type lock_priority: LockPriority, optional
        :param lock_sides: The side(s) of the door to lock. Default is Both Sides.
        :type lock_sides: LockSide, optional
        :param clear_existing_locks: The other types of locks to clear from the door when locking it. Default is ClearLock.CLEAR_OTHER_LOCK_TYPES.
        :type clear_existing_locks: ClearLock, optional
        :param replace_same_lock_type: Set to True to replace lock types that are the same. Set to False to keep lock types that are the same. Default is False.
        :type replace_same_lock_type: bool, optional
        :return: True, if the Door was locked successfully. False, if not.
        :rtype: bool
        """
        if not CommonTypeUtils.is_door(door):
            return False
        if not CommonComponentUtils.has_component(door, CommonComponentType.PORTAL_LOCKING):
            return False
        for sim_info in sim_info_list:
            lock_data = IndividualSimDoorLockData(lock_sim=sim_info, lock_priority=lock_priority, lock_sides=lock_sides, should_persist=True)
            door.add_lock_data(lock_data, replace_same_lock_type=replace_same_lock_type, clear_existing_locks=clear_existing_locks)

    @staticmethod
    def unlock_door(
        door: Door,
        sim_info_list: Iterator[SimInfo],
        unlock_sides: LockSide=LockSide.LOCK_BOTH,
        lock_priority: LockPriority=LockPriority.PLAYER_LOCK,
        clear_existing_locks: ClearLock=ClearLock.CLEAR_NONE
    ) -> bool:
        """unlock_door(\
            door,\
            sim_info_list,\
            lock_priority=LockPriority.PLAYER_LOCK,\
            unlock_sides=LockSide.LOCK_BOTH,\
            clear_existing_locks=ClearLock.CLEAR_NONE,\
            replace_same_lock_type=False\
        )

        Unlock a Door for Sims.

        :param door: An instance of a Door.
        :type door: Door
        :param sim_info_list: A collection of Sims to lock the door for.
        :type sim_info_list: Iterator[SimInfo]
        :param lock_priority: The priority of the lock being unlocked. Default is LockPriority.PLAYER_LOCK.
        :type lock_priority: LockPriority, optional
        :param unlock_sides: The side(s) of the door to unlock. Default is Both Sides.
        :type unlock_sides: LockSide, optional
        :param clear_existing_locks: The other types of locks to clear from the door when unlocking it. Default is ClearLock.CLEAR_NONE.
        :type clear_existing_locks: ClearLock, optional
        :return: True, if the Door was unlocked successfully. False, if not.
        :rtype: bool
        """
        if not CommonTypeUtils.is_door(door):
            return False
        if not CommonComponentUtils.has_component(door, CommonComponentType.PORTAL_LOCKING):
            return False
        for sim_info in sim_info_list:
            lock_data = IndividualSimDoorLockData(unlock_sim=sim_info, lock_priority=lock_priority, lock_sides=unlock_sides, should_persist=True)
            door.add_lock_data(lock_data, replace_same_lock_type=False, clear_existing_locks=clear_existing_locks)

    @staticmethod
    def refresh_portal_locks_on_all_objects(include_object_callback: Callable[[GameObject], bool]= None) -> bool:
        """refresh_portal_locks_on_all_objects(include_object_callback=None)

        Refresh the Portal Locks on all Objects.

        :param include_object_callback: If the result of this callback is True, the Object will be have it's locks refreshed. If set to None, All Objects will have their locks refreshed. Default is None.
        :type include_object_callback: Callable[[GameObject], bool], optional
        :return: True, if the locks on all Objects were successfully refreshed. False, if not.
        :rtype: bool
        """
        all_successful = True
        for game_object in CommonObjectUtils.get_instance_for_all_game_objects_generator(include_object_callback=include_object_callback):
            if not CommonObjectLockUtils.refresh_portal_locks(game_object):
                all_successful = False
        return all_successful

    @staticmethod
    def refresh_portal_locks(game_object: GameObject) -> bool:
        """refresh_portal_locks(game_object)

        Refresh the Portal Locks of an Object.

        .. note:: If an Object cannot be locked, this function will do nothing.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if locks were refreshed successfully. False, if not.
        :rtype: bool
        """
        locking_component: BaseLockingComponent = CommonObjectLockUtils.get_portal_locking_component(game_object)
        if locking_component is None:
            return False
        locking_component.refresh_locks()
        return True

    @staticmethod
    def get_portal_locking_component(game_object: GameObject) -> Union[BaseLockingComponent, None]:
        """get_portal_locking_component(game_object)

        Retrieve the Portal Locking component of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The Portal Locking component of the Object or None if an error occurs.
        :rtype: Union[BaseLockingComponent, None]
        """
        if game_object is None:
            return None
        result: BaseLockingComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.PORTAL_LOCKING)
        return result
