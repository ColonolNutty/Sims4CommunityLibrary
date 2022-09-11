"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from typing import Union, Tuple, Callable, Any, Iterator, Iterable
from sims.sim_info_lod import SimInfoLODLevel
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

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
        trait_ids: Iterable[int] = (),
        household: Household = None,
        source: str = 'testing'
    ) -> Union[SimInfo, None]:
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        household = household or CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
        vanilla_gender = CommonGender.convert_to_vanilla(gender)
        vanilla_age = CommonAge.convert_to_vanilla(age)
        vanilla_species = CommonSpecies.convert_to_vanilla(species)
        if vanilla_species is None:
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
        clone_sim_info = cls.create_sim_info(
            species=species,
            gender=gender,
            age=CommonAge.get_age(source_sim_info),
            first_name=SimSpawner.get_random_first_name(vanilla_gender, source_sim_info.species),
            last_name=source_sim_info._base.last_name,
            trait_ids=tuple(source_sim_info.trait_tracker.equipped_traits),
            household=household,
            source='cloning'
        )
        if clone_sim_info is None:
            return None
        try:
            source_sim_proto = source_sim_info.save_sim(for_cloning=True)
            clone_sim_id = clone_sim_info.sim_id
            source_first_name = source_sim_info._base.first_name
            source_last_name = source_sim_info._base.last_name
            source_breed_name = source_sim_info._base.breed_name
            source_first_name_key = source_sim_info._base.first_name_key
            source_last_name_key = source_sim_info._base.last_name_key
            source_full_name_key = source_sim_info._base.full_name_key
            source_breed_name_key = source_sim_info._base.breed_name_key
            clone_first_name = clone_sim_info._base.first_name
            clone_last_name = clone_sim_info._base.last_name
            clone_breed_name = clone_sim_info._base.breed_name
            clone_first_name_key = clone_sim_info._base.first_name_key
            clone_last_name_key = clone_sim_info._base.last_name_key
            clone_full_name_key = clone_sim_info._base.full_name_key
            clone_breed_name_key = clone_sim_info._base.breed_name_key
            clone_sim_info.load_sim_info(source_sim_proto, is_clone=True, default_lod=SimInfoLODLevel.FULL)
            clone_sim_info.sim_id = clone_sim_id
            clone_sim_info._base.first_name = clone_first_name or source_first_name
            clone_sim_info._base.last_name = clone_last_name or source_last_name
            clone_sim_info._base.breed_name = clone_breed_name or source_breed_name
            clone_sim_info._base.first_name_key = clone_first_name_key or source_first_name_key
            clone_sim_info._base.last_name_key = clone_last_name_key or source_last_name_key
            clone_sim_info._base.full_name_key = clone_full_name_key or source_full_name_key
            clone_sim_info._base.breed_name_key = clone_breed_name_key or source_breed_name_key
            clone_sim_info._household_id = household_id
            source_trait_tracker = source_sim_info.trait_tracker
            clone_trait_tracker = clone_sim_info.trait_tracker
            for trait in clone_trait_tracker.personality_traits:
                if not source_trait_tracker.has_trait(trait):
                    clone_sim_info.remove_trait(trait)
            for trait in clone_trait_tracker.gender_option_traits:
                if not source_trait_tracker.has_trait(trait):
                    clone_sim_info.remove_trait(trait)
            CommonSimUtils.get_sim_info_manager().set_default_genealogy(sim_infos=(clone_sim_info,))
            clone_sim_info.set_default_data()
            clone_sim_info.save_sim()
            household.save_data()
            if not household.is_active_household:
                clone_sim_info.request_lod(SimInfoLODLevel.BASE)
            clone_sim_info.resend_physical_attributes()
        except Exception as ex:
            cls.delete_sim(clone_sim_info)
            raise ex
        return clone_sim_info

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
                                 f'The spawned Large Dog Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
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
                                 f'The spawned Large Dog Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_human_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.HUMAN, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_large_dog_sims', 'Spawn Large Dog Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Large Dog Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_large_dog_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.LARGE_DOG, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_small_dog_sims', 'Spawn Small Dog Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Large Dog Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_small_dog_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.SMALL_DOG, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_cat_sims', 'Spawn Cat Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Large Dog Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_cat_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.CAT, count=count, gender=gender, age=age)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.spawn_fox_sims', 'Spawn Fox Sims of a certain gender and age.', command_arguments=(
    CommonConsoleCommandArgument('count', 'Number', 'The number of Sims to spawn.', is_optional=True, default_value=1),
    CommonConsoleCommandArgument('gender', 'CommonGender',
                                 f'The spawned Sims will have this gender. Valid genders include: {CommonGender.get_comma_separated_names_string()}', is_optional=True, default_value=CommonGender.MALE.name if hasattr(CommonGender.MALE, 'name') else CommonGender.MALE),
    CommonConsoleCommandArgument('age', 'CommonAge',
                                 f'The spawned Large Dog Sims will have this age. Valid ages include: {CommonAge.get_comma_separated_names_string()}', is_optional=True, default_value=CommonAge.ADULT.name if hasattr(CommonAge.ADULT, 'name') else CommonAge.ADULT)
))
def _s4cl_spawn_fox_sims(output: CommonConsoleCommandOutput, count: int = 1, gender: CommonGender = CommonGender.MALE, age: CommonAge = CommonAge.ADULT):
    return _s4cl_spawn_sims(output, CommonSpecies.FOX, count=count, gender=gender, age=age)


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
