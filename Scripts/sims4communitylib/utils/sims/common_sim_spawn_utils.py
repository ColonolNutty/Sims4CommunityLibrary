"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from typing import Union, Tuple, Callable, Any, Iterator
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if not ON_RTD:
    import build_buy
    try:
        import _buildbuy
    except ImportError:
        # noinspection SpellCheckingInspection
        _buildbuy = build_buy
    import services
    from interactions.interaction_finisher import FinishingType
    from sims.household import Household
    from sims.sim_info import SimInfo
    from sims.sim_spawner import SimCreator, SimSpawner
    from sims4.commands import Command, CommandType, CheatOutput
    from animation.posture_manifest import Hand
    from interactions.si_state import SIState
    from objects.object_enums import ResetReason
    from postures import posture_graph
    from postures.posture_specs import get_origin_spec, PostureSpecVariable
    from postures.posture_state import PostureState
else:
    # noinspection PyMissingOrEmptyDocstring
    class FinishingType:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Household:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class SimInfo:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class SimCreator:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class SimSpawner:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Command:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class CommandType:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class CheatOutput:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Hand:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class SIState:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class ResetReason:
        pass

    # noinspection PyMissingOrEmptyDocstring,PyMissingTypeHints
    def posture_graph(*_, **__):
        pass

    # noinspection PyMissingOrEmptyDocstring,PyMissingTypeHints
    def get_origin_spec(*_, **__):
        pass

    # noinspection PyMissingOrEmptyDocstring
    class PostureSpecVariable:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class PostureState:
        pass


class CommonSimSpawnUtils:
    """Utilities for creating, spawning, despawning, and resetting Sims.

    """

    @staticmethod
    def create_sim_info(
        species: CommonSpecies,
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_sim_info(\
            species,\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Sim.

        :param species: The species to create a SimInfo for.
        :type species: CommonSpecies
        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is an empty string.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is an empty string.
        :type last_name: str, optional
        :param trait_ids: The decimal identifiers of the Traits to add to the created Sim. Default is an empty collection.
        :type trait_ids: Tuple[int], optional
        :param household: The household to place the created Sim in. If None, the Sim will be placed in a hidden household. Default is None.
        :type household: Household, optional
        :param source: The reason for the Sims creation. Default is 'testing'.
        :type source: str, optional
        :return: The SimInfo of the created Sim or None if the Sim failed to be created.
        :rtype: SimInfo
        """
        return CommonSimSpawnUtils._create_sim_info(species, gender=gender, age=age, first_name=first_name, last_name=last_name, trait_ids=trait_ids, household=household, source=source)

    @staticmethod
    def create_human_sim_info(
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_human_sim_info(\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Human Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is an empty string.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is an empty string.
        :type last_name: str, optional
        :param trait_ids: The decimal identifiers of the Traits to add to the created Sim. Default is an empty collection.
        :type trait_ids: Tuple[int], optional
        :param household: The household to place the created Sim in. If None, the Sim will be placed in a hidden household. Default is None.
        :type household: Household, optional
        :param source: The reason for the Sims creation. Default is 'testing'.
        :type source: str, optional
        :return: The SimInfo of the created Sim or None if the Sim failed to be created.
        :rtype: SimInfo
        """
        return CommonSimSpawnUtils._create_sim_info(CommonSpecies.HUMAN, gender=gender, age=age, first_name=first_name, last_name=last_name, trait_ids=trait_ids, household=household, source=source)

    @staticmethod
    def create_large_dog_sim_info(
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_large_dog_sim_info(\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Large Dog Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is an empty string.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is an empty string.
        :type last_name: str, optional
        :param trait_ids: The decimal identifiers of the Traits to add to the created Sim. Default is an empty collection.
        :type trait_ids: Tuple[int], optional
        :param household: The household to place the created Sim in. If None, the Sim will be placed in a hidden household. Default is None.
        :type household: Household, optional
        :param source: The reason for the Sims creation. Default is 'testing'.
        :type source: str, optional
        :return: The SimInfo of the created Sim or None if the Sim failed to be created.
        :rtype: SimInfo
        """
        return CommonSimSpawnUtils._create_sim_info(CommonSpecies.LARGE_DOG, gender=gender, age=age, first_name=first_name, last_name=last_name, trait_ids=trait_ids, household=household, source=source)

    @staticmethod
    def create_small_dog_sim_info(
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_small_dog_sim_info(\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Small Dog Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is an empty string.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is an empty string.
        :type last_name: str, optional
        :param trait_ids: The decimal identifiers of the Traits to add to the created Sim. Default is an empty collection.
        :type trait_ids: Tuple[int], optional
        :param household: The household to place the created Sim in. If None, the Sim will be placed in a hidden household. Default is None.
        :type household: Household, optional
        :param source: The reason for the Sims creation. Default is 'testing'.
        :type source: str, optional
        :return: The SimInfo of the created Sim or None if the Sim failed to be created.
        :rtype: SimInfo
        """
        return CommonSimSpawnUtils._create_sim_info(CommonSpecies.SMALL_DOG, gender=gender, age=age, first_name=first_name, last_name=last_name, trait_ids=trait_ids, household=household, source=source)

    @staticmethod
    def create_cat_sim_info(
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_cat_sim_info(\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Cat Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is an empty string.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is an empty string.
        :type last_name: str, optional
        :param trait_ids: The decimal identifiers of the Traits to add to the created Sim. Default is an empty collection.
        :type trait_ids: Tuple[int], optional
        :param household: The household to place the created Sim in. If None, the Sim will be placed in a hidden household. Default is None.
        :type household: Household, optional
        :param source: The reason for the Sims creation. Default is 'testing'.
        :type source: str, optional
        :return: The SimInfo of the created Sim or None if the Sim failed to be created.
        :rtype: SimInfo
        """
        return CommonSimSpawnUtils._create_sim_info(CommonSpecies.CAT, gender=gender, age=age, first_name=first_name, last_name=last_name, trait_ids=trait_ids, household=household, source=source)

    @staticmethod
    def create_fox_sim_info(
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_fox_sim_info(\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Fox Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is an empty string.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is an empty string.
        :type last_name: str, optional
        :param trait_ids: The decimal identifiers of the Traits to add to the created Sim. Default is an empty collection.
        :type trait_ids: Tuple[int], optional
        :param household: The household to place the created Sim in. If None, the Sim will be placed in a hidden household. Default is None.
        :type household: Household, optional
        :param source: The reason for the Sims creation. Default is 'testing'.
        :type source: str, optional
        :return: The SimInfo of the created Sim or None if the Sim failed to be created.
        :rtype: SimInfo
        """
        return CommonSimSpawnUtils._create_sim_info(CommonSpecies.FOX, gender=gender, age=age, first_name=first_name, last_name=last_name, trait_ids=trait_ids, household=household, source=source)

    @staticmethod
    def _create_sim_info(
        species: CommonSpecies,
        gender: CommonGender=None,
        age: CommonAge=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        household = household or CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_age = CommonAge.convert_to_vanilla(age)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        if species is None:
            raise AssertionError(f'Invalid species specified for SimInfo creation! {species}')
        sim_creator = SimCreator(gender=vanilla_gender, age=vanilla_age, species=vanilla_species, first_name=first_name or SimSpawner.get_random_first_name(vanilla_gender, species=vanilla_species), last_name=last_name, traits=trait_ids)
        (sim_info_list, _) = SimSpawner.create_sim_infos((sim_creator,), household=household, generate_deterministic_sim=True, creation_source=source)
        if not sim_info_list:
            return None
        return sim_info_list[0]

    @staticmethod
    def spawn_sim(sim_info: SimInfo, location: CommonLocation=None, position: CommonVector3=None, **kwargs) -> bool:
        """spawn_sim(sim_info, location=None, position=None, **kwargs)

        Spawn a Sim.

        ..note:: Do not provide sim_position or sim_location in kwargs as they are already specified as location and position.

        :param sim_info: The Sim to Spawn.
        :type sim_info: SimInfo
        :param location: The location to spawn the Sim at. Default is None.
        :type location: CommonLocation, optional
        :param position: The position to spawn the Sim at. Default is None.
        :type position: CommonVector3, optional
        :return: True, if the Sim was spawned successfully. False, if not.
        :rtype: bool
        """
        SimSpawner.spawn_sim(sim_info, sim_location=location, sim_position=position, **kwargs)
        return True

    @staticmethod
    def spawn_sim_at_active_sim_location(sim_info: SimInfo, **kwargs) -> bool:
        """spawn_sim_at_active_sim_location(sim_info, **kwargs)

        Spawn a Sim at the location of the Active Sim.

        :param sim_info: The Sim to Spawn.
        :type sim_info: SimInfo
        :return: True, if the Sim was spawned successfully. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_location = CommonSimLocationUtils.get_location(active_sim_info)
        active_position = None
        if active_location is None:
            active_position = CommonSimLocationUtils.get_position(active_sim_info)
        return CommonSimSpawnUtils.spawn_sim(sim_info, location=active_location, position=active_position, **kwargs)

    @staticmethod
    def despawn_sim(sim_info: SimInfo, source: str=None, cause: str=None, **kwargs) -> bool:
        """despawn_sim(sim_info, source=None, cause=None, **kwargs)

        Despawn a Sim.

        :param sim_info: The Sim to despawn.
        :type sim_info: SimInfo
        :param source: The source of the destruction. Default is None.
        :type source: str, optional
        :param cause: The cause of the destruction. Default is None.
        :type cause: str, optional
        :return: True, if the Sim was despawn successfully. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return True
        cause = cause or 'Sim despawned.'
        sim.destroy(source=source, cause=cause, **kwargs)
        return True

    @staticmethod
    def schedule_sim_for_despawn(sim_info: SimInfo, source: str=None, cause: str=None, on_despawn: Callable[[], None]=None, **kwargs) -> bool:
        """schedule_sim_for_despawn(sim_info, source=None, cause=None, on_despawn=None, **kwargs)

        Schedule a Sim to be despawned.

        :param sim_info: The Sim to despawn.
        :type sim_info: SimInfo
        :param source: The source of the destruction. Default is None.
        :type source: str, optional
        :param cause: The cause of the destruction. Default is None.
        :type cause: str, optional
        :param on_despawn: A callback that occurs after the Sim is despawned. Default is None.
        :type on_despawn: Callable[[], None], optional
        :return: True, if the Object was successfully scheduled for destruction. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            if on_despawn is not None:
                on_despawn()
            return True
        cause = cause or 'Sim despawned.'
        sim.schedule_destroy_asap(post_delete_func=on_despawn, source=source, cause=cause, **kwargs)
        return True

    @staticmethod
    def delete_sim(sim_info: SimInfo, source: str=None, cause: str=None, **kwargs) -> bool:
        """delete_sim(sim_info, source=None, cause=None, **kwargs)

        Delete a Sim.

        :param sim_info: The Sim to delete.
        :type sim_info: SimInfo
        :param source: The source of the destruction. Default is None.
        :type source: str, optional
        :param cause: The cause of the destruction. Default is None.
        :type cause: str, optional
        :return: True, if the Sim was deleted successfully. False, if not.
        :rtype: bool
        """
        if not CommonSimSpawnUtils.despawn_sim(sim_info, source=source, cause=cause, **kwargs):
            return False
        sim_info.remove_permanently()
        return True

    @staticmethod
    def soft_reset(sim_info: SimInfo, reset_reason: ResetReason=ResetReason.RESET_EXPECTED, hard_reset_on_exception: bool=False, source: Any=None, cause: Any='S4CL Soft Reset') -> bool:
        """soft_reset(sim_info, reset_reason=ResetReason.RESET_EXPECTED, hard_reset_on_exception=False, source=None, cause=None)

        Perform a soft reset on a Sim.

        :param sim_info: An instance of an Sim.
        :type sim_info: SimInfo
        :param reset_reason: The reason for the reset. Default is ResetReason.RESET_EXPECTED.
        :type reset_reason: ResetReason, optional
        :param hard_reset_on_exception: If set to True, a hard reset of the Object will be attempted upon an error occurring. If set to False, nothing will occur if the reset failed. Default is False.
        :type hard_reset_on_exception: bool, optional
        :param source: The source of the reset. Default is the GameObject.
        :type source: Any, optional
        :param cause: The cause of the reset. Default is 'S4CL Soft Reset'.
        :type cause: Any, optional
        :return: True, if the reset was successful. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return True
        # noinspection PyBroadException
        try:
            # noinspection PyArgumentList
            if sim._should_be_swimming() or _buildbuy.is_location_pool(services.current_zone_id(), sim.position, sim.location.level):
                posture_type = posture_graph.SIM_SWIM_POSTURE_TYPE
            else:
                posture_type = posture_graph.SIM_DEFAULT_POSTURE_TYPE

            if sim.queue is not None:
                for interaction in sim.queue:
                    interaction.cancel(FinishingType.KILLED, 'S4CL soft_reset sim.queue')
                sim.queue.on_reset()
                sim.queue.unlock()

            if sim.si_state is not None:
                for interaction in sim.si_state:
                    interaction.cancel(FinishingType.KILLED, 'S4CL soft_reset sim.si_state')
                # noinspection PyBroadException
                try:
                    sim.si_state.on_reset()
                except:
                    sim._si_state = SIState(sim)
                    sim.si_state.on_reset()
            else:
                sim._si_state = SIState(sim)
                sim.si_state.on_reset()

            if sim.ui_manager is not None:
                sim.ui_manager.remove_all_interactions()

            sim.socials_locked = False
            sim.last_affordance = None
            sim.two_person_social_transforms.clear()
            sim.on_reset_send_op(reset_reason)
            # noinspection PyPropertyAccess
            if sim.posture_state is not None:
                # noinspection PyPropertyAccess
                sim.posture_state.on_reset(reset_reason)

            sim._stop_animation_interaction()
            sim.asm_auto_exit.clear()
            sim._start_animation_interaction()
            # noinspection PyBroadException
            try:
                sim.posture_state = PostureState(sim, None, get_origin_spec(posture_type), {PostureSpecVariable.HAND: (Hand.LEFT,)})
            except:
                sim.posture_state = PostureState(sim, None, get_origin_spec(posture_graph.SIM_DEFAULT_POSTURE_TYPE), {PostureSpecVariable.HAND: (Hand.LEFT,)})

            sim._posture_target_refs.clear()
            sim.run_full_autonomy_next_ping()
            return True
        except:
            if hard_reset_on_exception:
                return CommonSimSpawnUtils.hard_reset(sim_info, reset_reason, source=source, cause=cause)
        return False

    @staticmethod
    def hard_reset(sim_info: SimInfo, reset_reason: ResetReason=ResetReason.RESET_EXPECTED, source: Any=None, cause: Any='S4CL Hard Reset') -> bool:
        """hard_reset(sim_info, reset_reason=ResetReason.RESET_EXPECTED, source=None, cause=None)

        Perform a hard reset on a SimInfo.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param reset_reason: The reason for the reset. Default is ResetReason.RESET_EXPECTED.
        :type reset_reason: ResetReason, optional
        :param source: The source of the reset. Default is the SimInfo.
        :type source: Any, optional
        :param cause: The cause of the reset. Default is 'S4CL Hard Reset'.
        :type cause: Any, optional
        :return: True, if the reset was successful. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return True

        # noinspection PyBroadException
        try:
            sim.reset(reset_reason, source=source or sim_info, cause=cause)
            return True
        except:
            return False

    @staticmethod
    def fade_in(sim_info: SimInfo, fade_duration: float=1.0, immediate: bool=False, additional_channels: Iterator[Tuple[int, int, int]]=None):
        """fade_in(sim_info, fade_duration=1.0)

        Fade a Sim to become visible.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param fade_duration: The number of milliseconds the fade effect should take to complete. Default is 1.0.
        :type fade_duration: float, optional
        :param immediate: If set to True, fade in will occur immediately. Default is False.
        :type immediate: bool, optional
        :param additional_channels: A collection of additional channels. The order of the inner tuple is Manager Id, Sim Id, and Mask. Default is None.
        :type additional_channels: Iterator[Tuple[int, int, int]], optional
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        sim.fade_in(fade_duration=fade_duration, immediate=immediate, additional_channels=additional_channels)

    @staticmethod
    def fade_out(sim_info: SimInfo, fade_duration: float=1.0, immediate: bool=False, additional_channels: Iterator[Tuple[int, int, int]]=None):
        """fade_out(sim_info, fade_duration=1.0, immediate=False, additional_channels=None)

        Fade a Sim to become invisible.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param fade_duration: The number of milliseconds the fade effect should take to complete. Default is 1.0.
        :type fade_duration: float, optional
        :param immediate: If set to True, fade out will occur immediately. Default is False.
        :type immediate: bool, optional
        :param additional_channels: A collection of additional channels. The order of the inner tuple is Manager Id, Sim Id, and Mask. Default is None.
        :type additional_channels: Iterator[Tuple[int, int, int]], optional
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return
        sim.fade_out(fade_duration=fade_duration, immediate=immediate, additional_channels=additional_channels)


@Command('s4clib.spawn_sims', command_type=CommandType.Live)
def _s4cl_spawn_sims(species_str: str, count: int=1, gender_str: str='male', age_str: str='adult', _connection: int=None):
    output = CheatOutput(_connection)
    species: CommonSpecies = CommonResourceUtils.get_enum_by_name(species_str.upper(), CommonSpecies, default_value=None)
    if species is None:
        output('{} is not a valid species. Valid Species: ({})'.format(gender_str, ', '.join(CommonSpecies.get_all_names())))
        return
    gender: CommonGender = CommonResourceUtils.get_enum_by_name(gender_str.upper(), CommonGender, default_value=None)
    if gender is None:
        output('{} is not a valid gender. Valid Genders: ({})'.format(gender_str, ', '.join(CommonGender.get_all_names())))
        return
    age: CommonAge = CommonResourceUtils.get_enum_by_name(age_str.upper(), CommonAge, default_value=None)
    if age is None:
        output('{} is not a valid age. Valid Ages: ({})'.format(age_str, ', '.join(CommonAge.get_all_names())))
        return
    if count <= 0:
        output('Please enter a count above zero.')
        return
    output('Spawning {} {} Sim(s) of Gender: {} and Age: {}.'.format(count, species.name, gender.name, age.name))
    try:
        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_sim_location = CommonSimLocationUtils.get_location(active_sim_info)
        for x in range(count):
            created_sim_info = CommonSimSpawnUtils.create_sim_info(species, gender=gender, age=age, first_name=str(x), last_name=str(x))
            CommonSimSpawnUtils.spawn_sim(created_sim_info, location=active_sim_location)
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error spawning Sims {} Sim(s) of Species: {}, Gender: {}, and Age: {}.'.format(count, species.name, gender.name, age.name), exception=ex)
        output('An error occurred while spawning Sim(s).')
    output('Done Spawning {} {} Sim(s) of Gender: {} and Age: {}.'.format(count, species.name, gender.name, age.name))
    output('If the space around your Sim was too crowded for a new Sim to spawn, you may locate the spawned Sim(s) in front of the lot.')


@Command('s4clib.spawn_human_sims', command_type=CommandType.Live)
def _s4cl_spawn_human_sims(count: int=1, gender_str: str='male', age_str: str='adult', _connection: int=None):
    return _s4cl_spawn_sims(species_str=CommonSpecies.HUMAN.name, count=count, gender_str=gender_str, age_str=age_str, _connection=_connection)


@Command('s4clib.spawn_large_dog_sims', command_type=CommandType.Live)
def _s4cl_spawn_large_dog_sims(count: int=1, gender_str: str='male', age_str: str='adult', _connection: int=None):
    return _s4cl_spawn_sims(species_str=CommonSpecies.LARGE_DOG.name, count=count, gender_str=gender_str, age_str=age_str, _connection=_connection)


@Command('s4clib.spawn_small_dog_sims', command_type=CommandType.Live)
def _s4cl_spawn_small_dog_sims(count: int=1, gender_str: str='male', age_str: str='adult', _connection: int=None):
    return _s4cl_spawn_sims(species_str=CommonSpecies.SMALL_DOG.name, count=count, gender_str=gender_str, age_str=age_str, _connection=_connection)


@Command('s4clib.spawn_cat_sims', command_type=CommandType.Live)
def _s4cl_spawn_cat_sims(count: int=1, gender_str: str='male', age_str: str='adult', _connection: int=None):
    return _s4cl_spawn_sims(species_str=CommonSpecies.CAT.name, count=count, gender_str=gender_str, age_str=age_str, _connection=_connection)


@Command('s4clib.spawn_fox_sims', command_type=CommandType.Live)
def _s4cl_spawn_fox_sims(count: int=1, gender_str: str='male', age_str: str='adult', _connection: int=None):
    return _s4cl_spawn_sims(species_str=CommonSpecies.FOX.name, count=count, gender_str=gender_str, age_str=age_str, _connection=_connection)
