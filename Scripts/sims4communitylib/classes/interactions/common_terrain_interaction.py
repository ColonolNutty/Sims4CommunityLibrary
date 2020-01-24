"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from objects.terrain import TravelMixin, TerrainInteractionMixin
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction


class CommonTerrainInteraction(CommonInteraction, TravelMixin, TerrainInteractionMixin, ImmediateSuperInteraction):
    """An inheritable class that provides a way to create custom Terrain Interactions.

    The main use for this class is to create interactions that occur when clicking on the ground.

    """
    pass
