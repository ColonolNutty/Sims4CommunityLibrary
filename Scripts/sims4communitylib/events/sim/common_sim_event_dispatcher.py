"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from buffs.buff import Buff
from objects.components.buff_component import BuffComponent
from sims.aging.aging_mixin import AgingMixin
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims.sim_spawner import SimSpawner
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_added_occult_type import S4CLSimAddedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_buff_added import S4CLSimBuffAddedEvent
from sims4communitylib.events.sim.events.sim_buff_removed import S4CLSimBuffRemovedEvent
from sims4communitylib.events.sim.events.sim_changed_age import S4CLSimChangedAgeEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_body_frame import S4CLSimChangedGenderOptionsBodyFrameEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_breasts import \
    S4CLSimChangedGenderOptionsBreastsEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_can_impregnate import \
    S4CLSimChangedGenderOptionsCanImpregnateEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_can_reproduce import \
    S4CLSimChangedGenderOptionsCanReproduceEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_clothing_preference import S4CLSimChangedGenderOptionsClothingPreferenceEvent
from sims4communitylib.events.sim.events.sim_changed_gender import S4CLSimChangedGenderEvent
from sims4communitylib.events.sim.events.sim_changed_occult_type import S4CLSimChangedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_can_be_impregnated import S4CLSimChangedGenderOptionsCanBeImpregnatedEvent
from sims4communitylib.events.sim.events.sim_changed_gender_options_toilet_usage import S4CLSimChangedGenderOptionsToiletUsageEvent
from sims4communitylib.events.sim.events.sim_changing_occult_type import S4CLSimChangingOccultTypeEvent
from sims4communitylib.events.sim.events.sim_initialized import S4CLSimInitializedEvent
from sims4communitylib.events.sim.events.sim_loaded import S4CLSimLoadedEvent
from sims4communitylib.events.sim.events.sim_removed_occult_type import S4CLSimRemovedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_set_current_outfit import S4CLSimSetCurrentOutfitEvent
from sims4communitylib.events.sim.events.sim_skill_leveled_up import S4CLSimSkillLeveledUpEvent
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.skill import Skill


class CommonSimEventDispatcherService(CommonService):
    """A service that dispatches Sim events (Init, Spawn, Add Occult, Remove Occult, Change Gender, etc.).

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    def _on_sim_change_gender(self, sim_info: SimInfo) -> bool:
        from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
        new_gender = CommonGender.get_gender(sim_info)
        if CommonGenderUtils.is_male_gender(new_gender):
            # If they are now Male, it means they used to be Female.
            old_gender = CommonGender.FEMALE
        else:
            # If they are now Female, it means they used to be Male.
            old_gender = CommonGender.MALE
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderEvent(sim_info, old_gender, new_gender))

    def _on_sim_change_gender_options_breasts(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsBreastsEvent(sim_info))

    def _on_sim_change_gender_options_toilet_usage(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsToiletUsageEvent(sim_info))

    def _on_sim_change_gender_options_body_frame(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsBodyFrameEvent(sim_info))

    def _on_sim_change_gender_options_clothing_preference(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsClothingPreferenceEvent(sim_info))

    def _on_sim_change_gender_options_can_impregnate(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsCanImpregnateEvent(sim_info))

    def _on_sim_change_gender_options_can_be_impregnated(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsCanBeImpregnatedEvent(sim_info))

    def _on_sim_change_gender_options_can_reproduce(self, sim_info: SimInfo) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimChangedGenderOptionsCanReproduceEvent(sim_info))

    def _on_sim_init(self, sim_info: SimInfo, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimInitializedEvent(sim_info))

    def _on_sim_load(self, sim_info: SimInfo, *_, **__) -> bool:
        from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
        if CommonZoneSpinEventDispatcher.get().game_loading:
            return False
        return CommonEventRegistry.get().dispatch(S4CLSimLoadedEvent(sim_info))

    def _on_sim_spawned(self, sim_info: SimInfo, *_, **__) -> bool:
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        return CommonEventRegistry.get().dispatch(S4CLSimSpawnedEvent(CommonSimUtils.get_sim_info(sim_info)))

    def _on_sim_change_age(self, sim_info: SimInfo, new_age: Age, current_age: Age) -> bool:
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        return CommonEventRegistry.get().dispatch(S4CLSimChangedAgeEvent(CommonSimUtils.get_sim_info(sim_info), CommonAge.convert_from_vanilla(current_age), CommonAge.convert_from_vanilla(new_age)))

    def _on_sim_add_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType) -> bool:
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimAddedOccultTypeEvent(sim_info, occult_type, occult_tracker))

    def _on_sim_changing_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType, *_, **__) -> bool:
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimChangingOccultTypeEvent(sim_info, occult_type, occult_tracker))

    def _on_sim_changed_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType, *_, **__) -> bool:
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimChangedOccultTypeEvent(sim_info, occult_type, occult_tracker))

    def _on_sim_remove_occult_type(self, occult_tracker: OccultTracker, occult_type: OccultType) -> bool:
        sim_info = occult_tracker._sim_info
        return CommonEventRegistry.get().dispatch(S4CLSimRemovedOccultTypeEvent(sim_info, occult_type, occult_tracker))

    def _on_sim_buff_added(self, buff: Buff, sim_id: int) -> None:
        sim_info = CommonSimUtils.get_sim_info(sim_id)
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimBuffAddedEvent(sim_info, buff))

    def _on_sim_set_current_outfit(self, sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]) -> None:
        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        CommonEventRegistry.get().dispatch(S4CLSimSetCurrentOutfitEvent(sim_info, CommonOutfitUtils.get_current_outfit(sim_info), outfit_category_and_index))

    def _on_sim_buff_removed(self, buff: Buff, sim_id: int) -> None:
        sim_info = CommonSimUtils.get_sim_info(sim_id)
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimBuffRemovedEvent(sim_info, buff))

    def _on_skill_leveled_up(self, skill: Skill, old_skill_level: int, new_skill_level: int) -> None:
        if skill.tracker is None or skill.tracker._owner is None:
            return
        sim_info = CommonSimUtils.get_sim_info(skill.tracker._owner)
        CommonEventRegistry.get().dispatch(S4CLSimSkillLeveledUpEvent(sim_info, skill, old_skill_level, new_skill_level))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.__init__.__name__)
def _common_on_sim_init(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_init(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.load_sim_info.__name__)
def _common_on_sim_load(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_load(self, *args, **kwargs)
    return result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimSpawner, SimSpawner.spawn_sim.__name__)
def _common_on_sim_spawn(original, cls, *args, **kwargs) -> Any:
    result = original(*args, **kwargs)
    if result:
        CommonSimEventDispatcherService.get()._on_sim_spawned(*args, **kwargs)
    return result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Skill, Skill.on_skill_level_up.__name__)
def _common_on_sim_skill_level_up(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    if result:
        CommonSimEventDispatcherService.get()._on_skill_leveled_up(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AgingMixin, AgingMixin.change_age.__name__)
def _common_on_sim_change_age(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_change_age(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OccultTracker, OccultTracker.add_occult_type.__name__)
def _common_on_sim_add_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_add_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OccultTracker, OccultTracker.switch_to_occult_type.__name__)
def _common_on_sim_change_occult_type(original, self, *args, **kwargs) -> Any:
    CommonSimEventDispatcherService.get()._on_sim_changing_occult_type(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_changed_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OccultTracker, OccultTracker.remove_occult_type.__name__)
def _common_on_sim_remove_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_remove_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.set_current_outfit.__name__)
def _common_on_sim_set_current_outfit(original, self, *args, **kwargs) -> Any:
    CommonSimEventDispatcherService.get()._on_sim_set_current_outfit(self, *args, **kwargs)
    return original(self, *args, **kwargs)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_register_buff_added_or_removed_on_sim_spawned(event_data: S4CLSimSpawnedEvent) -> bool:
    buff_component: BuffComponent = CommonComponentUtils.get_component(event_data.sim_info, CommonComponentType.BUFF)
    if not buff_component:
        return False

    dispatcher_service = CommonSimEventDispatcherService()
    if dispatcher_service._on_sim_buff_added not in buff_component.on_buff_added:
        buff_component.on_buff_added.append(dispatcher_service._on_sim_buff_added)

    if dispatcher_service._on_sim_buff_removed not in buff_component.on_buff_removed:
        buff_component.on_buff_removed.append(dispatcher_service._on_sim_buff_removed)
    return True
