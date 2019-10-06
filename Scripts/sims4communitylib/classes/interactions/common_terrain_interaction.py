"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from objects.terrain import TravelMixin, TerrainInteractionMixin
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction


class CommonTerrainInteraction(CommonInteraction, TravelMixin, TerrainInteractionMixin, ImmediateSuperInteraction):
    """ A base for accessing terrain interaction hooks. """
    pass
