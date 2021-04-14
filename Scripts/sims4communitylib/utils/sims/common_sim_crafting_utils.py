"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.game_object import GameObject
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimCraftingUtils:
    """ Utilities for crafting various things. """
    @staticmethod
    def create_from_recipe(crafting_sim_info: SimInfo, recipe_id: int, inventory_target: Union[GameObject, Sim]=None) -> Union[GameObject, None]:
        """create_from_recipe(crafting_sim_info, recipe_id, inventory_target=None)

        Craft an item made by a Sim using a recipe and placing it in the inventory of an object or a Sim.

        .. note:: inventory_target must have an inventory_component attribute.

        :param crafting_sim_info: The name of this Sim will appear on the crafted object as being the crafter.
        :type crafting_sim_info: SimInfo
        :param recipe_id: The decimal identifier of a recipe for the object being created.
        :type recipe_id: int
        :param inventory_target: If set, the crafted object will be placed in the inventory of this object. If not set, the crafted object will be placed in the inventory of the Sim that crafted it. Default is None.
        :type inventory_target: Union[GameObject, Sim]
        :return: The crafted item, created from the specified recipe by the specified Sim, or None if an error occurs.
        :rtype: Union[GameObject, None]
        """
        if inventory_target is not None and not hasattr(inventory_target, 'inventory_component'):
            raise AttributeError('The specified inventory_target did not have an inventory component.')
        crafting_sim = CommonSimUtils.get_sim_instance(crafting_sim_info)
        if crafting_sim is None:
            return None
        recipe = CommonResourceUtils.load_instance(Types.RECIPE, recipe_id)
        try:
            from crafting.crafting_interactions import create_craftable
            crafted_item = create_craftable(recipe, crafting_sim, inventory_owner=inventory_target, place_in_inventory=True)
            return crafted_item
        except ImportError:
            return None
