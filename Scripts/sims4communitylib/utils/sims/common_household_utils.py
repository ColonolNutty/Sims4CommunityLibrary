"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

import services
from sims.household import Household
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from world.lot import Lot
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonHouseholdUtils(HasClassLog):
    """Utilities for manipulating households.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_household_utils'

    @classmethod
    def get_active_household(cls) -> Union[Household, None]:
        """get_active_household()

        Retrieve the Household of the Active Sim.

        :return: The Household of the Active Sim or None if no household is found.
        :rtype: Union[Household, None]
        """
        return services.active_household()

    @classmethod
    def get_active_household_id(cls) -> int:
        """get_active_household_id()

        Retrieve an identifier for the Household of the Active Sim.

        :return: The identifier of the Household of the Active Sim.
        :rtype: int
        """
        return cls.get_id(cls.get_active_household())

    @classmethod
    def get_household_zone_id(cls, sim_info: SimInfo) -> int:
        """get_household_zone_id(sim_info)

        Retrieve an zone identifier for the home Lot of the specified Sim.

        :param sim_info: The Sim to retrieve the household Lot id of.
        :type sim_info: SimInfo
        :return: The zone identifier of the Household the Sim belongs to.
        :rtype: int
        """
        household = cls.get_household(sim_info)
        return cls.get_household_home_zone_id(household)

    @classmethod
    def get_household_lot_id(cls, sim_info: SimInfo) -> int:
        """get_household_lot_id(sim_info)

        Retrieve an identifier for the home Lot of a Sim.

        :param sim_info: The Sim to retrieve the household Lot id of.
        :type sim_info: SimInfo
        :return: The identifier of the Household Lot for the Sim.
        :rtype: int
        """
        household = cls.get_household(sim_info)
        return cls.get_household_home_lot_id(household)

    @classmethod
    def get_household_home_zone_id(cls, household: Household) -> int:
        """get_household_home_zone_id(household)

        Retrieve the home zone identifier for a Household.

        :param household: An instance of a Household.
        :type household: Household
        :return: The home zone identifier of the specified Household or -1 if a problem occurs.
        :rtype: int
        """
        if household is None:
            return -1
        # noinspection PyTypeChecker
        return household.home_zone_id

    @classmethod
    def get_household_home_lot_id(cls, household: Household) -> int:
        """get_household_home_lot_id(household)

        Retrieve the decimal identifier of the home Lot for a Household.

        :param household: An instance of a Household.
        :type household: Household
        :return: The home zone identifier of the specified Household or -1 if a problem occurs.
        :rtype: int
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        if household is None:
            return -1
        home_zone_id = cls.get_household_home_zone_id(household)
        if home_zone_id == -1:
            return -1
        home_zone = CommonLocationUtils.get_zone(home_zone_id, allow_unloaded_zones=True)
        if home_zone is None or not home_zone.is_instantiated:
            return home_zone_id or -1
        lot = CommonLocationUtils.get_zone_lot(home_zone)
        if lot is None:
            return home_zone_id or -1
        return CommonLocationUtils.get_lot_id(lot)

    @classmethod
    def get_sim_info_of_all_sims_in_active_household_generator(cls) -> Iterator[SimInfo]:
        """get_sim_info_of_all_sims_in_active_household_generator()

        Retrieve a collection of Sims that are a part of the active household.

        :return: An iterator of Sims in the active household.
        :rtype: Iterator[SimInfo]
        """
        household = cls.get_active_household()
        for sim_info in cls.get_sim_info_of_all_sims_in_household_generator(household):
            yield sim_info

    @classmethod
    def get_sim_info_of_all_sims_in_household_generator(cls, household: Household) -> Iterator[SimInfo]:
        """get_sim_info_of_all_sims_in_household_generator(household)

        Retrieve a collection of Sims that are a part of the active household.

        :param household: The Household to retrieve Sims from.
        :type household: Household
        :return: An iterator of Sims in the specified Household.
        :rtype: Iterator[SimInfo]
        """
        if household is None:
            return tuple()
        for sim_info in list(household.sim_info_gen()):
            if sim_info is None:
                continue
            yield sim_info

    @classmethod
    def get_number_of_sims_in_household(cls, household: Household) -> int:
        """get_number_of_sims_in_household(household)

        Determine the number of Sims in the specified Household.

        :param household: An instance of a Household.
        :type household: Household
        :return: The number of Sims in the specified Household.
        :rtype: int
        """
        if household is None:
            return 0
        return len(tuple(cls.get_sim_info_of_all_sims_in_household_generator(household)))

    @classmethod
    def get_number_of_sims_in_household_of_sim(cls, sim_info: SimInfo) -> int:
        """get_number_of_sims_in_household_of_sim(sim_info)

        Determine the number of Sims in the household of the specified Sim.

        :param sim_info: An instance of a Sim.
        :type: sim_info: SimInfo
        :return: The number of Sims in the household of the specified Sim.
        :rtype: int
        """
        return cls.get_number_of_sims_in_household(cls.get_household(sim_info))

    @classmethod
    def is_part_of_active_household(cls, sim_info: SimInfo) -> bool:
        """is_part_of_active_household(sim_info)

        Determine if a Sim is part of the active household.

        :return: True, if the Sim is part of the Active Household. False, if not.
        :rtype: bool
        """
        return sim_info in cls.get_sim_info_of_all_sims_in_active_household_generator()

    @classmethod
    def is_part_of_a_single_sim_household(cls, sim_info: SimInfo) -> bool:
        """is_part_of_a_single_sim_household(sim_info)

        Determine if a Sim is the only Sim in their Household (Single Sim Household).

        :param sim_info: An instance of a Sim.
        :type: sim_info: SimInfo
        :return: True, if specified Sim is the only Sim in their Household (Single Sim Household). False, if not.
        :rtype: bool
        """
        return cls.get_number_of_sims_in_household_of_sim(sim_info) == 1

    @classmethod
    def is_alone_on_home_lot(cls, sim_info: SimInfo) -> bool:
        """is_alone_on_home_lot(sim_info)

        Determine if a Sim is alone on their home lot.

        :param sim_info: An instance of a Sim.
        :type: sim_info: SimInfo
        :return: True, if the Sim is on their home lot and alone. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
        return cls.is_part_of_a_single_sim_household(sim_info) and CommonSimLocationUtils.is_at_home(sim_info)

    @classmethod
    def get_all_households_generator(cls) -> Iterator[Household]:
        """get_all_households_generator()

        Retrieve a collection of all households.

        :return: An iterator of all Households.
        :rtype: Iterator[Household]
        """
        household_list = tuple(services.household_manager().get_all())
        for household in household_list:
            if household is None:
                continue
            yield household

    @classmethod
    def locate_household_by_id(cls, household_id: int) -> Union[Household, None]:
        """locate_household_by_id(household_id)

        Locate a household with the specified id.

        :param household_id: The decimal identifier of a Household.
        :type household_id: int
        :return: The Household with an identifier matching the specified identifier or None if no Household was found.
        :rtype: Union[Household, None]
        """
        # noinspection PyBroadException
        try:
            return services.household_manager().get(household_id)
        except:
            return None

    @classmethod
    def locate_household_by_name(cls, name: str, allow_partial_match: bool = False, create_on_missing: bool = False, starting_funds: int = 0, as_hidden_household: bool = False) -> Union[Household, None]:
        """locate_household_by_name(name, allow_partial_match=False, create_on_missing=False, starting_funds=0, as_hidden_household=False)

        Locate a household with the specified name.

        :param name: The name of a household to locate.
        :type name: str
        :param allow_partial_match: If True, households only need to contain the name to match.
        :type allow_partial_match: bool, optional
        :param create_on_missing: If True, a household will be created if one isn't found with the specified name.
        :type create_on_missing: bool, optional
        :param starting_funds: If a household is created, this will be the starting funds of that household.
        :type starting_funds: int, optional
        :param as_hidden_household: If True, the created household will be hidden.
        :type as_hidden_household: bool, optional
        :return: A Household with the specified name or None if no household is found.
        :rtype: Union[Household, None]
        """
        log = cls.get_log()
        for household in cls.locate_households_by_name_generator(name, allow_partial_match=allow_partial_match):
            if household is None:
                continue
            return household
        if not create_on_missing:
            log.debug(f'No household found matching name \'{name}\'.')
            return None
        log.debug('No household found, creating one.')
        empty_household = cls.create_empty_household(starting_funds=starting_funds, as_hidden_household=as_hidden_household)
        empty_household.name = name
        return empty_household

    @classmethod
    def locate_households_by_name_generator(cls, name: str, allow_partial_match: bool = False) -> Iterator[Household]:
        """locate_households_by_name_generator(name, allow_partial_match=False)

        Locate all households with the specified name.

        :param name: The name of the households to locate.
        :type name: str
        :param allow_partial_match: If True, households only need to contain the name to match.
        :type allow_partial_match: bool, optional
        :return: An iterator of Households with the specified name.
        :rtype: Iterator[Household]
        """
        log = cls.get_log()
        if allow_partial_match:
            log.debug(f'Locating households containing name: \'{name}\'')
        else:
            log.debug(f'Locating households with name: \'{name}\'')
        for household in cls.get_all_households_generator():
            if household is None:
                continue
            # noinspection PyPropertyAccess
            household_name = household.name
            # noinspection PyPropertyAccess
            log.debug(f'Checking household \'{household_name}\' for match.')
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

    @classmethod
    def create_empty_household(cls, starting_funds: int = 0, as_hidden_household: bool = False) -> Household:
        """create_empty_household(starting_funds=0, as_hidden_household=False)

        Create an empty household.

        :param starting_funds: The funds the Household will start with.
        :type starting_funds: int, optional
        :param as_hidden_household: If True, the created household will be hidden.
        :type as_hidden_household: bool, optional
        :return: The created Household
        :rtype: Household
        """
        household = Household(SimSpawner._get_default_account(), starting_funds=starting_funds)
        if as_hidden_household:
            household.set_to_hidden()
        services.household_manager().add(household)
        return household

    @classmethod
    def add_sim_to_active_household(cls, sim_info: SimInfo, destroy_if_empty_household: bool = True) -> bool:
        """add_sim_to_active_household(sim_info, destroy_if_empty_household=True)

        Add a Sim to the Active Sims household.

        :param sim_info: The Sim to add.
        :type sim_info: SimInfo
        :param destroy_if_empty_household: If True, if the Sim comes from a household containing only them, then it will be destroyed after they are moved.
        :type destroy_if_empty_household: bool, optional
        :return: True, if the Sim was added to the active household successfully. False, if not.
        :rtype: bool
        """
        target_sim_info = CommonSimUtils.get_active_sim_info()
        return cls.add_sim_to_target_household(sim_info, target_sim_info, destroy_if_empty_household=destroy_if_empty_household)

    @classmethod
    def add_sim_to_target_household(cls, sim_info: SimInfo, target_sim_info: SimInfo, destroy_if_empty_household: bool = True) -> bool:
        """add_sim_to_active_household(sim_info, destroy_if_empty_household=True)

        Add a Sim to the Household of the Target Sim.

        :param sim_info: The Sim to add.
        :type sim_info: SimInfo
        :param target_sim_info: This Sim will receive the Sim to their Household.
        :type target_sim_info: SimInfo
        :param destroy_if_empty_household: If True, if the Sim comes from a household containing only them, then it will be destroyed after they are moved.
        :type destroy_if_empty_household: bool, optional
        :return: True, if the Sim was added to the household of the target successfully. False, if not.
        :rtype: bool
        """
        log = cls.get_log()
        log.info('Adding Sim to target Sim household.')
        destination_household = target_sim_info.household
        log.format_info('Adding Sim to household of target sim', sim=CommonSimNameUtils.get_full_name(sim_info), target_sim=CommonSimNameUtils.get_full_name(target_sim_info), destination_household=destination_household)
        return cls.move_sim_to_household(sim_info, household_id=destination_household.id, destroy_if_empty_household=destroy_if_empty_household)

    @classmethod
    def move_sim_to_household(cls, sim_info: SimInfo, household_id: int = None, destroy_if_empty_household: bool = True) -> bool:
        """move_sim_to_household(sim_info, household_id=None, destroy_if_empty_household=True)

        Move a Sim to the specified household or a new household if no Household is specified.

        :param sim_info: The Sim to add.
        :type sim_info: SimInfo
        :param household_id: The identifier of the Household to add the Sim to.
        :type household_id: int
        :param destroy_if_empty_household: If True, if the Sim comes from a household containing only them, then it will be destroyed after they are moved.
        :type destroy_if_empty_household: bool, optional
        :return: True, if the Sim was added to the Household successfully. False, if not.
        :rtype: bool
        """
        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_household = services.active_household()
        starting_household = sim_info.household
        log = cls.get_log()
        log.format_info('Moving a Sim to a new household.', sim=CommonSimNameUtils.get_full_name(sim_info), household_id=household_id, starting_household=starting_household)
        if household_id is None:
            log.info('No destination household specified, creating a household for the sim.')
            destination_household = services.household_manager().create_household(sim_info.account)
        else:
            log.info('Household was specified, getting household of the sim.')
            destination_household = services.household_manager().get(household_id)
        if destination_household is None:
            raise AssertionError('Destination Household not specified!')
        log.format_info('Destination household acquired', destination_household=destination_household)
        if CommonSimStateUtils.is_hidden(sim_info):
            log.info('Making hidden Sim visible.')
            services.hidden_sim_service().unhide_sim(sim_info.id)
        if starting_household is destination_household:
            raise AssertionError('The Sim being moved is already in the destination household.')
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
            if active_sim_info is sim_info:
                client.set_next_sim()
            client.remove_selectable_sim_info(sim_info)
        if sim_info.career_tracker is not None:
            log.info('Removing invalid careers.')
            sim_info.career_tracker.remove_invalid_careers()
            log.info('Invalid careers removed.')
        sim = sim_info.get_sim_instance()
        if sim is not None:
            log.info('Updating sims intended position on the active Lot.')
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

    @classmethod
    def has_free_household_slots(cls, sim_info: SimInfo) -> bool:
        """has_free_household_slots(sim_info)

        Determine if the Household of the specified Sim has any free Sim slots.

        .. note:: Max household slots in vanilla Sims 4 is 8 sims.

        :param sim_info: The Sim whose household will be checked.
        :type sim_info: SimInfo
        :return: True, if there are free slots for new Sims in the Household of the specified Sim. False, if not.
        :rtype: bool
        """
        return cls.get_free_household_slots(sim_info) > 0

    @classmethod
    def get_free_household_slots(cls, sim_info: SimInfo) -> int:
        """get_free_household_slots(sim_info)

        Retrieve the number of free household slots in the Household of the specified Sim.

        .. note:: Max household slots in vanilla Sims 4 is 8 sims.

        :param sim_info: The Sim whose household will be checked.
        :type sim_info: SimInfo
        :return: The number of free household slots or -1 if no Household is found for the specified Sim.
        :rtype: int
        """
        household = cls.get_household(sim_info)
        if household is None:
            return -1
        return household.free_slot_count

    @classmethod
    def get_household_members_gen(cls, sim_info: SimInfo) -> Iterator[SimInfo]:
        """get_household_members_gen(sim_info)

        Retrieve the Sims within the household of a Sim.

        .. note:: The result will include the specified Sim as well.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterator of Sims within the household of the specified Sim.
        :rtype: Iterator[SimInfo]
        """
        household = cls.get_household(sim_info)
        if household is None:
            yield sim_info
        else:
            yield from cls.get_household_members_from_household_gen(household)

    @classmethod
    def get_household_members_from_household_gen(cls, household: Household) -> Iterator[SimInfo]:
        """get_household_members_from_household_gen(sim_info)

        Retrieve the Sims within a Household.

        :param household: An instance of a Household
        :type household: Household
        :return: An iterator of Sims within the specified household.
        :rtype: Iterator[SimInfo]
        """
        if household is None:
            return tuple()

        for household_member_sim_info in household:
            yield CommonSimUtils.get_sim_info(household_member_sim_info)

    @classmethod
    def get_household(cls, sim_info: SimInfo) -> Union[Household, None]:
        """get_household(sim_info)

        Retrieve the household of a Sim.

        :param sim_info: The Sim whose household will be retrieved.
        :type sim_info: SimInfo
        :return: The Household of the specified Sim or None if no household is found.
        :rtype: Union[Household, None]
        """
        if not cls.has_household(sim_info):
            return None
        return services.household_manager().get(sim_info.household.id)

    @classmethod
    def get_household_id(cls, sim_info: SimInfo) -> int:
        """get_household_id(sim_info)

        Retrieve an identifier for the Household a Sim is a part of.

        :param sim_info: The Sim whose household will be retrieved.
        :type sim_info: SimInfo
        :return: The identifier of the Household of the specified Sim or `0` if no household is found.
        :rtype: int
        """
        return cls.get_id(cls.get_household(sim_info))

    @classmethod
    def get_id(cls, household: Household) -> int:
        """get_id(household)

        Retrieve the decimal identifier of a Household.

        :param household: An instance of a Household.
        :type: Household
        :return: The identifier of the Household or `0` if an error occurs.
        :rtype: int
        """
        if household is None:
            return 0
        return household.id

    @classmethod
    def has_household(cls, sim_info: SimInfo) -> bool:
        """has_household(sim_info)

        Determine if the Sim is part of a Household.

        :param sim_info: The Sim whose household will be checked.
        :type sim_info: SimInfo
        :return: True, if the Sim is part of a Household. False, if not.
        :rtype: bool
        """
        return hasattr(sim_info, 'household') and sim_info.household is not None

    @classmethod
    def is_in_same_household(cls, sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """is_in_same_household(sim_info, target_sim_info)

        Determine if two Sims are in the same household.

        :param sim_info: The Sim whose household will be checked.
        :type sim_info: SimInfo
        :param target_sim_info: The Target whose household will be checked.
        :type target_sim_info: SimInfo
        :return: True, if the Sim is part of same Household as the Target Sim. False, if not.
        :rtype: bool
        """
        household = cls.get_household(sim_info)
        if household is None:
            return False
        target_household = cls.get_household(target_sim_info)
        if target_household is None:
            return False
        return household is target_household

    @classmethod
    def get_household_owning_current_lot(cls) -> Union[Household, None]:
        """get_household_owning_current_lot()

        Retrieve the Household that owns the current Lot.

        :return: A decimal identifier of the Household that owns the current Lot or None if no Household owns the current Lot.
        :rtype: Union[Household, None]
        """
        household_id = cls.get_household_id_owning_current_lot()
        if household_id is None or household_id == -1:
            return None
        return cls.locate_household_by_id(household_id)

    @classmethod
    def get_household_id_owning_current_lot(cls) -> int:
        """get_household_id_owning_current_lot()

        Retrieve the decimal identifier of the Household that owns the current Lot.

        :return: A decimal identifier of the Household that owns the current Lot or -1 if a problem occurs.
        :rtype: int
        """
        household_id = services.owning_household_id_of_active_lot()
        if household_id is None:
            return -1
        return household_id

    @classmethod
    def get_household_owning_lot(cls, lot: Lot) -> Union[Household, None]:
        """get_household_owning_lot(lot)

        Retrieve the Household that owns a Lot.

        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: A decimal identifier of the Household that owns the specified Lot or None if no Household owns the specified Lot.
        :rtype: Union[Household, None]
        """
        household_id = cls.get_household_id_owning_lot(lot)
        if household_id is None or household_id == -1:
            return None
        return cls.locate_household_by_id(household_id)

    @classmethod
    def get_household_id_owning_lot(cls, lot: Lot) -> int:
        """get_household_id_owning_lot(lot)

        Retrieve the decimal identifier of the Household that owns a Lot.

        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: A decimal identifier of the Household that owns the specified Lot or -1 if a problem occurs.
        :rtype: int
        """
        if lot is None:
            return -1
        return lot.owner_household_id

    @classmethod
    def delete_household(cls, household: Household) -> bool:
        """delete_household(household)

        Delete the specified household from the game.

        :param household: The Household to delete
        :type household: Household
        :return: True, if the Household was deleted successfully. False, if not.
        :rtype: bool
        """
        services.get_persistence_service().del_household_proto_buff(household.id)
        services.household_manager().remove(household)
        return True

    @classmethod
    def delete_households_with_name(cls, name: str, allow_partial_match: bool = False) -> bool:
        """delete_households_with_name(name, allow_partial_match=False)

        Delete all households with the specified name.

        :param name: The name of the households to delete.
        :type name: str
        :param allow_partial_match: If True, households only need to contain the name to match.
        :type allow_partial_match: bool
        :return: True, if Households were deleted successfully. False, if not.
        :rtype: bool
        """
        log = cls.get_log()
        if allow_partial_match:
            log.debug(f'Attempting to delete households containing name \'{name}\'.')
        else:
            log.debug(f'Attempting to delete households with name \'{name}\'.')
        all_completed = True
        for household in cls.locate_households_by_name_generator(name, allow_partial_match=allow_partial_match):
            if household is None:
                continue
            result = cls.delete_household(household)
            if not result:
                all_completed = False
        return all_completed


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_to_household',
    'Add a Sim to the household of another Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to add to the household.'),
        CommonConsoleCommandArgument('target_household_sim_info', 'Sim Id or Name', 'The instance id or name of a Sim. The other Sim (sim_info) will be added to this Sims household.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.addtohousehold',
    )
)
def _common_command_add_to_my_household(output: CommonConsoleCommandOutput, sim_info: SimInfo = None, target_household_sim_info: SimInfo = None):
    if sim_info is None:
        return
    if target_household_sim_info is None:
        return
    output(f'Attempting to move {sim_info} to the household of {target_household_sim_info}.')
    result = CommonHouseholdUtils.add_sim_to_active_household(sim_info)
    if result:
        output(f'SUCCESS: Successfully moved {sim_info} to the household of {target_household_sim_info}.')
    else:
        output(f'FAILED: Failed to move {sim_info} to the household of {target_household_sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_from_household',
    'Remove a Sim from the household they are in and put them into their own household.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance id or name of a Sim to remove from their household.'),
    ),
    command_aliases=(
        's4clib.removefromhousehold',
    )
)
def _common_command_remove_from_my_household(output: CommonConsoleCommandOutput, sim_info: SimInfo):
    if sim_info is None:
        return
    output(f'Attempting to move {sim_info} out of their current household.')
    empty_household = CommonHouseholdUtils.create_empty_household()
    result = CommonHouseholdUtils.move_sim_to_household(sim_info, household_id=empty_household.id, destroy_if_empty_household=True)
    if result:
        output(f'SUCCESS: Successfully removed {sim_info} from their current household.')
    else:
        output(f'FAILED: Failed to remove {sim_info} from their current household.')
