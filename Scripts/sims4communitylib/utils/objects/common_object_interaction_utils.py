"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Iterator
from interactions.base.interaction import Interaction
from objects.script_object import ScriptObject
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils


class CommonObjectInteractionUtils(HasClassLog):
    """Utilities for manipulating the interactions of Objects.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_object_interaction_utils'

    @staticmethod
    def get_all_interactions_registered_to_object_gen(script_object: ScriptObject, include_interaction_callback: Callable[[Interaction], bool]=None) -> Iterator[Interaction]:
        """get_all_interactions_registered_to_object_gen(script_object, include_interaction_callback=None)

        Retrieve all interactions that are registered to an object.

        :param script_object: An instance of a ScriptObject
        :type script_object: ScriptObject
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All Interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterable of Interactions that pass the include callback filter.
        :rtype: Iterator[Interaction]
        """
        if script_object is None or not hasattr(script_object, '_super_affordances') or not script_object._super_affordances:
            return tuple()
        interactions = (
            *script_object._super_affordances,
        )
        if hasattr(script_object, '_phone_affordances'):
            interactions = (
                *interactions,
                *script_object._phone_affordances
            )
        if hasattr(script_object, '_relation_panel_affordances'):
            interactions = (
                *interactions,
                *script_object._relation_panel_affordances
            )
        for interaction in interactions:
            interaction: Interaction = interaction
            if include_interaction_callback is not None and not include_interaction_callback(interaction):
                continue
            yield interaction

    @classmethod
    def add_super_interaction_to_object(cls, script_object: ScriptObject, interaction_guid: int):
        """add_super_interaction_to_object(script_object, interaction_guid)

        Add a super interaction to an object.

        :param script_object: The object to add the interaction to.
        :type script_object: ScriptObject
        :param interaction_guid: The GUID of the interaction to add.
        :type interaction_guid: int
        """
        return cls.add_super_interactions_to_object(script_object, (interaction_guid,))

    @classmethod
    def add_super_interactions_to_object(cls, script_object: ScriptObject, interaction_guids: Iterator[int]):
        """add_super_interactions_to_object(script_object, interaction_guids)

        Add super interactions to an object.

        :param script_object: The object to add the interaction to.
        :type script_object: ScriptObject
        :param interaction_guids: The GUIDs of the interactions to add.
        :type interaction_guids: Iterator[int]
        """
        script_object_type = type(script_object)
        cls.get_log().format_with_message('Adding interactions for type', script_object_type=script_object_type)
        if not hasattr(script_object_type, '_super_affordances'):
            cls.get_verbose_log().format_with_message('Object did not have super affordances.', script_object=script_object_type)
            return
        super_interactions_to_add = list()
        affordance_manager = CommonInteractionUtils.get_instance_manager()
        for affordance_id in interaction_guids:
            affordance_instance = affordance_manager.get(affordance_id)
            if affordance_instance is None:
                continue
            super_interactions_to_add.append(affordance_instance)

        new_super_affordances = list()
        for super_interaction_instance in super_interactions_to_add:
            if super_interaction_instance in new_super_affordances or super_interaction_instance in script_object_type._super_affordances:
                cls.get_verbose_log().format_with_message('Interaction was already found in the interactions list.', script_object_type=script_object_type, interaction_instance=super_interaction_instance)
                continue
            new_super_affordances.append(super_interaction_instance)
        if new_super_affordances:
            cls.get_log().format_with_message('Adding super affordances to object.', script_object=script_object, script_object_type=script_object_type, new_super_affordances=new_super_affordances)
            script_object_type._super_affordances += tuple(new_super_affordances)
        else:
            cls.get_log().format_with_message('No super affordances to add.', script_object=script_object, script_object_type=script_object_type, new_super_affordances=new_super_affordances)

        new_script_object_super_affordances = list()
        for new_super_affordance in super_interactions_to_add:
            if new_super_affordance in script_object._super_affordances:
                continue
            new_script_object_super_affordances.append(new_super_affordance)
        if new_script_object_super_affordances:
            script_object._super_affordances += tuple(new_script_object_super_affordances)

    @classmethod
    def remove_super_interaction_from_object(cls, script_object: ScriptObject, interaction_guid: int):
        """remove_super_interaction_from_object(script_object, interaction_guid)

        Remove a super interaction from an object.

        :param script_object: The object to remove the interaction from.
        :type script_object: ScriptObject
        :param interaction_guid: The GUID of the interaction to remove.
        :type interaction_guid: int
        """
        return cls.remove_super_interactions_from_object(script_object, (interaction_guid,))

    @classmethod
    def remove_super_interactions_from_object(cls, script_object: ScriptObject, interaction_guids: Iterator[int]):
        """remove_super_interactions_from_object(script_object, interaction_guids)

        Remove a super interaction from an object.

        :param script_object: The object to remove the interaction from.
        :type script_object: ScriptObject
        :param interaction_guids: The GUIDs of the interactions to remove.
        :type interaction_guids: Iterator[int]
        """
        script_object_type = type(script_object)
        cls.get_log().format_with_message('Removing interactions for type', script_object_type=script_object_type)
        if not hasattr(script_object_type, '_super_affordances'):
            cls.get_verbose_log().format_with_message('Object did not have super affordances.', script_object=script_object_type)
            return
        new_super_affordances = list(script_object_type._super_affordances)
        current_super_affordances_list = list(script_object_type._super_affordances)
        for super_interaction in current_super_affordances_list:
            super_interaction_id = CommonInteractionUtils.get_interaction_id(super_interaction)
            if super_interaction_id in interaction_guids:
                continue
            new_super_affordances.remove(super_interaction)
        script_object_type._super_affordances = tuple(new_super_affordances)

        new_object_super_affordances = list(script_object._super_affordances)
        current_object_super_affordances_list = list(script_object._super_affordances)
        for obj_super_interaction in current_object_super_affordances_list:
            obj_super_interaction_id = CommonInteractionUtils.get_interaction_id(obj_super_interaction)
            if obj_super_interaction_id in interaction_guids:
                continue
            new_object_super_affordances.remove(obj_super_interaction)
        script_object._super_affordances = tuple(new_object_super_affordances)
