"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Union, Iterator, Any, Tuple, List
from interactions.base.interaction import Interaction
from interactions.interaction_instance_manager import InteractionInstanceManager
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.interactions_enum import CommonInteractionId


class CommonInteractionUtils:
    """Utilities for manipulating Interactions.

    """

    @staticmethod
    def get_interaction_id(interaction_identifier: Union[int, Interaction]) -> Union[int, None]:
        """get_interaction_id(interaction_identifier)

        Retrieve the decimal identifier of an Interaction.

        :param interaction_identifier: The identifier or instance of a Interaction.
        :type interaction_identifier: Union[int, Interaction]
        :return: The decimal identifier of the Interaction or None if the Interaction does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(interaction_identifier, int):
            return interaction_identifier
        return getattr(interaction_identifier, 'guid64', None)

    @staticmethod
    def is_social_mixer_interaction(interaction: Interaction) -> bool:
        """is_social_mixer_interaction(interaction)

        Determine if an interaction is a Social Mixer interaction.

        :param interaction: An instance of an Interaction.
        :type interaction: Interaction
        :return: True, if the interaction is a Social Mixer interaction. False, if not.
        """
        if interaction is None:
            return False
        return interaction.is_social

    @staticmethod
    def is_super_interaction(interaction: Interaction) -> bool:
        """is_super_interaction(interaction)

        Determine if an interaction is a Super interaction.

        :param interaction: An instance of an Interaction.
        :type interaction: Interaction
        :return: True, if the interaction is a Super interaction. False, if not.
        """
        if interaction is None:
            return False
        return interaction.is_super

    @staticmethod
    def get_interaction_display_name(interaction: Interaction, tokens: Iterator[Any]=()) -> Union[LocalizedString, None]:
        """get_interaction_display_name(interaction, tokens=())

        Retrieve the display name of an interaction.

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :param tokens: A collection of tokens to format into the display name.
        :type tokens: Iterator[Any]
        :return: An instance of type LocalizedString or None if a problem occurs.
        :rtype: Union[LocalizedString, None]
        """
        from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
        if interaction is None or interaction.display_name is None:
            return None
        return CommonLocalizationUtils.create_localized_string(interaction.display_name._string_id, tokens=tuple(tokens))

    @staticmethod
    def get_interaction_short_name(interaction: Interaction) -> Union[str, None]:
        """get_interaction_short_name(interaction)

        Retrieve the Short Name of an Interaction.

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :return: The short name of an interaction or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if interaction is None:
            return None
        # noinspection PyBroadException
        try:
            return str(interaction.shortname() or '') or interaction.__class__.__name__
        except:
            return ''

    @staticmethod
    def get_interaction_short_names(interactions: Iterator[Interaction]) -> Tuple[str]:
        """get_interaction_short_names(interactions)

        Retrieve the Short Names of a collection of Interactions.

        :param interactions: A collection of interaction instances.
        :type interactions: Iterator[Interaction]
        :return: A collection of short names of all interaction instances.
        :rtype: Tuple[str]
        """
        if interactions is None or not interactions:
            return tuple()
        short_names: List[str] = []
        for interaction in interactions:
            # noinspection PyBroadException
            try:
                short_name = CommonInteractionUtils.get_interaction_short_name(interaction)
                if not short_name:
                    continue
            except:
                continue
            short_names.append(short_name)
        return tuple(short_names)

    @staticmethod
    def load_interaction_by_id(interaction_id: Union[int, CommonInteractionId, Interaction]) -> Union[Interaction, None]:
        """load_interaction_by_id(interaction_id)

        Load an instance of an Interaction by its decimal identifier.

        :param interaction_id: The decimal identifier of an Interaction.
        :type interaction_id: Union[int, CommonInteractionId, Interaction]
        :return: An instance of an Interaction matching the decimal identifier or None if not found.
        :rtype: Union[Interaction, None]
        """
        if isinstance(interaction_id, Interaction):
            return interaction_id
        # noinspection PyBroadException
        try:
            interaction_id: int = int(interaction_id)
        except:
            interaction_id: Interaction = interaction_id
            return interaction_id

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.INTERACTION, interaction_id)

    @staticmethod
    def get_instance_manager() -> InteractionInstanceManager:
        """get_instance_manager()

        Retrieve the instance manager for interactions.

        :return: The instance manager for interactions.
        :rtype: InteractionInstanceManager
        """
        from sims4.resources import Types
        return services.get_instance_manager(Types.INTERACTION)
