"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims.aging.aging_mixin import AgingMixin
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims.sim_spawner import SimSpawner
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_added_occult_type import S4CLSimAddedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_changed_age import S4CLSimChangedAgeEvent
from sims4communitylib.events.sim.events.sim_changed_occult_type import S4CLSimChangedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_initialized import S4CLSimInitializedEvent
from sims4communitylib.events.sim.events.sim_loaded import S4CLSimLoadedEvent
from sims4communitylib.events.sim.events.sim_removed_occult_type import S4CLSimRemovedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonSimEventDispatcherService(CommonService):
    """A service that dispatches Sim events (Init, Spawn, Add Occult, Remove Occult, etc.).

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    def _on_sim_init(self, sim_info: SimInfo, *_, **__):
        CommonEventRegistry.get().dispatch(S4CLSimInitializedEvent(sim_info))

    def _on_sim_load(self, sim_info: SimInfo, *_, **__):
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if CommonZoneSpinEventDispatcher.get().game_loading:
            return False
        return CommonEventRegistry.get().dispatch(S4CLSimLoadedEvent(sim_info))

    def _on_sim_spawned(self, sim_info: SimInfo, *_, **__):
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if CommonZoneSpinEventDispatcher.get().game_loading:
            return False
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        return CommonEventRegistry.get().dispatch(S4CLSimSpawnedEvent(CommonSimUtils.get_sim_info(sim_info)))

    def _on_sim_change_age(self, sim_info: SimInfo, new_age: Age, current_age: Age):
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        return CommonEventRegistry.get().dispatch(S4CLSimChangedAgeEvent(CommonSimUtils.get_sim_info(sim_info), current_age, new_age))

    def _on_sim_add_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType):
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimAddedOccultTypeEvent(sim_info, occult_type, occult_tracker))

    def _on_sim_change_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType, *_, **__):
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimChangedOccultTypeEvent(sim_info, occult_type, occult_tracker))

    def _on_sim_remove_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType):
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimRemovedOccultTypeEvent(sim_info, occult_type, occult_tracker))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, SimInfo, SimInfo.__init__.__name__)
def _common_on_sim_init(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_init(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, SimInfo, SimInfo.load_sim_info.__name__)
def _common_on_sim_load(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_load(self, *args, **kwargs)
    return result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, SimSpawner, SimSpawner.spawn_sim.__name__)
def _common_on_sim_spawn(original, cls, *args, **kwargs) -> Any:
    result = original(*args, **kwargs)
    if result:
        CommonSimEventDispatcherService.get()._on_sim_spawned(*args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, AgingMixin, AgingMixin.change_age.__name__)
def _common_on_sim_change_age(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_change_age(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, OccultTracker, OccultTracker.add_occult_type.__name__)
def _common_on_sim_add_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_add_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, OccultTracker, OccultTracker.switch_to_occult_type.__name__)
def _common_on_sim_change_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_change_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity().name, OccultTracker, OccultTracker.remove_occult_type.__name__)
def _common_on_sim_remove_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_remove_occult_type(self, *args, **kwargs)
    return result
