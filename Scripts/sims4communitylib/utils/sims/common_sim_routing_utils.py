"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.context import InteractionContext
from objects.terrain import Terrain
from server.pick_info import PickType
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3

from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.location.common_terrain_utils import CommonTerrainUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_body_utils import CommonSimBodyUtils
from sims4communitylib.utils.terrain.common_terrain_location_utils import CommonTerrainLocationUtils


class CommonSimRoutingUtils:
    """ Utilities for manipulating the Routing of Sims. """

    @staticmethod
    def can_route_to_pick_target_of_interaction_context(sim_info: SimInfo, interaction_context: InteractionContext) -> CommonTestResult:
        """can_route_to_pick_target_of_interaction_context(sim_info, interaction_context)

        Determine whether a Sim can route to a the picked target of an interaction context or not.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param interaction_context: An interaction context.
        :type interaction_context: InteractionContext
        :return: The result of running the test. True, if the Sim can route. False, if they cannot route.
        :rtype: CommonTestResult
        """
        pick_info = CommonInteractionUtils.get_pick_info_from_interaction_context(interaction_context)
        if pick_info is None:
            return CommonTestResult(False, reason='Missing PickInfo', hide_tooltip=True)
        if not isinstance(pick_info.pick_type, PickType):
            return CommonTestResult(False, reason=f'PickInfo {pick_info} did not have a pick type of type PickType {pick_info.pick_type}', hide_tooltip=True)

        pick_target = pick_info.target
        if pick_target is None:
            position = CommonVector3.from_vector3(pick_info.location)
            routing_surface = CommonSurfaceIdentifier.from_surface_identifier(pick_info.routing_surface)
        else:
            position = CommonVector3.from_vector3(pick_info.location)
            routing_surface = CommonSurfaceIdentifier.from_surface_identifier(pick_info.routing_surface)

            if CommonTypeUtils.is_water(pick_target):
                swim_at_position_test_result = CommonSimRoutingUtils.can_swim_at_position(sim_info, position, routing_surface)
                if not swim_at_position_test_result:
                    return swim_at_position_test_result

        if position is None or routing_surface is None:
            return CommonTestResult(False, reason=f'Failed to locate positional data for pick info {pick_info}.', hide_tooltip=True)

        if not CommonLocationUtils.can_position_be_routed_to(position, routing_surface):
            return CommonTestResult(False, reason=f'Pick Target cannot be routed to by Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_SIM_CANNOT_REACH_THAT_SPOT, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'Pick Target can be routed to by Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_SIM_CAN_REACH_THAT_SPOT, tooltip_tokens=(sim_info,))

    @staticmethod
    def can_route_to_terrain(sim_info: SimInfo, terrain_object: Terrain) -> CommonTestResult:
        """can_route_to_terrain(sim_info, terrain_object)

        Determine whether a Sim can route to a terrain object or not.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param terrain_object: The terrain object to check.
        :type terrain_object: Terrain
        :return: The result of running the test. True, if the Sim can route. False, if they cannot route.
        :rtype: CommonTestResult
        """
        position = CommonTerrainLocationUtils.get_position(terrain_object)
        routing_surface = CommonTerrainLocationUtils.get_routing_surface(terrain_object)
        if position is None or routing_surface is None:
            return CommonTestResult(False, reason=f'No position or routing surface found for terrain. {terrain_object}', hide_tooltip=True)

        if CommonTypeUtils.is_water(terrain_object):
            swim_at_position_test_result = CommonSimRoutingUtils.can_swim_at_position(sim_info, position, routing_surface)
            if not swim_at_position_test_result:
                return swim_at_position_test_result
        if not CommonLocationUtils.can_position_be_routed_to(position, routing_surface):
            return CommonTestResult(False, reason=f'Terrain {terrain_object} cannot be routed to by Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_SIM_CANNOT_REACH_THAT_SPOT, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'Terrain {terrain_object} can be routed to by Sim {sim_info}.', tooltip_text=CommonStringId.S4CL_SIM_CAN_REACH_THAT_SPOT, tooltip_tokens=(sim_info,))

    @staticmethod
    def can_swim_at_position(sim_info: SimInfo, position: CommonVector3, routing_surface: CommonSurfaceIdentifier) -> CommonTestResult:
        """can_swim_at_position(sim_info, position, routing_surface)

        Determine whether a Sim can swim to a target position or not.

        .. note:: This function assumes the target position is Ocean, a Pond, or a Swimming Pool.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param position: The position to check.
        :type position: CommonVector3
        :param routing_surface: The routing surface to check.
        :type routing_surface: CommonSurfaceIdentifier
        :return: The result of running the test. True, if the Sim can swim at the position. False, if they cannot.
        :rtype: CommonTestResult
        """
        if position is None or routing_surface is None:
            from routing.walkstyle.wading_tests import WadingIntervalTest
            water_height = WadingIntervalTest.WATER_DEPTH_ON_LAND
        else:
            water_height = CommonTerrainUtils.get_water_depth_at(position.x, position.z, surface_level=routing_surface.secondary_id)

        import build_buy
        if bool(build_buy.get_pond_id(position)):
            (lower_bound, upper_bound) = CommonSimBodyUtils.get_pond_wading_size(sim_info)
        else:
            (lower_bound, upper_bound) = CommonSimBodyUtils.get_ocean_wading_size(sim_info)

        if water_height <= upper_bound:
            return CommonTestResult(False, reason=f'Water is too shallow ({water_height}) for Sim {sim_info} ({lower_bound}, {upper_bound})', tooltip_text=CommonStringId.S4CL_SIM_CANNOT_REACH_THAT_SPOT, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} can swim at position.', tooltip_text=CommonStringId.S4CL_SIM_CAN_REACH_THAT_SPOT, tooltip_tokens=(sim_info,))
