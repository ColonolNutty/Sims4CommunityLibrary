"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import List, Callable, Dict, Tuple
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_set_current_outfit import S4CLSimSetCurrentOutfitEvent
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonEditSimCloneInCASResponseHandle:
    """CommonEditSimCloneInCASResponseHandle(\
        sim_clone_id,\
        on_outfit_modified=CommonFunctionUtils.noop,\
        on_finished=CommonFunctionUtils.noop,\
    )

    A handle for when changes are made (or not made) to a temporary Sim Clone.

    :param sim_clone_id: The decimal identifier of the Sim clone the handle is for.
    :type sim_clone_id: int
    :param on_outfit_modified: A callback invoked when the outfit of the Sim Clone is modified. It will receive the Sim Clone object itself as well as an Outfit IO for easy retrieval of outfit parts. Default is Noop.
    :type on_outfit_modified: Callable[[SimInfo, CommonSimOutfitIO], None], optional
    :param on_finished: A callback invoked when the outfit is either modified or not. Default is noop.
    :type on_finished: Callable[[], None], optional
    """

    def __init__(
        self,
        sim_clone_id: int,
        on_outfit_modified: Callable[[SimInfo, CommonSimOutfitIO], None]=CommonFunctionUtils.noop,
        on_finished: Callable[[], None]=CommonFunctionUtils.noop
    ):
        self.sim_clone_id = sim_clone_id
        self.on_outfit_modified = on_outfit_modified
        self.on_finished = on_finished


class CommonEditSimCloneInCASService(CommonService, HasLog):
    """CommonEditSimCloneInCASService()

    A service that will create a Sim clone, open CAS with that Sim clone for edit, invoke callbacks when the outfit of the Sim clone is modified, and finally delete the Sim clone.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_edit_sim_clone_in_cas_service'

    def __init__(self, outfit_category_and_index: Tuple[OutfitCategory, int]=(OutfitCategory.EVERYDAY, 0)) -> None:
        super().__init__()
        self._sim_clone_response_handle_library: Dict[int, CommonEditSimCloneInCASResponseHandle] = dict()
        self._sim_clone_sim_ids_awaiting_destruction: List[int] = list()
        self._outfit_category_and_index = outfit_category_and_index

    def modify_sim_clone_for_sim(
        self,
        sim_info: SimInfo,
        setup_outfit: Callable[[CommonSimOutfitIO], None]=CommonFunctionUtils.noop,
        on_outfit_modified: Callable[[SimInfo, CommonSimOutfitIO], None]=CommonFunctionUtils.noop,
        on_finished: Callable[[], None]=CommonFunctionUtils.noop
    ) -> None:
        """modify_sim_clone_for_sim()

        Modify a Clone of a Sim in CAS

        """
        self.modify_sim_clone(sim_info, setup_outfit=setup_outfit, on_outfit_modified=on_outfit_modified, on_finished=on_finished)

    def modify_sim_clone(
        self,
        source_sim_info: SimInfo,
        setup_outfit: Callable[[CommonSimOutfitIO], None]=CommonFunctionUtils.noop,
        on_outfit_modified: Callable[[SimInfo, CommonSimOutfitIO], None]=CommonFunctionUtils.noop,
        on_finished: Callable[[], None]=CommonFunctionUtils.noop
    ) -> None:
        """Create a temporary Sim clone, open cas with it, and invoke callbacks when the Sim clone outfit is modified."""
        if source_sim_info is None:
            self.log.error('No Sim was specified for cloning!')
            return
        if on_outfit_modified is None:
            self.log.error('Missing on_outfit_modified.')
            return
        if self._sim_clone_sim_ids_awaiting_destruction:
            sim_clone_sim_ids_awaiting_destruction = tuple(self._sim_clone_sim_ids_awaiting_destruction)
            for _sim_clone_sim_id in sim_clone_sim_ids_awaiting_destruction:
                _clone_sim_info = CommonSimUtils.get_sim_info(_sim_clone_sim_id)
                if _clone_sim_info is None:
                    continue
                if CommonSimSpawnUtils.delete_sim(_clone_sim_info, source=f'{self.mod_identity.name} Destroy Old Sim Clone', cause='Sim Clone is Old'):
                    if _sim_clone_sim_id in self._sim_clone_sim_ids_awaiting_destruction:
                        self._sim_clone_sim_ids_awaiting_destruction.remove(_sim_clone_sim_id)
        # if CommonOccultUtils.has_any_occult(source_sim_info):
        #     CommonOccultUtils.switch_to_occult_form(source_sim_info, CommonOccultType.NON_OCCULT)

        clone_sim_info = CommonSimSpawnUtils.clone_sim(source_sim_info, add_to_household=True)
        if clone_sim_info is None:
            self.log.format_error('Failed to create Clone Sim.')
            return
        try:
            clone_household_id = CommonHouseholdUtils.get_household_id(clone_sim_info)
            CommonSimSpawnUtils.spawn_sim(clone_sim_info, location=CommonSimLocationUtils.get_location(source_sim_info))
            self._delete_other_outfits(clone_sim_info)
            sim_clone_sim_id = CommonSimUtils.get_sim_id(clone_sim_info)
            clone_sim_info.skin_tone = source_sim_info.skin_tone
            clone_sim_info.skin_tone_val_shift = source_sim_info.skin_tone_val_shift

            self.verbose_log.format_with_message('Current Sim clone outfit', outfit_parts=CommonOutfitUtils.get_outfit_parts(clone_sim_info))
            self._setup_sim_clone_outfit(clone_sim_info, CommonOutfitUtils.get_outfit_parts(source_sim_info, outfit_category_and_index=(OutfitCategory.BATHING, 0)), setup_outfit)
            client = services.client_manager().get_first_client()
            self.log.format_with_message('Adding Sim Id to response handle library', sim_id=sim_clone_sim_id, sim=clone_sim_info)
            self._sim_clone_response_handle_library[sim_clone_sim_id] = CommonEditSimCloneInCASResponseHandle(sim_clone_sim_id, on_outfit_modified=on_outfit_modified, on_finished=on_finished)
            if client is not None:
                import sims4.commands
                sims4.commands.client_cheat('cas.fulleditmode', client.id)
                sims4.commands.client_cheat('sims.exit2cas {} {} {}'.format(sim_clone_sim_id, clone_household_id, CommonSimUtils.get_sim_info(source_sim_info)), client.id)
        except Exception as ex:
            self.log.error('An error occurred when trying to display clone Sim.', exception=ex)
            if clone_sim_info is not None:
                CommonSimSpawnUtils.delete_sim(clone_sim_info, source=f'{self.mod_identity.name} Destroy Sim Clone due to error', cause='Deleting Sim Clone due to error')

    def _setup_sim_clone_outfit(
        self,
        clone_sim_info: SimInfo,
        initial_outfit_parts: Dict[BodyType, int],
        setup_outfit: Callable[[CommonSimOutfitIO], None]=CommonFunctionUtils.noop
    ):
        self.log.format_with_message('Setting up Sim clone outfit', sim_clone_sim_info=clone_sim_info, initial_outfit_parts=initial_outfit_parts, outfit_category_and_index=CommonOutfitUtils.get_current_outfit(clone_sim_info))
        # noinspection PyTypeChecker
        outfit_io = CommonSimOutfitIO(clone_sim_info, outfit_category_and_index=self._outfit_category_and_index, initial_outfit_parts=initial_outfit_parts, mod_identity=self.mod_identity)
        if setup_outfit is not None:
            setup_outfit(outfit_io)

        # from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
        # if CommonOccultUtils.has_any_occult(clone_sim_info):
        #     CommonOccultUtils.switch_to_occult_form(clone_sim_info, OccultType.HUMAN)
        if outfit_io.apply(apply_to_all_outfits_in_same_category=True, apply_to_outfit_category_and_index=self._outfit_category_and_index):
            clone_sim_info.on_outfit_generated(*self._outfit_category_and_index)
            clone_sim_info.set_outfit_dirty(self._outfit_category_and_index[0])
            clone_sim_info.set_current_outfit(self._outfit_category_and_index)

    def _on_sim_clone_outfit_changed(
        self,
        clone_sim_info: SimInfo,
        outfit_category_and_index: Tuple[OutfitCategory, int]
    ) -> None:
        clone_sim_id = CommonSimUtils.get_sim_id(clone_sim_info)
        if clone_sim_id not in self._sim_clone_response_handle_library:
            self.log.format_with_message('No response handle found waiting for Sim clone outfit change.', clone_sim_id=clone_sim_id, sim=clone_sim_info)
            return
        self.log.format_with_message(
            'Sim Clone outfit changed',
            sim_clone_id=clone_sim_id,
            clone_sim_info=clone_sim_info,
            outfit_category_and_index=outfit_category_and_index
        )
        # noinspection PyTypeChecker
        outfit_io = CommonSimOutfitIO(clone_sim_info, mod_identity=ModInfo.get_identity(), outfit_category_and_index=self._outfit_category_and_index)

        sim_clone_response_handle = self._sim_clone_response_handle_library[clone_sim_id]
        try:
            if sim_clone_response_handle is None:
                self.log.format_with_message('No response handle found. Done handling on outfit changed', clone_sim_id=clone_sim_id)
                return
            self.log.format_with_message('Response handle found, invoking Sim clone callback', clone_sim_id=clone_sim_id)
            sim_clone_response_handle.on_outfit_modified(clone_sim_info, outfit_io)
        except Exception as ex:
            self.log.error('Error occurred while invoking Sim clone callback', exception=ex)
        finally:
            if clone_sim_id not in self._sim_clone_sim_ids_awaiting_destruction:
                self._sim_clone_sim_ids_awaiting_destruction.append(clone_sim_id)

    def _clean_up_sim_clones(self) -> None:
        for (sim_clone_id, response_handle) in self._sim_clone_response_handle_library.items():
            sim_clone_sim_info = CommonSimUtils.get_sim_info(sim_clone_id)
            if sim_clone_sim_info is not None:
                self._on_sim_clone_outfit_changed(sim_clone_sim_info, CommonOutfitUtils.get_current_outfit(sim_clone_sim_info))

        if not self._sim_clone_sim_ids_awaiting_destruction:
            self.log.debug('No sim_clones were awaiting destruction')
            return

        sim_clone_ids_awaiting_destruction = tuple(self._sim_clone_sim_ids_awaiting_destruction)
        for sim_clone_sim_id in sim_clone_ids_awaiting_destruction:
            self.log.format_with_message('Cleaning up Sim clone.', sim_clone_id=sim_clone_sim_id)
            if sim_clone_sim_id in self._sim_clone_response_handle_library:
                sim_clone_response_handle = self._sim_clone_response_handle_library[sim_clone_sim_id]
                try:
                    if sim_clone_response_handle is not None:
                        self.log.format_with_message('Calling response handle on finished.', sim_clone_id=sim_clone_sim_id)
                        if sim_clone_response_handle.on_finished is not None:
                            sim_clone_response_handle.on_finished()
                except Exception as ex:
                    self.log.error('An error occurred while invoking on finished.', exception=ex)
                finally:
                    del self._sim_clone_response_handle_library[sim_clone_sim_id]

            clone_sim_info = CommonSimUtils.get_sim_info(sim_clone_sim_id)
            if clone_sim_info is None:
                self.log.format_with_message('Sim Clone SimInfo not found.', sim_clone_id=sim_clone_sim_id)
                continue

            self.log.format_with_message('Destroying Sim Clone.', sim_clone_id=sim_clone_sim_id)

            if CommonSimSpawnUtils.delete_sim(clone_sim_info, source=self.mod_identity.name, cause=f'{self.mod_identity.name}: Sim Clone is being cleaned up'):
                if sim_clone_sim_id in self._sim_clone_sim_ids_awaiting_destruction:
                    self._sim_clone_sim_ids_awaiting_destruction.remove(sim_clone_sim_id)

    def _delete_other_outfits(self, sim_info: SimInfo):
        from sims.outfits.outfit_tracker import OutfitTrackerMixin
        outfits: OutfitTrackerMixin = sim_info.get_outfits()
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        for outfit_category in CommonOutfitUtils.get_all_outfit_categories():
            for outfit_index in range(CommonOutfitUtils.get_maximum_number_of_outfits_for_category(outfit_category)):
                outfit = (outfit_category, outfit_index)
                if outfit_category in (self._outfit_category_and_index[0], OutfitCategory.BATHING, OutfitCategory.SPECIAL) and outfit_index == 0:
                    self.log.format_with_message('Skipping first outfit.', sim=sim_info, outfit=outfit)
                    continue
                if not CommonOutfitUtils.has_outfit(sim_info, outfit):
                    self.log.format_with_message('Sim did not have outfit.', sim=sim_info, outfit=outfit)
                    continue
                outfits.remove_outfit(outfit_category, outfit_index=outfit_index)
                self.log.format_with_message('Removed outfit.', sim=sim_info, outfit=outfit)
        sim_info.appearance_tracker.evaluate_appearance_modifiers()
        CommonOutfitUtils.resend_outfits(sim_info)
        CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.modify_sim_clone',
    'Create a Clone of a Sim and open CAS to modify them.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to create and modify a clone of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.modifysimclone',
    )
)
def _s4clib_modify_sim_clone(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Modifying a clone of Sim \'{sim_info}\' in CAS.')
    CommonEditSimCloneInCASService().modify_sim_clone_for_sim(sim_info)
    output('Done')


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_clean_sim_clones_on_zone_load(event_data: S4CLZoneLateLoadEvent):
    CommonEditSimCloneInCASService()._clean_up_sim_clones()


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_sim_clone_on_outfit_change(event_data: S4CLSimSetCurrentOutfitEvent) -> bool:
    CommonEditSimCloneInCASService()._on_sim_clone_outfit_changed(event_data.sim_info, event_data.new_outfit_category_and_index)
    return True
