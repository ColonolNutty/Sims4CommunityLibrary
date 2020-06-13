"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Callable

from protocolbuffers.Math_pb2 import Vector3
from routing import Location
from sims.household import Household
from sims.sim_info import SimInfo
from sims.sim_info_types import Gender, Age, Species
from sims.sim_spawner import SimCreator, SimSpawner
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


class CommonSimSpawnUtils:
    """Utilities for creating, spawning, and despawning Sims.

    """

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=None)
    def create_human_sim_info(
        gender: Gender=None,
        age: Age=None,
        first_name: str='',
        last_name: str='',
        trait_ids: Tuple[int]=(),
        household: Household=None,
        source: str='testing'
    ) -> Union[SimInfo, None]:
        """create_human_sim_info(\
            gender=None,\
            age=None,\
            species=None,\
            first_name='',\
            last_name='',\
            trait_ids=(),\
            household=None,\
            source='testing'\
        )

        Create SimInfo for a Human Sim.

        :param gender: The Gender of the created Sim. Default is None.
        :type gender: Gender, optional
        :param age: The Age of the created Sim. Default is None.
        :type age: Age, optional
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
        from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
        household = household or CommonHouseholdUtils.create_empty_household(as_hidden_household=True)
        sim_creator = SimCreator(gender=gender, age=age, first_name=first_name or SimSpawner.get_random_first_name(gender, Species.HUMAN), last_name=last_name, traits=trait_ids)
        (sim_info_list, _) = SimSpawner.create_sim_infos((sim_creator,), household=household, generate_deterministic_sim=True, creation_source=source)
        if not sim_info_list:
            return None
        return sim_info_list[0]

    @staticmethod
    def spawn_sim(sim_info: SimInfo, location: Location=None, position: Vector3=None, **kwargs) -> bool:
        """spawn_sim(sim_info, location=None, position=None, **kwargs)

        Spawn a Sim.

        ..note:: Do not provide sim_position or sim_location in kwargs as they are already specified as location and position.

        :param sim_info: The Sim to Spawn.
        :type sim_info: SimInfo
        :param location: The location to spawn the Sim at. Default is None.
        :type location: Location, optional
        :param position: The position to spawn the Sim at. Default is None.
        :type position: Vector3, optional
        :return: True, if the Sim was spawned successfully. False, if not.
        :rtype: bool
        """
        try:
            SimSpawner.spawn_sim(sim_info, sim_location=location, sim_position=position, **kwargs)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to spawn Sim with SimInfo \'{}\' at location \'{}\'.'.format(sim_info, location), exception=ex)
            return False
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
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
