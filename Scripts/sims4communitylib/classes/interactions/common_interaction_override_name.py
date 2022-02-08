"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union

from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim import Sim
from sims4.utils import flexmethod
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonInteractionOverrideName(HasClassLog):
    """CommonInteractionOverrideName()

    An inheritable class that provides a way to override the :func:`~get_name` function of :class:`.CommonInteraction`.

    .. warning:: This class is obsolete. All interaction types come with their own :func:`~get_name` function. This class is to be used in conjunction with :class:`.CommonInteraction`. Inheriting from this class will do nothing for class that does not also inherit from :class:`.CommonInteraction`.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> Union[CommonModIdentity, None]:
        return None

    def __init__(self) -> None:
        super().__init__()
        HasClassLog.__init__(self)

    # noinspection PyMethodParameters,PyMissingOrEmptyDocstring
    @flexmethod
    def get_name(cls, inst: Interaction, target: Any=None, context: InteractionContext=None, **interaction_parameters) -> LocalizedString:
        inst_or_cls = inst or cls
        try:
            context_inst_or_cls = context or inst_or_cls
            interaction_sim = context_inst_or_cls.sim
            interaction_target = target or context_inst_or_cls.target

            cls.get_verbose_log().format_with_message(
                'Creating display name.',
                class_name=cls.__name__,
                interaction_sim=interaction_sim,
                interaction_target=interaction_target,
                interaction=inst,
                interaction_context=context
            )
            override_name = cls._create_display_name(
                interaction_sim,
                interaction_target,
                interaction=inst,
                interaction_context=context,
                **interaction_parameters
            )
            if override_name is not None:
                return override_name
        except Exception as ex:
            cls.get_log().error('An error occurred while running get_name of CommonInteractionOverrideName {}'.format(cls.__name__), exception=ex)
        result = super(Interaction, inst_or_cls).get_name(target=target, context=context, **interaction_parameters)
        if result is None:
            cls.get_log().error(f'Missing a name for interaction {cls.__name__}', throw=True)
        return result

    # noinspection PyUnusedLocal
    @classmethod
    def _create_display_name(cls, interaction_sim: Sim, interaction_target: Any, interaction: Union[Interaction, None]=None, interaction_context: Union[InteractionContext, None]=None, **interaction_parameters) -> Union[LocalizedString, None]:
        """_create_display_name(interaction_sim, interaction_target, interaction=None, interaction_context=None, **interaction_parameters)

        A hook that allows using a custom display name for an Interaction.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction: An instance of an interaction or None if no instance of the interaction is available. Default is None.
        :type interaction: Union[Interaction, None], optional
        :param interaction_context: The context of the interaction or None if no interaction context is available. Default is None.
        :type interaction_context: Union[InteractionContext, None], optional
        :param interaction_parameters: Extra interaction parameters.
        :type interaction_parameters: Any
        :return: A Localized String to display for the interaction or None if the original display name should be used.
        :rtype: Union[LocalizedString, None]
        """
        raise NotImplementedError()
