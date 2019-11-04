"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Tuple, Iterator
from interactions.base.interaction import Interaction
from objects.script_object import ScriptObject
from services.terrain_service import TerrainService
from sims4.resources import Types
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonInteractionType(CommonEnumIntBase):
    """ The type of object/area to add interactions to. """
    ON_TERRAIN_LOAD = 0
    ON_OCEAN_LOAD = 1
    ON_SCRIPT_OBJECT_LOAD = 2


class CommonInteractionHandler:
    """ An interaction handler that adds interactions to script objects, the terrain, or the ocean. """
    @property
    def interactions_to_add(self) -> Tuple[int]:
        """
            A tuple of interaction identifiers being added by the interaction handler.
        """
        raise NotImplementedError()

    def _interactions_to_add_gen(self) -> Iterator[Interaction]:
        affordance_manager = services.get_instance_manager(Types.INTERACTION)
        for affordance_id in self.interactions_to_add:
            affordance_instance = affordance_manager.get(affordance_id)
            if affordance_instance is None:
                continue
            yield affordance_instance


class CommonScriptObjectInteractionHandler(CommonInteractionHandler):
    """ An interaction handler that handles script objects, use this instead of the base class when you are adding interactions to script objects. """
    @property
    def interactions_to_add(self) -> Tuple[int]:
        """
            A tuple of interaction identifiers being added by the interaction handler to the script object.
        """
        raise NotImplementedError()

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        """
            Determine whether to add the interactions of this handler to the script object.
        :param script_object: An object of type ScriptObject
        """
        raise NotImplementedError()


class CommonInteractionRegistry(CommonService):
    """ A registry used to register interactions to specific places, whether they are script objects, terrain, or what have you. """
    def __init__(self):
        self._interaction_handlers = {
            CommonInteractionType.ON_TERRAIN_LOAD: [],
            CommonInteractionType.ON_OCEAN_LOAD: [],
            CommonInteractionType.ON_SCRIPT_OBJECT_LOAD: []
        }

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def on_script_object_add(self, script_object: ScriptObject, *args, **kwargs):
        """
            Occurs upon a script object being added.
        :param script_object: The script object being added.
        """
        new_super_affordances = []
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_SCRIPT_OBJECT_LOAD]:
            if hasattr(interaction_handler, 'should_add') and not interaction_handler.should_add(script_object, *args, **kwargs):
                continue
            if not hasattr(script_object, '_super_affordances'):
                continue
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances:
                    continue
                new_super_affordances.append(interaction_instance)
        script_object._super_affordances += tuple(new_super_affordances)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def on_terrain_load(self, terrain_service: TerrainService, *_, **__):
        """
            Occurs upon the terrain loading
        """
        new_super_affordances = []
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_TERRAIN_LOAD]:
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances:
                    continue
                new_super_affordances.append(interaction_instance)
        new_terrain_class = terrain_service.TERRAIN_DEFINITION.cls
        new_terrain_class._super_affordances += tuple(new_super_affordances)
        terrain_service.TERRAIN_DEFINITION.set_class(new_terrain_class)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def on_ocean_load(self, terrain_service: TerrainService, *_, **__):
        """
            Occurs upon the ocean loading
        """
        new_super_affordances = []
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_OCEAN_LOAD]:
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances:
                    continue
                new_super_affordances.append(interaction_instance)
        new_terrain_class = terrain_service.OCEAN_DEFINITION.cls
        new_terrain_class._super_affordances += tuple(new_super_affordances)
        terrain_service.OCEAN_DEFINITION.set_class(new_terrain_class)

    def register_handler(self, handler: CommonInteractionHandler, interaction_type: CommonInteractionType):
        """
            Add an interaction handler to register interactions in specific places.
        :param handler: The interaction handler being registered.
        :param interaction_type: The type of places the interactions will show up.
        """
        self._interaction_handlers[interaction_type].append(handler)

    @staticmethod
    def register_interaction_handler(interaction_type: CommonInteractionType):
        """
            A decorator for registering interaction handlers.
        :param interaction_type: The type of places the interactions will show up.
        :return: A wrapped function.
        """
        def _wrapper(interaction_handler):
            CommonInteractionRegistry.get().register_handler(interaction_handler(), interaction_type)
            return interaction_handler
        return _wrapper


@CommonInjectionUtils.inject_into(ScriptObject, ScriptObject.on_add.__name__)
def _common_script_object_on_add(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry.get().on_script_object_add(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_into(TerrainService, TerrainService.start.__name__)
def _common_terrain_service_start(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry.get().on_terrain_load(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_into(TerrainService, TerrainService.on_zone_load.__name__)
def _common_terrain_service_on_zone_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry.get().on_ocean_load(self, *args, **kwargs)
    return result


# noinspection PyMissingOrEmptyDocstring
# @CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class ExampleInteractionHandler(CommonScriptObjectInteractionHandler):
    @property
    def interactions_to_add(self) -> Tuple[int]:
        # Interaction Ids
        # These are the decimal identifiers of the interactions from a package file.
        from sims4communitylib.enums.interactions_enum import CommonInteractionId
        return tuple([int(CommonInteractionId.SIM_CHAT), 2])

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        # Verify it is the object your are expecting. Return True, if it is.
        # In this case we are adding these interactions to Sims.
        from sims.sim import Sim
        return isinstance(script_object, Sim)
