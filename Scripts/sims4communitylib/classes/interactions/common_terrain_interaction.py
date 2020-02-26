"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any

from event_testing.results import TestResult
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from interactions.context import InteractionContext
from objects.terrain import TravelMixin, TerrainInteractionMixin
from sims.sim import Sim
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

        :Example:

        .. highlight:: python
        .. code-block:: python

            class _ExampleTerrainInteraction(CommonTerrainInteraction):
                @classmethod
                def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
                    result = 1 + 1
                    if result == 2:
                        # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
                        return cls.create_test_result(False, reason="Test Tooltip")
                        # Alternative way to specify a tooltip with the text "Test Tooltip"
                        # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
                    if result == 3:
                        # Interaction will be hidden completely.
                        return TestResult.NONE
                    # Interaction will display and be enabled.
                    return TestResult.TRUE

                def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
                    result = True
                    if not result:
                        return False
                    # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                    return True

        """
        pass
else:
    class CommonTerrainInteraction(CommonInteraction, TravelMixin, TerrainInteractionMixin, ImmediateSuperInteraction):
        """An inheritable class that provides a way to create custom Terrain Interactions.

        .. note:: The main use for this class is to create interactions that occur when clicking on the ground.

        :Example:

        .. highlight:: python
        .. code-block:: python

            class _ExampleTerrainInteraction(CommonTerrainInteraction):
                @classmethod
                def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
                    result = 1 + 1
                    if result == 2:
                        # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
                        return cls.create_test_result(False, reason="Test Tooltip")
                        # Alternative way to specify a tooltip with the text "Test Tooltip"
                        # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
                    if result == 3:
                        # Interaction will be hidden completely.
                        return TestResult.NONE
                    # Interaction will display and be enabled.
                    return TestResult.TRUE

                def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
                    result = True
                    if not result:
                        return False
                    # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                    return True
        """
        pass


# The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
class _ExampleTerrainInteraction(CommonTerrainInteraction):
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        result = 1 + 1
        if result == 2:
            # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
            return cls.create_test_result(False, reason="Test Tooltip")
            # Alternative way to specify a tooltip with the text "Test Tooltip"
            # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
        if result == 3:
            # Interaction will be hidden completely.
            return TestResult.NONE
        # Interaction will display and be enabled.
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        result = True
        if not result:
            return False
        # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
        return True
