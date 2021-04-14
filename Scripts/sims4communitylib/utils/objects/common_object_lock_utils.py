"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Callable

from objects.components.locking_components import BaseLockingComponent
from objects.game_object import GameObject
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class CommonObjectLockUtils:
    """ Utilities for manipulating the locking component of Objects, such as the ones found on Doors. """

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
