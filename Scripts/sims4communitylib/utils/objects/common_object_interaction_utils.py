"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Iterator
from interactions.base.interaction import Interaction
from objects.script_object import ScriptObject


class CommonObjectInteractionUtils:
    """Utilities for manipulating the interactions of Objects.

    """

    @staticmethod
    def get_all_interactions_registered_to_object_gen(script_object: ScriptObject, include_interaction_callback: Callable[[Interaction], bool]=None) -> Iterator[Interaction]:
        """get_all_interactions_registered_to_object_gen(script_object, include_interaction_callback=None)

        Retrieve all interactions that are registered to an object.

        :param script_object: An instance of a ScriptObject
        :type script_object: ScriptObject
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All sims will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterable of Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        if script_object is None or not hasattr(script_object, '_super_affordances') or not script_object._super_affordances:
            return tuple()
        for interaction in script_object._super_affordances:
            interaction: Interaction = interaction
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction
