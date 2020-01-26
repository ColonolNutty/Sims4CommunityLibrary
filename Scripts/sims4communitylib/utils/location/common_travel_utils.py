"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils


class CommonTravelUtils:
    """Utilities for moving Sims around.

    """

    @staticmethod
    def travel_to_lot(sim_info: SimInfo, lot_id: int):
        """travel_to_lot(sim_info, lot_id)

        Travel with the specified Sim to the Lot with the specified identifier.

        :param sim_info: The Sim to travel with.
        :type sim_info: SimInfo
        :param lot_id: The identifier of the lot to travel to.
        :type lot_id: int
        """
        sim_info.send_travel_switch_to_zone_op(zone_id=lot_id)

    @staticmethod
    def travel_to_home_lot_of(sim_info: SimInfo):
        """travel_to_home_lot_of(sim_info)

        Travel to the home lot of a Sim.

        :param sim_info: The owner of the home lot to travel to.
        :type sim_info: SimInfo
        """
        lot_id = CommonHouseholdUtils.get_household_lot_id(sim_info)
        CommonTravelUtils.travel_to_lot(sim_info, lot_id)

    @staticmethod
    def travel_to_home_lot_of_active_sim(sim_info: SimInfo):
        """travel_to_home_lot_of_active_sim(sim_info)

        Travel with the specified Sim to the home lot of the Active Sim.

        :param sim_info: The Sim to travel with.
        :type sim_info: SimInfo
        """
        lot_id = CommonHouseholdUtils.get_active_household().home_zone_id
        CommonTravelUtils.travel_to_lot(sim_info, lot_id)
