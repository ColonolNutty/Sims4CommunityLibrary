"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from interactions.base.interaction import Interaction
from sims4.resources import Types
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonInteractionUtils:
    """Utilities for manipulating Interactions.

    """

    @staticmethod
    def get_interaction_id(interaction_identifier: Union[int, Interaction]) -> Union[int, None]:
        """get_interaction_id(interaction_identifier)

        Retrieve the decimal identifier of an Interaction.

        :param interaction_identifier: The identifier or instance of a Interaction.
        :type interaction_identifier: Union[int, Interaction]
        :return: The decimal identifier of the Buff or None if the Buff does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(interaction_identifier, int):
            return interaction_identifier
        return getattr(interaction_identifier, 'guid64', None)

    @staticmethod
    def _load_interaction_instance(interaction_identifier: int) -> Union[Interaction, None]:
        if interaction_identifier is None:
            return None
        return CommonResourceUtils.load_instance(Types.INTERACTION, interaction_identifier)
