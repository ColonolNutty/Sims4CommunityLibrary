"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from event_testing.results import EnqueueResult
from server.pick_info import PickType
import sims4.math
import objects.terrain
from typing import Union

import routing
import services
from autonomy.autonomy_component import AutonomyComponent
from protocolbuffers.Math_pb2 import Vector3
from routing import Location
from sims.sim_info import SimInfo
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimLocationUtils:
    """Utilities for manipulating the locations of Sims.

    """

    @staticmethod
    def get_position(sim_info: SimInfo) -> Union[Vector3, None]:
        """get_position(sim_info)

        Retrieve the current position of a Sim.

        :param sim_info: The Sim to get the position of.
        :type sim_info: SimInfo
        :return: The current position of the Sim or None if the Sim does not have a position.
        :rtype: Union[Vector3, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return sim.position

    @staticmethod
    def get_location(sim_info: SimInfo) -> Union[Location, None]:
        """get_location(sim_info)

        Retrieve the current location of a Sim.

        :param sim_info: The Sim to get the location of.
        :type sim_info: SimInfo
        :return: The current location of the Sim or None if the Sim does not have a location.
        :rtype: Union[Vector3, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return sim.location

    @staticmethod
    def can_swim_at_location(sim_info: SimInfo, location: Location) -> bool:
        """can_swim_at_location(sim_info, location)

        Determine if a Sim can swim at the specified location.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param location: The Location to check.
        :type location: Location
        :return: True, if the Sim can swim at the specified location. False, if not.
        :rtype: bool
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        return sim.should_be_swimming_at_position(location.transform.translation, location.level)

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

        Determine if a sim is on the current lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is on the active lot. False, if not.
        :rtype: bool
        """
        sim_position = CommonSimLocationUtils.get_position(sim_info)
        return sim_position is not None and services.active_lot().is_position_on_lot(sim_position)

    @staticmethod
    def is_renting_current_lot(sim_info: SimInfo) -> bool:
        """is_renting_current_lot(sim_info)

        Determine if a Sim is renting the current lot.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is renting the active lot. False, if not.
        :rtype: bool
        """
        return sim_info.is_renting_zone(CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def is_at_home(sim_info: SimInfo) -> bool:
        """is_at_home(sim_info)

        Determine if a Sim is currently at home.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is at their home lot. False, if not.
        :rtype: bool
        """
        active_lot = CommonLocationUtils.get_current_lot()
        return CommonLocationUtils.get_current_zone_id() == CommonHouseholdUtils.get_household_lot_id(sim_info) and active_lot.is_position_on_lot(CommonSimLocationUtils.get_position(sim_info))

    @staticmethod
    def send_to_position(sim_info: SimInfo, location_position: Vector3, level: int) -> Union[EnqueueResult, None]:
        """send_to_position(sim_info, location_position, level)

        Send a Sim to the specified location.

        :param sim_info: The Sim to send.
        :type sim_info: SimInfo
        :param location_position: The position to send the sim to.
        :type location_position: Vector3
        :param level: The level at which the position is.
        :type level: int
        :return: The result of sending the Sim to the specified location or None if they could not go there.
        :rtype: EnqueueResult
        """
        from server_commands.sim_commands import _build_terrain_interaction_target_and_context, CommandTuning
        if location_position is None:
            return None
        sim = CommonSimUtils.get_sim_instance(sim_info)
        # noinspection PyUnresolvedReferences
        pos = sims4.math.Vector3(location_position.x, location_position.y, location_position.z)
        routing_surface = routing.SurfaceIdentifier(CommonLocationUtils.get_current_zone_id(), level, routing.SurfaceType.SURFACETYPE_WORLD)
        (target, context) = _build_terrain_interaction_target_and_context(sim, pos, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
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
