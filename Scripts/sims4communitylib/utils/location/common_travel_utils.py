"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils


class CommonTravelUtils:
    """Utilities for moving Sims around.

    """

    @staticmethod
    def travel_to_lot(sim_info: SimInfo, lot_id: int):
        """Send the specified Sim to the Lot with the specified id.

        """
        sim_info.send_travel_switch_to_zone_op(zone_id=lot_id)

    @staticmethod
    def travel_to_home_lot_of(sim_info: SimInfo):
        """Send the specified Sim to their Home Lot.

        """
        lot_id = CommonHouseholdUtils.get_household_lot_id(sim_info)
        CommonTravelUtils.travel_to_lot(sim_info, lot_id)

    @staticmethod
    def travel_to_home_lot_of_active_sim(sim_info: SimInfo):
        """Send the specified Sim to the Home Lot of the Active Sim.

        """
        lot_id = CommonHouseholdUtils.get_active_household().home_zone_id
        CommonTravelUtils.travel_to_lot(sim_info, lot_id)
