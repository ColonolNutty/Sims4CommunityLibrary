"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Tuple, Iterator, Callable, Any
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
    """The type of object/area to add interactions to.

    """
    ON_TERRAIN_LOAD = 0
    ON_OCEAN_LOAD = 1
    ON_SCRIPT_OBJECT_LOAD = 2


class CommonInteractionHandler:
    """An interaction handler that adds interactions to script objects, the terrain, or the ocean.

    """
    @property
    def interactions_to_add(self) -> Tuple[int]:
        """A tuple of interaction identifiers being added by the interaction handler.

        :return: A collection of interaction identifiers.
        :rtype: Tuple[int]
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
    """An inheritable class that enables registration of interactions to script objects.

    .. note:: Script Objects can be both Sims and Furniture.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

       # In this example, the interaction `sim-chat` will be added to any script object that is a `Sim`.
       @CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
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

    """
    @property
    def interactions_to_add(self) -> Tuple[int]:
        """A collection of interactions that will be added to the script objects that pass the :func:`~should_add` check.

        :return: A collection of interaction decimal identifiers.
        :rtype: Tuple[int]
        """
        raise NotImplementedError()

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        """should_add(script_object, args, kwargs)
        Determine whether to add the interactions of this handler to the script object.

        :param script_object: An object of type ScriptObject
        :param script_object: ScriptObject
        :return: True if the interactions specified by `interactions_to_add` should be added to the `script_object`. False if not.
        :rtype: bool
        """
        raise NotImplementedError()


class CommonInteractionRegistry(CommonService):
    """Manages the registration of interactions to script objects, terrain, sims, etc.

    Take a look at :class:`.CommonScriptObjectInteractionHandler` for more info and an example of usage.

    """
    def __init__(self) -> None:
        super().__init__()
        self._interaction_handlers = {
            CommonInteractionType.ON_TERRAIN_LOAD: [],
            CommonInteractionType.ON_OCEAN_LOAD: [],
            CommonInteractionType.ON_SCRIPT_OBJECT_LOAD: []
        }

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def on_script_object_add(self, script_object: ScriptObject, *args, **kwargs):
        """on_script_object_add(script_object, *args, **kwargs)

        Occurs upon a script object being added.

        :param script_object: The script object being added.
        :type script_object: ScriptObject
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

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def on_terrain_load(self, terrain_service: TerrainService, *_, **__):
        """on_terrain_load(terrain_service, *_, **__)

        Occurs upon the terrain loading

        :param terrain_service: The terrain service
        :type terrain_service: TerrainService
        """
        new_super_affordances = []
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_TERRAIN_LOAD]:
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances:
                    continue
                new_super_affordances.append(interaction_instance)
        new_terrain_definition_class = terrain_service.TERRAIN_DEFINITION.cls
        new_terrain_definition_class._super_affordances += tuple(new_super_affordances)
        terrain_service.TERRAIN_DEFINITION.set_class(new_terrain_definition_class)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def on_ocean_load(self, terrain_service: TerrainService, *_, **__):
        """on_ocean_load(terrain_service, *_, **__)

        Occurs upon the ocean loading

        :param terrain_service: The terrain service
        :type terrain_service: TerrainService
        """
        new_super_affordances = []
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_OCEAN_LOAD]:
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances:
                    continue
                new_super_affordances.append(interaction_instance)
        new_ocean_definition_class = terrain_service.OCEAN_DEFINITION.cls
        new_ocean_definition_class._super_affordances += tuple(new_super_affordances)
        terrain_service.OCEAN_DEFINITION.set_class(new_ocean_definition_class)

    def register_handler(self, handler: CommonInteractionHandler, interaction_type: CommonInteractionType):
        """register_handler(handler, interaction_type)

        Manually register an interaction handler.

        .. note:: It is recommended to decorate classes with :func:`~register_interaction_handler`\
            instead of manually registering interaction handlers.

        :param handler: The interaction handler being registered.
        :type handler: CommonInteractionHandler
        :param interaction_type: The type of place the interactions will show up.
        :type interaction_type: CommonInteractionType
        """
        self._interaction_handlers[interaction_type].append(handler)

    @staticmethod
    def register_interaction_handler(interaction_type: CommonInteractionType) -> Callable[..., Any]:
        """register_interaction_handler(interaction_type)

        Decorate a class to register that class as an interaction handler.

        Take a look at :class:`.CommonScriptObjectInteractionHandler` for more info and example usage.

        :param interaction_type: The type of place the interactions will show up.
        :type interaction_type: CommonInteractionType
        :return: A wrapped function.
        :rtype: Callable[..., Any]
        """
        def _wrapper(interaction_handler) -> CommonInteractionHandler:
            CommonInteractionRegistry.get().register_handler(interaction_handler(), interaction_type)
            return interaction_handler
        return _wrapper


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, ScriptObject, ScriptObject.on_add.__name__)
def _common_script_object_on_add(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry.get().on_script_object_add(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, TerrainService, TerrainService.start.__name__)
def _common_terrain_service_start(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry.get().on_terrain_load(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, TerrainService, TerrainService.on_zone_load.__name__)
def _common_terrain_service_on_zone_load(original, self, *args, **kwargs) -> Any:
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
