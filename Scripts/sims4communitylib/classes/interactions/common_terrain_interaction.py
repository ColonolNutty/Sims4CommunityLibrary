"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any

from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class MockClass(object):
        # noinspection PyMissingTypeHints,PyUnusedLocal
        def __init__(self, *args, **kwargs):
            super(MockClass, self).__init__()

        # noinspection PyMissingTypeHints
        def __call__(self, *args, **kwargs):
            return None

    # noinspection PyMissingOrEmptyDocstring
    class TravelMixin(MockClass):
        pass

    # noinspection PyMissingOrEmptyDocstring
    class TerrainInteractionMixin(MockClass):
        pass

if not ON_RTD:
    from objects.terrain import TravelMixin, TerrainInteractionMixin


class CommonTerrainInteraction(TravelMixin, TerrainInteractionMixin, CommonImmediateSuperInteraction):
    """CommonTerrainInteraction(*_, **__)

    An inheritable class that provides a way to create custom Terrain Interactions.

    .. note::

        The main use for this class is to create interactions that appear when clicking on the ground.\
        It CAN be used for interactions that appear when clicking on Sims and Objects, but it is not recommended.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        class _ExampleTerrainInteraction(CommonTerrainInteraction):
            @classmethod
            def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
                result = 1 + 1
                if result == 2:
                    # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
                    return cls.create_test_result(False, reason="Test Tooltip")
                    # Alternative way to specify a tooltip with the text "Test Tooltip"
                    # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
                if result == 3:
                    # Interaction will be hidden completely.
                    return CommonTestResult.NONE
                # Interaction will display and be enabled.
                return CommonTestResult.TRUE

            def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
                result = True
                if not result:
                    return CommonExecutionResult.FALSE
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return CommonExecutionResult.TRUE
    """
    pass


# The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
class _ExampleTerrainInteraction(CommonTerrainInteraction):
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        result = 1 + 1
        if result == 2:
            # Interaction will be displayed, but disabled, it will also have a tooltip that displays on hover with the text "Test Tooltip"
            return cls.create_test_result(False, reason="Test Tooltip")
            # Alternative way to specify a tooltip with the text "Test Tooltip"
            # return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))
        if result == 3:
            # Interaction will be hidden completely.
            return CommonTestResult.NONE
        # Interaction will display and be enabled.
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
        result = True
        if not result:
            return CommonExecutionResult.FALSE
        # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
        return CommonExecutionResult.TRUE
