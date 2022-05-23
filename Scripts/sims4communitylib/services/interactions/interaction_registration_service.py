"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Callable, Any
from interactions.base.interaction import Interaction
from objects.script_object import ScriptObject
from services.terrain_service import TerrainService
from sims.sim import Sim
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.logging._has_s4cl_log import _HasS4CLLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class CommonInteractionType(CommonInt):
    """The type of object/area to add interactions to.

    """
    ON_TERRAIN_LOAD: 'CommonInteractionType' = ...
    ON_OCEAN_LOAD: 'CommonInteractionType' = ...
    ON_SCRIPT_OBJECT_LOAD: 'CommonInteractionType' = ...
    ADD_PRE_ROLL_SUPER_INTERACTION_ON_SCRIPT_OBJECT_LOAD: 'CommonInteractionType' = ...
    ADD_TO_SIM_RELATIONSHIP_PANEL_INTERACTIONS: 'CommonInteractionType' = ...
    ADD_TO_SIM_PHONE_INTERACTIONS: 'CommonInteractionType' = ...


class CommonInteractionHandler:
    """An interaction handler that adds interactions to script objects, the terrain, or the ocean.

    """
    def __init__(self) -> None:
        self._cached_interactions_to_add = None

    @property
    def interactions_to_add(self) -> Tuple[int]:
        """A collection of interaction identifiers being added by the interaction handler.

        :return: A collection of interaction identifiers.
        :rtype: Tuple[int]
        """
        raise NotImplementedError()

    def _interactions_to_add_gen(self) -> Iterator[Interaction]:
        if self._cached_interactions_to_add is not None:
            yield from self._cached_interactions_to_add
        else:
            cached_interactions = list()
            from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
            affordance_manager = CommonInteractionUtils.get_instance_manager()
            for affordance_id in self.interactions_to_add:
                affordance_instance = affordance_manager.get(affordance_id)
                if affordance_instance is None:
                    continue
                yield affordance_instance
                cached_interactions.append(affordance_instance)
            self._cached_interactions_to_add = cached_interactions


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


class CommonInteractionRegistry(CommonService, _HasS4CLLog):
    """Manage the registration of interactions to script objects, terrain, sims, etc.

    .. note:: Take a look at :class:`.CommonScriptObjectInteractionHandler` for more info and an example of usage.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_interaction_registry'

    def __init__(self) -> None:
        super().__init__()
        self._interaction_handlers = {
            CommonInteractionType.ON_TERRAIN_LOAD: list(),
            CommonInteractionType.ON_OCEAN_LOAD: list(),
            CommonInteractionType.ON_SCRIPT_OBJECT_LOAD: list(),
            CommonInteractionType.ADD_PRE_ROLL_SUPER_INTERACTION_ON_SCRIPT_OBJECT_LOAD: list(),
            CommonInteractionType.ADD_TO_SIM_RELATIONSHIP_PANEL_INTERACTIONS: list(),
            CommonInteractionType.ADD_TO_SIM_PHONE_INTERACTIONS: list()
        }

    def on_script_object_add(self, script_object: ScriptObject, *args, **kwargs):
        """on_script_object_add(script_object, *args, **kwargs)

        A hook that occurs upon a Script Object being added.

        :param script_object: The script object being added.
        :type script_object: ScriptObject
        """
        script_object_type = type(script_object)
        self.log.format_with_message('Adding interactions for type', script_object_type=script_object_type)
        if not hasattr(script_object_type, '_super_affordances'):
            self.verbose_log.format_with_message('Object did not have super affordances.', script_object=script_object_type)
            return
        new_super_affordances = list()
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_SCRIPT_OBJECT_LOAD]:
            if hasattr(interaction_handler, 'should_add') and not interaction_handler.should_add(script_object, *args, **kwargs):
                continue
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances or interaction_instance in script_object_type._super_affordances:
                    self.verbose_log.format_with_message('Interaction was already found in the interactions list.', script_object_type=script_object_type, interaction_instance=interaction_instance)
                    continue
                new_super_affordances.append(interaction_instance)
        self.log.format_with_message('Adding super affordances to object.', script_object=script_object, script_object_type=script_object_type, new_super_affordances=new_super_affordances)
        script_object_type._super_affordances += tuple(new_super_affordances)
        new_script_object_super_affordances = list()
        for new_super_affordance in new_super_affordances:
            if new_super_affordance in script_object._super_affordances:
                continue
            new_script_object_super_affordances.append(new_super_affordance)
        script_object._super_affordances += tuple(new_script_object_super_affordances)

    def register_pre_roll_super_interactions_on_script_object_add(self, script_object: ScriptObject, *args, **kwargs):
        """register_pre_roll_super_interactions_on_script_object_add(script_object, *args, **kwargs)

        A hook that occurs upon a Script Object being added.

        :param script_object: The script object being added.
        :type script_object: ScriptObject
        """
        script_object_type = type(script_object)
        self.log.format_with_message('Adding pre roll super interactions for type', script_object_type=script_object_type)
        if not hasattr(script_object_type, '_preroll_super_affordances'):
            self.verbose_log.format_with_message('Object did not have super affordances.', script_object=script_object_type)
            return
        new_preroll_super_affordances = list()
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ADD_PRE_ROLL_SUPER_INTERACTION_ON_SCRIPT_OBJECT_LOAD]:
            if hasattr(interaction_handler, 'should_add') and not interaction_handler.should_add(script_object, *args, **kwargs):
                continue
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_preroll_super_affordances or interaction_instance in script_object_type._preroll_super_affordances:
                    self.verbose_log.format_with_message('Interaction was already found in the interactions list.', script_object_type=script_object_type, interaction_instance=interaction_instance)
                    continue
                new_preroll_super_affordances.append(interaction_instance)
        self.log.format_with_message('Adding super affordances to object.', script_object=script_object, script_object_type=script_object_type, new_preroll_super_affordances=new_preroll_super_affordances)
        script_object_type._preroll_super_affordances += tuple(new_preroll_super_affordances)
        new_script_object_preroll_super_affordances = list()
        for new_super_affordance in new_preroll_super_affordances:
            if new_super_affordance in script_object._preroll_super_affordances:
                continue
            new_script_object_preroll_super_affordances.append(new_super_affordance)
        script_object._preroll_super_affordances += tuple(new_script_object_preroll_super_affordances)

    def _on_sim_relationship_panel_load(self, sim: Sim, *args, **kwargs):
        sim_class = type(sim)
        if not hasattr(sim_class, '_relation_panel_affordances'):
            return
        new_relationship_panel_affordances = list()
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ADD_TO_SIM_RELATIONSHIP_PANEL_INTERACTIONS]:
            if hasattr(interaction_handler, 'should_add') and not interaction_handler.should_add(sim, *args, **kwargs):
                continue
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_relationship_panel_affordances or interaction_instance in sim_class._relation_panel_affordances:
                    continue
                new_relationship_panel_affordances.append(interaction_instance)
        sim_class._relation_panel_affordances += tuple(new_relationship_panel_affordances)

    def _on_sim_phone_load(self, sim: Sim, *args, **kwargs):
        sim_class = type(sim)
        if not hasattr(sim_class, '_phone_affordances'):
            return
        new_phone_affordances_affordances = list()
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ADD_TO_SIM_PHONE_INTERACTIONS]:
            if hasattr(interaction_handler, 'should_add') and not interaction_handler.should_add(sim, *args, **kwargs):
                continue
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_phone_affordances_affordances or interaction_instance in sim_class._phone_affordances:
                    continue
                new_phone_affordances_affordances.append(interaction_instance)
        sim_class._phone_affordances += tuple(new_phone_affordances_affordances)

    def on_terrain_load(self, terrain_service: TerrainService, *_, **__):
        """on_terrain_load(terrain_service, *_, **__)

        A hook that occurs upon the Terrain loading

        :param terrain_service: The terrain service
        :type terrain_service: TerrainService
        """
        new_super_affordances = list()
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_TERRAIN_LOAD]:
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances or interaction_instance in terrain_service.TERRAIN_DEFINITION.cls._super_affordances:
                    continue
                new_super_affordances.append(interaction_instance)
        new_terrain_definition_class = terrain_service.TERRAIN_DEFINITION.cls
        new_terrain_definition_class._super_affordances += tuple(new_super_affordances)
        terrain_service.TERRAIN_DEFINITION.set_class(new_terrain_definition_class)

    def on_ocean_load(self, terrain_service: TerrainService, *_, **__):
        """on_ocean_load(terrain_service, *_, **__)

        A hook that occurs upon the Ocean loading

        :param terrain_service: The terrain service
        :type terrain_service: TerrainService
        """
        new_super_affordances = list()
        for interaction_handler in self._interaction_handlers[CommonInteractionType.ON_OCEAN_LOAD]:
            for interaction_instance in interaction_handler._interactions_to_add_gen():
                if interaction_instance in new_super_affordances or interaction_instance in terrain_service.OCEAN_DEFINITION.cls._super_affordances:
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

        .. note:: Take a look at :class:`.CommonScriptObjectInteractionHandler` for more info and example usage.

        :param interaction_type: The type of place the interactions will show up.
        :type interaction_type: CommonInteractionType
        :return: A wrapped function.
        :rtype: Callable[..., Any]
        """
        def _wrapper(interaction_handler) -> CommonInteractionHandler:
            CommonInteractionRegistry().register_handler(interaction_handler(), interaction_type)
            return interaction_handler
        return _wrapper


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ScriptObject, ScriptObject.on_add.__name__, handle_exceptions=False)
def _common_script_object_on_add(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry().on_script_object_add(self, *args, **kwargs)
    CommonInteractionRegistry().register_pre_roll_super_interactions_on_script_object_add(self, *args, **kwargs)
    if CommonTypeUtils.is_sim_instance(self):
        CommonInteractionRegistry()._on_sim_relationship_panel_load(self, *args, **kwargs)
        CommonInteractionRegistry()._on_sim_phone_load(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TerrainService, TerrainService.start.__name__, handle_exceptions=False)
def _common_terrain_service_start(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry().on_terrain_load(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TerrainService, TerrainService.on_zone_load.__name__, handle_exceptions=False)
def _common_terrain_service_on_zone_load(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonInteractionRegistry().on_ocean_load(self, *args, **kwargs)
    return result


# noinspection PyMissingOrEmptyDocstring
# @CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class ExampleInteractionHandler(CommonScriptObjectInteractionHandler):
    @property
    def interactions_to_add(self) -> Tuple[int]:
        # Interaction Ids
        # These are the decimal identifiers of the interactions from a package file.
        from sims4communitylib.enums.interactions_enum import CommonInteractionId
        # noinspection PyTypeChecker
        return tuple([int(CommonInteractionId.SIM_CHAT), 2])

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        # Verify it is the object your are expecting. Return True, if it is.
        # In this case we are adding these interactions to Sims.
        from sims.sim import Sim
        return isinstance(script_object, Sim)
