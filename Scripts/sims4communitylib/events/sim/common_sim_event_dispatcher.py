"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, Union

from buffs.buff import Buff
from interactions.utils.death import DeathTracker, DeathType
from objects.components.buff_component import BuffComponent
from objects.game_object import GameObject
from objects.script_object import ScriptObject
from relationships.relationship_objects.relationship import Relationship
from relationships.relationship_bit import RelationshipBit
from relationships.data.relationship_data import RelationshipData
from sims.aging.aging_mixin import AgingMixin
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims.sim_spawner import SimSpawner
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_added_occult_type import S4CLSimAddedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_after_set_current_outfit import S4CLSimAfterSetCurrentOutfitEvent
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
from sims4communitylib.events.sim.events.sim_changing_age import S4CLSimChangingAgeEvent
from sims4communitylib.events.sim.events.sim_changing_occult_type import S4CLSimChangingOccultTypeEvent
from sims4communitylib.events.sim.events.sim_died import S4CLSimDiedEvent
from sims4communitylib.events.sim.events.sim_pre_despawned import S4CLSimPreDespawnedEvent
from sims4communitylib.events.sim.events.sim_initialized import S4CLSimInitializedEvent
from sims4communitylib.events.sim.events.sim_loaded import S4CLSimLoadedEvent
from sims4communitylib.events.sim.events.game_object_added_to_sim_inventory import S4CLGameObjectAddedToSimInventoryEvent
from sims4communitylib.events.sim.events.game_object_pre_removed_from_sim_inventory import S4CLGameObjectPreRemovedFromSimInventoryEvent
from sims4communitylib.events.sim.events.sim_relationship_bit_added import S4CLSimRelationshipBitAddedEvent
from sims4communitylib.events.sim.events.sim_relationship_bit_removed import S4CLSimRelationshipBitRemovedEvent
from sims4communitylib.events.sim.events.sim_removed_occult_type import S4CLSimRemovedOccultTypeEvent
from sims4communitylib.events.sim.events.sim_revived import S4CLSimRevivedEvent
from sims4communitylib.events.sim.events.sim_set_current_outfit import S4CLSimSetCurrentOutfitEvent
from sims4communitylib.events.sim.events.sim_skill_leveled_up import S4CLSimSkillLeveledUpEvent
from sims4communitylib.events.sim.events.sim_spawned import S4CLSimSpawnedEvent
from sims4communitylib.events.sim.events.sim_trait_added import S4CLSimTraitAddedEvent
from sims4communitylib.events.sim.events.sim_trait_removed import S4CLSimTraitRemovedEvent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.skill import Skill
from traits.trait_tracker import TraitTracker
from traits.traits import Trait

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_sim_event_dispatcher')


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

    def _on_sim_died(self, sim_info: SimInfo, death_type: CommonDeathType, is_off_lot_death: bool, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimDiedEvent(sim_info, death_type, is_off_lot_death))

    def _on_sim_revived(self, sim_info: SimInfo, previous_death_type: CommonDeathType, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimRevivedEvent(sim_info, previous_death_type))

    def _pre_sim_despawned(self, sim_info: SimInfo, *_, **__) -> bool:
        return CommonEventRegistry.get().dispatch(S4CLSimPreDespawnedEvent(sim_info))

    def _on_sim_changing_age(self, sim_info: SimInfo, new_age: Age, current_age: Age, *_, **__) -> bool:
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        return CommonEventRegistry.get().dispatch(S4CLSimChangingAgeEvent(CommonSimUtils.get_sim_info(sim_info), CommonAge.convert_from_vanilla(current_age), CommonAge.convert_from_vanilla(new_age)))

    def _on_sim_change_age(self, sim_info: SimInfo, new_age: Age, current_age: Age, *_, **__) -> bool:
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

    def _on_sim_trait_added(self, trait_tracker: TraitTracker, trait: Trait, *_, **__) -> None:
        sim_info = trait_tracker.get_sim_info_from_provider()
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimTraitAddedEvent(sim_info, trait, trait_tracker))

    def _on_sim_trait_removed(self, trait_tracker: TraitTracker, trait: Trait, *_, **__) -> None:
        sim_info = trait_tracker.get_sim_info_from_provider()
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimTraitRemovedEvent(sim_info, trait, trait_tracker))

    def _on_sim_buff_added(self, buff: Buff, sim_id: int) -> None:
        sim_info = CommonSimUtils.get_sim_info(sim_id)
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimBuffAddedEvent(sim_info, buff))

    def _on_sim_buff_removed(self, buff: Buff, sim_id: int) -> None:
        sim_info = CommonSimUtils.get_sim_info(sim_id)
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimBuffRemovedEvent(sim_info, buff))

    def _on_sim_set_current_outfit(self, sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]) -> None:
        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        CommonEventRegistry.get().dispatch(S4CLSimSetCurrentOutfitEvent(sim_info, CommonOutfitUtils.get_current_outfit(sim_info), outfit_category_and_index))

    def _after_sim_set_current_outfit(self, sim_info: SimInfo, previous_outfit_category_and_index: Tuple[OutfitCategory, int], outfit_category_and_index: Tuple[OutfitCategory, int]) -> None:
        CommonEventRegistry.get().dispatch(S4CLSimAfterSetCurrentOutfitEvent(sim_info, previous_outfit_category_and_index, outfit_category_and_index))

    def _on_skill_leveled_up(self, skill: Skill, old_skill_level: int, new_skill_level: int) -> None:
        if skill.tracker is None or skill.tracker._owner is None:
            return
        sim_info = CommonSimUtils.get_sim_info(skill.tracker._owner)
        CommonEventRegistry.get().dispatch(S4CLSimSkillLeveledUpEvent(sim_info, skill, old_skill_level, new_skill_level))

    def _on_object_added_to_sim_inventory(self, sim: Sim, added_game_object: GameObject) -> None:
        sim_info = CommonSimUtils.get_sim_info(sim)
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLGameObjectAddedToSimInventoryEvent(sim_info, added_game_object))

    def _on_object_removed_from_sim_inventory(self, sim: Sim, removed_game_object: GameObject) -> None:
        sim_info = CommonSimUtils.get_sim_info(sim)
        if sim_info is None:
            return
        CommonEventRegistry.get().dispatch(S4CLGameObjectPreRemovedFromSimInventoryEvent(sim_info, removed_game_object))

    def _on_relationship_bit_added(self, sim_id_a: int, sim_id_b: int, relationship_bit: RelationshipBit) -> None:
        sim_info_a = CommonSimUtils.get_sim_info(sim_id_a)
        if sim_info_a is None:
            return
        sim_info_b = CommonSimUtils.get_sim_info(sim_id_b)
        if sim_info_b is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimRelationshipBitAddedEvent(sim_info_a, sim_info_b, relationship_bit))

    def _on_relationship_bit_removed(self, sim_id_a: int, sim_id_b: int, relationship_bit: RelationshipBit) -> None:
        sim_info_a = CommonSimUtils.get_sim_info(sim_id_a)
        if sim_info_a is None:
            return
        sim_info_b = CommonSimUtils.get_sim_info(sim_id_b)
        if sim_info_b is None:
            return
        CommonEventRegistry.get().dispatch(S4CLSimRelationshipBitRemovedEvent(sim_info_a, sim_info_b, relationship_bit))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.__init__.__name__, handle_exceptions=False)
def _common_on_sim_init(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_init(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.load_sim_info.__name__, handle_exceptions=False)
def _common_on_sim_load(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_load(self, *args, **kwargs)
    return result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimSpawner, SimSpawner.spawn_sim.__name__, handle_exceptions=False)
def _common_on_sim_spawn(original, cls, *args, **kwargs) -> Any:
    result = original(*args, **kwargs)
    if result:
        CommonSimEventDispatcherService.get()._on_sim_spawned(*args, **kwargs)
    return result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.destroy.__name__, handle_exceptions=False)
def _common_on_sim_despawn(original, self, *args, **kwargs) -> Any:
    CommonSimEventDispatcherService.get()._pre_sim_despawned(CommonSimUtils.get_sim_info(self), *args, **kwargs)
    return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), DeathTracker, DeathTracker.set_death_type.__name__)
def _common_on_sim_set_death_type(original, self, death_type: Union[DeathType, None], is_off_lot_death: bool = False, *_, **__) -> Any:
    previous_death_type = self._death_type
    original_result = original(self, death_type, is_off_lot_death=is_off_lot_death, *_, **__)
    if death_type is None and previous_death_type is None:
        return original_result

    sim_info = CommonSimUtils.get_sim_info(self._sim_info)
    if death_type is None:
        CommonSimEventDispatcherService.get()._on_sim_revived(sim_info, CommonDeathType.convert_from_vanilla(previous_death_type))
    else:
        if previous_death_type is None:
            CommonSimEventDispatcherService.get()._on_sim_died(sim_info, CommonDeathType.convert_from_vanilla(death_type), is_off_lot_death)
    return original_result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), DeathTracker, DeathTracker.clear_death_type.__name__)
def _common_on_sim_clear_death_type(original, self, *_, **__) -> Any:
    previous_death_type = self._death_type
    original_result = original(self, *_, **__)
    if previous_death_type is None:
        return original_result
    sim_info = CommonSimUtils.get_sim_info(self._sim_info)
    CommonSimEventDispatcherService.get()._on_sim_revived(sim_info, CommonDeathType.convert_from_vanilla(previous_death_type))
    return original_result


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Skill, Skill.on_skill_level_up.__name__, handle_exceptions=False)
def _common_on_sim_skill_level_up(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    if result:
        CommonSimEventDispatcherService.get()._on_skill_leveled_up(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), AgingMixin, AgingMixin.change_age.__name__, handle_exceptions=False)
def _common_on_sim_change_age(original, self, *args, **kwargs) -> Any:
    CommonSimEventDispatcherService.get()._on_sim_changing_age(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_change_age(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OccultTracker, OccultTracker.add_occult_type.__name__, handle_exceptions=False)
def _common_on_sim_add_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_add_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OccultTracker, OccultTracker.switch_to_occult_type.__name__, handle_exceptions=False)
def _common_on_sim_change_occult_type(original, self, *args, **kwargs) -> Any:
    CommonSimEventDispatcherService.get()._on_sim_changing_occult_type(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_changed_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), OccultTracker, OccultTracker.remove_occult_type.__name__, handle_exceptions=False)
def _common_on_sim_remove_occult_type(original, self, *args, **kwargs) -> Any:
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_remove_occult_type(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.set_current_outfit.__name__, handle_exceptions=False)
def _common_on_sim_set_current_outfit(original, self, *args, **kwargs) -> Any:
    old_outfit_category_and_index = CommonOutfitUtils.get_current_outfit(self)
    CommonSimEventDispatcherService.get()._on_sim_set_current_outfit(self, *args, **kwargs)
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._after_sim_set_current_outfit(self, old_outfit_category_and_index, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TraitTracker, TraitTracker._add_trait.__name__, handle_exceptions=False)
def _common_on_sim_trait_added(original, self: TraitTracker, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_trait_added(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), TraitTracker, TraitTracker._remove_trait.__name__, handle_exceptions=False)
def _common_on_sim_trait_removed(original, self: TraitTracker, *args, **kwargs):
    result = original(self, *args, **kwargs)
    CommonSimEventDispatcherService.get()._on_sim_trait_removed(self, *args, **kwargs)
    return result


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_register_buff_added_or_removed_on_sim_spawned(event_data: S4CLSimSpawnedEvent) -> bool:
    from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
    buff_component: BuffComponent = CommonBuffUtils.get_buff_component(event_data.sim_info)
    if not buff_component:
        return False

    dispatcher_service = CommonSimEventDispatcherService()
    if dispatcher_service._on_sim_buff_added not in buff_component.on_buff_added:
        buff_component.on_buff_added.append(dispatcher_service._on_sim_buff_added)

    if dispatcher_service._on_sim_buff_removed not in buff_component.on_buff_removed:
        buff_component.on_buff_removed.append(dispatcher_service._on_sim_buff_removed)
    return True


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.on_object_added_to_inventory.__name__, handle_exceptions=False)
def _common_on_object_added_to_sim_inventory(original, self: Sim, obj: ScriptObject, *args, **kwargs):
    result = original(self, obj, *args, **kwargs)
    if isinstance(obj, GameObject):
        CommonSimEventDispatcherService.get()._on_object_added_to_sim_inventory(self, obj)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.on_object_removed_from_inventory.__name__, handle_exceptions=False)
def _common_on_object_removed_from_sim_inventory(original, self: Sim, obj: ScriptObject, *args, **kwargs):
    if isinstance(obj, GameObject):
        CommonSimEventDispatcherService.get()._on_object_removed_from_sim_inventory(self, obj)
    result = original(self, obj, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Relationship, Relationship.add_relationship_bit.__name__)
def _common_on_add_relationship_bit(original, self: Relationship, actor_sim_id: int, target_sim_id: int, bit_to_add: RelationshipBit, *_, **__):
    try:
        result = original(self, actor_sim_id, target_sim_id, bit_to_add, *_, **__)
        CommonSimEventDispatcherService()._on_relationship_bit_added(actor_sim_id, target_sim_id, bit_to_add)
    except Exception as ex:
        log.format_error_with_message('Error occurred when adding relationship bit.', bit_to_add=bit_to_add, source_sim=CommonSimUtils.get_sim_info(actor_sim_id), target_sim=CommonSimUtils.get_sim_info(target_sim_id), exception=ex)
        raise ex
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), RelationshipData, RelationshipData.remove_bit.__name__)
def _common_on_remove_relationship_bit(original, self: RelationshipData, bit: RelationshipBit, *_, **__):
    result = original(self, bit, *_, **__)
    (actor_sim_id, target_sim_id) = self._sim_ids()
    CommonSimEventDispatcherService()._on_relationship_bit_removed(actor_sim_id, target_sim_id, bit)
    return result
