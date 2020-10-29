"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Any, Union

from interactions import ParticipantType
from interactions.base.interaction import Interaction
from interactions.constraints import Constraint
from sims4communitylib.classes.interactions.common_interaction import CommonInteraction

# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if not ON_RTD:
    from interactions.base.super_interaction import SuperInteraction
    from scheduling import Timeline
    from sims4.utils import flexmethod
    from sims.sim import Sim
else:
    # noinspection PyMissingOrEmptyDocstring
    class MockClass(object):
        # noinspection PyMissingTypeHints,PyUnusedLocal
        def __init__(self, *args, **kwargs):
            super(MockClass, self).__init__()

        # noinspection PyMissingTypeHints
        def __call__(self, *args, **kwargs):
            return None

    # noinspection PyMissingOrEmptyDocstring
    class SuperInteraction(MockClass):
        pass


    # noinspection PyMissingOrEmptyDocstring
    class Sim:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass


    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring,SpellCheckingInspection
    def flexmethod():
        pass


class CommonBaseSuperInteraction(CommonInteraction, SuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions.

    .. note:: Use this Base class when you don't wish _run_interaction_gen to be overridden.

    .. note::

        The main use for this class is to create interactions that wrap sub interactions.
        One example Super interaction is the `sim-chat` interaction, where other interactions (Such as the `Get To Know` interaction), run as sub interactions of `sim-chat`

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonBaseSuperInteraction):
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

    """
    pass


class CommonSuperInteraction(CommonBaseSuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions.

    .. note::

        The main use for this class is to create interactions that wrap sub interactions.
        One example Super interaction is the `sim-chat` interaction, where other interactions (Such as the `Get To Know` interaction), run as sub interactions of `sim-chat`

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    :Example:

    .. highlight:: python
    .. code-block:: python

        # The following is an example interaction that varies when it will display, when it will be hidden, and when it will be disabled with a tooltip.
        class _ExampleInteraction(CommonSuperInteraction):
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

            # Instead of on_started, SuperInteractions use on_run.
            def on_run(self, interaction_sim: Sim, interaction_target: Any: timeline: Timeline) -> bool:
                result = True
                if not result:
                    return False
                # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
                return True

    """
    # noinspection PyMissingTypeHints
    @classmethod
    def _tuning_loaded_callback(cls):
        return super()._tuning_loaded_callback()

    def _run_interaction_gen(self, timeline: Timeline):
        super()._run_interaction_gen(timeline)
        try:
            return self.on_run(self.sim, self.target, timeline)
        except Exception as ex:
            self.log.error('Error occurred while running interaction \'{}\' on_run.'.format(self.__class__.__name__), exception=ex)
        return False

    # noinspection PyUnusedLocal
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline: Timeline) -> bool:
        """on_run(interaction_sim, interaction_target, timeline)

        A hook that occurs upon the interaction being run.

        :param interaction_sim: The sim performing the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target of the interaction.
        :type interaction_target: Any
        :param timeline: The timeline the interaction is running on.
        :type timeline: Timeline
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        return True


class CommonConstrainedSuperInteraction(SuperInteraction):
    """An inheritable class that provides a way to create custom Super Interactions that provide custom constraints.

    .. note:: For more information see :class:`.CommonSuperInteraction`.

    .. warning:: Due to an issue with how Read The Docs functions, the base classes of this class will have different namespaces than they do in the source code!

    """

    # noinspection PyMethodParameters
    @flexmethod
    def _constraint_gen(cls, inst: Interaction, sim: Sim, target: Any, participant_type: ParticipantType=ParticipantType.Actor, **kwargs) -> Constraint:
        inst_or_cls = inst if inst is not None else cls
        try:
            result = cls.on_constraint_gen(inst if inst is not None else cls, sim or inst_or_cls.sim, target or inst_or_cls.target)
            if result is not None:
                yield result
            else:
                return super(CommonConstrainedSuperInteraction, inst_or_cls)._constraint_gen(sim, target, participant_type=participant_type, **kwargs)
        except Exception as ex:
            cls.get_log().error('Error occurred while running interaction \'{}\' _on_constraint_gen.'.format(cls.__name__), exception=ex)

    @classmethod
    def on_constraint_gen(cls, inst: Interaction, sim: Sim, target: Any) -> Union[Constraint, None]:
        """on_constraint_gen(inst, sim, target)

        A hook that occurs when generating the constraints of an interaction to enable modification or replacement of the constraints.

        .. note:: Return None from this function to use the original constraints.

        :param inst: An instance of the interaction.
        :type inst: Interaction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: The constraints of the interaction.
        :rtype: Union[Constraint, None]
        """
        raise NotImplementedError()

