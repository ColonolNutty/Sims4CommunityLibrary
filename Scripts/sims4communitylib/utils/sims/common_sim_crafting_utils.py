"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from random import Random
from typing import Union, Callable

from objects.game_object import GameObject
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_object_quality import CommonObjectQuality
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimCraftingUtils:
    """ Utilities for crafting various things. """
    @staticmethod
    def create_from_recipe(
        crafting_sim_info: SimInfo,
        recipe_id: int,
        inventory_target: Union[GameObject, Sim] = None,
        set_target_as_owner: bool = True,
        quality: CommonObjectQuality = None,
        owning_household_id_override: int = None,
        post_add: Callable[[GameObject], None] = None,
        seeded_random: Random = None
    ) -> Union[GameObject, None]:
        """create_from_recipe(\
            crafting_sim_info,\
            recipe_id,\
            inventory_target=None,\
            set_target_as_owner=True,\
            owning_household_id_override=None,\
            post_add=None,\
            seeded_random=None,\
        )

        Craft an item made by a Sim using a recipe and placing it in the inventory of an object or a Sim.

        .. note:: inventory_target must have an inventory_component attribute.

        :param crafting_sim_info: The name of this Sim will appear on the crafted object as being the crafter.
        :type crafting_sim_info: SimInfo
        :param recipe_id: The decimal identifier of a recipe for the object being created.
        :type recipe_id: int
        :param inventory_target: If set, the crafted object will be placed in the inventory of this object. If not set, the crafted object will be placed in the inventory of the Sim that crafted it. Default is None.
        :type inventory_target: Union[GameObject, Sim]
        :param set_target_as_owner: If True, the inventory where the crafted item will be placed will become the owner of the crafted item. If False, the crafted item will be owned by the one who created it. Default is True.
        :type set_target_as_owner: bool, optional
        :param owning_household_id_override: An override for which household to set as the owner of the crafted object. If not specified, then the crafting Sim will be the owner. If set_target_as_owner is True, then the target will be the owner regardless of what this argument is set to. Default is None.
        :type owning_household_id_override: int, optional
        :param post_add: A callback invoked when the object is created. Default is None.
        :type post_add: Callable[[GameObject], None], optional
        :param seeded_random: An instance of Random that will be used in various aspects of the created object. Default is None.
        :type seeded_random: Random, optional
        :param quality: The quality of the output object. Default is None.
        :type quality: CommonObjectQuality, optional
        :return: The crafted item, created from the specified recipe by the specified Sim, or None if an error occurs.
        :rtype: Union[GameObject, None]
        """
        if inventory_target is not None and not hasattr(inventory_target, 'inventory_component'):
            raise AttributeError('The specified inventory_target did not have an inventory component.')
        crafting_sim = CommonSimUtils.get_sim_instance(crafting_sim_info)
        if crafting_sim is None:
            return None
        from sims4communitylib.utils.resources.common_recipe_utils import CommonRecipeUtils
        recipe = CommonRecipeUtils.load_recipe_by_guid(recipe_id)
        try:
            from crafting.crafting_interactions import create_craftable
            from sims4communitylib.utils.objects.common_object_ownership_utils import CommonObjectOwnershipUtils
            from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
            quality_state = CommonObjectStateUtils.convert_quality_to_object_state_value(quality)
            if set_target_as_owner:
                if CommonTypeUtils.is_sim_or_sim_info(inventory_target):
                    owning_sim_info = CommonSimUtils.get_sim_info(inventory_target) if inventory_target is not None else crafting_sim_info
                    owning_household_id_override = CommonHouseholdUtils.get_household_id(owning_sim_info)
                elif inventory_target is not None:
                    owning_household_id_override = CommonObjectOwnershipUtils.get_owning_household_id(inventory_target)
            crafted_item = create_craftable(
                recipe,
                crafting_sim,
                inventory_owner=inventory_target,
                place_in_inventory=True,
                quality=quality_state,
                owning_household_id_override=owning_household_id_override,
                post_add=post_add,
                seeded_random=seeded_random
            )
            if crafted_item is not None:
                if set_target_as_owner:
                    if CommonTypeUtils.is_sim_or_sim_info(inventory_target):
                        owning_sim_info = CommonSimUtils.get_sim_info(inventory_target) if inventory_target is not None else crafting_sim_info
                        CommonObjectOwnershipUtils.set_owning_sim(crafted_item, owning_sim_info)
                    elif inventory_target is not None:
                        owning_household_id = CommonObjectOwnershipUtils.get_owning_household_id(inventory_target)
                        CommonObjectOwnershipUtils.set_owning_household_id(crafted_item, owning_household_id)
            return crafted_item
        except ImportError:
            return None
