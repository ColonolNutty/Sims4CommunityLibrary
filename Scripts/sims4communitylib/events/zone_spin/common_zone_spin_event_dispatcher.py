"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from server.client import Client
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.events.zone_spin.events.zone_manager_start_event import S4CLZoneManagerStartEvent
from sims4communitylib.events.zone_spin.events.zone_post_load import \
    S4CLZonePostLoadEvent
from sims4communitylib.events.zone_spin.events.zone_save import S4CLZoneSaveEvent
from sims4communitylib.events.zone_spin.events.zone_teardown import S4CLZoneTeardownEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from zone import Zone
from zone_manager import ZoneManager


class CommonZoneSpinEventDispatcher(CommonService):
    """A service that dispatches zone spin events (Teardown, Save, Early/Late Load).

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """
    def __init__(self: 'CommonZoneSpinEventDispatcher'):
        self._game_loaded = False
        self._game_loading = True

    @property
    def game_loaded(self) -> bool:
        """Determine if the game has loaded.

        :return: True, if the game has loaded. False, if the game has not loaded.
        :rtype: bool
        """
        return self._game_loaded

    @property
    def game_loading(self) -> bool:
        """Determine if the game is loading.

        :return: True, if the game is currently loading. False, if the game is not currently loading.
        :rtype: bool
        """
        return self._game_loading

    def _on_early_zone_load(self, zone: Zone):
        CommonEventRegistry.get().dispatch(S4CLZoneEarlyLoadEvent(zone, game_loaded=self.game_loaded, game_loading=self.game_loading))

    def _on_late_zone_load(self, zone: Zone, household_id: int, active_sim_id: int):
        CommonEventRegistry.get().dispatch(S4CLZoneLateLoadEvent(zone, household_id, active_sim_id, game_loaded=self.game_loaded, game_loading=self.game_loading))
        self._game_loaded = True
        self._game_loading = False

    def _on_zone_teardown(self, zone: Zone, client: Client):
        CommonEventRegistry.get().dispatch(S4CLZoneTeardownEvent(zone, client, game_loaded=self.game_loaded, game_loading=self.game_loading))
        self._game_loading = True

    def _on_zone_save(self, zone: Zone, save_slot_data: Any = None):
        CommonEventRegistry.get().dispatch(S4CLZoneSaveEvent(zone, save_slot_data=save_slot_data, game_loaded=self.game_loaded, game_loading=self.game_loading))

    def _on_loading_screen_animation_finished(self, zone: Zone):
        CommonEventRegistry.get().dispatch(S4CLZonePostLoadEvent(zone, game_loaded=self.game_loaded, game_loading=self.game_loading))

    def _on_zone_manager_start(self, zone_manager: ZoneManager):
        CommonEventRegistry.get().dispatch(S4CLZoneManagerStartEvent(zone_manager))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.load_zone.__name__, handle_exceptions=False)
def _common_on_early_zone_load(original, self: Zone, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonZoneSpinEventDispatcher.get()._on_early_zone_load(self)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.do_zone_spin_up.__name__, handle_exceptions=False)
def _common_on_late_zone_load(original, self: Zone, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonZoneSpinEventDispatcher.get()._on_late_zone_load(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.on_teardown.__name__, handle_exceptions=False)
def _common_on_zone_teardown(original, self: Zone, client):
    CommonZoneSpinEventDispatcher.get()._on_zone_teardown(self, client)
    return original(self, client)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.save_zone.__name__, handle_exceptions=False)
def _common_on_zone_save(original, self: Zone, *args, **kwargs):
    CommonZoneSpinEventDispatcher.get()._on_zone_save(self, *args, **kwargs)
    return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.on_loading_screen_animation_finished.__name__, handle_exceptions=False)
def _common_on_loading_screen_animation_finished(original, self: Zone, *args, **kwargs):
    original_result = original(self, *args, **kwargs)
    CommonZoneSpinEventDispatcher.get()._on_loading_screen_animation_finished(self)
    return original_result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ZoneManager, ZoneManager.start.__name__, handle_exceptions=False)
def _common_on_zone_manager_start(original, self: ZoneManager, *args, **kwargs):
    original_result = original(self, *args, **kwargs)
    CommonZoneSpinEventDispatcher.get()._on_zone_manager_start(self)
    return original_result
