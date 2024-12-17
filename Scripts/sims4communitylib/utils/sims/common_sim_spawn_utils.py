"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
import random
import time

from typing import Union, Tuple, Callable, Any, Iterator, Dict, List

import indexed_manager
from bucks.bucks_tracker import PerkData
from protocolbuffers import Outfits_pb2, S4Common_pb2
from protocolbuffers.S4Common_pb2 import SimPronoun
from sims.ghost import Ghost
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_enums import OutfitCategory, BodyType, SpecialOutfitIndex
from sims.outfits.outfit_tuning import OutfitTuning
from sims.sim_info_lod import SimInfoLODLevel
from sims.sim_info_types import SpeciesExtended, SimSerializationOption
from sims4.resources import Types
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_bucks_types import CommonBucksType
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_date_utils import CommonRealDateUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.math.common_bitwise_utils import CommonBitwiseUtils
from sims4communitylib.utils.resources.common_game_pack_utils import CommonGamePackUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_death_utils import CommonSimDeathUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from statistics.commodity import Commodity
from statistics.life_skill_statistic import LifeSkillStatistic
from statistics.ranked_statistic import RankedStatistic
from statistics.skill import Skill
from statistics.trait_statistic import TraitStatisticStates, TraitStatistic

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
    from animation.posture_manifest import Hand
    from interactions.si_state import SIState
    from objects.object_enums import ResetReason
    from postures import posture_graph
    from postures.posture_specs import PostureSpecVariable
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
        RESET_EXPECTED = 0

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

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_spawn_utils')


class CommonSimSpawnUtils:
    """Utilities for creating, spawning, despawning, and resetting Sims.

    """

    @classmethod
    def create_sim_info(
        cls,
        species: CommonSpecies,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        """create_sim_info(\
            species,\
            gender=None,\
            age=None,\
            first_name=None,\
            last_name=None,\
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
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            species,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def create_human_sim_info(
        cls,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        """create_human_sim_info(\
            gender=None,\
            age=None,\
            first_name=None,\
            last_name=None,\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Human Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            CommonSpecies.HUMAN,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def create_large_dog_sim_info(
        cls,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        """create_large_dog_sim_info(\
            gender=None,\
            age=None,\
            first_name=None,\
            last_name=None,\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Large Dog Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            CommonSpecies.LARGE_DOG,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def create_small_dog_sim_info(
        cls,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
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
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            CommonSpecies.SMALL_DOG,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def create_cat_sim_info(
        cls,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
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
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            CommonSpecies.CAT,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def create_fox_sim_info(
        cls,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
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
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            CommonSpecies.FOX,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def create_horse_sim_info(
        cls,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        last_name: str = None,
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        """create_horse_sim_info(\
            gender=None,\
            age=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Horse Sim.

        :param gender: The gender of the created Sim. Default is None.
        :type gender: CommonGender, optional
        :param age: The age of the created Sim. Default is None.
        :type age: CommonAge, optional
        :param first_name: The First Name of the created Sim. Default is random name.
        :type first_name: str, optional
        :param last_name: The Last Name of the created Sim. Default is random name.
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
        return cls._create_sim_info(
            CommonSpecies.HORSE,
            gender=gender,
            age=age,
            first_name=first_name,
            last_name=last_name,
            trait_ids=trait_ids,
            household=household,
            source=source
        )

    @classmethod
    def _create_sim_info(
        cls,
        species: CommonSpecies,
        gender: CommonGender = None,
        age: CommonAge = None,
        first_name: str = None,
        first_name_key: int = 0,
        last_name: str = None,
        last_name_key: int = 0,
        full_name_key: int = 0,
        breed_name: str = '',
        breed_name_key: int = 0,
        trait_ids: Iterator[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        household = household or CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_age = CommonAge.convert_to_vanilla(age)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        if vanilla_species is None or vanilla_species == SpeciesExtended.INVALID:
            raise AssertionError(f'Invalid species specified for SimInfo creation! {species}')
        first_name = first_name or CommonSimNameUtils.create_random_first_name(gender, species=species)
        last_name = last_name or CommonSimNameUtils.create_random_last_name(gender, species=species)
        traits = tuple([CommonTraitUtils.load_trait_by_id(trait_id) for trait_id in trait_ids if CommonTraitUtils.load_trait_by_id(trait_id) is not None])
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        sim_creator = SimCreator(
            gender=vanilla_gender,
            age=vanilla_age,
            species=vanilla_species,
            first_name=first_name,
            first_name_key=first_name_key,
            last_name=last_name,
            last_name_key=last_name_key,
            full_name_key=full_name_key,
            traits=traits,
            breed_name=breed_name if breed_name else 'Custom Breed' if CommonSpeciesUtils.is_animal_species(vanilla_species) else '',
            breed_name_key=breed_name_key if breed_name_key else CommonStringId.S4CL_CUSTOM_BREED if CommonSpeciesUtils.is_animal_species(vanilla_species) else 0,
        )
        (sim_info_list, _) = SimSpawner.create_sim_infos((sim_creator,), household=household, generate_deterministic_sim=True, creation_source=source)
        if not sim_info_list:
            return None
        return sim_info_list[0]

    @classmethod
    def spawn_sim(
        cls,
        sim_info: SimInfo,
        location: CommonLocation = None,
        position: CommonVector3 = None,
        **kwargs
    ) -> bool:
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
        if sim_info is None:
            return False
        if CommonSimUtils.get_sim_instance(sim_info) is not None:
            return True
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonAgeUtils.is_baby(sim_info):
            # Sim is baby, they spawn differently.
            from sims.baby.baby_utils import create_and_place_baby
            position_to_spawn_at = None
            routing_surface_to_spawn = None
            if position is not None:
                position_to_spawn_at = position
                routing_surface_to_spawn = CommonSurfaceIdentifier.empty()
            if location is not None:
                position_to_spawn_at = location.transform.translation
                routing_surface_to_spawn = location.routing_surface
            if position_to_spawn_at is None or routing_surface_to_spawn is None:
                return False
            create_and_place_baby(sim_info, position=position_to_spawn_at, routing_surface=routing_surface_to_spawn)
        else:
            SimSpawner.spawn_sim(sim_info, sim_location=location, sim_position=position, **kwargs)

        household = CommonHouseholdUtils.get_household(sim_info)
        if household and CommonSimUtils.get_sim_instance(sim_info) is None:
            sim_info.inject_into_inactive_zone(household.home_zone_id)
        return True

    @classmethod
    def spawn_sim_at_active_sim_location(
        cls,
        sim_info: SimInfo,
        **kwargs
    ) -> bool:
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
        return cls.spawn_sim(sim_info, location=active_location, position=active_position, **kwargs)

    @classmethod
    def clone_sim(
        cls,
        source_sim_info: SimInfo,
        add_to_household: bool = True,
        household_override: Household = None
    ) -> Union[SimInfo, None]:
        """clone_sim(source_sim_info, add_to_household=True, household_override=None)

        Clone a Sim and add them to the household of source_sim_info.

        :param source_sim_info: The Sim to clone.
        :type source_sim_info: SimInfo
        :param add_to_household: If True, the Sim will be added to the household of "source_sim_info". If False, the Sim will be cloned into their own household. Default is True.
        :type add_to_household: bool, optional
        :param household_override: If specified, this household will be the one the cloned Sim will be added to. Default is None.
        :type household_override: Household, optional
        :return: The cloned Sim Info or None if cloning failed.
        :rtype: Union[SimInfo, None]
        """
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        if household_override is not None:
            household = household_override
        else:
            if add_to_household:
                household = CommonHouseholdUtils.get_household(source_sim_info)
                if household is None:
                    raise Exception(f'No household was specified from source Sim {source_sim_info} with household {household}!')
            else:
                household = CommonHouseholdUtils.create_empty_household()
        household_id = CommonHouseholdUtils.get_id(household)
        species = CommonSpecies.get_species(source_sim_info)
        gender = CommonGender.get_gender(source_sim_info)
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        clone_sim_data = cls._build_sim_data(source_sim_info)
        clone_sim_info = cls._load_sim_data(clone_sim_data, trait_ids=tuple(source_sim_info.trait_tracker.equipped_traits), household=household, source='cloning sim')
        # clone_sim_info = cls.create_sim_info(
        #     species=species,
        #     gender=gender,
        #     age=CommonAge.get_age(source_sim_info),
        #     first_name=SimSpawner.get_random_first_name(vanilla_gender, source_sim_info.species),
        #     last_name=source_sim_info._base.last_name,
        #     trait_ids=tuple(source_sim_info.trait_tracker.equipped_traits),
        #     household=household,
        #     source='cloning'
        # )
        if clone_sim_info is None:
            return None
        # try:
        #     source_sim_proto = source_sim_info.save_sim(for_cloning=True)
        #     clone_sim_id = clone_sim_info.sim_id
        #     source_first_name = source_sim_info._base.first_name
        #     source_last_name = source_sim_info._base.last_name
        #     source_breed_name = source_sim_info._base.breed_name
        #     source_first_name_key = source_sim_info._base.first_name_key
        #     source_last_name_key = source_sim_info._base.last_name_key
        #     source_full_name_key = source_sim_info._base.full_name_key
        #     source_breed_name_key = source_sim_info._base.breed_name_key
        #     clone_first_name = clone_sim_info._base.first_name
        #     clone_last_name = clone_sim_info._base.last_name
        #     clone_breed_name = clone_sim_info._base.breed_name
        #     clone_first_name_key = clone_sim_info._base.first_name_key
        #     clone_last_name_key = clone_sim_info._base.last_name_key
        #     clone_full_name_key = clone_sim_info._base.full_name_key
        #     clone_breed_name_key = clone_sim_info._base.breed_name_key
        #     clone_sim_info.load_sim_info(source_sim_proto, is_clone=True, default_lod=SimInfoLODLevel.FULL)
        #     clone_sim_info.sim_id = clone_sim_id
        #     clone_sim_info._base.first_name = clone_first_name or source_first_name
        #     clone_sim_info._base.last_name = clone_last_name or source_last_name
        #     clone_sim_info._base.breed_name = clone_breed_name or source_breed_name
        #     clone_sim_info._base.first_name_key = clone_first_name_key or source_first_name_key
        #     clone_sim_info._base.last_name_key = clone_last_name_key or source_last_name_key
        #     clone_sim_info._base.full_name_key = clone_full_name_key or source_full_name_key
        #     clone_sim_info._base.breed_name_key = clone_breed_name_key or source_breed_name_key
        #     clone_sim_info._household_id = household_id
        #     source_trait_tracker = source_sim_info.trait_tracker
        #     clone_trait_tracker = clone_sim_info.trait_tracker
        #     for trait in clone_trait_tracker.personality_traits:
        #         if not source_trait_tracker.has_trait(trait):
        #             clone_sim_info.remove_trait(trait)
        #     for trait in clone_trait_tracker.gender_option_traits:
        #         if not source_trait_tracker.has_trait(trait):
        #             clone_sim_info.remove_trait(trait)
        #     CommonSimUtils.get_sim_info_manager().set_default_genealogy(sim_infos=(clone_sim_info,))
        #     clone_sim_info.set_default_data()
        #     clone_sim_info.save_sim()
        #     household.save_data()
        #     if not household.is_active_household:
        #         clone_sim_info.request_lod(SimInfoLODLevel.BASE)
        #     clone_sim_info.resend_physical_attributes()
        # except Exception as ex:
        #     cls.delete_sim(clone_sim_info)
        #     raise ex
        return clone_sim_info

    # Load
    @classmethod
    def _load_sim_data(
        cls,
        sim_save_data: Dict[str, Any],
        trait_ids: Tuple[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        """load_sim_data(\
            sim_save_data,\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create a Sim Info from a dictionary of data.

        :param sim_save_data:
        :param trait_ids:
        :param household:
        :param source:
        :return:
        """
        species_str: str = sim_save_data.get('species', None)
        if species_str is None:
            return None
        species = CommonResourceUtils.get_enum_by_name(species_str, CommonSpecies, default_value=None)
        if species is None:
            return None
        gender_str = sim_save_data.get('gender', None)
        if gender_str is None:
            return None
        gender = CommonResourceUtils.get_enum_by_name(gender_str, CommonGender, default_value=None)
        if gender is None:
            return None
        age_str = sim_save_data.get('age', None)
        if age_str is None:
            return None
        age = CommonResourceUtils.get_enum_by_name(age_str, CommonAge, default_value=None)
        if age is None:
            return None
        first_name: str = sim_save_data.get('first_name', None)
        last_name: str = sim_save_data.get('last_name', None)
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        household = household or CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_age = CommonAge.convert_to_vanilla(age)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        if vanilla_species is None or vanilla_species == SpeciesExtended.INVALID:
            log.format_with_message('The required pack for Sim was not available.', species=species)
            return None
        first_name = first_name or CommonSimNameUtils.create_random_first_name(gender, species=species)
        last_name = last_name or CommonSimNameUtils.create_random_last_name(gender, species=species)
        traits = tuple([CommonTraitUtils.load_trait_by_id(trait_id) for trait_id in trait_ids if CommonTraitUtils.load_trait_by_id(trait_id) is not None])
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        breed_name = sim_save_data.get('breed_name', '')
        first_name_key = sim_save_data.get('first_name_key', 0)
        last_name_key = sim_save_data.get('last_name_key', 0)
        full_name_key = sim_save_data.get('full_name_key', 0)
        breed_name_key = sim_save_data.get('breed_name_key', 0)
        sim_creator = SimCreator(
            gender=vanilla_gender,
            age=vanilla_age,
            species=vanilla_species,
            first_name=first_name,
            first_name_key=first_name_key,
            last_name=last_name,
            last_name_key=last_name_key,
            full_name_key=full_name_key,
            traits=traits,
            breed_name=breed_name if breed_name else 'Custom Breed' if CommonSpeciesUtils.is_animal_species(vanilla_species) else '',
            breed_name_key=breed_name_key if breed_name_key else 0x599432EA if CommonSpeciesUtils.is_animal_species(vanilla_species) else 0
        )
        (sim_info_list, _) = SimSpawner.create_sim_infos((sim_creator,), household=household, generate_deterministic_sim=True, creation_source=source)
        if not sim_info_list:
            return None
        sim_info: SimInfo = sim_info_list[0]

        time_stamp = time.time()
        sim_info._base.species = vanilla_species
        # noinspection PyPropertyAccess
        extended_species = sim_info.extended_species
        sim_info._species = SpeciesExtended.get_species(extended_species)
        required_pack = SpeciesExtended.get_required_pack(extended_species)
        if required_pack is not None and not CommonGamePackUtils.has_game_pack_available(required_pack):
            log.format_with_message('The required pack for Sim was not available.', species=extended_species)
            return None
        species_def = None
        if indexed_manager.capture_load_times:
            species_def = sim_info.get_sim_definition(sim_info.species)
            if species_def not in indexed_manager.object_load_times:
                indexed_manager.object_load_times[species_def] = indexed_manager.ObjectLoadData()

        lod_str = sim_save_data.get('lod', None)
        if lod_str is not None:
            lod = CommonResourceUtils.get_enum_by_name(lod_str, SimInfoLODLevel, default_value=SimInfoLODLevel.BACKGROUND)
        else:
            lod = SimInfoLODLevel.BACKGROUND
        sim_info._lod = lod
        sim_info._initialize_sim_info_trackers(sim_info._lod)
        skip_load = False
        if gender == CommonGender.MALE or gender == CommonGender.FEMALE:
            sim_info._base.gender = vanilla_gender
        sim_info._base.age = vanilla_age
        from sims.sim_info import lod_logger
        from sims.sim_info import INJECT_LOD_NAME_IN_CALLSTACK
        if not INJECT_LOD_NAME_IN_CALLSTACK:
            cls._load_sim_info(sim_info, sim_save_data, skip_load, household)
            time_elapsed = time.time() - time_stamp
            if indexed_manager.capture_load_times:
                indexed_manager.object_load_times[species_def].time_spent_loading += time_elapsed
                indexed_manager.object_load_times[species_def].loads += 1
            lod_logger.info('Loaded {} with lod {} in {} seconds.', sim_info.full_name, sim_info._lod.name, time_elapsed)
            from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
            current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
            sim_info.outfit_type_and_index = current_outfit
            sim_info.resend_outfits()
            return sim_info
        from sims4.profiler_utils import create_custom_named_profiler_function
        name_f = create_custom_named_profiler_function('Load LOD {} SimInfo'.format(sim_info._lod.name))
        name_f(lambda: cls._load_sim_info(sim_info, sim_save_data, skip_load, household))
        if indexed_manager.capture_load_times:
            time_elapsed = time.time() - time_stamp
            indexed_manager.object_load_times[species_def].time_spent_loading += time_elapsed
            indexed_manager.object_load_times[species_def].loads += 1
            lod_logger.info('Loaded {} with lod {} in {} seconds.', sim_info.full_name, sim_info._lod.name, time_elapsed)
        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        sim_info._base.outfit_type_and_index = current_outfit
        sim_info.resend_outfits()
        sim_info.on_outfit_generated(*current_outfit)
        sim_info.set_outfit_dirty(current_outfit[0])
        sim_info.set_current_outfit(current_outfit)
        sim_info._set_fit_fat()
        return sim_info

    @classmethod
    def _load_sim_info(
        cls,
        sim_info: SimInfo,
        sim_save_data: Dict[str, Any],
        skip_load: bool,
        household: Household
    ) -> None:
        species_str: str = sim_save_data.get('species', None)
        if species_str is None:
            return None
        species = CommonResourceUtils.get_enum_by_name(species_str, CommonSpecies, default_value=None)
        if species is None:
            return None
        gender_str = sim_save_data.get('gender', None)
        if gender_str is None:
            return None
        gender = CommonResourceUtils.get_enum_by_name(gender_str, CommonGender, default_value=None)
        if gender is None:
            return None
        age_str = sim_save_data.get('age', None)
        if age_str is None:
            return None
        age = CommonResourceUtils.get_enum_by_name(age_str, CommonAge, default_value=None)
        if age is None:
            return None
        first_name: str = sim_save_data.get('first_name', None)
        last_name: str = sim_save_data.get('last_name', None)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        if vanilla_species is None or vanilla_species == SpeciesExtended.INVALID:
            log.format_with_message('The required pack for Sim was not available.', species=species)
            return None
        first_name = first_name or CommonSimNameUtils.create_random_first_name(gender, species=species)
        last_name = last_name or CommonSimNameUtils.create_random_last_name(gender, species=species)
        breed_name = sim_save_data.get('breed_name', '')
        first_name_key = sim_save_data.get('first_name_key', 0)
        last_name_key = sim_save_data.get('last_name_key', 0)
        full_name_key = sim_save_data.get('full_name_key', 0)
        breed_name_key = sim_save_data.get('breed_name_key', 0)

        sim_info._base.first_name = first_name
        sim_info._base.last_name = last_name
        sim_info._base.breed_name = breed_name
        sim_info._base.first_name_key = first_name_key
        sim_info._base.last_name_key = last_name_key
        sim_info._base.full_name_key = full_name_key
        sim_info._base.breed_name_key = breed_name_key

        pronouns = sim_save_data.get('pronouns_data', None)
        if pronouns is not None:
            cls._load_pronouns_data(sim_info._base, pronouns)

        from objects.components.consumable_component import ConsumableComponent
        sim_info.commodity_tracker.set_value(ConsumableComponent.FAT_COMMODITY, sim_save_data.get('fat'))
        sim_info.commodity_tracker.set_value(ConsumableComponent.FIT_COMMODITY, sim_save_data.get('fit'))

        sim_info._household_id = CommonHouseholdUtils.get_id(household)
        sim_info._serialization_option = SimSerializationOption.UNDECLARED
        physical_attributes = sim_save_data.get('physical_attributes', None)
        if physical_attributes is not None:
            cls._load_physical_attributes(sim_info, physical_attributes)
        sim_info.custom_texture = sim_save_data.get('custom_texture', 0)

        # noinspection SpellCheckingInspection
        sim_info.do_first_sim_info_load_fixups = True
        sim_info._get_fit_fat()

        # if sim_attribute_data is not None:
        #     sim_info.set_trait_ids_on_base(trait_ids_override=list(set(itertools.chain(sim_attribute_data.trait_tracker.trait_ids, sim_info.trait_ids))))

        age_progress = sim_save_data.get('age_progress', 0)
        sim_info._age_progress.set_value(age_progress)

        primary_aspiration_id = sim_save_data.get('primary_aspiration', 0)
        primary_aspiration = CommonResourceUtils.load_instance(Types.ASPIRATION_TRACK, primary_aspiration_id)
        if primary_aspiration is not None:
            sim_info._primary_aspiration = primary_aspiration

        outfit_data = sim_save_data.get('outfit_data', None)
        if outfit_data is not None:
            cls._load_outfit_data(sim_info._base, outfit_data)

        initial_fitness_value = sim_save_data.get('initial_fitness_value', None)
        if initial_fitness_value is not None:
            sim_info._initial_fitness_value = initial_fitness_value

        # if sim_attribute_data is not None:
        #     sim_info._relationship_tracker.load(sim_attribute_data.relationship_tracker.relationships)
        #     sim_info._genealogy_tracker.load_genealogy(sim_attribute_data.genealogy_tracker)

        death_data = sim_save_data.get('death_data', None)
        if death_data is not None:
            cls._load_death_data(sim_info, death_data)

        sim_occult_data = sim_save_data.get('occult_data', None)
        if sim_occult_data is not None:
            cls._load_occult_data(sim_info, sim_occult_data)
        #     if sim_proto.significant_other != 0:
        #         sim_info.update_spouse_sim_id(sim_proto.significant_other)
        #     if sim_proto.fiance != 0:
        #         sim_info.update_fiance_sim_id(sim_proto.fiance)
        Ghost.make_ghost_if_needed(sim_info)

        # sim_info._build_buy_unlocks = set()
        # old_unlocks = set(list(sim_proto.gameplay_data.build_buy_unlocks))
        # for unlock in old_unlocks:
        #     if isinstance(unlock, int):
        #         key = sims4.resources.Key(Types.OBJCATALOG, unlock, 0)
        #         sim_info._build_buy_unlocks.add(key)
        # if hasattr(sim_proto.gameplay_data, 'build_buy_unlock_list'):
        #     for key_proto in sim_proto.gameplay_data.build_buy_unlock_list.resource_keys:
        #         key = sims4.resources.Key(key_proto.type, key_proto.instance, key_proto.group)
        #         sim_info._build_buy_unlocks.add(key)
        if not CommonAgeUtils.is_baby_or_toddler(sim_info):
            available_aspirations = list()
            aspiration_track_manager = CommonResourceUtils.get_instance_manager(Types.ASPIRATION_TRACK)
            for aspiration_track in aspiration_track_manager.types.values():
                if aspiration_track.is_hidden_unlockable or aspiration_track.is_valid_for_sim(sim_info):
                    available_aspirations.append(aspiration_track)
            sim_info._primary_aspiration = random.choice(available_aspirations)

        # sim_info._cached_inventory_value = sim_proto.gameplay_data.inventory_value
        # if sim_info._primary_aspiration is None or sim_info._primary_aspiration.is_available() or sim_info.is_human and skip_load or sim_info._away_action_tracker is not None:
        #     sim_info._away_action_tracker.load_away_action_info_from_proto(sim_proto.gameplay_data.away_action_tracker)
        # sim_info.spawn_point_id = sim_proto.gameplay_data.spawn_point_id if sim_proto.gameplay_data.HasField('spawn_point_id') else None
        # sim_info.spawn_point_option = SpawnPointOption(sim_proto.gameplay_data.spawn_point_option) if sim_proto.gameplay_data.HasField('spawn_point_option') else SpawnPointOption.SPAWN_ANY_POINT_WITH_CONSTRAINT_TAGS
        # sim_info.spawner_tags = []
        # if sim_proto.gameplay_data.HasField('time_alive'):
        #     time_alive = TimeSpan(sim_proto.gameplay_data.time_alive)
        # else:
        #     time_alive = None
        sim_info.load_time_alive(None)
        # for spawner_tag in sim_proto.gameplay_data.spawner_tags:
        #     sim_info.spawner_tags.append(tag.Tag(spawner_tag))
        try:
            sim_info.Buffs.load_in_progress = True
            sim_info.commodity_tracker.load_in_progress = True
            sim_info.on_base_characteristic_changed()
            with services.relationship_service().suppress_client_updates_context_manager():
                trait_data = sim_save_data.get('trait_data', None)
                if trait_data:
                    cls._load_trait_data(sim_info, trait_data, skip_load)
        finally:
            sim_info.Buffs.load_in_progress = False
            sim_info.commodity_tracker.load_in_progress = False

        sim_info._create_additional_statistics()
        # if sim_info._whim_tracker is not None:
        #     sim_info._whim_tracker.cache_whim_goal_proto(sim_proto.gameplay_data.whim_tracker, skip_load=skip_load)
        # if sim_info._satisfaction_tracker is not None:
        #     sim_info._satisfaction_tracker.set_satisfaction_points(sim_proto.gameplay_data.whim_bucks, SetWhimBucks.LOAD)
        current_outfit_info = sim_save_data.get('current_outfit_info', None)
        if current_outfit_info is not None:
            current_outfit_category_str = current_outfit_info.get('outfit_category', 'EVERYDAY')
            current_outfit_category = CommonResourceUtils.get_enum_by_name(current_outfit_category_str, OutfitCategory, default_value=OutfitCategory.EVERYDAY)
            current_outfit_index = current_outfit_info.get('outfit_index', 0)
            sim_info._set_current_outfit_without_distribution((current_outfit_category, current_outfit_index))

        # sim_info._load_inventory(sim_proto, skip_load)
        additional_bonus_days = sim_save_data.get('additional_bonus_days', 0)
        sim_info._additional_bonus_days = additional_bonus_days

        favorite_recipe_ids = sim_save_data.get('favorite_recipe_ids', None)
        if favorite_recipe_ids is not None:
            recipe_manager = CommonResourceUtils.get_instance_manager(Types.RECIPE)
            for recipe_id in favorite_recipe_ids:
                recipe = recipe_manager.get(recipe_id)
                if recipe is not None:
                    sim_info.set_favorite_recipe(recipe)

        # if sim_proto.gameplay_data.zone_time_stamp.HasField('time_sim_was_saved'):
        #     sim_info._time_sim_was_saved = DateAndTime(sim_proto.gameplay_data.zone_time_stamp.time_sim_was_saved)
        # if skip_load or sim_proto.gameplay_data.zone_time_stamp.game_time_expire != 0:
        #     sim_info.game_time_bring_home = sim_proto.gameplay_data.zone_time_stamp.game_time_expire

        try:
            sim_info.Buffs.load_in_progress = True
            sim_info._blacklisted_statistics_cache = sim_info.get_blacklisted_statistics()

            sim_statistic_data = sim_save_data.get('statistics_data', None)
            if sim_statistic_data is not None:
                cls._load_statistic_data(sim_info, sim_statistic_data, skip_load)

            sim_commodity_data = sim_save_data.get('commodity_data', None)
            if sim_commodity_data is not None:
                cls._load_commodity_data(sim_info, sim_commodity_data, skip_load)

            if sim_info.is_human:
                trait_statistic_data = sim_save_data.get('trait_statistic_data', None)
                if trait_statistic_data is not None:
                    cls._load_trait_statistic_data(sim_info, trait_statistic_data)

            if sim_commodity_data is not None:
                skill_data = sim_commodity_data.get('skills', None)
                if skill_data:
                    skills_to_check_for_unlocks = [commodity for commodity in sim_info.commodity_tracker.get_all_commodities() if commodity.unlocks_skills_on_max() and len(commodity.skill_unlocks_on_max) > 0]
                    if skills_to_check_for_unlocks:
                        cls._update_unlock_skills(sim_info, skills_to_check_for_unlocks, skill_data)

            suntan_data = sim_save_data.get('suntan_data', None)
            if suntan_data is not None:
                cls._load_suntan_data(sim_info, suntan_data)

            # sim_info._pregnancy_tracker.load(sim_attribute_data.pregnancy_tracker)
            appearance_data = sim_save_data.get('appearance_data', None)
            if appearance_data is not None:
                cls._load_appearance_data(sim_info, appearance_data)

            # if sim_attribute_data.HasField('sickness_tracker'):
            #     sim_info.sickness_tracker.load_sickness_tracker_data(sim_attribute_data.sickness_tracker)
            #     if sim_info.has_sickness_tracking():
            #         sim_info.current_sickness.on_sim_info_loaded(sim_info)
            # if sim_attribute_data.HasField('stored_object_info_component'):
            #     component_def = objects.components.types.STORED_OBJECT_INFO_COMPONENT
            #     if sim_info.add_dynamic_component(component_def):
            #         stored_object_info_component = sim_info.get_component(component_def)
            #         stored_object_info_component.load_stored_object_info(sim_attribute_data.stored_object_info_component)
            # for entry in sim_attribute_data.object_preferences.preferences:
            #     sim_info._autonomy_scoring_preferences[entry.tag] = entry.object_id
            # for entry in sim_attribute_data.object_ownership.owned_object:
            #     sim_info._autonomy_use_preferences[entry.tag] = entry.object_id
            # sim_info._career_tracker.load(sim_attribute_data.sim_careers, skip_load=skip_load)
            # if sim_info._adventure_tracker is not None:
            #     sim_info._adventure_tracker.load(sim_attribute_data.adventure_tracker)
            # if sim_info._notebook_tracker is not None:
            #     sim_info._notebook_tracker.load_notebook(sim_attribute_data.notebook_tracker)
            # if sim_info._royalty_tracker is not None and not skip_load:
            #     sim_info._royalty_tracker.load(sim_attribute_data.royalty_tracker)
            # if sim_info._unlock_tracker is not None:
            #     skip_load = skip_load and not is_clone
            #     sim_info._unlock_tracker.load_unlock(sim_attribute_data.unlock_tracker, skip_load=skip_load)
            # if sim_info._relic_tracker is not None and not skip_load:
            #     sim_info._relic_tracker.load(sim_attribute_data.relic_tracker)
            # if sim_info._lifestyle_brand_tracker is not None and not skip_load:
            #     sim_info._lifestyle_brand_tracker.load(sim_attribute_data.lifestyle_brand_tracker)
            # if sim_info._favorites_tracker is not None and not skip_load:
            #     sim_info._favorites_tracker.load(sim_attribute_data.favorites_tracker)
            # if sim_info._degree_tracker is not None:
            #     sim_info.degree_tracker.load(sim_attribute_data.degree_tracker)
            # if sim_info._organization_tracker is not None and not skip_load:
            #     sim_info._organization_tracker.load(sim_attribute_data.organization_tracker)
            # if sim_info._fixup_tracker is not None and not skip_load:
            #     sim_info._fixup_tracker.load(sim_attribute_data.fixup_tracker)
            # if sim_info._story_progression_tracker is not None and not skip_load:
            #     sim_info._story_progression_tracker.load(sim_attribute_data.story_progression_tracker)
            # if sim_info._lunar_effect_tracker is not None and not skip_load:
            #     sim_info._lunar_effect_tracker.load_lunar_effects(sim_attribute_data.lunar_effect_tracker)
        except Exception as ex:
            log.error(f'Failed to load attributes for sim {sim_info._base.first_name}.', exception=ex, throw=False)
        finally:
            sim_info._blacklisted_statistics_cache = None
            sim_info.Buffs.load_in_progress = False

        sim_info._setup_fitness_commodities()
        sim_info._trait_tracker.fixup_gender_preference_statistics()
        sim_info._add_gender_preference_listeners()

        # if sim_info._serialization_option != SimSerializationOption.UNDECLARED:
        #     world_coord = sims4.math.Transform()
        #     location = sim_proto.gameplay_data.location
        #     world_coord.translation = sims4.math.Vector3(location.x, location.y, location.z)
        #     world_coord.orientation = sims4.math.Quaternion(location.rot_x, location.rot_y, location.rot_z, location.rot_w)
        #     sim_info._transform_on_load = world_coord
        #     sim_info._level_on_load = location.level
        #     sim_info._surface_id_on_load = location.surface_id

        # sim_info._si_state = gameplay_serialization.SuperInteractionSaveState()
        # if skip_load or sim_proto.gameplay_data.HasField('location') and sim_proto.gameplay_data.HasField('interaction_state'):
        #     sim_info._has_loaded_si_state = True
        #     sim_info._si_state.MergeFrom(sim_proto.gameplay_data.interaction_state)

        services.sim_info_manager().add_sim_info_if_not_in_manager(sim_info)

        bucks_data = sim_save_data.get('bucks_data', None)
        if bucks_data is not None:
            cls._load_bucks_data(sim_info, bucks_data)

        # if sim_proto.gameplay_data.HasField('gameplay_options'):
        #     sim_info._gameplay_options = sim_proto.gameplay_data.gameplay_options
        #     if sim_info.get_gameplay_option(SimInfoGameplayOptions.FORCE_CURRENT_ALLOW_FAME_SETTING) and not sim_info.get_gameplay_option(SimInfoGameplayOptions.ALLOW_FAME):
        #         sim_info.allow_fame = False
        #     elif sim_info.get_gameplay_option(SimInfoGameplayOptions.FREEZE_FAME):
        #         sim_info.set_freeze_fame(True, force=True)
        # for squad_member_id in sim_proto.gameplay_data.squad_members:
        #     sim_info.add_sim_info_id_to_squad(squad_member_id)
        # if sim_proto.gameplay_data.HasField('vehicle_id'):
        #     sim_info._vehicle_id = sim_proto.gameplay_data.vehicle_id
        sim_info._post_load()

    @classmethod
    def _load_bucks_data(
        cls,
        sim_info: SimInfo,
        sim_bucks_data: Dict[str, Any],
    ):
        bucks_tracker = sim_info.get_bucks_tracker(add_if_none=True)

        bucks_perk_manager = CommonResourceUtils.get_instance_manager(Types.BUCKS_PERK)
        for bucks_data in sim_bucks_data.get('bucks', tuple()):
            bucks_type_str = bucks_data.get('bucks_type', None)
            if bucks_type_str is None:
                continue
            bucks_type = CommonResourceUtils.get_enum_by_name(bucks_type_str, CommonBucksType, default_value=None)
            if bucks_type is None:
                continue
            bucks_amount = bucks_data.get('amount', 0)

            if bucks_amount >= 0:
                vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
                bucks_tracker.try_modify_bucks(vanilla_bucks_type, bucks_amount, allow_distribute=False, from_load=True)

            for perk_data in bucks_data.get('perk_data', tuple()):
                perk_id = perk_data.get('perk_id', None)
                if perk_id is None:
                    continue
                perk_ref = bucks_perk_manager.get(perk_id)
                if perk_ref is None:
                    log.format_with_message('Trying to load unavailable BUCKS_PERK resource', perk_id=perk_id)
                    continue
                unlock_reason = perk_data.get('unlock_reason', None)
                if unlock_reason is not None:
                    unlocked_by = bucks_perk_manager.get(unlock_reason)
                else:
                    unlocked_by = None
                timestamp = CommonTimeUtils.get_current_date_and_time()
                currently_unlocked = perk_data.get('currently_unlocked', False)
                bucks_tracker._unlocked_perks[perk_ref.associated_bucks_type][perk_ref] = PerkData(unlocked_by, timestamp, currently_unlocked)
                if currently_unlocked:
                    bucks_tracker._award_buffs(perk_ref)
                    bucks_tracker._award_traits(perk_ref)
                    time_left = perk_data.get('time_left', None)
                    if time_left is not None:
                        bucks_tracker._set_up_temporary_perk_timer(perk_ref, time_left)

    @classmethod
    def _load_trait_data(
        cls,
        sim_info: SimInfo,
        sim_trait_data: Dict[str, Any],
        skip_load: bool
    ):
        from traits.trait_quirks import add_quirks
        trait_tracker = sim_info._trait_tracker
        saved_trait_ids = sim_trait_data.get('trait_ids', tuple())
        trait_manager = CommonResourceUtils.get_instance_manager(Types.TRAIT)
        try:
            trait_tracker._load_in_progress = True
            trait_tracker._sim_info._update_age_trait(trait_tracker._sim_info.age)
            pre_made_sim_needing_fixup = bool(trait_tracker._sim_info.sim_template_id)
            for trait_instance_id in saved_trait_ids:
                trait = trait_manager.get(trait_instance_id, None)
                if trait is None:
                    continue
                if not trait_tracker._has_valid_lod(trait):
                    if trait.min_lod_value == SimInfoLODLevel.ACTIVE:
                        if trait_tracker._delayed_active_lod_traits is None:
                            trait_tracker._delayed_active_lod_traits = list()
                        trait_tracker._delayed_active_lod_traits.append(trait)
                        if skip_load and not (pre_made_sim_needing_fixup or trait.allow_from_gallery):
                            continue
                        else:
                            trait_tracker._sim_info.add_trait(trait)
                elif skip_load and not (pre_made_sim_needing_fixup or trait.allow_from_gallery):
                    continue
                else:
                    trait_tracker._sim_info.add_trait(trait)
            if trait_tracker.personality_traits or not trait_tracker._sim_info.is_baby:
                possible_traits = [trait for trait in trait_manager.types.values() if trait.is_personality_trait and trait_tracker.can_add_trait(trait)]
                if possible_traits:
                    chosen_trait = random.choice(possible_traits)
                    trait_tracker._add_trait(chosen_trait)
            trait_tracker._add_default_gender_option_traits()
            add_quirks(trait_tracker._sim_info)
            trait_tracker._sim_info.on_all_traits_loaded()
        finally:
            trait_tracker._load_in_progress = False

    @classmethod
    def _load_outfit_data(
        cls,
        sim_info: SimInfo,
        outfit_data_external: Dict[str, Any]
    ):
        outfits_msg = Outfits_pb2.OutfitList()
        parsed_outfits = list()
        for (outfit_category_name, outfit_data_list) in outfit_data_external.items():
            outfit_category = CommonResourceUtils.get_enum_by_name(outfit_category_name, OutfitCategory, default_value=None)
            if outfit_category is None:
                continue
            for outfit_data in outfit_data_list:
                outfit = Outfits_pb2.OutfitData()
                outfit.category = int(outfit_category)
                part_data_list = outfit_data.get('part_data_list', None)
                if part_data_list is None:
                    continue
                body_types = list()
                part_ids = list()
                part_color_shifts = list()
                added_parts = False
                for part_data in part_data_list:
                    body_type = part_data.get('body_type', None)
                    part_id = part_data.get('part_id', None)
                    part_color_shift = part_data.get('part_color_shift', None)
                    if body_type is None or part_id is None or part_color_shift is None:
                        continue
                    if not CommonCASUtils.is_cas_part_loaded(part_id)\
                            and int(body_type) in (
                        int(BodyType.LOWER_BODY),
                        int(BodyType.UPPER_BODY),
                        int(BodyType.FULL_BODY),
                        int(BodyType.SHOES)
                    ):
                        added_parts = False
                        break
                    added_parts = True
                    body_types.append(body_type)
                    part_ids.append(part_id)
                    part_color_shifts.append(part_color_shift)

                if not added_parts:
                    continue

                outfit.body_types_list = Outfits_pb2.BodyTypesList()
                # noinspection PyUnresolvedReferences
                outfit.body_types_list.body_types.extend(body_types)
                outfit.parts = S4Common_pb2.IdList()
                # noinspection PyUnresolvedReferences
                outfit.parts.ids.extend(part_ids)
                outfit.part_shifts = Outfits_pb2.ColorShiftList()
                # noinspection PyUnresolvedReferences
                outfit.part_shifts.color_shift.extend(part_color_shifts)

                # noinspection PyUnresolvedReferences
                outfit.outfit_id = outfit_data.get('outfit_id')
                # noinspection PyUnresolvedReferences
                outfit.outfit_flags = outfit_data.get('outfit_flags')
                # noinspection PyUnresolvedReferences
                outfit.outfit_flags_high = outfit_data.get('outfit_flags_high')
                outfit.title = outfit_data.get('title')
                outfit.match_hair_style = outfit_data.get('match_hair_style')
                outfit.created = outfit_data.get('created')
                parsed_outfits.append(outfit)

        # noinspection PyUnresolvedReferences
        outfits_msg.outfits.extend(parsed_outfits)

        try:
            sim_info.outfits = outfits_msg.SerializeToString()
        except Exception as ex:
            log.format_error_with_message('An error occurred when attempting to load outfit data for Slave.', outfit_data_external=outfit_data_external, exception=ex)

    @classmethod
    def _update_unlock_skills(
        cls,
        sim_info: SimInfo,
        skills: Iterator[Skill],
        sim_loading_skills: List[Dict[str, Any]]
    ):
        open_set = set(skills)
        closed_set = set()
        while open_set:
            current_skill = open_set.pop()
            closed_set.add(current_skill)
            if not current_skill.reached_max_level:
                continue

            for skill_to_unlock in current_skill.skill_unlocks_on_max:
                if skill_to_unlock not in closed_set:
                    sim_info.commodity_tracker.add_statistic(skill_to_unlock, force_add=True)
                    skill_data_objects = [sdo for sdo in sim_loading_skills if sdo.get('stat_id', 0) == skill_to_unlock.guid64]
                    cls._load_commodity_tracker_data(sim_info, skill_data_objects)
                    open_set.add(skill_to_unlock)

    @classmethod
    def _load_commodity_tracker_data(
        cls,
        sim_info: SimInfo,
        statistics_data: List[Dict[str, Any]],
        skip_load=False,
        update_affordance_cache=True
    ):
        commodity_tracker = sim_info.commodity_tracker
        statistic_manager = CommonResourceUtils.get_instance_manager(Types.STATISTIC)
        try:
            commodity_tracker.load_in_progress = True
            owner_lod = commodity_tracker._owner.lod if isinstance(commodity_tracker._owner, SimInfo) else None
            for statistic_data in statistics_data:
                stat_id = statistic_data.get('stat_id', 0)
                if stat_id == 0:
                    continue
                stat_value = statistic_data.get('stat_value', 0)
                commodity_class = statistic_manager.get(stat_id)
                if commodity_class is None:
                    log.format_with_message('Trying to load unavailable STATISTIC resource', skill_id=stat_id)
                    continue
                elif not commodity_class.persisted:
                    log.format_with_message('Trying to load unavailable STATISTIC resource', skill_id=stat_id)
                    continue
                elif commodity_tracker.statistics_to_skip_load is not None and commodity_class in commodity_tracker.statistics_to_skip_load:
                    continue
                elif commodity_class.is_skill and stat_value == commodity_class.initial_value:
                    continue
                elif skip_load and commodity_class.remove_on_convergence:
                    log.format_with_message('Not loading skill because load is not required.', commodity_class=commodity_class)
                    continue
                elif not commodity_tracker._should_add_commodity_from_gallery(commodity_class, skip_load):
                    continue
                elif owner_lod is not None and owner_lod < commodity_class.min_lod_value:
                    if commodity_class.min_lod_value >= SimInfoLODLevel.ACTIVE:
                        if commodity_tracker._delayed_active_lod_statistics is None:
                            commodity_tracker._delayed_active_lod_statistics = list()
                        commodity_tracker._delayed_active_lod_statistics.append((stat_id, stat_value))
                        commodity_tracker.set_value(commodity_class, stat_value, from_load=True)
                        # if commodity_class.is_commodity:
                        #     stat = commodity_tracker.get_statistic(commodity_class)
                        #     if stat is not None:
                        #         stat.force_apply_buff_on_start_up = data.apply_buff_on_start_up
                        #         if data.buff_reason.hash:
                        #             stat.force_buff_reason = Localization_pb2.LocalizedString()
                        #             stat.force_buff_reason.MergeFrom(data.buff_reason)
                        #         stat.load_time_of_last_value_change(data)
                        # elif commodity_class.is_ranked:
                        #     stat = commodity_tracker.get_statistic(commodity_class)
                        #     if stat is not None:
                        #         stat._initial_loots_awarded = data.initial_loots_awarded
                        #         stat._inclusive_rank_threshold = data.inclusive_rank_threshold
                        #         stat.set_level_and_rank()
                        #         stat.highest_level = data.highest_level
                        #         stat.load_time_of_last_value_change(data)
                        #         stat.fixup_callbacks_during_load()
                    continue
                else:
                    commodity_tracker.set_value(commodity_class, stat_value, from_load=True)
                    # if commodity_class.is_commodity:
                    #     stat = commodity_tracker.get_statistic(commodity_class)
                    #     if stat is not None:
                    #         stat.force_apply_buff_on_start_up = data.apply_buff_on_start_up
                    #         if data.buff_reason.hash:
                    #             stat.force_buff_reason = Localization_pb2.LocalizedString()
                    #             stat.force_buff_reason.MergeFrom(data.buff_reason)
                    #         stat.load_time_of_last_value_change(data)
                    # elif commodity_class.is_ranked:
                    #     stat = commodity_tracker.get_statistic(commodity_class)
                    #     if stat is not None:
                    #         stat._initial_loots_awarded = data.initial_loots_awarded
                    #         stat._inclusive_rank_threshold = data.inclusive_rank_threshold
                    #         stat.set_level_and_rank()
                    #         stat.highest_level = data.highest_level
                    #         stat.load_time_of_last_value_change(data)
                    #         stat.fixup_callbacks_during_load()
                    continue
        finally:
            commodity_tracker.statistics_to_skip_load = None
            commodity_tracker.load_in_progress = False
        if update_affordance_cache:
            commodity_tracker.update_affordance_caches()

    @classmethod
    def _load_appearance_data(
        cls,
        sim_info: SimInfo,
        sim_appearance_data: Dict[str, Any]
    ):
        appearance_tracker = sim_info.appearance_tracker
        for appearance_item_data in sim_appearance_data.get('appearance_items', tuple()):
            guid = appearance_item_data.get('guid', None)
            if guid is None:
                continue
            seed = appearance_item_data.get('seed', None)
            if seed is None:
                continue
            appearance_tracker.add_persistent_appearance_modifier_data(guid, seed)

    @classmethod
    def _load_suntan_data(
        cls,
        sim_info: SimInfo,
        sim_suntan_data: Dict[str, Any]
    ):
        suntan_tracker = sim_info._suntan_tracker
        suntan_tracker._tan_level = sim_suntan_data.get('tan_level', 0)

        suntan_parts = sim_suntan_data.get('suntan_parts', tuple())
        if suntan_parts:
            if suntan_tracker._outfit_part_data_list is None:
                suntan_tracker._outfit_part_data_list = []
            else:
                suntan_tracker._outfit_part_data_list.clear()

            for part_data in suntan_parts:
                part_id = part_data.get('part_id', None)
                if part_id is None:
                    continue
                body_type_value = part_data.get('body_type', None)
                if body_type_value is None:
                    continue
                body_type = CommonCASUtils.convert_value_to_body_type(body_type_value)
                suntan_tracker._outfit_part_data_list.append((part_id, body_type))

    @classmethod
    def _load_trait_statistic_data(
        cls,
        sim_info: SimInfo,
        sim_statistic_data: Dict[str, Any]
    ):
        trait_statistic_tracker = sim_info.trait_statistic_tracker
        if trait_statistic_tracker._statistics is None:
            return None
        trait_statistic_data = dict()
        trait_statistics = list()
        for statistic in sorted(list(trait_statistic_tracker._statistics.values()), key=lambda x: x.guid64 if x is not None and hasattr(x, 'guid64') else 0):
            stat_data = dict()
            stat_id = statistic.guid64
            if stat_id is None or stat_id == 0:
                continue
            stat_data['stat_id'] = stat_id
            stat_data['stat_value'] = statistic.get_value()
            stat_data['stat_state'] = statistic._state.name
            if statistic._neglect_buff_index is not None:
                stat_data['neglect_buff_index'] = statistic._neglect_buff_index
            stat_data['value_added'] = statistic._value_added
            if statistic._max_daily_cap is not None:
                stat_data['max_daily_cap'] = statistic._max_daily_cap
            if statistic._min_daily_cap is not None:
                stat_data['min_daily_cap'] = statistic._min_daily_cap
            trait_statistics.append(stat_data)
        if trait_statistics:
            trait_statistic_data['trait_statistics'] = trait_statistics
        if not trait_statistic_data:
            return None

        statistic_manager = CommonResourceUtils.get_instance_manager(Types.STATISTIC)
        for trait_statistic_data in sim_statistic_data.get('trait_statistics', tuple()):
            stat_id = trait_statistic_data.get('stat_id', None)
            if stat_id is None:
                continue
            stat_value = trait_statistic_data.get('stat_value', None)
            if stat_value is None:
                continue
            statistic_type = statistic_manager.get(stat_id)
            if statistic_type is None:
                continue
            trait_state_name = trait_statistic_data.get('stat_state', None)
            if trait_state_name is None:
                continue
            trait_state = CommonResourceUtils.get_enum_by_name(trait_state_name, TraitStatisticStates, default_value=None)
            if trait_state is None:
                continue
            if trait_statistic_tracker.owner.lod >= statistic_type.min_lod_value:
                stat: TraitStatistic = trait_statistic_tracker.add_statistic(statistic_type, from_load=True)
                if stat is None:
                    continue
                stat.set_value(stat_value, ignore_caps=True)
                stat._state = trait_state
                neglect_buff_index = trait_statistic_data.get('neglect_buff_index', None)
                if neglect_buff_index is not None:
                    stat._neglect_buff_index = neglect_buff_index
                    if stat._state >= TraitStatisticStates.UNLOCKED:
                        # noinspection PyUnresolvedReferences
                        trait_data = stat.trait_data
                    else:
                        # noinspection PyUnresolvedReferences
                        trait_data = stat.opposing_trait_data
                    try:
                        neglect_buff_data = trait_data.neglect_buffs[stat._neglect_buff_index]
                        stat._neglect_buff_handle = stat.tracker.owner.add_buff(neglect_buff_data.buff_type, buff_reason=neglect_buff_data.buff_reason)
                    except Exception as ex:
                        log.format_error_with_message(f'Stat: {stat} Current State: {stat._state} should not have neglect buff index set: {stat._neglect_buff_index}', exception=ex, throw=False)
                        stat._neglect_buff_index = None
                stat._value_added = trait_statistic_data.get('value_added', 0)
                max_daily_cap = trait_statistic_data.get('max_daily_cap', None)
                if max_daily_cap is not None:
                    stat._max_daily_cap = max_daily_cap
                min_daily_cap = trait_statistic_data.get('min_daily_cap', None)
                if min_daily_cap is not None:
                    stat._min_daily_cap = min_daily_cap

                stat.startup_statistic(from_load=True)
                # noinspection PyUnresolvedReferences
                if stat._state >= TraitStatisticStates.UNLOCKED:
                    # noinspection PyUnresolvedReferences
                    if not stat.tracker.owner.has_trait(stat.trait_data.trait):
                        # noinspection PyUnresolvedReferences
                        stat.tracker.owner.add_trait(stat.trait_data.trait)
                # noinspection PyUnresolvedReferences
                elif stat._state <= TraitStatisticStates.OPPOSING_UNLOCKED and not stat.tracker.owner.has_trait(stat.opposing_trait_data.trait):
                    # noinspection PyUnresolvedReferences
                    stat.tracker.owner.add_trait(stat.opposing_trait_data.trait)

                if statistic_type.min_lod_value == SimInfoLODLevel.ACTIVE:
                    if trait_statistic_tracker._delayed_active_lod_statistics is None:
                        trait_statistic_tracker._delayed_active_lod_statistics = list()
                    trait_statistic_tracker._delayed_active_lod_statistics.append((stat_id, stat_value))

            elif statistic_type.min_lod_value == SimInfoLODLevel.ACTIVE:
                if trait_statistic_tracker._delayed_active_lod_statistics is None:
                    trait_statistic_tracker._delayed_active_lod_statistics = list()
                trait_statistic_tracker._delayed_active_lod_statistics.append((stat_id, stat_value))

    @classmethod
    def _load_statistic_data(
        cls,
        sim_info: SimInfo,
        sim_statistic_data: Dict[str, Any],
        skip_load: bool
    ):
        statistic_tracker = sim_info.statistic_tracker
        try:
            statistics_manager = CommonResourceUtils.get_instance_manager(Types.STATISTIC)
            owner_lod = statistic_tracker._owner.lod if isinstance(statistic_tracker._owner, SimInfo) else None
            for statistics_data in sim_statistic_data.get('statistics', tuple()):
                stat_id = statistics_data.get('stat_id', None)
                if stat_id is None:
                    continue
                stat_value = statistics_data.get('stat_value', None)
                stat_cls = statistics_manager.get(stat_id)
                if stat_cls is not None:
                    if not statistic_tracker._should_add_commodity_from_gallery(stat_cls, skip_load):
                        continue
                    elif not stat_cls.persisted:
                        continue
                    elif statistic_tracker.statistics_to_skip_load is not None and stat_cls in statistic_tracker.statistics_to_skip_load:
                        continue
                    elif owner_lod is not None and owner_lod < stat_cls.min_lod_value:
                        if stat_cls.min_lod_value == SimInfoLODLevel.ACTIVE:
                            if statistic_tracker._delayed_active_lod_statistics is None:
                                statistic_tracker._delayed_active_lod_statistics = list()
                            statistic_tracker._delayed_active_lod_statistics.append((stat_id, stat_value))
                            if stat_value is not None:
                                statistic_tracker.set_value(stat_cls, stat_value, from_load=True)
                            else:
                                if statistic_tracker._statistics is None:
                                    statistic_tracker._statistics = {}
                                if stat_cls not in statistic_tracker._statistics:
                                    statistic_tracker._statistics[stat_cls] = None
                                    log.format_with_message('Trying to load unavailable STATISTIC resource', stat_id=stat_id)
                    else:
                        if stat_value is not None:
                            statistic_tracker.set_value(stat_cls, stat_value, from_load=True)
                        else:
                            if statistic_tracker._statistics is None:
                                statistic_tracker._statistics = {}
                            if stat_cls not in statistic_tracker._statistics:
                                statistic_tracker._statistics[stat_cls] = None
                                log.format_with_message('Trying to load unavailable STATISTIC resource', stat_id=stat_id)
                else:
                    log.format_with_message('Trying to load unavailable STATISTIC resource', stat_id=stat_id)
        finally:
            statistic_tracker.statistics_to_skip_load = None
        statistic_tracker.check_for_unneeded_initial_statistics()

    @classmethod
    def _load_commodity_data(
        cls,
        sim_info: SimInfo,
        sim_commodity_data: Dict[str, Any],
        skip_load: bool
    ):
        commodity_tracker = sim_info.commodity_tracker

        cls._load_commodity_tracker_data(sim_info, sim_commodity_data.get('commodities', tuple()), skip_load=skip_load, update_affordance_cache=False)
        if sim_info.lod > SimInfoLODLevel.BASE:
            for commodity in tuple(commodity_tracker):
                if commodity.has_auto_satisfy_value():
                    commodity.set_to_auto_satisfy_value()
        cls._load_commodity_tracker_data(sim_info, sim_commodity_data.get('other_statistics', tuple()), update_affordance_cache=False)
        cls._load_commodity_tracker_data(sim_info, sim_commodity_data.get('skills', tuple()), update_affordance_cache=False)
        cls._load_commodity_tracker_data(sim_info, sim_commodity_data.get('ranked_statistics', tuple()), update_affordance_cache=True)

    @classmethod
    def _load_occult_data(
        cls,
        sim_info: SimInfo,
        sim_occult_data: Dict[str, Any]
    ):
        occult_tracker = sim_info._occult_tracker
        occult_types_list = sim_occult_data.get('occult_types', tuple())
        occult_types = None
        for occult_type_value in occult_types_list:
            vanilla_occult_type = cls._to_occult_type(occult_type_value)
            if vanilla_occult_type is None:
                continue
            if occult_types is None:
                occult_types = vanilla_occult_type
            else:
                occult_types = CommonBitwiseUtils.add_flags(occult_types, vanilla_occult_type)

        occult_tracker._sim_info.occult_types = occult_types or OccultType.HUMAN

        current_occult_types_list = sim_occult_data.get('current_occult_types', tuple())
        current_occult_types = None
        for current_occult_type_value in current_occult_types_list:
            vanilla_current_occult_type = cls._to_occult_type(current_occult_type_value)
            if vanilla_current_occult_type is None:
                continue
            if current_occult_types is None:
                current_occult_types = vanilla_current_occult_type
            else:
                current_occult_types = CommonBitwiseUtils.add_flags(occult_types, vanilla_current_occult_type)

        occult_tracker._sim_info.current_occult_types = current_occult_types or OccultType.HUMAN

        pending_occult_type_value = sim_occult_data.get('pending_occult_type', None)

        if pending_occult_type_value is not None:
            pending_occult_type = cls._to_occult_type(pending_occult_type_value)
            if pending_occult_type is not None:
                occult_tracker._pending_occult_type = pending_occult_type

        occult_tracker._occult_form_available = sim_occult_data.get('occult_form_available', True)

        occult_data_map = dict()
        for (occult_type_str, occult_type_data) in sim_occult_data.get('occult_info_by_occult_type', dict()).items():
            if occult_type_str is None:
                continue
            occult_type = cls._to_occult_type(occult_type_str)
            if occult_type is None:
                continue

            occult_type_data['occult_type'] = occult_type

            occult_data_map[occult_type] = occult_type_data

        for occult_type in OccultType:
            if occult_type != OccultType.HUMAN and occult_type not in occult_tracker.OCCULT_DATA:
                occult_tracker._sim_info.occult_types &= ~occult_type
                if occult_tracker._sim_info.current_occult_types == occult_type:
                    occult_tracker._sim_info.current_occult_types = OccultType.HUMAN
                if occult_tracker._pending_occult_type == occult_type:
                    occult_tracker._pending_occult_type = None
            elif occult_type in occult_data_map:
                sim_info_occult_data = occult_data_map[occult_type]
                occult_tracker_sim_info = occult_tracker._generate_sim_info(sim_info_occult_data.get('occult_type'), generate_new=False)
                outfits_data = sim_info_occult_data.get('occult_outfit_data', None)
                physical_attributes = sim_info_occult_data.get('occult_physical_attributes', None)
                if occult_type == occult_tracker._sim_info.current_occult_types:
                    if outfits_data is not None:
                        cls._load_outfit_data(sim_info, outfits_data)
                    if physical_attributes is not None:
                        cls._load_physical_attributes(sim_info, physical_attributes)
                else:
                    if outfits_data is not None:
                        cls._load_outfit_data(occult_tracker_sim_info._base, outfits_data)
                    if physical_attributes is not None:
                        cls._load_physical_attributes(occult_tracker_sim_info._base, physical_attributes)
            elif occult_type != OccultType.HUMAN and occult_tracker.has_occult_type(occult_type) and occult_type == occult_tracker._sim_info.current_occult_types:
                occult_tracker._generate_sim_info(occult_type, generate_new=False)

    @classmethod
    def _to_occult_type(cls, value: Union[str, int]) -> Union[OccultType, None]:
        if isinstance(value, str):
            return CommonResourceUtils.get_enum_by_name(value, OccultType, default_value=None)
        elif isinstance(value, int):
            return CommonResourceUtils.get_enum_by_int_value(value, OccultType, default_value=None)
        return None

    @classmethod
    def _load_death_data(
        cls,
        sim_info: SimInfo,
        sim_death_data: Dict[str, Any]
    ):
        death_type_str = sim_death_data.get('death_type', None)
        if death_type_str is None:
            return
        death_type = CommonResourceUtils.get_enum_by_name(death_type_str, CommonDeathType, default_value=None)
        if death_type is None:
            return
        death_tracker = CommonSimDeathUtils.get_death_tracker(sim_info)
        death_tracker._death_type = CommonDeathType.convert_to_vanilla(death_type)
        death_tracker._death_time = CommonTimeUtils.get_current_date_and_time()

    @classmethod
    def _load_physical_attributes(
        cls,
        sim_info: SimInfo,
        physical_attributes_data: Dict[str, Any]
    ):
        try:
            physique = physical_attributes_data.get('physique', None)
            if physique is not None:
                sim_info.physique = physique

            facial_attributes = physical_attributes_data.get('facial_attributes', None)
            if facial_attributes is not None:
                cls._load_facial_attribute_data(sim_info, facial_attributes)

            sim_info.voice_pitch = physical_attributes_data.get('voice_pitch', 0)
            sim_info.voice_actor = physical_attributes_data.get('voice_actor', 0)
            sim_info.voice_effect = physical_attributes_data.get('voice_effect', 0)
            sim_info.skin_tone = physical_attributes_data.get('skin_tone', 0)
            sim_info.skin_tone_val_shift = physical_attributes_data.get('skin_tone_val_shift', 0)

            sim_info.flags = physical_attributes_data.get('flags', 0)

            pelt_layers = physical_attributes_data.get('pelt_layers', None)
            if pelt_layers is not None:
                cls._load_pelt_layer_data(sim_info, pelt_layers)

            base_trait_ids = physical_attributes_data.get('base_trait_ids', None)
            if base_trait_ids is not None:
                sim_info.base_trait_ids = list(base_trait_ids)

            genetic_data = physical_attributes_data.get('genetics_data', None)
            if genetic_data is not None:
                cls._load_genetics_data(sim_info, genetic_data)
        except Exception as ex:
            log.error('Failed to save physical attributes', exception=ex, throw=False)

    @classmethod
    def _load_pelt_layer_data(cls, sim_info: SimInfo, sim_pelt_layers_data: Dict[str, Any]):
        pelt_layer_data = Outfits_pb2.PeltLayerDataList()
        layers = list()
        for layer_data in sim_pelt_layers_data.get('layers', tuple()):
            layer = Outfits_pb2.PeltLayerData()
            layer.color = layer_data.get('color')
            layer.layer_id = layer_data.get('layer_id')
            layers.append(layer)
        # noinspection PyUnresolvedReferences
        pelt_layer_data.layers.extend(layers)
        sim_info.pelt_layers = pelt_layer_data.SerializeToString()

    @classmethod
    def _load_facial_attribute_data(cls, sim_info: SimInfo, facial_attributes_data: Dict[str, Any]):
        from protocolbuffers.PersistenceBlobs_pb2 import BlobSimFacialCustomizationData
        facial_attributes = BlobSimFacialCustomizationData()

        face_modifiers = list()
        for face_modifier in facial_attributes_data.get('face_modifiers', tuple()):
            modifier = BlobSimFacialCustomizationData().Modifier()
            modifier.key = face_modifier.get('modifier_key')
            modifier.amount = face_modifier.get('modifier_value')
            face_modifiers.append(modifier)

        # noinspection PyUnresolvedReferences
        facial_attributes.face_modifiers.extend(face_modifiers)

        body_modifiers = list()
        for body_modifier in facial_attributes_data.get('body_modifiers', tuple()):
            modifier = BlobSimFacialCustomizationData().Modifier()
            modifier.key = body_modifier.get('modifier_key')
            modifier.amount = body_modifier.get('modifier_value')
            body_modifiers.append(modifier)

        # noinspection PyUnresolvedReferences
        facial_attributes.body_modifiers.extend(body_modifiers)

        sculpts = list()
        for sculpt in facial_attributes_data.get('sculpts', tuple()):
            sculpt: int = sculpt
            sculpts.append(sculpt)

        # noinspection PyUnresolvedReferences
        facial_attributes.sculpts.extend(sculpts)

        sim_info.facial_attributes = facial_attributes.SerializeToString()

    @classmethod
    def _load_genetics_data(cls, sim_info: SimInfo, sim_genetics_data: Dict[str, Any]):
        genetic_data = Outfits_pb2.GeneticData()

        genetic_data.physique = sim_genetics_data.get('physique')
        genetic_data.voice_actor = sim_genetics_data.get('voice_actor')
        genetic_data.voice_pitch = sim_genetics_data.get('voice_pitch')

        from protocolbuffers.PersistenceBlobs_pb2 import BlobSimFacialCustomizationData
        facial_attributes = BlobSimFacialCustomizationData()

        sculpt_and_modifiers_data = sim_genetics_data.get('sculpts_and_modifiers', dict())

        face_modifiers = list()
        # noinspection PyUnresolvedReferences
        for face_modifier in sculpt_and_modifiers_data.get('face_modifiers', tuple()):
            modifier = BlobSimFacialCustomizationData().Modifier()
            modifier.key = face_modifier.get('modifier_key')
            modifier.amount = face_modifier.get('modifier_value')
            face_modifiers.append(modifier)

        # noinspection PyUnresolvedReferences
        facial_attributes.face_modifiers.extend(face_modifiers)

        body_modifiers = list()
        # noinspection PyUnresolvedReferences
        for body_modifier in sculpt_and_modifiers_data.get('body_modifiers', tuple()):
            modifier = BlobSimFacialCustomizationData().Modifier()
            modifier.key = body_modifier.get('modifier_key')
            modifier.amount = body_modifier.get('modifier_value')
            body_modifiers.append(modifier)

        # noinspection PyUnresolvedReferences
        facial_attributes.body_modifiers.extend(body_modifiers)

        sculpts = list()
        # noinspection PyUnresolvedReferences
        for sculpt in sculpt_and_modifiers_data.get('sculpts', tuple()):
            sculpt: int = sculpt
            sculpts.append(sculpt)

        # noinspection PyUnresolvedReferences
        facial_attributes.sculpts.extend(sculpts)

        genetic_data.sculpts_and_mods_attr = facial_attributes.SerializeToString()

        growth_parts_items = list()
        # noinspection PyUnresolvedReferences
        for part in sim_genetics_data.get('growth_parts_items', tuple()):  # RepeatedCompositeContainer
            # noinspection PyUnresolvedReferences
            part_id = part.get('part_id', None)
            # noinspection PyUnresolvedReferences
            part_body_type = part.get('part_body_type', None)
            # noinspection PyUnresolvedReferences
            part_color_shift = part.get('part_color_shift', None)
            if part_id is None or part_body_type is None or part_color_shift is None:
                continue

            part_item = Outfits_pb2.PartData()
            part_item.id = part_id
            part_item.body_type = part_body_type
            part_item.color_shift = part_color_shift
            growth_parts_items.append(part_item)

        genetic_data.growth_parts_list = Outfits_pb2.PartDataList()
        if growth_parts_items:
            # noinspection PyUnresolvedReferences
            genetic_data.growth_parts_list.parts.extend(growth_parts_items)

        parts_items = list()
        # noinspection PyUnresolvedReferences
        for part in sim_genetics_data.get('parts_items', tuple()):  # RepeatedCompositeContainer
            # noinspection PyUnresolvedReferences
            part_id = part.get('part_id', None)
            # noinspection PyUnresolvedReferences
            part_body_type = part.get('part_body_type', None)
            # noinspection PyUnresolvedReferences
            part_color_shift = part.get('part_color_shift', None)
            if part_id is None or part_body_type is None or part_color_shift is None:
                continue

            part_item = Outfits_pb2.PartData()
            part_item.id = part_id
            part_item.body_type = part_body_type
            part_item.color_shift = part_color_shift
            parts_items.append(part_item)

        genetic_data.parts_list = Outfits_pb2.PartDataList()
        # noinspection PyUnresolvedReferences
        genetic_data.parts_list.parts.extend(parts_items)

        sim_info.genetic_data = genetic_data.SerializeToString()

    @classmethod
    def _load_pronouns_data(cls, sim_info: SimInfo, sim_pronouns_data: Dict[str, Any]):
        from protocolbuffers import S4Common_pb2
        pronouns_list = S4Common_pb2.SimPronounList()
        pronouns = list()
        # noinspection PyUnresolvedReferences
        for sim_pronoun in sim_pronouns_data.get('pronouns'):  # RepeatedCompositeContainer
            pronoun = SimPronoun()
            pronoun.pronoun = sim_pronoun.get('pronoun')
            pronoun.case = sim_pronoun.get('pronoun_case')
            pronouns.append(pronoun)

        # noinspection PyUnresolvedReferences
        pronouns_list.pronouns.extend(pronouns)
        sim_info.pronouns = pronouns_list.SerializeToString()

    # Save
    @classmethod
    def _build_sim_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        """build_sim_data(sim_info)

        Convert a SimInfo object into a serializable dictionary of data.

        :param sim_info:
        :return:
        """
        sim_save_data = dict()
        sim_info._set_fit_fat()
        sim_save_data['physical_attributes'] = cls._build_physical_attributes(sim_info)

        sim_save_data['first_name'] = sim_info._base.first_name
        sim_save_data['last_name'] = sim_info._base.last_name
        sim_save_data['breed_name'] = sim_info._base.breed_name
        sim_save_data['first_name_key'] = sim_info._base.first_name_key
        sim_save_data['last_name_key'] = sim_info._base.last_name_key
        sim_save_data['full_name_key'] = sim_info._base.full_name_key
        sim_save_data['breed_name_key'] = sim_info._base.breed_name_key
        sim_save_data['gender'] = CommonGender.get_gender(sim_info).name
        sim_save_data['species'] = CommonSpecies.get_species(sim_info).name
        sim_save_data['age'] = CommonAge.get_age(sim_info).name
        sim_save_data['custom_texture'] = sim_info._base.custom_texture
        sim_save_data['pronouns_data'] = cls._build_pronouns(sim_info._base)
        from objects.components.consumable_component import ConsumableComponent
        sim_save_data['fat'] = sim_info.commodity_tracker.get_value(ConsumableComponent.FAT_COMMODITY)
        sim_save_data['fit'] = sim_info.commodity_tracker.get_value(ConsumableComponent.FIT_COMMODITY)

        sim_save_data['lod'] = sim_info._get_persisted_lod().name

        sim_save_data['outfit_data'] = cls._build_outfit_data(sim_info._base)

        sim_save_data['occult_data'] = cls._build_occult_data(sim_info)
        death_data = cls._build_death_data(sim_info)
        if death_data is not None:
            sim_save_data['death_data'] = death_data

        # attributes_save.genealogy_tracker = sim_info._genealogy_tracker.save_genealogy()
        # attributes_save.pregnancy_tracker = sim_info._pregnancy_tracker.save()
        # attributes_save.sim_careers = sim_info._career_tracker.save()
        sim_save_data['trait_data'] = cls._build_trait_data(sim_info)
        # for (tag, obj_id) in sim_info._autonomy_scoring_preferences.items():
        #     with ProtocolBufferRollback(attributes_save.object_preferences.preferences) as entry:
        #         entry.tag = tag
        #         entry.object_id = obj_id
        # for (tag, obj_id) in sim_info._autonomy_use_preferences.items():
        #     with ProtocolBufferRollback(attributes_save.object_ownership.owned_object) as entry:
        #         entry.tag = tag
        #         entry.object_id = obj_id
        # stored_object_info_component = cls.get_component(objects.components.types.STORED_OBJECT_INFO_COMPONENT)
        # if stored_object_info_component is not None:
        #     attributes_save.stored_object_info_component = stored_object_info_component.get_save_data()
        commodity_data = cls._build_commodity_data(sim_info)
        if commodity_data is not None:
            sim_save_data['commodity_data'] = commodity_data
        statistics_data = cls._build_statistics_data(sim_info)
        if statistics_data is not None:
            sim_save_data['statistics_data'] = statistics_data

        if sim_info.is_human:
            trait_statistic_data = cls._build_trait_statistic_data(sim_info)
            if trait_statistic_data is not None:
                sim_save_data['trait_statistic_data'] = trait_statistic_data
        sim_save_data['suntan_data'] = cls._build_suntan_data(sim_info)

        # if sim_info._familiar_tracker is not None:
        #     attributes_save.familiar_tracker = sim_info._familiar_tracker.save()
        # if sim_info._favorites_tracker is not None:
        #     favorites_save = sim_info._favorites_tracker.save()
        #     if sim_info.get_sim_instance() is None and old_attributes_save is not None:
        #         favorites_save.stack_favorites.extend(old_attributes_save.favorites_tracker.stack_favorites)
        #     attributes_save.favorites_tracker = favorites_save
        # if sim_info._aspiration_tracker is not None:
        #     sim_info._aspiration_tracker.save(attributes_save.event_data_tracker)
        # if sim_info._unlock_tracker is not None:
        #     attributes_save.unlock_tracker = sim_info._unlock_tracker.save_unlock()
        # if sim_info._notebook_tracker is not None:
        #     attributes_save.notebook_tracker = sim_info._notebook_tracker.save_notebook()
        # if sim_info._adventure_tracker is not None:
        #     attributes_save.adventure_tracker = sim_info._adventure_tracker.save()
        # if sim_info._royalty_tracker is not None:
        #     attributes_save.royalty_tracker = sim_info._royalty_tracker.save()
        # if sim_info._relic_tracker is not None:
        #     attributes_save.relic_tracker = sim_info._relic_tracker.save()
        # if sim_info._sickness_tracker is not None:
        #     if sim_info._sickness_tracker.should_persist_data():
        #         attributes_save.sickness_tracker = sim_info._sickness_tracker.sickness_tracker_save_data()
        # if sim_info._lifestyle_brand_tracker is not None:
        #     attributes_save.lifestyle_brand_tracker = sim_info._lifestyle_brand_tracker.save()
        # if sim_info._degree_tracker is not None:
        #     attributes_save.degree_tracker = sim_info._degree_tracker.save()
        # if sim_info._organization_tracker is not None:
        #     attributes_save.organization_tracker = sim_info._organization_tracker.save()
        # if sim_info._fixup_tracker is not None:
        #     attributes_save.fixup_tracker = sim_info._fixup_tracker.save()

        sim_save_data['appearance_data'] = cls._build_appearance_data(sim_info)

        # if sim_info._story_progression_tracker is not None:
        #     story_progression_data = SimObjectAttributes_pb2.PersistableStoryProgressionTracker()
        #     sim_info._story_progression_tracker.save(story_progression_data)
        #     attributes_save.story_progression_tracker = story_progression_data
        # if sim_info._lunar_effect_tracker is not None and sim_info._lunar_effect_tracker.has_data_to_save:
        #     lunar_effect_data = SimObjectAttributes_pb2.PersistableLunarEffectTracker()
        #     sim_info._lunar_effect_tracker.save_lunar_effects(lunar_effect_data)
        #     attributes_save.lunar_effect_tracker = lunar_effect_data

        sim_save_data['age_progress'] = sim_info._age_progress.get_value()
        sim_save_data['primary_aspiration'] = sim_info._primary_aspiration.guid64 if sim_info._primary_aspiration is not None else 0

        current_outfit_info = dict()
        # noinspection PyPropertyAccess
        current_outfit = sim_info.get_current_outfit()
        if current_outfit is None:
            (outfit_type, outfit_index) = (OutfitCategory.EVERYDAY, 0)
        else:
            (outfit_type, outfit_index) = current_outfit
        if outfit_index == SpecialOutfitIndex.DEFAULT:
            previous_outfit = sim_info.get_previous_outfit()
            if previous_outfit is None:
                (outfit_type, outfit_index) = (OutfitCategory.EVERYDAY, 0)
            else:
                (outfit_type, outfit_index) = previous_outfit
        if outfit_type == OutfitCategory.SPECIAL and outfit_type == OutfitCategory.BATHING:
            outfit_type = OutfitCategory.EVERYDAY
            outfit_index = 0
        outfit_category_tuning = OutfitTuning.OUTFIT_CATEGORY_TUNING.get(outfit_type)
        outfit_type = CommonOutfitUtils.convert_value_to_outfit_category(outfit_type)
        if outfit_category_tuning.save_outfit_category is None:
            current_outfit_info['outfit_category'] = outfit_type.name
        else:
            current_outfit_info['outfit_category'] = outfit_category_tuning.save_outfit_category.name
        current_outfit_info['outfit_index'] = outfit_index
        sim_save_data['current_outfit_info'] = current_outfit_info

        sim_save_data['additional_bonus_days'] = sim_info._additional_bonus_days
        sim_save_data['saved_at_time'] = CommonRealDateUtils.get_current_date_string()

        if sim_info._initial_fitness_value is not None:
            sim_save_data['initial_fitness_value'] = sim_info._initial_fitness_value

        favorite_recipe_ids = list()
        for recipe in sim_info._favorite_recipes:
            favorite_recipe_ids.append(recipe.guid64)
        if favorite_recipe_ids:
            sim_save_data['favorite_recipe_ids'] = favorite_recipe_ids

        if sim_info._bucks_tracker is not None:
            sim_save_data['bucks_data'] = cls._build_bucks_data(sim_info)
        return sim_save_data

    @classmethod
    def _build_facial_attributes(cls, sim_info: SimInfo) -> Dict[str, Any]:
        facial_attributes_data = dict()
        from protocolbuffers.PersistenceBlobs_pb2 import BlobSimFacialCustomizationData
        facial_attributes = BlobSimFacialCustomizationData()
        # noinspection PyPropertyAccess
        facial_attributes.MergeFromString(sim_info.facial_attributes)

        face_modifiers = list()
        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            face_modifier_key = face_modifier.key
            face_modifier_value = face_modifier.amount
            face_modifier_data = dict()
            face_modifier_data['modifier_key'] = face_modifier_key
            face_modifier_data['modifier_value'] = face_modifier_value
            face_modifiers.append(face_modifier_data)
        facial_attributes_data['face_modifiers'] = face_modifiers

        body_modifiers = list()
        # noinspection PyUnresolvedReferences
        for body_modifier in facial_attributes.body_modifiers:
            body_modifier_key = body_modifier.key
            body_modifier_value = body_modifier.amount
            body_modifier_data = dict()
            body_modifier_data['modifier_key'] = body_modifier_key
            body_modifier_data['modifier_value'] = body_modifier_value
            body_modifiers.append(body_modifier_data)
        facial_attributes_data['body_modifiers'] = body_modifiers

        sculpts = list()
        # noinspection PyUnresolvedReferences
        for sculpt in facial_attributes.sculpts:
            sculpt: int = sculpt
            sculpts.append(sculpt)
        facial_attributes_data['sculpts'] = sculpts
        return facial_attributes_data

    @classmethod
    def _build_pronouns(cls, sim_info: SimInfo) -> Dict[str, Any]:
        sim_pronouns_data = dict()
        from protocolbuffers import S4Common_pb2
        pronouns_list = S4Common_pb2.SimPronounList()
        pronouns_list.MergeFromString(sim_info.pronouns)
        pronouns_data = list()
        # noinspection PyUnresolvedReferences
        for sim_pronoun in pronouns_list.pronouns:  # RepeatedCompositeContainer
            sim_pronoun: SimPronoun = sim_pronoun
            # noinspection PyUnresolvedReferences
            pronoun = sim_pronoun.pronoun
            # noinspection PyUnresolvedReferences
            case = sim_pronoun.case
            pronoun_info = dict()
            pronoun_info['pronoun'] = pronoun
            pronoun_info['pronoun_case'] = case
            pronouns_data.append(pronoun_info)
        sim_pronouns_data['pronouns'] = pronouns_data
        return sim_pronouns_data

    @classmethod
    def _build_pelt_layers(cls, sim_info: SimInfo) -> Dict[str, Any]:
        sim_pelt_layers_data = dict()
        pelt_layer_data = Outfits_pb2.PeltLayerDataList()
        # noinspection PyPropertyAccess
        pelt_layer_data.MergeFromString(sim_info.pelt_layers)
        pelt_layers = list()
        # noinspection PyUnresolvedReferences
        for layer in pelt_layer_data.layers:
            layer: Outfits_pb2.PeltLayerData = layer
            layer_data = dict()
            # noinspection PyUnresolvedReferences
            color = layer.color
            # noinspection PyUnresolvedReferences
            layer_id = layer.layer_id
            layer_data['color'] = color
            layer_data['layer_id'] = layer_id
            pelt_layers.append(layer_data)

        sim_pelt_layers_data['layers'] = pelt_layers
        return sim_pelt_layers_data

    @classmethod
    def _build_bucks_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        bucks_tracker = sim_info._bucks_tracker
        sim_bucks_data = dict()
        bucks_list = list()
        for bucks_type in CommonBucksType.get_all():
            vanilla_bucks_type = CommonBucksType.convert_to_vanilla(bucks_type)
            bucks_data = dict()
            bucks_data['bucks_type'] = bucks_type.name
            bucks_data['amount'] = bucks_tracker._bucks.get(vanilla_bucks_type, 0)
            bucks_perk_data = list()
            for (perk, perk_data) in bucks_tracker._unlocked_perks[vanilla_bucks_type].items():
                unlocked_perks_data = dict()
                unlocked_perks_data['perk_id'] = perk.guid64
                unlocked_perks_data['currently_unlocked'] = perk_data.currently_unlocked
                if perk_data.unlocked_by is not None:
                    unlocked_perks_data['unlock_reason'] = perk_data.unlocked_by.guid64
                if perk in bucks_tracker._inactive_perk_timers[vanilla_bucks_type]:
                    unlocked_perks_data['time_left'] = bucks_tracker._inactive_perk_timers[vanilla_bucks_type][perk]
                bucks_perk_data.append(unlocked_perks_data)
            bucks_data['perk_data'] = bucks_perk_data
            bucks_list.append(bucks_data)
        sim_bucks_data['bucks'] = bucks_list
        return sim_bucks_data

    @classmethod
    def _build_appearance_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        appearance_tracker = sim_info.appearance_tracker
        appearance_data = dict()
        appearance_items = list()
        for (guid, seed) in sorted(list(appearance_tracker._persisted_appearance_data.items()), key=lambda x: x[0]):
            appearance_item_data = dict()
            appearance_item_data['guid'] = guid
            appearance_item_data['seed'] = seed
            appearance_items.append(appearance_item_data)
        appearance_data['appearance_items'] = appearance_items
        return appearance_data

    @classmethod
    def _build_suntan_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        suntan_tracker = sim_info._suntan_tracker
        suntan_data = dict()
        suntan_parts = list()
        suntan_data['tan_level'] = suntan_tracker._tan_level
        if suntan_tracker._outfit_part_data_list is not None:
            for (part_id, body_type) in suntan_tracker._outfit_part_data_list:
                part_tan_data = dict()
                part_tan_data['part_id'] = part_id
                part_tan_data['body_type'] = int(body_type)
                suntan_parts.append(part_tan_data)
        suntan_data['suntan_parts'] = suntan_parts
        return suntan_data

    @classmethod
    def _build_trait_statistic_data(cls, sim_info: SimInfo) -> Union[Dict[str, Any], None]:
        trait_statistic_tracker = sim_info.trait_statistic_tracker
        if trait_statistic_tracker._statistics is None:
            return None
        trait_statistic_data = dict()
        trait_statistics = list()
        for statistic in sorted(list(trait_statistic_tracker._statistics.values()), key=lambda x: x.guid64 if x is not None and hasattr(x, 'guid64') else 0):
            stat_data = dict()
            stat_id = statistic.guid64
            if stat_id is None or stat_id == 0:
                continue
            stat_data['stat_id'] = stat_id
            stat_data['stat_value'] = statistic.get_value()
            stat_data['stat_state'] = statistic._state.name
            if statistic._neglect_buff_index is not None:
                stat_data['neglect_buff_index'] = statistic._neglect_buff_index
            stat_data['value_added'] = statistic._value_added
            if statistic._max_daily_cap is not None:
                stat_data['max_daily_cap'] = statistic._max_daily_cap
            if statistic._min_daily_cap is not None:
                stat_data['min_daily_cap'] = statistic._min_daily_cap
            trait_statistics.append(stat_data)
        if trait_statistics:
            trait_statistic_data['trait_statistics'] = trait_statistics
        if not trait_statistic_data:
            return None
        return trait_statistic_data

    @classmethod
    def _build_statistics_data(cls, sim_info: SimInfo) -> Union[Dict[str, Any], None]:
        statistics_tracker = sim_info.statistic_tracker
        statistics_tracker.check_for_unneeded_initial_statistics()
        if statistics_tracker._statistics is None:
            return None
        statistics_data = dict()
        stat_list = list()
        for (stat_type, stat) in sorted(list(statistics_tracker._statistics.items()), key=lambda x: x[0].guid64 if x[0] is not None and hasattr(x[0], 'guid64') else 0):
            if not stat_type.persisted:
                continue
            try:
                if stat is None or not hasattr(stat_type, 'guid64'):
                    continue
                stat_id = stat_type.guid64
                if stat_id is None or stat_id == 0:
                    continue
                current_value = stat.get_saved_value()
                stat_data = dict()
                stat_data['stat_id'] = stat_id
                stat_data['stat_value'] = current_value
                stat_list.append(stat_data)
            except Exception as ex:
                log.error(f'thrown while trying to save stat {stat}', exception=ex, throw=False)
                continue
        if not stat_list:
            return None
        statistics_data['statistics'] = stat_list
        return statistics_data

    @classmethod
    def _build_commodity_data(cls, sim_info: SimInfo) -> Union[Dict[str, Any], None]:
        sim_commodity_data = dict()
        commodities = list()
        skills = list()
        ranked_statistics = list()
        other_statistics = list()
        commodity_tracker = sim_info.commodity_tracker

        for stat in sorted(list(commodity_tracker._statistics_values_gen()), key=lambda x: x.guid64 if x is not None and hasattr(x, 'guid64') else 0):
            if not stat.persisted:
                continue

            stat_id = stat.guid64
            if stat_id is None or stat_id == 0:
                continue
            current_value = stat.get_saved_value()
            statistic_data = dict()
            statistic_data['stat_id'] = stat_id
            statistic_data['stat_value'] = current_value

            if stat.is_skill or isinstance(stat, Skill) or isinstance(stat, LifeSkillStatistic):
                # noinspection PyUnresolvedReferences
                if hasattr(stat, 'initial_value') and current_value == stat.initial_value:
                    continue
                skills.append(statistic_data)
                continue

            if stat.is_commodity or isinstance(stat, Commodity):
                commodities.append(statistic_data)
                continue

            if stat.is_ranked or isinstance(stat, RankedStatistic):
                ranked_statistics.append(statistic_data)
                continue

            other_statistics.append(statistic_data)

        if commodities:
            sim_commodity_data['commodities'] = commodities
        if skills:
            sim_commodity_data['skills'] = skills
        if ranked_statistics:
            sim_commodity_data['ranked_statistics'] = ranked_statistics
        if other_statistics:
            sim_commodity_data['other_statistics'] = other_statistics

        if not sim_commodity_data:
            return None
        return sim_commodity_data

    @classmethod
    def _build_trait_data(cls, sim_info: SimInfo) -> Union[Dict[str, Any], None]:
        trait_tracker = sim_info._trait_tracker
        trait_ids = [trait.guid64 for trait in trait_tracker._equipped_traits if trait.persistable]
        if trait_tracker._delayed_active_lod_traits is not None:
            trait_ids.extend(trait.guid64 for trait in trait_tracker._delayed_active_lod_traits)
        trait_data = dict()
        trait_data['trait_ids'] = trait_ids
        return trait_data

    @classmethod
    def _build_death_data(cls, sim_info: SimInfo) -> Union[Dict[str, Any], None]:
        death_type = CommonSimDeathUtils.get_death_type(sim_info)
        if death_type == CommonDeathType.NONE:
            return None
        sim_death_data = dict()
        sim_death_data['death_type'] = death_type.name
        return sim_death_data

    @classmethod
    def _build_occult_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        sim_occult_data = dict()
        occult_tracker = sim_info._occult_tracker
        occult_tracker_sim_info = occult_tracker._sim_info
        sim_occult_types = occult_tracker_sim_info.occult_types
        occult_types = list()
        for occult_type_val in OccultType.list_values_from_flags(sim_occult_types):
            occult_type_type = CommonResourceUtils.get_enum_by_int_value(int(occult_type_val), OccultType, default_value=None)
            if occult_type_type is None or not hasattr(occult_type_type, 'name'):
                continue
            occult_types.append(occult_type_type.name)
        sim_occult_data['occult_types'] = occult_types
        current_occult_types = list()
        for current_occult_type_val in OccultType.list_values_from_flags(occult_tracker_sim_info.current_occult_types):
            current_occult_type_type = CommonResourceUtils.get_enum_by_int_value(int(current_occult_type_val), OccultType, default_value=None)
            if current_occult_type_type is None or not hasattr(current_occult_type_type, 'name'):
                continue
            current_occult_types.append(current_occult_type_type.name)
        sim_occult_data['current_occult_types'] = current_occult_types
        occult_form_available = occult_tracker._occult_form_available
        sim_occult_data['occult_form_available'] = occult_form_available
        if occult_tracker._pending_occult_type is not None:
            pending_occult_type = occult_tracker._pending_occult_type
            if pending_occult_type is not None and pending_occult_type != 0:
                pending_occult_type_type = CommonResourceUtils.get_enum_by_int_value(int(pending_occult_type), OccultType, default_value=None)
                if pending_occult_type_type is not None and hasattr(pending_occult_type_type, 'name'):
                    sim_occult_data['pending_occult_type'] = pending_occult_type_type.name

        sim_occult_types_data = dict()
        for (occult_type, occult_sim_info) in occult_tracker._sim_info_map.items():
            occult_type_type = CommonResourceUtils.get_enum_by_int_value(int(occult_type), OccultType, default_value=None)
            if occult_type_type is None or not hasattr(occult_type_type, 'name'):
                continue
            occult_type_data = dict()
            occult_tracker._copy_shared_attributes(sim_info, occult_type, occult_tracker._sim_info, occult_tracker._sim_info.current_occult_types)
            occult_type_data['occult_type'] = occult_type_type.name
            occult_type_data['occult_outfit_data'] = cls._build_outfit_data(occult_sim_info._base)
            occult_type_data['occult_physical_attributes'] = cls._build_physical_attributes(occult_sim_info)
            sim_occult_types_data[occult_type_type.name] = occult_type_data
        sim_occult_data['occult_info_by_occult_type'] = sim_occult_types_data
        return sim_occult_data

    @classmethod
    def _build_outfit_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        outfits_msg = Outfits_pb2.OutfitList()
        outfits_msg.ParseFromString(sim_info.outfits)

        outfits_by_category = dict()
        # noinspection PyUnresolvedReferences
        for outfit in outfits_msg.outfits:  # RepeatedCompositeContainer
            outfit: Outfits_pb2.OutfitData = outfit
            # noinspection PyUnresolvedReferences
            category: OutfitCategory = CommonOutfitUtils.convert_value_to_outfit_category(outfit.category)
            if not isinstance(category, OutfitCategory):
                continue
            if category.name not in outfits_by_category:
                outfits_by_category[category.name] = list()
            outfits_list = outfits_by_category[category.name]
            outfit_data = dict()
            # noinspection PyUnresolvedReferences
            body_types_list: Outfits_pb2.BodyTypesList = outfit.body_types_list
            # noinspection PyUnresolvedReferences
            body_types = body_types_list.body_types
            # noinspection PyUnresolvedReferences
            parts: S4Common_pb2.IdList = outfit.parts
            # noinspection PyUnresolvedReferences
            part_ids = parts.ids
            part_data_list = list()
            # noinspection PyUnresolvedReferences
            part_shifts: Outfits_pb2.ColorShiftList = outfit.part_shifts
            # noinspection PyUnresolvedReferences
            part_shift_colors = part_shifts.color_shift
            parts_info = zip(body_types, part_ids, part_shift_colors)
            for (body_type, part_id, part_color_shift) in parts_info:
                part_data = dict()
                part_data['body_type'] = body_type
                part_data['part_id'] = part_id
                part_data['part_color_shift'] = part_color_shift
                part_data_list.append(part_data)

            outfit_data['part_data_list'] = part_data_list
            # noinspection PyUnresolvedReferences
            outfit_id: int = outfit.outfit_id
            # noinspection PyUnresolvedReferences
            outfit_flags: int = outfit.outfit_flags
            # noinspection PyUnresolvedReferences
            outfit_flags_high: int = outfit.outfit_flags_high
            # noinspection PyUnresolvedReferences
            title: str = outfit.title
            # noinspection PyUnresolvedReferences
            match_hair_style: bool = outfit.match_hair_style
            # noinspection PyUnresolvedReferences
            created: int = outfit.created
            outfit_data['outfit_id'] = outfit_id
            outfit_data['category'] = category.name
            outfit_data['outfit_flags'] = outfit_flags
            outfit_data['outfit_flags_high'] = outfit_flags_high
            outfit_data['title'] = title
            outfit_data['match_hair_style'] = match_hair_style
            outfit_data['created'] = created
            outfit_data['outfit_index'] = len(outfits_list)
            outfits_list.append(outfit_data)
            outfits_by_category[category.name] = outfits_list
        return outfits_by_category

    @classmethod
    def _build_physical_attributes(cls, sim_info: SimInfo) -> Dict[str, Any]:
        physical_attributes_data = dict()
        # noinspection PyPropertyAccess
        physical_attributes_data['physique'] = sim_info.physique

        # noinspection PyPropertyAccess
        physical_attributes_data['voice_pitch'] = sim_info.voice_pitch
        # noinspection PyPropertyAccess
        physical_attributes_data['voice_actor'] = sim_info.voice_actor
        # noinspection PyPropertyAccess
        physical_attributes_data['voice_effect'] = sim_info.voice_effect
        # noinspection PyPropertyAccess
        physical_attributes_data['skin_tone'] = sim_info.skin_tone
        # noinspection PyPropertyAccess
        physical_attributes_data['skin_tone_val_shift'] = sim_info.skin_tone_val_shift

        physical_attributes_data['facial_attributes'] = cls._build_facial_attributes(sim_info)

        physical_attributes_data['flags'] = sim_info.flags
        if hasattr(sim_info, 'pelt_layers'):
            physical_attributes_data['pelt_layers'] = cls._build_pelt_layers(sim_info)

        if hasattr(sim_info, 'base_trait_ids'):
            # originally a tuple, convert it to a tuple when setting it!
            physical_attributes_data['base_trait_ids'] = sorted(list(sim_info.base_trait_ids), key=lambda x: x)

        physical_attributes_data['genetics_data'] = cls._build_genetics_data(sim_info)
        return physical_attributes_data

    @classmethod
    def _build_genetics_data(cls, sim_info: SimInfo) -> Dict[str, Any]:
        sim_genetics_data = dict()
        genetic_data = Outfits_pb2.GeneticData()
        # noinspection PyPropertyAccess
        genetic_data.MergeFromString(sim_info.genetic_data)
        # noinspection PyUnresolvedReferences
        growth_parts_list: Outfits_pb2.PartDataList = genetic_data.growth_parts_list
        # noinspection PyUnresolvedReferences
        parts_list: Outfits_pb2.PartDataList = genetic_data.parts_list
        # noinspection PyUnresolvedReferences
        physique: str = genetic_data.physique
        sculpts_and_modifier_data = dict()
        from protocolbuffers.PersistenceBlobs_pb2 import BlobSimFacialCustomizationData
        facial_attributes = BlobSimFacialCustomizationData()
        # noinspection PyUnresolvedReferences
        facial_attributes.MergeFromString(genetic_data.sculpts_and_mods_attr)

        face_modifiers = list()
        # noinspection PyUnresolvedReferences
        for face_modifier in facial_attributes.face_modifiers:
            face_modifier_key = face_modifier.key
            face_modifier_value = face_modifier.amount
            face_modifier_data = dict()
            face_modifier_data['modifier_key'] = face_modifier_key
            face_modifier_data['modifier_value'] = face_modifier_value
            face_modifiers.append(face_modifier_data)
        sculpts_and_modifier_data['face_modifiers'] = face_modifiers

        body_modifiers = list()
        # noinspection PyUnresolvedReferences
        for body_modifier in facial_attributes.body_modifiers:
            body_modifier_key = body_modifier.key
            body_modifier_value = body_modifier.amount
            body_modifier_data = dict()
            body_modifier_data['modifier_key'] = body_modifier_key
            body_modifier_data['modifier_value'] = body_modifier_value
            body_modifiers.append(body_modifier_data)
        sculpts_and_modifier_data['body_modifiers'] = body_modifiers

        sculpts = list()
        # noinspection PyUnresolvedReferences
        for sculpt in facial_attributes.sculpts:
            sculpt: int = sculpt
            sculpts.append(sculpt)
        sculpts_and_modifier_data['sculpts'] = sculpts

        sim_genetics_data['sculpts_and_modifiers'] = sculpts_and_modifier_data

        # noinspection PyUnresolvedReferences
        voice_actor: int = genetic_data.voice_actor
        # noinspection PyUnresolvedReferences
        voice_pitch: float = genetic_data.voice_pitch
        growth_parts_items = list()
        # noinspection PyUnresolvedReferences
        for part in growth_parts_list.parts:  # RepeatedCompositeContainer
            part: Outfits_pb2.PartData = part
            # noinspection PyUnresolvedReferences
            part_id = part.id
            # noinspection PyUnresolvedReferences
            part_body_type = part.body_type
            # noinspection PyUnresolvedReferences
            part_color_shift = part.color_shift
            growth_part_item = dict()
            growth_part_item['part_id'] = part_id
            growth_part_item['part_body_type'] = part_body_type
            growth_part_item['part_color_shift'] = part_color_shift
            growth_parts_items.append(growth_part_item)

        sim_genetics_data['growth_parts_items'] = growth_parts_items

        parts_items = list()
        # noinspection PyUnresolvedReferences
        for part in parts_list.parts:  # RepeatedCompositeContainer
            part: Outfits_pb2.PartData = part
            # noinspection PyUnresolvedReferences
            part_id = part.id
            # noinspection PyUnresolvedReferences
            part_body_type = part.body_type
            # noinspection PyUnresolvedReferences
            part_color_shift = part.color_shift
            part_item = dict()
            part_item['part_id'] = part_id
            part_item['part_body_type'] = part_body_type
            part_item['part_color_shift'] = part_color_shift
            parts_items.append(part_item)
        sim_genetics_data['parts_items'] = parts_items

        sim_genetics_data['physique'] = physique
        sim_genetics_data['voice_actor'] = voice_actor
        sim_genetics_data['voice_pitch'] = voice_pitch
        return sim_genetics_data

    @classmethod
    def despawn_sim(
        cls,
        sim_info: SimInfo,
        source: str = None,
        cause: str = None,
        **kwargs
    ) -> bool:
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
        if cls.hard_reset(sim_info, reset_reason=ResetReason.BEING_DESTROYED, source=cls, cause='S4CL Despawn'):
            sim.destroy(source=source, cause=cause, **kwargs)
        return True

    @classmethod
    def schedule_sim_for_despawn(
        cls,
        sim_info: SimInfo,
        source: str = None,
        cause: str = None,
        on_despawn: Callable[[], None] = None,
        **kwargs
    ) -> bool:
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

    @classmethod
    def delete_sim(cls, sim_info: SimInfo, source: str = None, cause: str = None, **kwargs) -> bool:
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
        if not cls.despawn_sim(sim_info, source=source, cause=cause, **kwargs):
            return False
        client = services.client_manager().get_first_client()
        if sim_info.household is not None and hasattr(sim_info.household, 'refresh_aging_updates'):
            client.remove_selectable_sim_info(sim_info)
        household = sim_info.household or CommonHouseholdUtils.create_empty_household()
        sim_info.remove_permanently(household=household)
        return True

    @classmethod
    def soft_reset(
        cls,
        sim_info: SimInfo,
        reset_reason: ResetReason = ResetReason.RESET_EXPECTED,
        hard_reset_on_exception: bool = False,
        source: Any = None,
        cause: str = 'S4CL Soft Reset'
    ) -> bool:
        """soft_reset(\
            sim_info,\
            reset_reason=ResetReason.RESET_EXPECTED,\
            hard_reset_on_exception=False,\
            source=None,\
            cause='S4CL Soft Reset'\
        )

        Perform a soft reset on a Sim.

        :param sim_info: An instance of an Sim.
        :type sim_info: SimInfo
        :param reset_reason: The reason for the reset. Default is ResetReason.RESET_EXPECTED.
        :type reset_reason: ResetReason, optional
        :param hard_reset_on_exception: If set to True, a hard reset of the Object will be attempted upon an error occurring.\
            If set to False, nothing will occur if the reset failed. Default is False.
        :type hard_reset_on_exception: bool, optional
        :param source: The source of the reset. Default is the GameObject.
        :type source: Any, optional
        :param cause: Text indicating the cause of the reset. Default is 'S4CL Hard Reset'.
        :type cause: str, optional
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
                    interaction.cancel(FinishingType.KILLED, '{} sim.queue'.format(cause))
                sim.queue.on_reset()
                sim.queue.unlock()

            if sim.si_state is not None:
                for interaction in sim.si_state:
                    interaction.cancel(FinishingType.KILLED, '{} sim.si_state'.format(cause))
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
                posture_state = sim.posture_state
                if posture_state._primitive is not None:
                    # noinspection PyPropertyAccess
                    posture_state._primitive._prev_posture = None
                # noinspection PyPropertyAccess
                posture_state.on_reset(reset_reason)

            sim._stop_animation_interaction()
            sim.asm_auto_exit.clear()
            sim._start_animation_interaction()
            from postures.posture_specs import get_origin_spec
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
                return cls.hard_reset(sim_info, reset_reason, source=source, cause=cause)
        return False

    @classmethod
    def hard_reset(
        cls,
        sim_info: SimInfo,
        reset_reason: ResetReason = ResetReason.RESET_EXPECTED,
        source: Any = None,
        cause: str = 'S4CL Hard Reset'
    ) -> bool:
        """hard_reset(
            sim_info,\
            reset_reason=ResetReason.RESET_EXPECTED,\
            source=None,\
            cause='S4CL Hard Reset'\
        )

        Perform a hard reset on a SimInfo.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param reset_reason: The reason for the reset. Default is ResetReason.RESET_EXPECTED.
        :type reset_reason: ResetReason, optional
        :param source: The source of the reset. Default is None.
        :type source: Any, optional
        :param cause: Text indicating the cause of the reset. Default is 'S4CL Hard Reset'.
        :type cause: str, optional
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

    @classmethod
    def fade_in(
        cls,
        sim_info: SimInfo,
        fade_duration: float = 1.0,
        immediate: bool = False,
        additional_channels: Iterator[Tuple[int, int, int]] = None
    ):
        """fade_in(sim_info, fade_duration=1.0, immediate=False, additional_channels=None)

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

    @classmethod
    def fade_out(
        cls,
        sim_info: SimInfo,
        fade_duration: float = 1.0,
        immediate: bool = False,
        additional_channels: Iterator[Tuple[int, int, int]] = None
    ):
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


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_sims', 'Spawn Sims of a certain species, gender, and age.', command_arguments=(
    CommonConsoleCommandArgument('species', 'CommonSpecies',
                                 f'The spawned Sims will have this species. Valid species include: {CommonSpecies.get_comma_separated_names_string()}', is_optional=False),
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_sims(output: CommonConsoleCommandOutput, species: CommonSpecies, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    if species is None:
        return
    if gender == CommonGender.INVALID or not isinstance(gender, CommonGender):
        output(f'ERROR: {gender} is not a valid gender. Valid Genders: ({CommonGender.get_comma_separated_names_string()})')
        return
    if age == CommonAge.INVALID or not isinstance(age, CommonAge):
        output(f'ERROR: {age} is not a valid age. Valid Ages: ({CommonAge.get_comma_separated_names_string()})')
        return
    if count <= 0:
        output('ERROR: Please enter a count above zero.')
        return
    output(f'Spawning {count} {species.name} Sim(s) of Gender: {gender.name} and Age: {age.name}.')
    try:
        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_sim_location = CommonSimLocationUtils.get_location(active_sim_info)
        for x in range(count):
            created_sim_info = CommonSimSpawnUtils.create_sim_info(species, gender=gender, age=age)
            CommonSimSpawnUtils.spawn_sim(created_sim_info, location=active_sim_location)
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), f'Error spawning Sims {count} Sim(s) of Species: {species.name}, Gender: {gender.name}, and Age: {age.name}.', exception=ex)
        output('An error occurred while spawning Sim(s).')
    output(f'Done Spawning {count} {species.name} Sim(s) of Gender: {gender.name} and Age: {age.name}.')
    output('If the space around your Sim was too crowded for a new Sim to spawn, you may locate the spawned Sim(s) in front of the lot.')


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_human_sims', 'Spawn Human Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_human_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.HUMAN, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_large_dog_sims', 'Spawn Large Dog Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_large_dog_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.LARGE_DOG, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_small_dog_sims', 'Spawn Small Dog Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_small_dog_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.SMALL_DOG, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_cat_sims', 'Spawn Cat Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_cat_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.CAT, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_fox_sims', 'Spawn Fox Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_fox_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.FOX, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_horse_sims', 'Spawn Horse Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_horse_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.HORSE, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_random_sims', 'Spawn a random number of Sims.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=5),
))
def _s4clib_spawn_random_sims(output: CommonConsoleCommandOutput, count: int = 5):
    _s4cl_spawn_human_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.TODDLER)
    _s4cl_spawn_human_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.CHILD)
    _s4cl_spawn_human_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.ADULT)

    _s4cl_spawn_human_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.TODDLER)
    _s4cl_spawn_human_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.CHILD)
    _s4cl_spawn_human_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.ADULT)

    _s4cl_spawn_large_dog_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.CHILD)
    _s4cl_spawn_large_dog_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.ADULT)

    _s4cl_spawn_large_dog_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.CHILD)
    _s4cl_spawn_large_dog_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.ADULT)

    _s4cl_spawn_small_dog_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.CHILD)
    _s4cl_spawn_small_dog_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.ADULT)

    _s4cl_spawn_small_dog_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.CHILD)
    _s4cl_spawn_small_dog_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.ADULT)

    _s4cl_spawn_cat_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.CHILD)
    _s4cl_spawn_cat_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.ADULT)

    _s4cl_spawn_cat_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.CHILD)
    _s4cl_spawn_cat_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.ADULT)

    _s4cl_spawn_fox_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.ADULT)
    _s4cl_spawn_fox_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.ADULT)

    _s4cl_spawn_horse_sims(output, count=count, gender=CommonGender.MALE, age=CommonAge.CHILD)
    _s4cl_spawn_horse_sims(output, count=count, gender=CommonGender.FEMALE, age=CommonAge.ADULT)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_testing.spawn_sims', 'Spawn a number of Sims of each species.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4clib_spawn_random_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    for species in CommonSpecies.get_all():
        _s4cl_spawn_sims(output, species=species, count=count, gender=gender, age=age)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.purge_self',
    'Delete the active Sim. WARNING: Not recommended in single Sim households, since you cannot do interactions without an active Sim!'
)
def _s4cl_purge_self(output: CommonConsoleCommandOutput):
    active_sim_info = CommonSimUtils.get_active_sim_info()
    output(f'Purging the active Sim ({active_sim_info}) from existence.')
    return CommonSimSpawnUtils.delete_sim(active_sim_info)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.purge_sim',
    'Purge a Sim, essentially deleting them.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to purge.', is_optional=False),
    )
)
def _s4cl_purge_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo):
    if sim_info is None:
        return
    if sim_info is CommonSimUtils.get_active_sim_info():
        output('Failed, If you want to purge the active Sim, use "s4clib.purge_self" instead.')
        return
    output(f'Purging Sim from existence {sim_info}')
    CommonSimSpawnUtils.delete_sim(sim_info, source='Player', cause='Command Purged')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.be_alone',
    'Purge all Sims except the active Sim from the neighborhood.'
)
def _s4cl_be_alone(output: CommonConsoleCommandOutput):
    active_sim_info = CommonSimUtils.get_active_sim_info()
    output('Purging everyone but your active Sim.')
    sim_count = 0
    sim_info_list = tuple(CommonSimUtils.get_sim_info_for_all_sims_generator())
    for sim_info in sim_info_list:
        if sim_info is active_sim_info:
            continue
        CommonSimSpawnUtils.delete_sim(sim_info, source='Player', cause='Command Purged')
        sim_count += 1
    output(f'Purged {sim_count} Sims')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.purge_neighborhood',
    'Purge all Sims including the active Sim from the neighborhood, essentially making your neighborhood a ghost town. WARNING: Only use this for fun, since you cannot do interactions without an active Sim!'
)
def _s4cl_purge_neighborhood(output: CommonConsoleCommandOutput):
    output('Purging all Sims')
    sim_count = 0
    sim_info_list = tuple(CommonSimUtils.get_sim_info_for_all_sims_generator())
    for sim_info in sim_info_list:
        CommonSimSpawnUtils.delete_sim(sim_info, source='Player', cause='Command Purged')
        sim_count += 1
    output(f'Purged {sim_count} Sims')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.purge_non_household',
    'Purge all Sims outside of the active household.'
)
def _s4cl_purge_non_household(output: CommonConsoleCommandOutput):
    output('Purging all Sims outside of the Active Household.')
    sim_count = 0
    sim_info_list = tuple(CommonSimUtils.get_sim_info_for_all_sims_generator())
    from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
    for sim_info in sim_info_list:
        if CommonHouseholdUtils.is_part_of_active_household(sim_info):
            continue
        CommonSimSpawnUtils.delete_sim(sim_info, source='Player', cause='Command Purged')
        sim_count += 1
    output(f'Purged {sim_count} Sims')
