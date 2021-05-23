"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Iterator, Union, Tuple, Any
from interactions.base.create_object_interaction import ObjectDefinition
from objects.components.sim_inventory_component import SimInventoryComponent
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimInventoryUtils:
    """ Utilities for manipulating the inventory of Sims. """
    @staticmethod
    def get_all_objects_in_inventory_gen(sim_info: SimInfo, include_object_callback: Callable[[GameObject], bool]=None) -> Iterator[GameObject]:
        """get_all_objects_in_inventory_gen(sim_info, include_object_callback=None)

        Retrieve all Objects in the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_object_callback: If the result of this callback is True, the object will be included in the results. If set to None, All objects in the inventory will be included.
        :type include_object_callback: Callable[[int], bool], optional
        :return: An iterator containing the decimal identifiers for the objects in the inventory of a Sim.
        :rtype: Iterator[GameObject]
        """
        inventory = CommonSimInventoryUtils._get_inventory(sim_info)
        if inventory is None:
            return tuple()
        inventory_objects = tuple(inventory)
        if not inventory_objects or include_object_callback is None:
            for inventory_object in inventory_objects:
                yield inventory_object
        else:
            for inventory_object in inventory_objects:
                if include_object_callback(inventory_object):
                    yield inventory_object

    @staticmethod
    def add_to_inventory(sim_info: SimInfo, object_id: int, count: int=1) -> bool:
        """add_to_inventory(sim_info, object_definition_id, count=1)

        Add a number of Newly Created Objects to the Inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_id: The decimal identifier of an Object.
        :type object_id: int
        :param count: The number of the specified Object to add. Default is 1.
        :type count: int, optional
        :return: True, if the count of the specified Object were added successfully. False, it not.
        :rtype: bool
        """
        inventory = CommonSimInventoryUtils._get_inventory(sim_info)
        if inventory is None:
            return False

        def _post_create(_game_object: GameObject) -> bool:
            return CommonSimInventoryUtils.move_object_to_inventory(sim_info, _game_object)

        success = True
        for _ in range(count):
            game_object = CommonObjectSpawnUtils.spawn_object_on_lot(object_id, CommonLocation.empty(), post_object_spawned_callback=_post_create)
            if game_object is None:
                success = False
        return success

    @staticmethod
    def remove_from_inventory(sim_info: SimInfo, object_id: int, count: int=1) -> bool:
        """remove_from_inventory(sim_info, object_id, count=1)

        Remove a number of Objects from the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_id: The decimal identifier of an Object.
        :type object_id: int
        :param count: The amount of the Object to remove. Default is 1.
        :type count: int, optional
        :return: True, if the count of the specified Object were removed successfully. False, if not.
        """
        inventory = CommonSimInventoryUtils._get_inventory(sim_info)
        if inventory is None:
            return False
        return inventory.try_remove_object_by_id(object_id, count=count)

    @staticmethod
    def remove_from_inventory_by_definition(sim_info: SimInfo, object_definition: ObjectDefinition, count: int=1) -> bool:
        """remove_from_inventory(sim_info, object_id, count=1)

        Remove a number of Objects from the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_definition: The definition of an Object.
        :type object_definition: ObjectDefinition
        :param count: The amount of the Object to remove. Default is 1.
        :type count: int, optional
        :return: True, if the count of the specified Object were removed successfully. False, if not.
        """
        def _include_object_callback(_game_object: GameObject) -> bool:
            return _game_object.definition == object_definition

        inventory_objects = CommonSimInventoryUtils.get_all_objects_in_inventory_gen(sim_info, include_object_callback=_include_object_callback)
        for inventory_object in inventory_objects:
            object_id = CommonObjectUtils.get_object_id(inventory_object)
            if CommonSimInventoryUtils.remove_from_inventory(sim_info, object_id, count=count):
                return True
        return False

    @staticmethod
    def move_object_to_inventory(sim_info: SimInfo, game_object: GameObject) -> bool:
        """move_object_to_inventory(sim_info, game_object)

        Move an Object to the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the object was successfully moved to the inventory of the specified Sim. False, if not.
        :rtype: bool
        """
        inventory = CommonSimInventoryUtils._get_inventory(sim_info)
        if inventory is None:
            return False
        game_object.update_ownership(sim_info, make_sim_owner=True)
        return inventory.player_try_add_object(game_object)

    @staticmethod
    def move_objects_to_inventory(sim_info: SimInfo, game_objects: Tuple[GameObject]) -> bool:
        """move_objects_to_inventory(sim_info, game_objects)

        Move Objects to the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param game_objects: A collection of Object instances.
        :type game_objects: GameObject
        :return: True, if all objects were successfully moved to the inventory of the specified Sim. False, if not.
        :rtype: bool
        """
        if not game_objects:
            return False
        successfully_moved_all = True
        for game_object in game_objects:
            if not CommonSimInventoryUtils.move_object_to_inventory(sim_info, game_object):
                successfully_moved_all = False
        return successfully_moved_all

    @staticmethod
    def get_count_of_object_in_inventory(sim_info: SimInfo, object_id: int) -> int:
        """get_count_of_object_in_inventory(sim_info, object_id)

        Count the number of an Object in the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_id: The decimal identifier of an object.
        :type object_id: int
        :return: The number of the specified Object in the inventory of the specified Sim.
        :type: int
        """
        inventory = CommonSimInventoryUtils._get_inventory(sim_info)
        if inventory is None:
            return 0
        object_definition = CommonObjectUtils.get_object_definition(object_id)
        return inventory.get_count(object_definition)

    @staticmethod
    def _get_inventory(sim_info: SimInfo) -> Union[SimInventoryComponent, None]:
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return CommonComponentUtils.get_component(sim, CommonComponentType.INVENTORY)


@Command('s4clib_testing.add_object_to_inventory', command_type=CommandType.Live)
def _s4clib_testing_add_object_to_inventory(object_id: str='20359', count: str='1', sim_id: str=None, _connection: Any=None):
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
    output = CheatOutput(_connection)
    # noinspection PyBroadException
    try:
        object_id = int(object_id)
    except Exception:
        output('ERROR: object_id must be a number.')
        return
    if object_id < 0:
        output('ERROR: object_id must be a positive number.')
        return
    # noinspection PyBroadException
    try:
        count = int(count)
    except Exception:
        output('ERROR: count must be a number.')
        return
    if count <= 0:
        output('ERROR: count must be greater than zero.')
        return
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    if sim_id is not None:
        # noinspection PyBroadException
        try:
            sim_id = int(sim_id)
        except Exception:
            output('ERROR: sim_id must be a number.')
            return
        sim_info = CommonSimUtils.get_sim_info(sim_id)
        if sim_info is None:
            output('ERROR: No sim found with id: {}'.format(sim_id))
            return
    else:
        sim_info = CommonSimUtils.get_active_sim_info()
    output('Attempting to add object with id \'{}\' to the inventory of Sim \'{}\'.'.format(object_id, CommonSimNameUtils.get_full_name(sim_info)))
    try:
        if CommonSimInventoryUtils.add_to_inventory(sim_info, object_id, count):
            output('Object added the object to the inventory of Sim {} successfully.'.format(CommonSimNameUtils.get_full_name(sim_info)))
    except Exception as ex:
        output('ERROR: A problem occurred while attempting to add the object.')
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred trying to add an object to the inventory of a Sim.', exception=ex)
    output('Done adding object to the inventory of the Sim.')
