"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from objects.terrain import TravelMixin, TerrainInteractionMixin
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction


# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, don't extend from all these classes.
if ON_RTD:
    class CommonTerrainInteraction(CommonInteraction):
        """CommonTerrainInteraction()

        An inheritable class that provides a way to create custom Terrain Interactions.

        .. note::

            Extends from the following classes:

           * :class:`.CommonInteraction`
           * :class:`TravelMixin`
           * :class:`TerrainInteractionMixin`
           * :class:`ImmediateSuperInteraction`

        .. note:: The main use for this class is to create interactions that occur when clicking on the ground.

        .. warning:: Due to issues with Read The Docs, the source code will look different for this class than it does here!

        """
        pass
else:
    class CommonTerrainInteraction(CommonInteraction, TravelMixin, TerrainInteractionMixin, ImmediateSuperInteraction):
        """An inheritable class that provides a way to create custom Terrain Interactions.

        .. note:: The main use for this class is to create interactions that occur when clicking on the ground.

        """
        pass
