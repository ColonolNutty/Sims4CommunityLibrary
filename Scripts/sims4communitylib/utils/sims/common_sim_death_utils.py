"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Union, Callable, Iterator, Dict

from interactions.utils.death import DeathType, DeathTracker
from objects.game_object import GameObject
from sims.ghost import Ghost
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_transform import CommonTransform
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.enums.common_region_id import CommonRegionId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.objects.common_object_spawn_utils import CommonObjectSpawnUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from sims4communitylib.utils.time.common_alarm_utils import CommonAlarmUtils


class CommonSimDeathUtils(_HasS4CLClassLog):
    """Utilities for manipulating the body of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_death_utils'

    @classmethod
    def is_dead(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_dead(sim_info)

        Determine if a Sim is dead.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if it passes. False, if it fails.
        :rtype: CommonTestResult
        """
        if cls.get_death_type(sim_info) != CommonDeathType.NONE:
            return CommonTestResult(True, reason=f'{sim_info} is dead.', tooltip_text=CommonStringId.S4CL_SIM_IS_DEAD, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not dead.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_DEAD, tooltip_tokens=(sim_info,))

    @classmethod
    def get_sim_info_for_all_dead_sims_generator(
        cls,
        death_type: Union[CommonDeathType, DeathType] = None,
        include_sim_callback: Callable[[SimInfo], Union[bool, CommonExecutionResult, CommonTestResult]] = None
    ) -> Iterator[SimInfo]:
        """get_sim_info_for_all_dead_sims_generator(death_type=None, include_sim_callback=None)

        Retrieve a SimInfo object for each and every Dead Sim.

        :param death_type: If specified, only Sims with this type of death will be returned, otherwise all Sims will be returned.
        :type death_type: Union[CommonDeathType, DeathType], optional
        :param include_sim_callback: If the result of this callback is True, the sim will be included in the results. If set to None, All sims will be included.
        :type include_sim_callback: Callable[[SimInfo], bool], optional
        :return: An iterator of all Sims matching the `include_sim_callback` filter.
        :rtype: Iterator[SimInfo]
        """
        if death_type is not None:
            death_type = CommonDeathType.convert_from_vanilla(death_type)

        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=include_sim_callback):
            if sim_info is None:
                continue
            is_dead_result = cls.is_dead(sim_info)
            if not is_dead_result:
                continue
            death_tracker = cls.get_death_tracker(sim_info)
            if death_tracker is None:
                _death_type = None
            else:
                _death_type = death_tracker.death_type
            if death_type is not None and death_type != CommonDeathType.NONE:
                sim_death_type = cls.get_death_type(sim_info)
                if sim_death_type == CommonDeathType.NONE:
                    continue
                if sim_death_type != death_type:
                    continue
            yield sim_info

    @classmethod
    def kill_sim(
        cls,
        sim_info: SimInfo,
        death_type: Union[CommonDeathType, DeathType]
    ) -> CommonExecutionResult:
        """kill_sim(sim_info, death_type)

        Kill a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param death_type: The type of death to invoke upon the Sim.
        :type death_type: Union[CommonDeathType, DeathType]
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        if CommonSimUtils.get_sim_instance(sim_info) is None:
            is_off_lot_death = True
        else:
            is_off_lot_death = False
        death_tracker = cls.get_death_tracker(sim_info)
        if death_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} did not have a death tracker.', hide_tooltip=True)
        is_dead_result = cls.is_dead(sim_info)
        if is_dead_result:
            return is_dead_result
        if death_tracker.is_ghost:
            return CommonExecutionResult(False, reason=f'{sim_info} is already a ghost.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_GHOST, tooltip_tokens=(sim_info,))
        death_type = CommonDeathType.convert_from_vanilla(death_type)
        if not is_off_lot_death:
            def _on_object_spawned(_death_object: Union[GameObject, None]) -> None:
                if _death_object is None:
                    return
                death_interaction_id = cls.get_death_interaction(sim_info, death_type)
                if death_interaction_id:
                    enqueue_result = CommonSimInteractionUtils.queue_interaction(sim_info, death_interaction_id, target=_death_object)
                    if not enqueue_result:
                        cls.get_log().format_error_with_message(f'Failed to kill {sim_info} via {death_type.name}.', result=enqueue_result)
                    else:
                        cls.get_log().format_with_message('Successfully queued death interaction.', result=enqueue_result)

            death_object = cls._spawn_death_related_object(sim_info, death_type, _on_object_spawned)
            if death_object is not None:
                def _on_destroy_alarm_triggered(_) -> None:
                    CommonObjectSpawnUtils.schedule_object_for_destroy(death_object)

                time_until_object_destroy = CommonTimeUtils.create_time_span(hours=1)
                CommonAlarmUtils.schedule_alarm(CommonSimDeathUtils, time_until_first_occurrence=time_until_object_destroy, on_alarm_triggered_callback=_on_destroy_alarm_triggered)
                return CommonExecutionResult.TRUE

        sim_household = CommonHouseholdUtils.get_household(sim_info)
        death_tracker.set_death_type(CommonDeathType.convert_to_vanilla(death_type), is_off_lot_death=is_off_lot_death)
        Ghost.make_ghost_if_needed(sim_info)
        if sim_household is not None:
            CommonHouseholdUtils.move_sim_to_household(sim_info, household_id=CommonHouseholdUtils.get_id(sim_household))
        return CommonExecutionResult.TRUE

    @classmethod
    def _spawn_death_related_object(cls, sim_info: SimInfo, death_type: CommonDeathType, on_object_spawned: Callable[[Union[GameObject, None]], None]) -> Union[GameObject, None]:
        mapping: Dict[CommonDeathType, int] = {
            CommonDeathType.COW_PLANT: 22481,  # cowplantGEN_01
            CommonDeathType.MURPHY_BED: 235916,  # bedMurphy_SP16GEN_set1
            CommonDeathType.MOTHER_PLANT: 208953,  # motherPlant_GP07GEN
        }

        chosen_object_definition_id = mapping.get(death_type, None)

        vending_machine_ids = (
            293171,  # object_VendingMachine_HighSchool
            256973,  # object_VendingMachine_Gachapon_Default
            256971,  # vendingMachine_ColdDrinkAndSnack
            256970,  # vendingMachine_HotFoodAndDrink
        )

        if death_type == CommonDeathType.VENDING_MACHINE:
            chosen_object_definition_id = random.choice(vending_machine_ids)

        if chosen_object_definition_id is None or chosen_object_definition_id == 0:
            on_object_spawned(None)
            return None

        def _on_spawned(_game_object: GameObject):
            if _game_object is None:
                on_object_spawned(None)
                return

            if death_type == CommonDeathType.MURPHY_BED:
                murphy_bed_open_state = 228113  # murphy_Bed_Values_Open
                CommonObjectStateUtils.set_object_state(_game_object, murphy_bed_open_state)

            if death_type == CommonDeathType.COW_PLANT:
                cow_plant_mature_state = 32491  # Cowplant_GrowthState_Mature
                CommonObjectStateUtils.set_object_state(_game_object, cow_plant_mature_state)
                cow_plant_hungry_state = 15231  # Hunger_3_Hungry
                CommonObjectStateUtils.set_object_state(_game_object, cow_plant_hungry_state)
                CommonBuffUtils.add_buff(sim_info, 12396)  # Buff_Drained
            on_object_spawned(_game_object)

        location = CommonSimLocationUtils.get_location(sim_info)
        loc_transform = location.transform
        loc_translation = loc_transform.translation
        new_transform = CommonVector3(loc_translation.x + 1, loc_translation.y, loc_translation.z)
        spawn_location = CommonLocation(CommonTransform(new_transform, loc_transform.orientation), location.routing_surface)

        spawned_object = CommonObjectSpawnUtils.spawn_object_on_lot(chosen_object_definition_id, spawn_location, post_object_spawned_callback=_on_spawned)
        if spawned_object is None:
            on_object_spawned(None)
            return None
        return spawned_object

    @classmethod
    def get_death_interaction(cls, sim_info: SimInfo, death_type: CommonDeathType) -> Union[int, None]:
        """get_death_interaction(sim_info, death_type)

        Retrieve an appropriate death interaction for the Sim to die by.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param death_type: The type of death slated for the Sim.
        :type death_type: CommonDeathType
        :return: The decimal identifier of the interaction appropriate for the Sim to play a death animation with or None if not found.
        :rtype: int
        """
        mapping: Dict[CommonDeathType, int] = {
            CommonDeathType.ANGER: 9252,  # death_Anger
            CommonDeathType.CLIMBING_ROUTE: 250185,  # death_ClimbingRoute
            CommonDeathType.DEATH_FLOWER_ARRANGEMENT: 190745,  # death_ElderExhaustion_DeathFlower
            CommonDeathType.ELDER_EXHAUSTION: 9316,  # death_ElderExhaustion
            CommonDeathType.EMBARRASSMENT: 32314,  # death_Embarrassment
            CommonDeathType.FIRE: 77372,  # death_Fire
            CommonDeathType.FLIES: 231091,  # death_Flies
            CommonDeathType.FROZEN: 182162,  # death_Frozen
            CommonDeathType.HUNGER: 13299,  # death_Hunger
            CommonDeathType.KILLER_CHICKEN: 267938,  # death_AnimalObjects_Chicken_DeadOnGround
            CommonDeathType.KILLER_RABBIT: 259988,  # death_AnimalObjects_KillerRabbit
            CommonDeathType.LAUGHTER: 9297,  # death_Laughter
            CommonDeathType.LIGHTNING: 186301,  # death_Electrocution_Lightning
            CommonDeathType.METEORITE: 286935,  # death_Meteorite
            CommonDeathType.MOTHER_PLANT: 204098,  # death_MotherPlant
            CommonDeathType.MURPHY_BED: 231080,  # death_MurphyBed_NoLoveseat
            CommonDeathType.OVERHEAT: 183022,  # death_Overheat
            CommonDeathType.POISON: 176190,  # death_Poison
            CommonDeathType.PUFFERFISH: 143418,  # death_Initiator_Pufferfish
            CommonDeathType.RODENT_DISEASE: 181916,  # death_RodentDisease
            CommonDeathType.STEAM: 119504,  # death_SteamRoom
            # Stink Bomb does not have an associated interaction.
            # CommonDeathType.STINK_BOMB: 0,
            CommonDeathType.SUN: 151542,  # death_Vampire_Sun
            # Urban Myth is reserved for Sims that are already a ghost.
            # CommonDeathType.URBAN_MYTH: 0,
            CommonDeathType.VENDING_MACHINE: 249705,  # death_VendingMachine
            CommonDeathType.WITCH_OVERLOAD: 216969,  # death_WitchOverload
        }

        if death_type == CommonDeathType.OLD_AGE:
            if CommonSpeciesUtils.is_human(sim_info):
                if CommonOccultUtils.is_robot(sim_info):
                    return 220401  # death_Solo_HumanoidRobot
                return 13300  # death_OldAge
            elif CommonSpeciesUtils.is_cat(sim_info):
                return 159835  # death_OldAge_Cat
            elif CommonSpeciesUtils.is_dog(sim_info):
                return 159868  # death_OldAge_Dog
            elif CommonSpeciesUtils.is_horse(sim_info):
                return 321074  # death_OldAge_Horse
            else:
                return 265869  # death_OldAge_Fox

        if death_type == CommonDeathType.COW_PLANT:
            if CommonOccultUtils.is_robot(sim_info):
                return 229340  # death_Cowplant_HumanoidRobot
            return 13298  # death_Cowplant

        # 220401,  # death_Solo_HumanoidRobot
        # 132535,  # death_Pufferfish_SeatedAtSurface
        # 132534,  # death_Pufferfish
        # 132609,  # Death_Pufferfish_Seated

        ocean_drown_id = 211504  # Death_Drowning_Ocean
        drown_interaction_ids = (
            103463,  # death_Drown
            ocean_drown_id,
        )
        if death_type == CommonDeathType.DROWN:
            if CommonInteractionUtils.load_interaction_by_id(ocean_drown_id) is None:
                return 103463  # death_Drown
            return random.choice(drown_interaction_ids)

        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is not None:
            if death_type == CommonDeathType.ELECTROCUTION:
                if CommonLocationUtils.is_current_region(CommonRegionId.JUNGLE):
                    return 182673  # death_Electrocution_Jungle
                if sim.is_outside:
                    return 186301  # death_Electrocution_Lightning
                if CommonOccultUtils.is_robot(sim_info):
                    return 228257  # humanoid_Robots_ElectricOverload_Death
                return 8650  # death_Electrocution

        # 284361
        # 284362
        #
        # 98476  # rescueNeglectedChild
        # 155605  # rescueNeglectedToddler
        # 103810  # death_Netherworld
        return mapping.get(death_type, None)

    @classmethod
    def revive_sim(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """revive_sim(sim_info)

        Revive a Dead Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of executing the function. True, if successful. False, if not.
        :rtype: CommonExecutionResult
        """
        death_tracker = cls.get_death_tracker(sim_info)
        if death_tracker is None:
            return CommonExecutionResult(False, reason=f'{sim_info} did not have a death tracker.', hide_tooltip=True)
        if death_tracker.death_type is None:
            return CommonExecutionResult(True, reason=f'{sim_info} is not dead.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_DEAD, tooltip_tokens=(sim_info,))
        urn_game_object = Ghost.get_urnstone_for_sim_id(CommonSimUtils.get_sim_id(sim_info))
        death_tracker.clear_death_type()
        Ghost.remove_ghost_from_sim(sim_info)
        game_object = CommonObjectUtils.get_game_object(urn_game_object)
        CommonObjectSpawnUtils.schedule_object_for_destroy(game_object)
        return CommonExecutionResult.TRUE

    @classmethod
    def get_death_type(cls, sim_info: SimInfo) -> CommonDeathType:
        """get_death_type(sim_info)

        Retrieve the type of Death the Sim was faced with.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The type of death the Sim succumbed to or NONE if the Sim is not dead.
        :rtype: CommonDeathType
        """
        death_tracker = cls.get_death_tracker(sim_info)
        if death_tracker is None:
            return CommonDeathType.NONE
        return CommonDeathType.convert_from_vanilla(death_tracker.death_type)

    @classmethod
    def get_death_tracker(cls, sim_info: SimInfo) -> Union[DeathTracker, None]:
        """get_death_tracker(sim_info)

        Retrieve the death tracker for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The death tracker for the Sim or None if not found.
        :rtype: Union[DeathTracker, None]
        """
        if sim_info is None:
            return None
        return sim_info.death_tracker


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_death',
    'Print information about a Sim and their death.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_print_death(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if not CommonSimDeathUtils.is_dead(sim_info):
        output(f'Sim {sim_info} is not dead.')
        return
    death_type = CommonSimDeathUtils.get_death_type(sim_info)
    if death_type == CommonDeathType.NONE:
        output(f'Sim {sim_info} died in an unknown way.')
        return
    output(f'Sim {sim_info} died via {death_type.name}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.kill_sim',
    'Greet a Sim with the Kiss of Death.',
    command_arguments=(
        CommonConsoleCommandArgument('death_type', 'Name of Death Type', 'The type of death to bring upon a Sim.', is_optional=True, default_value='Random'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_kill_all_sims(output: CommonConsoleCommandOutput, death_type: CommonDeathType = CommonDeathType.NONE, sim_info: SimInfo = None):
    if death_type == CommonDeathType.NONE:
        death_type = CommonDeathType.convert_from_vanilla(DeathType.get_random_death_type())
    household_count = CommonHouseholdUtils.get_number_of_sims_in_household_of_sim(sim_info)
    if household_count == 1:
        output('Bad things can happen when you kill the only member of a Household!')
        return False
    output(f'Killing Sim {sim_info} with death {death_type.name}.')
    result = CommonSimDeathUtils.kill_sim(sim_info, death_type)
    if result:
        output(f'Successfully killed {sim_info} with death {death_type.name}.')
    else:
        output(f'Failed to kill {sim_info} with death {death_type.name}. Reason: {result}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.kill_all_sims',
    'Greet all Sims with the Kiss of Death.',
    command_arguments=(
        CommonConsoleCommandArgument('death_type', 'Name of Death Type', 'The type of death to bring upon the Sims.', is_optional=True, default_value='Random'),
    )
)
def _common_kill_sim(output: CommonConsoleCommandOutput, death_type: CommonDeathType = CommonDeathType.NONE):
    output(f'Killing Sims.')
    kill_count = 0
    saved_count = 0
    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=CommonFunctionUtils.run_predicate_with_reversed_result(CommonSimDeathUtils.is_dead)):
        household_count = CommonHouseholdUtils.get_number_of_sims_in_household_of_sim(sim_info)
        if household_count == 1:
            saved_count += 1
            continue
        if death_type == CommonDeathType.NONE:
            death_type_override = CommonDeathType.convert_from_vanilla(DeathType.get_random_death_type())
        else:
            death_type_override = death_type
        result = CommonSimDeathUtils.kill_sim(sim_info, death_type_override)
        if result:
            kill_count += 1
        else:
            saved_count += 1
    output(f'{kill_count} Sim(s) have met with a terrible fate.')
    output(f'{saved_count} Sim(s) were spared a terrible fate.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.revive_sim',
    'Revive a Sim and stop them being a ghost.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to modify.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_revive_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output(f'Reviving Sim {sim_info}.')
    result = CommonSimDeathUtils.revive_sim(sim_info)
    if result:
        output(f'Successfully revived {sim_info}.')
    else:
        output(f'Failed to revive {sim_info}. Reason: {result}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.revive_all_sims',
    'Revive all Sims and stop them from being spooky.'
)
def _common_revive_sim(output: CommonConsoleCommandOutput):
    output(f'Reviving All Sims.')
    revive_count = 0
    for sim_info in CommonSimDeathUtils.get_sim_info_for_all_dead_sims_generator():
        result = CommonSimDeathUtils.revive_sim(sim_info)
        if result:
            revive_count += 1
    output(f'{revive_count} Sim(s) have been blessed with life anew.')
