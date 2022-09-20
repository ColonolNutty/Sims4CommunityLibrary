"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Callable, Iterator, List, Union
from interactions.base.interaction import Interaction
from objects.game_object import GameObject
from objects.script_object import ScriptObject
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_utils import CommonLogUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


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
    def get_all_interactions_registered_to_object_gen(script_object: ScriptObject, include_interaction_callback: Callable[[Interaction], bool] = None) -> Iterator[Interaction]:
        """get_all_interactions_registered_to_object_gen(script_object, include_interaction_callback=None)

        Retrieve all interactions that are registered to an object.

        :param script_object: An instance of a ScriptObject
        :type script_object: ScriptObject
        :param include_interaction_callback: If the result of this callback is True, the Interaction will be included in the results. If set to None, All Interactions will be included. Default is None.
        :type include_interaction_callback: Callable[[Interaction], bool], optional
        :return: An iterator of Interactions that pass the include callback filter.
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
    def remove_super_interaction_from_terrain(cls, interaction_identifier: Union[int, Interaction]):
        """remove_super_interaction_from_terrain(interaction_identifier)

        Remove a super interaction from the terrain.

        :param interaction_identifier: The GUID or instance of the interaction to remove.
        :type interaction_identifier: Union[int, Interaction]
        """
        return cls.remove_super_interactions_from_terrain((interaction_identifier,))

    @classmethod
    def remove_super_interactions_from_terrain(cls, interaction_identifiers: Iterator[Union[int, Interaction]]):
        """remove_super_interactions_from_terrain(interaction_identifiers)

        Remove a super interaction from the terrain.

        :param interaction_identifiers: The GUIDs or instances of the interactions to remove.
        :type interaction_identifiers: Iterator[Union[int, Interaction]]
        """
        from services import get_terrain_service
        terrain_service = get_terrain_service()

        interactions_to_remove = list()
        for interaction_id in interaction_identifiers:
            interaction = CommonInteractionUtils.load_interaction_by_id(interaction_id)
            if interaction is not None:
                interactions_to_remove.append(interaction)

        if not interactions_to_remove:
            return None

        new_terrain_definition_class = terrain_service.TERRAIN_DEFINITION.cls
        new_super_affordances = list()
        current_super_affordances_list = list(new_terrain_definition_class._super_affordances)
        for super_interaction in current_super_affordances_list:
            if super_interaction in interactions_to_remove:
                continue
            new_super_affordances.append(super_interaction)
        new_terrain_definition_class._super_affordances = tuple(new_super_affordances)
        terrain_service.TERRAIN_DEFINITION.set_class(new_terrain_definition_class)

    @classmethod
    def remove_super_interaction_from_ocean(cls, interaction_identifier: Union[int, Interaction]):
        """remove_super_interaction_from_ocean(interaction_identifier)

        Remove a super interaction from the ocean.

        :param interaction_identifier: The GUID or instance of the interaction to remove.
        :type interaction_identifier: Union[int, Interaction]
        """
        return cls.remove_super_interactions_from_ocean((interaction_identifier,))

    @classmethod
    def remove_super_interactions_from_ocean(cls, interaction_identifiers: Iterator[Union[int, Interaction]]):
        """remove_super_interactions_from_ocean(interaction_identifiers)

        Remove a super interaction from the ocean.

        :param interaction_identifiers: The GUIDs of the interactions or instances to remove.
        :type interaction_identifiers: Iterator[Union[int, Interaction]]
        """
        from services import get_terrain_service
        terrain_service = get_terrain_service()

        interactions_to_remove = list()
        for interaction_guid in interaction_identifiers:
            interaction = CommonInteractionUtils.load_interaction_by_id(interaction_guid)
            if interaction is not None:
                interactions_to_remove.append(interaction)

        new_ocean_definition_class = terrain_service.OCEAN_DEFINITION.cls
        new_super_affordances = list()
        current_super_affordances_list = list(new_ocean_definition_class._super_affordances)
        for super_interaction in current_super_affordances_list:
            if super_interaction in interactions_to_remove:
                continue
            new_super_affordances.append(super_interaction)
        new_ocean_definition_class._super_affordances = tuple(new_super_affordances)
        terrain_service.OCEAN_DEFINITION.set_class(new_ocean_definition_class)

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
            if super_interaction_id not in interaction_guids:
                continue
            new_super_affordances.remove(super_interaction)
        script_object_type._super_affordances = tuple(new_super_affordances)

        new_object_super_affordances = list(script_object._super_affordances)
        current_object_super_affordances_list = list(script_object._super_affordances)
        for obj_super_interaction in current_object_super_affordances_list:
            obj_super_interaction_id = CommonInteractionUtils.get_interaction_id(obj_super_interaction)
            if obj_super_interaction_id not in interaction_guids:
                continue
            new_object_super_affordances.remove(obj_super_interaction)
        script_object._super_affordances = tuple(new_object_super_affordances)

    @classmethod
    def _log_all_interactions(cls, target_object: ScriptObject):
        log = cls.get_log()
        log.enable()
        object_id = CommonObjectUtils.get_object_id(target_object) if target_object is not None else -1
        definition_id = -1
        if CommonTypeUtils.is_sim_or_sim_info(target_object):
            # noinspection PyTypeChecker
            object_id = CommonSimUtils.get_sim_id(target_object)
        elif CommonTypeUtils.is_game_object(target_object):
            # noinspection PyTypeChecker
            definition = CommonObjectUtils.get_game_object_definition(target_object)
            if definition is not None:
                definition_id = definition.id
        log.debug(f'Interactions that can be performed on \'{target_object}\' id:{object_id} def_id:{definition_id}:')
        interactions = CommonObjectInteractionUtils.get_all_interactions_registered_to_object_gen(target_object)
        # noinspection PyTypeChecker
        target_object: GameObject = target_object
        interaction_short_names: List[str] = list()
        for interaction in interactions:
            interaction: Interaction = interaction
            try:
                interaction_short_name = CommonInteractionUtils.get_interaction_short_name(interaction)
                interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
                interaction_short_names.append(f'{interaction_short_name} ({interaction_id})')
            except Exception as ex:
                log.error('Problem while attempting to handle interaction {}'.format(pformat(interaction)), exception=ex)
                continue
        for component in target_object.components:
            if not hasattr(component, 'component_super_affordances_gen'):
                continue
            for affordance in component.component_super_affordances_gen():
                try:
                    interaction_short_name = CommonInteractionUtils.get_interaction_short_name(affordance)
                    interaction_id = CommonInteractionUtils.get_interaction_id(affordance)
                    interaction_short_names.append(f'{interaction_short_name} ({interaction_id})')
                except Exception as ex:
                    log.error(f'Problem while attempting to handle affordance {pformat(affordance)}', exception=ex)
                    continue

        sorted_short_names = sorted(interaction_short_names, key=lambda x: x)
        log.format(interactions=sorted_short_names)
        log.debug('Done Logging Available Interactions.')
        log.disable()
        CommonBasicNotification(
            CommonStringId.S4CL_LOG_ALL_INTERACTIONS,
            CommonStringId.S4CL_DONE_LOGGING_ALL_INTERACTIONS,
            description_tokens=(CommonLogUtils.get_message_file_path(cls.get_mod_identity()), )
        ).show()
        return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_object_interactions',
    'Log all interactions an object has.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Id', 'The instance id of the game object to check.'),
    )
)
def _s4clib_testing_print_all_interactions(output: CommonConsoleCommandOutput, game_object: GameObject):
    if game_object is None:
        return
    output(f'Logging interactions of {game_object}')
    CommonObjectInteractionUtils._log_all_interactions(game_object)
