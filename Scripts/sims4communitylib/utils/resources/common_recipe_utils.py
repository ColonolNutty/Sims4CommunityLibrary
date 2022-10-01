"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from crafting.recipe import Recipe
from typing import Callable, Iterator, Union, Tuple, List

from sims4.resources import Types
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog


class CommonRecipeUtils(_HasS4CLClassLog):
    """Utilities for manipulating Recipes in various ways.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_recipe_utils'

    @staticmethod
    def get_recipe_guid(recipe_identifier: Union[int, Recipe]) -> Union[int, None]:
        """get_recipe_guid(recipe_identifier)

        Retrieve the GUID of a Recipe.

        :param recipe_identifier: The identifier or instance of a Recipe.
        :type recipe_identifier: Union[int, Recipe]
        :return: The decimal identifier of the Recipe or None if the Recipe does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(recipe_identifier, int):
            return recipe_identifier
        return getattr(recipe_identifier, 'guid64', None)

    @staticmethod
    def get_short_name(recipe: Recipe) -> Union[str, None]:
        """get_short_name(recipe)

        Retrieve the Short Name of a Recipe.

        :param recipe: An instance of a Recipe.
        :type recipe: Recipe
        :return: The short name of a Recipe or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if recipe is None:
            return None
        # noinspection PyBroadException
        try:
            return recipe.__class__.__name__
        except:
            return ''

    @staticmethod
    def get_short_names(recipes: Iterator[Recipe]) -> Tuple[str]:
        """get_short_names(recipes)

        Retrieve the Short Names of a collection of Recipes.

        :param recipes: A collection of Recipe instances.
        :type recipes: Iterator[Recipe]
        :return: A collection of short names of all Recipe instances.
        :rtype: Tuple[str]
        """
        if recipes is None or not recipes:
            return tuple()
        short_names: List[str] = []
        for recipe in recipes:
            # noinspection PyBroadException
            try:
                short_name = CommonRecipeUtils.get_short_name(recipe)
                if not short_name:
                    continue
            except:
                continue
            short_names.append(short_name)
        return tuple(short_names)

    @staticmethod
    def get_all_recipes_gen(include_recipe_callback: Callable[[Recipe], bool] = None) -> Iterator[Recipe]:
        """get_all_recipes_gen(include_recipe_callback=None)

        Retrieve all Recipes.

        :param include_recipe_callback: If the result of this callback is True, the Recipe will be included in the results. If set to None, All Recipes will be included.
        :type include_recipe_callback: Callable[[Recipe], bool], optional
        :return: An iterator of Recipes that pass the specified include_recipe_callback.
        :rtype: Iterator[Recipe]
        """
        from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
        statistic_manager = CommonStatisticUtils.get_statistic_instance_manager()
        for recipe in statistic_manager.get_ordered_types(only_subclasses_of=Recipe):
            recipe: Recipe = recipe
            recipe_id = CommonRecipeUtils.get_recipe_guid(recipe)
            if recipe_id is None:
                continue
            if include_recipe_callback is not None and not include_recipe_callback(recipe):
                continue
            yield recipe

    @staticmethod
    def load_recipe_by_guid(value_id: Union[int, Recipe]) -> Union[Recipe, None]:
        """load_recipe_by_guid(recipe_id)

        Load an instance of a Recipe by a GUID.

        :param value_id: The GUID of a Recipe.
        :type value_id: Union[int, Recipe]
        :return: An instance of a Recipe matching the decimal identifier or None if not found.
        :rtype: Union[Recipe, None]
        """
        if isinstance(value_id, Recipe) or hasattr(value_id, 'is_recipe'):
            return value_id
        # noinspection PyBroadException
        try:
            value_id: int = int(value_id)
        except:
            # noinspection PyTypeChecker
            value_id: Recipe = value_id
            return value_id

        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.RECIPE, value_id)
