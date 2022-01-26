"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union
from interactions.context import InteractionContext
from objects.terrain import TerrainPoint
from routing import SurfaceType
from server.pick_info import PickType
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonTerrainInteractionUtils(HasClassLog):
    """Utilities for manipulating the interactions of Terrain.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_terrain_interaction_utils'

    @staticmethod
    def build_terrain_point_and_interaction_context_from_sim_and_position(sim_info: SimInfo, target_position: CommonVector3, target_surface_level: int) -> Tuple[Union[TerrainPoint, None], Union[InteractionContext, None]]:
        """build_terrain_point_and_interaction_context_from_sim_and_position(sim_info, position, target_surface_level)

        Build a target and a context for the terrain.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param target_position: The target position.
        :type target_position: CommonVector3
        :param target_surface_level: The surface level at the target position.
        :type target_surface_level: int
        :return: A tuple of the terrain point and the interaction context created from the position and surface level for the Sim or (None, None) if an error occurs.
        :rtype: Tuple[Union[TerrainPoint, None], Union[InteractionContext, None]]
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        from server_commands.sim_commands import _build_terrain_interaction_target_and_context
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None, None
        routing_surface = CommonSurfaceIdentifier(CommonLocationUtils.get_current_zone_id(), secondary_id=target_surface_level, surface_type=SurfaceType.SURFACETYPE_WORLD)
        return _build_terrain_interaction_target_and_context(sim, target_position, routing_surface, PickType.PICK_TERRAIN, TerrainPoint)
