"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Union, Iterator

import services
from sims.household import Household
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 's4cl_household_utils')


class CommonHouseholdUtils:
    """Utilities for manipulating households.

    """
    @staticmethod
    def get_active_household() -> Union[Household, None]:
        """Retrieve the Household of the Active Sim.

        """
        sim_info = CommonSimUtils.get_active_sim_info()
        return CommonHouseholdUtils.get_household(sim_info)

    @staticmethod
    def get_active_household_id() -> int:
        """Retrieve an identifier for the Household of the Active Sim.

        """
        sim_info = CommonSimUtils.get_active_sim_info()
        return CommonHouseholdUtils.get_household_lot_id(sim_info)

    @staticmethod
    def get_household_lot_id(sim_info: SimInfo) -> int:
        """Retrieve an identifier for the home lot of the specified Sim.

        """
        household = CommonHouseholdUtils.get_household(sim_info)
        if household is None:
            return 0
        return household.home_zone_id

    @staticmethod
    def get_sim_info_of_all_sims_in_active_household_generator() -> Iterator[SimInfo]:
        """Retrieve a collection of Sims that are a part of the active household.

        """
        household = CommonHouseholdUtils.get_active_household()
        for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_household_generator(household):
            yield sim_info

    @staticmethod
    def get_sim_info_of_all_sims_in_household_generator(household: Household) -> Iterator[SimInfo]:
        """Retrieve a collection of Sims that are a part of the active household.

        """
        if household is None:
            return tuple()
        for sim_info in list(household.sim_info_gen()):
            if sim_info is None:
                continue
            yield sim_info

    @staticmethod
    def is_part_of_active_household(sim_info: SimInfo) -> bool:
        """Determine if a Sim is part of the active household.

        """
        return sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator()

    @staticmethod
    def get_all_households_generator() -> Iterator[Household]:
        """Retrieve a collection of all households.

        """
        for household in list(services.household_manager().get_all()):
            if household is None:
                continue
            yield household

    @staticmethod
    def locate_household_by_name(name: str, allow_partial_match: bool=False, create_on_missing: bool=False, starting_funds: int=0, as_hidden_household: bool=False) -> Union[Household, None]:
        """Locate a household with the specified name.

        :param name: The name of a household to locate.
        :param create_on_missing: If True, a household will be created if one isn't found with the specified name.
        :param starting_funds: If a household is created, this will be the starting funds of that household.
        :param as_hidden_household: If True, the created household will be hidden.
        :param allow_partial_match: If True, households only need to contain the name to match.
        :return: A Household with the specified name.
        """
        for household in CommonHouseholdUtils.locate_households_by_name_generator(name, allow_partial_match=allow_partial_match):
            if household is None:
                continue
            return household
        if not create_on_missing:
            log.debug('No household found matching name \'{}\'.'.format(name))
            return None
        log.debug('No household found, creating one.')
        return CommonHouseholdUtils.create_empty_household(starting_funds=starting_funds, as_hidden_household=as_hidden_household)

    @staticmethod
    def locate_households_by_name_generator(name: str, allow_partial_match: bool=False) -> Iterator[Household]:
        """Locate all households with the specified name.

        :param name: The name of the households to locate.
        :param allow_partial_match: If True, households only need to contain the name to match.
        :return: A Household with the specified name.
        """
        if allow_partial_match:
            log.debug('Locating households containing name: \'{}\''.format(name))
        else:
            log.debug('Locating households with name: \'{}\''.format(name))
        for household in CommonHouseholdUtils.get_all_households_generator():
            if household is None:
                continue
            # noinspection PyPropertyAccess
            household_name = household.name
            # noinspection PyPropertyAccess
            log.debug('Checking household \'{}\' for match.'.format(household_name))
            if household_name is None:
                continue
            if allow_partial_match:
                if name not in household_name:
                    log.debug('Household name did not match.')
                    continue
            elif household_name != name:
                log.debug('Household name did not match.')
                continue
            log.debug('Located household.')
            yield household

    @staticmethod
    def create_empty_household(starting_funds: int=0, as_hidden_household: bool=False) -> Household:
        """Create an empty household.

        """
        household = Household(SimSpawner._get_default_account(), starting_funds=starting_funds)
        if as_hidden_household:
            household.set_to_hidden()
        services.household_manager().add(household)
        return household

    @staticmethod
    def add_sim_to_active_household(sim_info: SimInfo, destroy_if_empty_household: bool=True) -> bool:
        """Add a Sim to the Active Sims household.

        """
        target_sim_info = CommonSimUtils.get_active_sim_info()
        return CommonHouseholdUtils.add_sim_to_target_household(sim_info, target_sim_info, destroy_if_empty_household=destroy_if_empty_household)

    @staticmethod
    def add_sim_to_target_household(sim_info: SimInfo, target_sim_info: SimInfo, destroy_if_empty_household: bool=True) -> bool:
        """Add a Sim to the Target Sims household.

        """
        log.info('Adding Sim to target Sim household.')
        destination_household = target_sim_info.household
        log.format_info('Adding Sim to household of target sim', sim=CommonSimNameUtils.get_full_name(sim_info), target_sim=CommonSimNameUtils.get_full_name(target_sim_info), destination_household=destination_household)
        return CommonHouseholdUtils.move_sim_to_household(sim_info, household_id=destination_household.id, destroy_if_empty_household=destroy_if_empty_household)

    @staticmethod
    def move_sim_to_household(sim_info: SimInfo, household_id: int=None, destroy_if_empty_household: bool=True) -> bool:
        """Move a Sim to the specified household or a new household if no Household is specified.

        """
        active_household = services.active_household()
        starting_household = sim_info.household
        log.format_info('Moving a Sim to a new household.', sim=CommonSimNameUtils.get_full_name(sim_info), household_id=household_id, starting_household=starting_household)
        if household_id is None:
            log.info('No destination household specified, creating a household for the sim.')
            destination_household = services.household_manager().create_household(sim_info.account)
        else:
            log.info('Household was specified, getting household of the sim.')
            destination_household = services.household_manager().get(household_id)
        if destination_household is None:
            log.error('Destination Household not specified!')
        log.format_info('Destination household acquired', destination_household=destination_household)
        if CommonSimStateUtils.is_hidden(sim_info):
            log.info('Making hidden Sim visible.')
            services.hidden_sim_service().unhide(sim_info.id)
        if starting_household is destination_household:
            log.error('The Sim being moved is already in the destination household.', throw=False)
            return False
        if not destination_household.can_add_sim_info(sim_info):
            log.error('The destination household has no room for additions.', throw=False)
            return False
        log.info('Removing Sim from the starting household.')
        starting_household.remove_sim_info(sim_info, destroy_if_empty_household=destroy_if_empty_household)
        log.info('Adding Sim to the destination household.')
        destination_household.add_sim_info_to_household(sim_info)
        client = services.client_manager().get_first_client()
        if destination_household is active_household:
            log.info('The destination household is the active household. Changing the Sim to be selectable.')
            client.add_selectable_sim_info(sim_info)
        else:
            log.info('The destination household is different from the active household. Removing the selectability of the sim.')
            client.remove_selectable_sim_info(sim_info)
        if sim_info.career_tracker is not None:
            log.info('Removing invalid careers.')
            sim_info.career_tracker.remove_invalid_careers()
            log.info('Invalid careers removed.')
        sim = sim_info.get_sim_instance()
        if sim is not None:
            log.info('Updating sims intended position on the active lot.')
            sim.update_intended_position_on_active_lot(update_ui=True)
            situation_manager = services.get_zone_situation_manager()
            log.info('Removing Sim from currently active situations.')
            for situation in situation_manager.get_situations_sim_is_in(sim):
                if destination_household is active_household and situation.is_user_facing:
                    pass
                else:
                    log.format_info('Removing situation', situation_id=situation.id)
                    situation_manager.remove_sim_from_situation(sim, situation.id)
            log.info('Done removing situations. Updating daycare service information.')
            services.daycare_service().on_sim_spawn(sim_info)
        log.info('Done moving Sim to household.')
        return True

    @staticmethod
    def has_free_household_slots(sim_info: SimInfo) -> bool:
        """Determine if the Household of the specified Sim has any free Sim slots.
        note:: Max household slots in vanilla Sims 4 is 8 sims.

        """
        return CommonHouseholdUtils.get_free_household_slots(sim_info) > 0

    @staticmethod
    def get_free_household_slots(sim_info: SimInfo) -> int:
        """Retrieve the number of free household slots in the Household of the specified Sim.
        note:: Max household slots in vanilla Sims 4 is 8 sims.

        :return: The number of free household slots or -1 if no Household is found for the specified Sim.
        """
        household = CommonHouseholdUtils.get_household(sim_info)
        if household is None:
            return -1
        return household.free_slot_count

    @staticmethod
    def get_household(sim_info: SimInfo) -> Union[Household, None]:
        """Retrieve the household of a Sim.

        """
        if not CommonHouseholdUtils.has_household(sim_info):
            return None
        return services.household_manager().get(sim_info.household.id)

    @staticmethod
    def get_household_id(sim_info: SimInfo) -> int:
        """Retrieve an identifier for the Household a Sim is a part of.

        """
        household = CommonHouseholdUtils.get_household(sim_info)
        if household is None:
            return 0
        return household.id

    @staticmethod
    def has_household(sim_info: SimInfo) -> bool:
        """Determine if the Sim is part of a Household.

        """
        return hasattr(sim_info, 'household') and sim_info.household is not None

    @staticmethod
    def is_in_same_household(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """Determine if two Sims are in the same household.

        """
        household = CommonHouseholdUtils.get_household(sim_info)
        if household is None:
            return False
        target_household = CommonHouseholdUtils.get_household(target_sim_info)
        if target_household is None:
            return False
        return household is target_household

    @staticmethod
    def delete_household(household: Household) -> bool:
        """Delete the specified household from the game.

        """
        try:
            services.get_persistence_service().del_household_proto_buff(household.id)
            services.household_manager().remove(household)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Failed to delete household \'{}\'.'.format(pformat(household)), exception=ex)
            return False
        return True

    @staticmethod
    def delete_households_with_name(name: str, allow_partial_match: bool=False) -> bool:
        """Delete all households with the specified name.

        :param name: The name of the households to delete.
        :param allow_partial_match: If True, households only need to contain the name to match.
        """
        if allow_partial_match:
            log.debug('Attempting to delete households containing name \'{}\'.'.format(name))
        else:
            log.debug('Attempting to delete households with name \'{}\'.'.format(name))
        all_completed = True
        for household in CommonHouseholdUtils.locate_households_by_name_generator(name, allow_partial_match=allow_partial_match):
            if household is None:
                continue
            result = CommonHouseholdUtils.delete_household(household)
            if not result:
                all_completed = False
        return all_completed
