"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Iterator, Union, Tuple

from crafting.recipe import Recipe
from interactions.base.create_object_interaction import ObjectDefinition
from objects.components.sim_inventory_component import SimInventoryComponent
from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.resources.common_recipe_utils import CommonRecipeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimInventoryUtils(_HasS4CLClassLog):
    """ Utilities for manipulating the inventory of Sims. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_sim_inventory_utils'

    @classmethod
    def has_inventory(cls, sim_info: SimInfo) -> bool:
        """has_inventory(sim_info)

        Determine if a Sim has an inventory.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has an inventory. False, if not.
        :rtype: bool
        """
        return cls.get_inventory(sim_info) is not None

    @classmethod
    def get_inventory(cls, sim_info: SimInfo) -> Union[SimInventoryComponent, None]:
        """get_inventory(sim_info)

        Retrieve the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The inventory component of the Sim or None if not found.
        :rtype: Union[SimInventoryComponent, None]
        """
        return cls._get_inventory(sim_info)

    @classmethod
    def get_objects_in_inventory_by_definition_ids_gen(cls, sim_info: SimInfo, object_definition_ids: Tuple[int, ...], include_object_callback: Callable[[GameObject], bool] = None) -> Iterator[GameObject]:
        """get_objects_in_inventory_by_definition_id_gen(sim_info, object_definition_ids, include_object_callback=None)

        Retrieve all Objects in the inventory of a Sim that match the definition ids.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_definition_ids: The Definition IDs of the objects to locate.
        :type object_definition_ids: Tuple[int]
        :param include_object_callback: If the result of this callback is True, the object will be included in the results. If set to None, All objects in the inventory will be included.
        :type include_object_callback: Callable[[int], bool], optional
        :return: An iterator containing the decimal identifiers for the objects in the inventory of a Sim.
        :rtype: Iterator[GameObject]
        """
        log = cls.get_log()
        log.format_with_message('Getting objects in inventory', sim=sim_info, object_definition_ids=object_definition_ids)
        for game_object in cls.get_all_objects_in_inventory_gen(sim_info, include_object_callback=include_object_callback):
            definition_id = CommonObjectUtils.get_object_definition_id(game_object)
            log.format_with_message('Got definition id.', definition_id=definition_id, game_object=game_object)
            if definition_id in object_definition_ids:
                log.format_with_message('Definition found in objects.', definition_id=definition_id)
                yield game_object
            else:
                log.format_with_message('Definition not found.', definition_id=definition_id)

    @classmethod
    def get_objects_in_inventory_by_definition_id_gen(cls, sim_info: SimInfo, object_definition_id: int, include_object_callback: Callable[[GameObject], bool] = None) -> Iterator[GameObject]:
        """get_objects_in_inventory_by_definition_id_gen(sim_info, object_definition_id, include_object_callback=None)

        Retrieve all Objects in the inventory of a Sim that match the definition id.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_definition_id: The Definition ID of the objects to locate.
        :type object_definition_id: int
        :param include_object_callback: If the result of this callback is True, the object will be included in the results. If set to None, All objects in the inventory will be included.
        :type include_object_callback: Callable[[int], bool], optional
        :return: An iterator containing the decimal identifiers for the objects in the inventory of a Sim.
        :rtype: Iterator[GameObject]
        """
        yield from cls.get_objects_in_inventory_by_definition_ids_gen(sim_info, (object_definition_id,), include_object_callback=include_object_callback)

    @classmethod
    def get_all_objects_in_inventory_gen(cls, sim_info: SimInfo, include_object_callback: Callable[[GameObject], bool] = None) -> Iterator[GameObject]:
        """get_all_objects_in_inventory_gen(sim_info, include_object_callback=None)

        Retrieve all Objects in the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_object_callback: If the result of this callback is True, the object will be included in the results. If set to None, All objects in the inventory will be included.
        :type include_object_callback: Callable[[int], bool], optional
        :return: An iterator containing the decimal identifiers for the objects in the inventory of a Sim.
        :rtype: Iterator[GameObject]
        """
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return tuple()
        if include_object_callback is None:
            for inventory_object in inventory_component:
                yield inventory_object
        else:
            for inventory_object in inventory_component:
                if include_object_callback(inventory_object):
                    yield inventory_object

    @classmethod
    def add_to_inventory(cls, sim_info: SimInfo, object_definition_id: int, count: int = 1, on_added: Callable[[GameObject], None] = CommonFunctionUtils.noop) -> CommonExecutionResult:
        """add_to_inventory(sim_info, object_definition_id, count=1, on_added=CommonFunctionUtils.noop)

        Add a number of Newly Created Objects to the Inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_definition_id: The decimal identifier of an Object.
        :type object_definition_id: int
        :param count: The number of the specified Object to add. Default is 1.
        :type count: int, optional
        :param on_added: A callback invoked when the object is added to the inventory.
        :type on_added: Callable[[GameObject], None]
        :return: True, if the count of the specified Object were added successfully. False, it not.
        :rtype: CommonExecutionResult
        """
        if not CommonSimInventoryUtils.has_inventory(sim_info):
            return CommonExecutionResult(False, reason=f'{sim_info} has no inventory.', tooltip_text=CommonStringId.S4CL_SIM_HAS_NO_INVENTORY, tooltip_tokens=(sim_info,))

        def _post_create(_game_object: GameObject) -> bool:
            move_result = CommonSimInventoryUtils.move_object_to_inventory(sim_info, _game_object)
            on_added(_game_object)
            return move_result

        success = CommonExecutionResult.TRUE
        count = int(count)
        for _ in range(count):
            game_object = CommonObjectSpawnUtils.spawn_object_on_lot(object_definition_id, CommonLocation.empty(), post_object_spawned_callback=_post_create)
            if game_object is None:
                success = CommonExecutionResult(False, reason=f'Failed to create object with definition id {object_definition_id}', tooltip_text=CommonStringId.S4CL_FAILED_TO_CREATE_OBJECT_BY_DEFINITION_ID, tooltip_tokens=(str(object_definition_id),))
        return success

    @classmethod
    def remove_from_inventory(cls, sim_info: SimInfo, object_id: int, count: int = 1) -> bool:
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
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return False
        return inventory_component.try_remove_object_by_id(object_id, count=count)

    @classmethod
    def remove_from_inventory_by_definition(cls, sim_info: SimInfo, object_definition: ObjectDefinition, count: int = 1) -> bool:
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

    @classmethod
    def move_object_to_inventory(cls, sim_info: SimInfo, game_object: GameObject) -> bool:
        """move_object_to_inventory(sim_info, game_object)

        Move an Object to the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the object was successfully moved to the inventory of the specified Sim. False, if not.
        :rtype: bool
        """
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return False
        from sims4communitylib.utils.objects.common_object_ownership_utils import CommonObjectOwnershipUtils
        CommonObjectOwnershipUtils.set_owning_sim(game_object, sim_info)
        return inventory_component.player_try_add_object(game_object)

    @classmethod
    def move_objects_to_inventory(cls, sim_info: SimInfo, game_objects: Tuple[GameObject]) -> bool:
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

    @classmethod
    def get_count_of_object_in_inventory(cls, sim_info: SimInfo, object_id: int) -> int:
        """get_count_of_object_in_inventory(sim_info, object_id)

        Count the number of an Object in the inventory of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param object_id: The decimal identifier of an object.
        :type object_id: int
        :return: The number of the specified Object in the inventory of the specified Sim.
        :type: int
        """
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return 0
        object_definition = CommonObjectUtils.get_object_definition(object_id)
        return inventory_component.get_count(object_definition)

    @classmethod
    def make_inventory_visible(cls, sim_info: SimInfo) -> bool:
        """make_inventory_visible(sim_info)

        Change the flags of the inventory of a Sim so that it becomes visible to the player.

        .. note:: A Sim needs to be Instances in order to have an inventory to make visible.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the inventory of the specified Sim was made visible. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return False
        if inventory_component.visible_storage is None:
            return False
        inventory_component.visible_storage.allow_ui = True
        inventory_component.publish_inventory_items()
        sim.ui_manager.refresh_ui_data()
        return True

    @classmethod
    def make_inventory_hidden(cls, sim_info: SimInfo) -> bool:
        """make_inventory_hidden(sim_info)

        Change the flags of the inventory of a Sim so that it becomes hidden to the player.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the inventory of the specified Sim was made hidden. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return True
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return True
        if inventory_component.visible_storage is None:
            return True
        inventory_component.visible_storage.allow_ui = False
        inventory_component.publish_inventory_items()
        sim.ui_manager.refresh_ui_data()
        return True

    @classmethod
    def open_inventory(cls, sim_info: SimInfo) -> None:
        """open_inventory(sim_info)

        Open the inventory of a Sim.

        :param sim_info: The Sim to open the inventory of.
        :type sim_info: SimInfo
        """
        if sim_info is None:
            return
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info)
        if inventory_component is None:
            return
        if not CommonSimInventoryUtils.make_inventory_visible(sim_info):
            return
        inventory_component.open_ui_panel()

    @classmethod
    def set_ownership_of_all_items_in_sim_inventory_to_sim(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """set_ownership_of_all_items_in_sim_inventory_to_sim(sim_info_a, sim_info_b)

        Change the ownership status of all items in the inventory of Sim A to be owned by the household of Sim B

        :param sim_info_a: The objects in the inventory of this Sim will become owned by the household of Sim B
        :type sim_info_a: SimInfo
        :param sim_info_b: The household of this Sim will be the new owner for all items in the inventory of Sim A.
        :type sim_info_b: SimInfo
        :return: True, if ownership was transferred successfully. False, if not.
        :rtype: bool
        """
        if sim_info_a is None or sim_info_b is None:
            return False
        if not CommonSimInventoryUtils.make_inventory_visible(sim_info_a):
            return False
        inventory_component: SimInventoryComponent = cls.get_inventory(sim_info_a)
        if inventory_component is None:
            return False
        from sims4communitylib.utils.objects.common_object_ownership_utils import CommonObjectOwnershipUtils
        for inventory_object in inventory_component:
            inventory_object: GameObject = inventory_object
            CommonObjectOwnershipUtils.set_owning_sim(inventory_object, sim_info_b)
        return True

    @classmethod
    def _get_inventory(cls, sim_info: SimInfo) -> Union[SimInventoryComponent, None]:
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return CommonComponentUtils.get_component(sim, CommonComponentType.INVENTORY)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_object_to_inventory',
    'Add an Object to the inventory of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('object_definition_id', 'Decimal Identifier', 'The decimal identifier of the Object Definition for the object to add.'),
        CommonConsoleCommandArgument('count', 'Positive Number', 'The number of objects to add.', is_optional=True, default_value=1),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to add the object to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.addtosim',
    )
)
def _s4clib_testing_add_object_to_inventory(output: CommonConsoleCommandOutput, object_definition_id: int, count: int = 1, sim_info: SimInfo = None):
    if object_definition_id < 0:
        output('ERROR: Object Definition Id must be a positive number.')
        return
    if count <= 0:
        output('ERROR: count must be greater than zero.')
        return
    output(f'Attempting to add object with definition id \'{object_definition_id}\' to the inventory of Sim {sim_info}.')
    if CommonSimInventoryUtils.add_to_inventory(sim_info, object_definition_id, count):
        output(f'SUCCESS: Successfully added object with definition id {object_definition_id} to Sim {sim_info}')
    else:
        output(f'FAILED: Failed to add object with definition id {object_definition_id} to Sim {sim_info}')
    output('Done adding object to the inventory of the Sim.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_servo_ingredients',
    'Add the ingredients needed to craft a Servo to the inventory of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to add the ingredients to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.give_servo_ingredients',
    )
)
def _s4clib_testing_add_servo_ingredients(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    servo_recipe_id = 221691  # recipe_RoboticsTable_HumanoidRobot
    recipe = CommonRecipeUtils.load_recipe_by_guid(servo_recipe_id)
    if recipe is None:
        output('No recipe found for Servos.')
        return
    output(f'Adding ingredients required to make a Servo to inventory of {sim_info}')
    ingredients_list = recipe.use_ingredients.ingredient_list

    for ingredient_factory in ingredients_list:
        ingredient_requirement = ingredient_factory()
        if not hasattr(ingredient_requirement, '_definition'):
            continue
        number_required = ingredient_requirement.count_required
        ingredient_definition = ingredient_requirement.get_definition()
        ingredient_definition_id = ingredient_definition.id
        CommonSimInventoryUtils.add_to_inventory(sim_info, ingredient_definition_id, number_required)
    output('Done adding object to the inventory of the Sim.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.give_ingredients_for_recipe',
    'Add ingredients for a recipe. (Only works with recipes that do not use tags!)',
    command_arguments=(
        CommonConsoleCommandArgument('recipe', 'Decimal Identifier', 'The decimal identifier of the Recipe for the ingredients to add.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to add the ingredients to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.give_ingredients',
    )
)
def _s4clib_testing_add_object_to_inventory(output: CommonConsoleCommandOutput, recipe: Recipe, sim_info: SimInfo = None):
    if recipe is None or not isinstance(recipe, Recipe):
        output(f'No recipe found for {recipe}.')
        return
    output(f'Adding ingredients required to make a {recipe} to inventory of {sim_info}')
    ingredients_list = recipe.use_ingredients.ingredient_list

    for ingredient_factory in ingredients_list:
        ingredient_requirement = ingredient_factory()
        if not hasattr(ingredient_requirement, '_definition'):
            continue
        number_required = ingredient_requirement.count_required
        ingredient_definition = ingredient_requirement.get_definition()
        ingredient_definition_id = ingredient_definition.id
        CommonSimInventoryUtils.add_to_inventory(sim_info, ingredient_definition_id, number_required)
    output('Done adding object to the inventory of the Sim.')
