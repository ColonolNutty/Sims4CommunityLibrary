"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from objects.game_object import GameObject
from objects.script_object import ScriptObject
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.game_object.events.game_object_added_to_inventory import S4CLGameObjectAddedToInventoryEvent
from sims4communitylib.events.game_object.events.game_object_pre_despawned import S4CLGameObjectPreDespawnedEvent
from sims4communitylib.events.game_object.events.game_object_pre_deleted import S4CLGameObjectPreDeletedEvent
from sims4communitylib.events.game_object.events.game_object_initialized import S4CLGameObjectInitializedEvent
from sims4communitylib.events.game_object.events.game_object_loaded import S4CLGameObjectLoadedEvent
from sims4communitylib.events.game_object.events.game_object_pre_removed_from_inventory import \
    S4CLGameObjectPreRemovedFromInventoryEvent
from sims4communitylib.events.game_object.events.game_object_spawned import S4CLGameObjectSpawnedEvent
from sims4communitylib.events.game_object.events.game_object_added_to_game_object_inventory import \
    S4CLGameObjectAddedToGameObjectInventoryEvent
from sims4communitylib.events.game_object.events.game_object_pre_removed_from_game_object_inventory import \
    S4CLGameObjectPreRemovedFromGameObjectInventoryEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonGameObjectEventDispatcherService(CommonService):
    """A service that dispatches Game Object events (Init, Spawn, Destroy, etc.).

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    def _on_game_object_init(self, game_object: GameObject, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLGameObjectInitializedEvent(game_object))

    def _on_game_object_load(self, game_object: GameObject, *_, **__) -> bool:
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if CommonZoneSpinEventDispatcher.get().game_loading:
            return False
        return CommonEventRegistry.get().dispatch(S4CLGameObjectLoadedEvent(game_object))

    def _on_game_object_spawned(self, game_object: GameObject, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLGameObjectSpawnedEvent(game_object))

    def _on_game_object_despawned(self, game_object: GameObject, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLGameObjectPreDespawnedEvent(game_object))

    def _on_game_object_destroy(self, game_object: GameObject, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLGameObjectPreDeletedEvent(game_object))

    def _on_game_object_added_to_inventory(self, game_object: GameObject, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLGameObjectAddedToInventoryEvent(game_object))

    def _on_game_object_pre_removed_from_inventory(self, game_object: GameObject, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLGameObjectPreRemovedFromInventoryEvent(game_object))

    def _on_game_object_added_to_game_object_inventory(self, game_object: GameObject, added_object: GameObject) -> None:
        CommonEventRegistry.get().dispatch(S4CLGameObjectAddedToGameObjectInventoryEvent(game_object, added_object))

    def _on_game_object_pre_removed_from_game_object_inventory(self, game_object: GameObject, removed_object: GameObject) -> None:
        CommonEventRegistry.get().dispatch(S4CLGameObjectPreRemovedFromGameObjectInventoryEvent(game_object, removed_object))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.__init__.__name__, handle_exceptions=False)
def _common_on_game_object_init(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonGameObjectEventDispatcherService.get()._on_game_object_init(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.load_object.__name__, handle_exceptions=False)
def _common_on_game_object_load(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonGameObjectEventDispatcherService.get()._on_game_object_load(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.destroy.__name__, handle_exceptions=False)
def _common_on_game_object_load(original, self, *args, **kwargs) -> Any:
    CommonGameObjectEventDispatcherService.get()._on_game_object_destroy(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.on_add.__name__)
def _common_on_game_object_added(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonGameObjectEventDispatcherService.get()._on_game_object_spawned(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.on_remove.__name__)
def _common_on_game_object_removed(original, self, *args, **kwargs) -> Any:
    CommonGameObjectEventDispatcherService.get()._on_game_object_despawned(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.on_added_to_inventory.__name__)
def _common_on_game_object_added_to_inventory(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonGameObjectEventDispatcherService.get()._on_game_object_added_to_inventory(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.on_removed_from_inventory.__name__)
def _common_on_game_object_removed_from_inventory(original, self, *args, **kwargs) -> Any:
    CommonGameObjectEventDispatcherService.get()._on_game_object_pre_removed_from_inventory(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.on_object_added_to_inventory.__name__, handle_exceptions=False)
def _common_on_game_object_added_to_game_object_inventory(original, self: GameObject, obj: ScriptObject, *args, **kwargs):
    result = original(self, obj, *args, **kwargs)
    if isinstance(obj, GameObject):
        CommonGameObjectEventDispatcherService.get()._on_game_object_added_to_game_object_inventory(self, obj)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameObject, GameObject.on_object_removed_from_inventory.__name__, handle_exceptions=False)
def _common_on_game_object_removed_from_game_object_inventory(original, self: GameObject, obj: ScriptObject, *args, **kwargs):
    if isinstance(obj, GameObject):
        CommonGameObjectEventDispatcherService.get()._on_game_object_pre_removed_from_game_object_inventory(self, obj)
    result = original(self, obj, *args, **kwargs)
    return result
