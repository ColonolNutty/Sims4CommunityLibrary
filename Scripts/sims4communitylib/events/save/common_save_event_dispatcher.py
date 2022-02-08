"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.save.events.save_loaded import S4CLSaveLoadedEvent
from sims4communitylib.events.save.events.save_saved import S4CLSaveSavedEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class SaveGameData:
        pass

if not ON_RTD:
    from services.persistence_service import SaveGameData


class CommonSaveEventDispatcher(CommonService):
    """A service that dispatches save file save/load events.

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """
    def __init__(self) -> None:
        self._current_save_slot_guid = None

    def _on_game_save(self, save_game_data: SaveGameData):
        CommonEventRegistry.get().dispatch(S4CLSaveSavedEvent(save_game_data))

    def _on_save_loaded(self) -> None:
        from sims4communitylib.utils.save_load.common_save_utils import CommonSaveUtils
        current_save_slot_guid = CommonSaveUtils().get_save_slot_guid()
        if self._current_save_slot_guid is None:
            self._current_save_slot_guid = current_save_slot_guid
            CommonEventRegistry.get().dispatch(S4CLSaveLoadedEvent())
        elif self._current_save_slot_guid != current_save_slot_guid:
            self._current_save_slot_guid = current_save_slot_guid
            CommonEventRegistry.get().dispatch(S4CLSaveLoadedEvent())


if not ON_RTD:
    from game_services import GameServiceManager
    from services.persistence_service import PersistenceService, SaveGameData

    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), PersistenceService, PersistenceService.save_game_gen.__name__, handle_exceptions=False)
    def _common_save_game_gen(original, self: PersistenceService, timeline, save_game_data: SaveGameData, send_save_message: bool=True, **kwargs):
        if send_save_message:
            CommonSaveEventDispatcher.get()._on_game_save(save_game_data)
        return original(self, timeline, save_game_data, send_save_message=send_save_message, **kwargs)

    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), GameServiceManager, GameServiceManager.on_all_households_and_sim_infos_loaded.__name__, handle_exceptions=False)
    def _common_save_game_loaded(original, self: GameServiceManager, *args, **kwargs):
        result = original(self, *args, **kwargs)
        CommonSaveEventDispatcher()._on_save_loaded()
        return result
