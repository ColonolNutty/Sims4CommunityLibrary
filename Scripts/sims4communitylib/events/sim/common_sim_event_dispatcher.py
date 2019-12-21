"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_changed_occult_type import S4CLSimChangedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_initialized import S4CLSimInitializedEvent
from sims4communitylib.events.sim.events.sim_loaded import S4CLSimLoadedEvent
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class CommonSimEventDispatcherService(CommonService):
    """
        A service for dispatching sim events.
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

    def _on_sim_change_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType, *_, **__):
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimChangedOccultTypeEvent(sim_info, occult_type, occult_tracker))


@CommonInjectionUtils.inject_into(SimInfo, SimInfo.__init__.__name__)
def _common_on_sim_init(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_init(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_into(SimInfo, SimInfo.load_sim_info.__name__)
def _common_on_sim_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_load(self, *args, **kwargs)
    return result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_into(SimSpawner, SimSpawner.spawn_sim.__name__)
def _common_on_sim_spawn(original, cls, *args, **kwargs):
    result = original(*args, **kwargs)
    if result:
        CommonSimEventDispatcherService.get()._on_sim_spawned(*args, **kwargs)
    return result


@CommonInjectionUtils.inject_into(OccultTracker, OccultTracker.switch_to_occult_type.__name__)
def _common_on_sim_change_occult_type(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_change_occult_type(self, *args, **kwargs)
    return result
