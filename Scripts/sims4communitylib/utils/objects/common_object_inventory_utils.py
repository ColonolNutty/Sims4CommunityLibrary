"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Iterator, Union
from interactions.base.create_object_interaction import ObjectDefinition
from objects.components.object_inventory_component import ObjectInventoryComponent
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class CommonObjectInventoryUtils:
    """ Utilities for manipulating the inventory of Objects. """
    @staticmethod
    def has_inventory(game_object: GameObject) -> bool:
        """has_inventory(game_object)

        Determine if an Object has an inventory.

        :param game_object: An instance of a Game Object.
        :type game_object: GameObject
        :return: True, if the Sim has an inventory. False, if not.
        :rtype: bool
        """
        return CommonObjectInventoryUtils._get_inventory(game_object) is not None

    @staticmethod
    def get_all_objects_in_inventory_gen(game_object: GameObject, include_object_callback: Callable[[GameObject], bool]=None) -> Iterator[GameObject]:
        """get_all_objects_in_inventory_gen(game_object, include_object_callback=None)

        Retrieve all Objects in the inventory of an Object.

        :param game_object: An instance of a Game Object.
        :type game_object: GameObject
        :param include_object_callback: If the result of this callback is True, the object will be included in the results. If set to None, All objects in the inventory will be included.
        :type include_object_callback: Callable[[int], bool], optional
        :return: An iterator containing the decimal identifiers for the objects in the inventory of an Object.
        :rtype: Iterator[GameObject]
        """
        inventory_component: ObjectInventoryComponent = CommonObjectInventoryUtils._get_inventory(game_object)
        if inventory_component is None:
            return tuple()
        if include_object_callback is None:
            for inventory_object in inventory_component:
                yield inventory_object
        else:
            for inventory_object in inventory_component:
                if include_object_callback(inventory_object):
                    yield inventory_object

    @staticmethod
    def move_object_to_inventory(game_object_container: GameObject, game_object_to_move: GameObject) -> bool:
        """move_object_to_inventory(game_object_container, game_object_to_move)

        Move an Object to the inventory of an Object container.

        :param game_object_container: The Object container to receive the moved Object.
        :type game_object_container: GameObject
        :param game_object_to_move: The Object to move.
        :type game_object_to_move: GameObject
        :return: True, if the object was successfully moved to the inventory of the specified Object container. False, if not.
        :rtype: bool
        """
        if game_object_container is None or game_object_to_move is None:
            return False
        inventory_component = CommonObjectInventoryUtils._get_inventory(game_object_container)
        if inventory_component is None:
            return False
        from sims4communitylib.utils.objects.common_object_ownership_utils import CommonObjectOwnershipUtils
        CommonObjectOwnershipUtils.set_owning_household_id(game_object_to_move, CommonObjectOwnershipUtils.get_owning_household_id(game_object_container))
        return inventory_component.player_try_add_object(game_object_to_move)

    @staticmethod
    def add_to_inventory(game_object: GameObject, object_id: int, count: int=1) -> bool:
        """add_to_inventory(game_object, object_definition_id, count=1)

        Add a number of Newly Created Objects to the Inventory of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_id: The decimal identifier of an Object.
        :type object_id: int
        :param count: The number of the specified Object to add. Default is 1.
        :type count: int, optional
        :return: True, if the count of the specified Object were added successfully. False, it not.
        :rtype: bool
        """
        inventory_component: ObjectInventoryComponent = CommonObjectInventoryUtils._get_inventory(game_object)
        if inventory_component is None:
            return False

        def _post_create(_game_object: GameObject) -> bool:
            return CommonObjectInventoryUtils.move_object_to_inventory(game_object, _game_object)

        success = True
        for _ in range(count):
            game_object = CommonObjectSpawnUtils.spawn_object_on_lot(object_id, CommonLocation.empty(), post_object_spawned_callback=_post_create)
            if game_object is None:
                success = False
        return success

    @staticmethod
    def remove_from_inventory_by_id(game_object: GameObject, object_id: int, count: int = 1) -> bool:
        """remove_from_inventory_by_id(game_object, object_id, count=1)

        Remove a number of Objects by their Id from the inventory of an Object.

        :param game_object: The Object to remove Objects from.
        :type game_object: GameObject
        :param object_id: The decimal identifier of an Object.
        :type object_id: int
        :param count: The amount of the Object to remove. Default is 1.
        :type count: int, optional
        :return: True, if the count of the specified Object were removed successfully. False, if not.
        """
        inventory_component: ObjectInventoryComponent = CommonObjectInventoryUtils._get_inventory(game_object)
        if inventory_component is None:
            return False
        return inventory_component.try_remove_object_by_id(object_id, count=count)

    @staticmethod
    def remove_from_inventory_by_definition(game_object: GameObject, object_definition: ObjectDefinition, count: int = 1) -> bool:
        """remove_from_inventory(game_object, object_id, count=1)

        Remove a number of Objects from the inventory of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_definition: The definition of an Object.
        :type object_definition: ObjectDefinition
        :param count: The amount of the Object to remove. Default is 1.
        :type count: int, optional
        :return: True, if the count of the specified Object were removed successfully. False, if not.
        """
        def _include_object_callback(_game_object: GameObject) -> bool:
            return _game_object.definition == object_definition

        inventory_objects = CommonObjectInventoryUtils.get_all_objects_in_inventory_gen(game_object, include_object_callback=_include_object_callback)
        for inventory_object in inventory_objects:
            object_id = CommonObjectUtils.get_object_id(inventory_object)
            if CommonObjectInventoryUtils.remove_from_inventory_by_id(game_object, object_id, count=count):
                return True
        return False

    @staticmethod
    def get_count_of_object_in_inventory(game_object: GameObject, object_id: int) -> int:
        """get_count_of_object_in_inventory(game_object, object_id)

        Count the number of an Object in the inventory of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_id: The decimal identifier of an object.
        :type object_id: int
        :return: The number of a particular Object found in the inventory of the specified Object.
        :type: int
        """
        inventory_component: ObjectInventoryComponent = CommonObjectInventoryUtils._get_inventory(game_object)
        if inventory_component is None:
            return 0
        object_definition = CommonObjectUtils.get_object_definition(object_id)
        return inventory_component.get_count(object_definition)

    @staticmethod
    def open_inventory(game_object: GameObject) -> None:
        """open_inventory(game_object)

        Open the inventory of an Object.

        :param game_object: The Object to open the inventory of.
        :type game_object: GameObject
        """
        if game_object is None:
            return
        inventory_component: ObjectInventoryComponent = CommonObjectInventoryUtils._get_inventory(game_object)
        if inventory_component is None:
            return
        inventory_component.open_ui_panel()

    @staticmethod
    def set_ownership_of_all_items_in_object_inventory_to_sim(game_object: GameObject, sim_info: SimInfo) -> bool:
        """set_ownership_of_all_items_in_object_inventory_to_sim(game_object, sim_info)

        Change the ownership status of all items in the inventory of an Object to be owned by the household of a Sim.

        :param game_object: The objects in the inventory of this Object will become owned by the household of the Sim
        :type game_object: GameObject
        :param sim_info: The household of this Sim will be the new owner for all items in the inventory of the Object.
        :type sim_info: SimInfo
        :return: True, if ownership was transferred successfully. False, if not.
        :rtype: bool
        """
        if game_object is None or sim_info is None:
            return False
        inventory_component: ObjectInventoryComponent = CommonObjectInventoryUtils._get_inventory(game_object)
        if inventory_component is None:
            return False

        from sims4communitylib.utils.objects.common_object_ownership_utils import CommonObjectOwnershipUtils
        for inventory_object in inventory_component:
            CommonObjectOwnershipUtils.set_owning_sim(inventory_object, sim_info)
        return True

    @staticmethod
    def _get_inventory(game_object: GameObject) -> Union[ObjectInventoryComponent, None]:
        return CommonComponentUtils.get_component(game_object, CommonComponentType.INVENTORY)
