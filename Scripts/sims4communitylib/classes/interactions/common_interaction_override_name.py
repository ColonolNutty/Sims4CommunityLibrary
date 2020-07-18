from typing import Any, Union

from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim import Sim
from sims4.utils import flexmethod
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonInteractionOverrideName(HasClassLog):
    """CommonInteractionOverrideName()

    An inheritable class that provides a way to override the :func:`~get_name` function of :class:`.CommonInteraction`.

    .. warning:: This class is to be used in conjunction with :class:`.CommonInteraction`. Inheriting from this class will do nothing for class that does not also inherit from :class:`.CommonInteraction`.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    def __init__(self) -> None:
        super().__init__()
        HasClassLog.__init__(self)

    # noinspection PyMethodParameters,PyMissingOrEmptyDocstring
    @flexmethod
    def get_name(cls, inst: Interaction, target: Any=None, context: InteractionContext=None, *args, **kwargs) -> Union[LocalizedString, None]:
        try:
            inst_or_cls = context or inst or cls
            return cls._create_display_name(inst_or_cls.sim, target or inst_or_cls.target, interaction=inst, interaction_context=context, *args, **kwargs)
        except Exception as ex:
            CommonExceptionHandler.log_exception(cls.get_mod_identity(), 'An error occurred while running get_name of interaction {}'.format(cls.__name__), exception=ex)

    # noinspection PyUnusedLocal
    @classmethod
    def _create_display_name(cls, interaction_sim: Sim, interaction_target: Any, interaction: Union[Interaction, None]=None, interaction_context: Union[InteractionContext, None]=None, *args, **kwargs) -> Union[LocalizedString, None]:
        """_create_display_name(interaction_sim, interaction_target, interaction=None, interaction_context=None)

        A hook that allows using a custom display name for an Interaction.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction: An instance of an interaction or None if no instance of the interaction is available. Default is None.
        :type interaction: Union[Interaction, None], optional
        :param interaction_context: The context of the interaction or None if no interaction context is available. Default is None.
        :type interaction_context: Union[InteractionContext, None], optional
        :param args: Extra arguments not accounted for.
        :type args: Any
        :param kwargs: Extra Keyword arguments not accounted for.
        :type kwargs: Any
        :return: A Localized String to display for the interaction or None if the original display name should be used.
        :rtype: Union[LocalizedString, None]
        """
        raise NotImplementedError()
