"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.results import EnqueueResult
from server.pick_info import PickType
import objects.terrain
from typing import Union
from autonomy.autonomy_component import AutonomyComponent
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from world.lot import Lot


class CommonSimLocationUtils:
    """Utilities for manipulating the locations of Sims.

    """
    @staticmethod
    def get_position(sim_info: SimInfo) -> Union[CommonVector3, None]:
        """get_position(sim_info)

        Retrieve the current position of a Sim.

        :param sim_info: The Sim to get the position of.
        :type sim_info: SimInfo
        :return: The current position of the Sim or None if the Sim does not have a position.
        :rtype: Union[CommonVector3, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        # noinspection PyBroadException
        try:
            return CommonVector3.from_vector3(sim.position)
        except:
            return None

    @staticmethod
    def get_location(sim_info: SimInfo) -> Union[CommonLocation, None]:
        """get_location(sim_info)

        Retrieve the current location of a Sim.

        :param sim_info: The Sim to get the location of.
        :type sim_info: SimInfo
        :return: The current location of the Sim or None if the Sim does not have a location.
        :rtype: Union[CommonLocation, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        # noinspection PyBroadException
        try:
            return CommonLocation.from_location(sim.location)
        except:
            return None

    @staticmethod
    def get_orientation(sim_info: SimInfo) -> CommonQuaternion:
        """get_orientation(sim_info)

        Retrieve the orientation of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The orientation of the Sim.
        :rtype: CommonQuaternion
        """
        if sim_info is None:
            return CommonQuaternion.empty()
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonQuaternion.empty()
        return CommonQuaternion.from_quaternion(sim.orientation)

    @staticmethod
    def get_orientation_degrees(sim_info: SimInfo) -> float:
        """get_orientation_degrees(sim_info)

        Retrieve the orientation of a Sim represented in degrees.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The orientation of the Sim represented in degrees.
        :rtype: float
        """
        return CommonQuaternion.to_degrees(CommonSimLocationUtils.get_orientation(sim_info))

    @staticmethod
    def can_swim_at_location(sim_info: SimInfo, location: CommonLocation) -> bool:
        """can_swim_at_location(sim_info, location)

        Determine if a Sim can swim at the specified location.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param location: The Location to check.
        :type location: CommonLocation
        :return: True, if the Sim can swim at the specified location. False, if not.
        :rtype: bool
        """
        if location is None:
            return False
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        return sim.should_be_swimming_at_position(location.transform.translation, location.routing_surface.secondary_id)

    @staticmethod
    def can_swim_at_current_location(sim_info: SimInfo) -> bool:
        """can_swim_at_current_location(sim_info)

        Determine if a Sim can swim at their current location.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim can swim at their current location. False, if not.
        :rtype: bool
        """
        location = CommonSimLocationUtils.get_location(sim_info)
        return CommonSimLocationUtils.can_swim_at_location(sim_info, location)

    @staticmethod
    def is_on_current_lot(sim_info: SimInfo) -> bool:
        """is_on_current_lot(sim_info)

        Determine if a Sim is on the active Lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is on the active Lot. False, if not.
        :rtype: bool
        """
        active_lot = CommonLocationUtils.get_current_lot()
        return CommonSimLocationUtils.is_on_lot(sim_info, active_lot)

    @staticmethod
    def is_on_lot(sim_info: SimInfo, lot: Lot) -> bool:
        """is_on_lot(sim_info, lot)

        Determine if a Sim is on a Lot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: True, if the Sim is on the specified Lot. False, if not.
        :rtype: bool
        """
        sim_position = CommonSimLocationUtils.get_position(sim_info)
        if sim_position is None:
            return False
        return CommonLocationUtils.is_position_on_lot(sim_position, lot)

    @staticmethod
    def is_renting_current_lot(sim_info: SimInfo) -> bool:
        """is_renting_current_lot(sim_info)

        Determine if a Sim is renting the current lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is renting the active lot. False, if not.
        :rtype: bool
        """
        return sim_info.is_renting_zone(CommonLocationUtils.get_current_zone_id())

    @staticmethod
    def is_at_home(sim_info: SimInfo) -> bool:
        """is_at_home(sim_info)

        Determine if a Sim is on their home Lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is on their home Lot. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None or not CommonHouseholdUtils.has_household(sim_info):
            return False
        return sim.on_home_lot or (CommonLocationUtils.get_current_zone_id() == CommonHouseholdUtils.get_household_zone_id(sim_info) and CommonSimLocationUtils.is_on_current_lot(sim_info))

    @staticmethod
    def send_to_position(sim_info: SimInfo, position: CommonVector3, level: int) -> Union[EnqueueResult, None]:
        """send_to_position(sim_info, position, level)

        Send a Sim to the specified location.

        :param sim_info: The Sim to send.
        :type sim_info: SimInfo
        :param position: The position to send the sim to.
        :type position: CommonVector3
        :param level: The level at which the position is located.
        :type level: int
        :return: The result of sending the Sim to the specified location or None if they could not go there.
        :rtype: EnqueueResult
        """
        from server_commands.sim_commands import _build_terrain_interaction_target_and_context, CommandTuning
        if position is None:
            return None
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        routing_surface = CommonSurfaceIdentifier.empty(secondary_id=level)
        (target, context) = _build_terrain_interaction_target_and_context(sim, position, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
        return sim.push_super_affordance(CommandTuning.TERRAIN_GOHERE_AFFORDANCE, target, context)

    @staticmethod
    def is_allowed_on_current_lot(sim_info: SimInfo) -> bool:
        """is_allowed_on_current_lot(sim_info)

        Determine if a Sim is allowed on the current lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is allowed on the current lot. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.common_component_utils import CommonComponentUtils
        from sims4communitylib.enums.types.component_types import CommonComponentType
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        if CommonSimLocationUtils.is_at_home(sim_info):
            return True
        if CommonSimLocationUtils.is_renting_current_lot(sim_info):
            return True
        if CommonSimTypeUtils.is_player_sim(sim_info) and (CommonLocationUtils.current_venue_allows_role_state_routing() or not CommonLocationUtils.current_venue_requires_player_greeting()):
            return True
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        autonomy_component: AutonomyComponent = CommonComponentUtils.get_component(sim, CommonComponentType.AUTONOMY)
        if autonomy_component is None or not hasattr(autonomy_component, 'active_roles'):
            return False
        for role_state_instance in autonomy_component.active_roles():
            if CommonSimTypeUtils.is_non_player_sim(sim_info):
                if role_state_instance._portal_disallowance_tags or not role_state_instance._allow_npc_routing_on_active_lot:
                    return False
            elif role_state_instance._portal_disallowance_tags:
                return False
        return True
