"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Any, Tuple, List

from interactions.base.immediate_interaction import ImmediateSuperInteraction
from interactions.base.interaction import Interaction
from interactions.base.mixer_interaction import MixerInteraction
from interactions.base.super_interaction import SuperInteraction
from interactions.context import InteractionContext
from interactions.interaction_instance_manager import InteractionInstanceManager
from interactions.social.social_mixer_interaction import SocialMixerInteraction
from interactions.social.social_super_interaction import SocialSuperInteraction
from protocolbuffers.Localization_pb2 import LocalizedString
from server.pick_info import PickInfo
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from tag import Tag


class CommonInteractionUtils:
    """Utilities for manipulating Interactions.

    """

    @staticmethod
    def has_any_static_commodities(interaction: Interaction, static_commodity_ids: Iterator[int]) -> bool:
        """has_any_static_commodities(interaction, static_commodity_ids)

        Determine if an interaction has any of the specified static commodities.

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :param static_commodity_ids: A collection of static commodity ids.
        :type static_commodity_ids: Iterator[int], optional
        :return: True, if the interaction has any of the specified static commodities. False, if not.
        :rtype: bool
        """
        interaction_commodities = interaction.static_commodities
        if not interaction_commodities:
            return False
        static_commodity_ids = tuple(static_commodity_ids)
        if not static_commodity_ids:
            return True
        for static_commodity_id in static_commodity_ids:
            for interaction_commodity in interaction_commodities:
                interaction_commodity_id = getattr(interaction_commodity, 'guid64', None)
                if static_commodity_id == interaction_commodity_id:
                    return True
        return False

    @staticmethod
    def has_all_static_commodities(interaction: Interaction, static_commodity_ids: Iterator[int]) -> bool:
        """has_all_static_commodities(interaction, static_commodity_ids)

        Determine if an interaction has all the specified static commodities.

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :param static_commodity_ids: A collection of static commodity ids.
        :type static_commodity_ids: Iterator[int], optional
        :return: True, if the interaction has all the specified static commodities. False, if not.
        :rtype: bool
        """
        interaction_commodities = interaction.static_commodities
        if not interaction_commodities:
            return False
        static_commodity_ids = tuple(static_commodity_ids)
        if not static_commodity_ids:
            return True
        for static_commodity_id in static_commodity_ids:
            has_commodity = False
            for interaction_commodity in interaction_commodities:
                interaction_commodity_id = getattr(interaction_commodity, 'guid64', None)
                if static_commodity_id == interaction_commodity_id:
                    has_commodity = True
                    break
            if not has_commodity:
                return False
        return True

    @staticmethod
    def has_any_appropriateness_tags(interaction: Interaction, appropriateness_tags: Iterator[CommonGameTag]) -> bool:
        """has_any_appropriateness_tags(interaction, appropriateness_tags)

        Determine if an interaction has Appropriateness Tags

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :param appropriateness_tags: A collection of appropriateness tags.
        :type appropriateness_tags: Iterator[CommonGameTag]
        :return: True, if the Interaction has any of the specified appropriateness tags. False, if not.
        :rtype: bool
        """
        if interaction.appropriateness_tags is None:
            return False
        appropriateness_tags = tuple(appropriateness_tags)
        if not appropriateness_tags:
            return False
        for appropriateness_tag in interaction.appropriateness_tags:
            appropriateness_tag_converted = CommonResourceUtils.get_enum_by_int_value(int(appropriateness_tag), CommonGameTag, default_value=int(appropriateness_tag))
            if appropriateness_tag_converted is None:
                continue
            if appropriateness_tag_converted in appropriateness_tags:
                return True
        return False

    @staticmethod
    def has_all_appropriateness_tags(interaction: Interaction, appropriateness_tags: Iterator[CommonGameTag]) -> bool:
        """has_all_appropriateness_tags(interaction, appropriateness_tags)

        Determine if an interaction has Appropriateness Tags

        :param interaction: An instance of an interaction.
        :type interaction: Interaction
        :param appropriateness_tags: A collection of appropriateness tags.
        :type appropriateness_tags: Iterator[CommonGameTag]
        :return: True, if the Interaction has all the specified appropriateness tags. False, if not.
        :rtype: bool
        """
        if interaction.appropriateness_tags is None:
            return False
        if not appropriateness_tags:
            return False
        interaction_appropriateness_tags = interaction.appropriateness_tags
        for appropriateness_tag in tuple(appropriateness_tags):
            tag = CommonResourceUtils.get_enum_by_int_value(int(appropriateness_tag), Tag, default_value=int(appropriateness_tag))
            if tag not in interaction_appropriateness_tags:
                return False
        return True

    @staticmethod
    def get_pick_info_from_interaction_context(interaction_context: InteractionContext) -> Union[PickInfo, None]:
        """get_pick_info_from_interaction_context(interaction_context)

        Retrieve the pick info of an interaction context.

        :param interaction_context: An interaction context.
        :type interaction_context: InteractionContext
        :return: The pick info of the interaction context or None, if not found.
        :rtype: PickInfo
        """
        if interaction_context is None or interaction_context.pick is None:
            return None
        return interaction_context.pick

    @staticmethod
    def get_picked_routing_surface_from_interaction_context(interaction_context: InteractionContext) -> Union[CommonSurfaceIdentifier, None]:
        """get_picked_routing_surface_from_interaction_context(interaction_context)

        Retrieve the picked routing surface from an interaction context.

        :param interaction_context: An interaction context.
        :type interaction_context: InteractionContext
        :return: The picked routing surface from the interaction context or None if a problem occurs.
        :rtype: Union[CommonSurfaceIdentifier, None]
        """
        pick_info = CommonInteractionUtils.get_pick_info_from_interaction_context(interaction_context)
        if pick_info is None:
            return None
        return CommonSurfaceIdentifier.from_surface_identifier(pick_info.routing_surface)

    @staticmethod
    def get_picked_position_from_interaction_context(interaction_context: InteractionContext) -> Union[CommonVector3, None]:
        """get_picked_position_from_interaction_context(interaction_context)

        Retrieve the picked position from an interaction context.

        :param interaction_context: An interaction context.
        :type interaction_context: InteractionContext
        :return: The picked position from the interaction context or None if a problem occurs.
        :rtype: Union[CommonVector3, None]
        """
        pick_info = CommonInteractionUtils.get_pick_info_from_interaction_context(interaction_context)
        if pick_info is None:
            return None
        return CommonVector3.from_vector3(pick_info.location)

    @staticmethod
    def get_picked_routing_position_from_interaction_context(interaction_context: InteractionContext) -> Union[CommonVector3, None]:
        """get_picked_routing_position_from_interaction_context(interaction_context)

        Retrieve the picked routing position from an interaction context.

        :param interaction_context: An interaction context.
        :type interaction_context: InteractionContext
        :return: The picked routing position with the routing surface applied to it from the interaction context or None if a problem occurs.
        :rtype: Union[CommonVector3, None]
        """
        pick_info = CommonInteractionUtils.get_pick_info_from_interaction_context(interaction_context)
        if pick_info is None:
            return None
        picked_position = CommonVector3.from_vector3(pick_info.location)
        picked_routing_surface = CommonSurfaceIdentifier.from_surface_identifier(pick_info.routing_surface)
        picked_position.y = CommonLocationUtils.get_surface_height_at(picked_position.x, picked_position.z, picked_routing_surface)
        return picked_position

    @staticmethod
    def get_picked_routing_surface_level_from_interaction_context(interaction_context: InteractionContext) -> Union[int, None]:
        """get_picked_routing_surface_level_from_interaction_context(interaction_context)

        Retrieve the picked routing surface level from an interaction context.

        :param interaction_context: An interaction context.
        :type interaction_context: InteractionContext
        :return: The picked routing surface level from the interaction context or None if a problem occurs.
        :rtype: Union[int, None]
        """
        routing_surface = CommonInteractionUtils.get_picked_routing_surface_from_interaction_context(interaction_context)
        if routing_surface is None:
            return None
        return routing_surface.secondary_id

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
    def is_mixer_interaction(interaction: Interaction) -> bool:
        """is_mixer_interaction(interaction)

        Determine if an interaction is a Mixer interaction.

        :param interaction: An instance of an Interaction.
        :type interaction: Interaction
        :return: True, if the interaction is a Mixer interaction. False, if not.
        """
        if interaction is None:
            return False
        return isinstance(interaction, MixerInteraction)

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
        if isinstance(interaction, SocialMixerInteraction):
            return True
        if not hasattr(interaction, 'is_social'):
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
        if isinstance(interaction, SuperInteraction):
            return True
        if not hasattr(interaction, 'is_super'):
            return False
        return interaction.is_super

    @staticmethod
    def is_immediate_super_interaction(interaction: Interaction) -> bool:
        """is_immediate_super_interaction(interaction)

        Determine if an interaction is an Immediate Super interaction.

        :param interaction: An instance of an Interaction.
        :type interaction: Interaction
        :return: True, if the interaction is an Immediate Super interaction. False, if not.
        """
        if interaction is None:
            return False
        return isinstance(interaction, ImmediateSuperInteraction)

    @staticmethod
    def is_social_super_interaction(interaction: Interaction) -> bool:
        """is_social_super_interaction(interaction)

        Determine if an interaction is a Social Super interaction.

        :param interaction: An instance of an Interaction.
        :type interaction: Interaction
        :return: True, if the interaction is a Social Super interaction. False, if not.
        """
        if interaction is None:
            return False
        return isinstance(interaction, SocialSuperInteraction)

    @staticmethod
    def get_interaction_display_name(interaction: Interaction, tokens: Iterator[Any] = ()) -> Union[LocalizedString, None]:
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
        display_name_string_id = interaction.display_name._string_id
        if not display_name_string_id:
            return None
        return CommonLocalizationUtils.create_localized_string(display_name_string_id, tokens=tuple(tokens))

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
            return str(interaction.shortname() or '') or interaction.__name__ or interaction.__class__.__name__
        except:
            # noinspection PyBroadException
            try:
                return interaction.__name__
            except:
                # noinspection PyBroadException
                try:
                    return interaction.__class__.__name__
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
        short_names: List[str] = list()
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
            # noinspection PyCallingNonCallable
            interaction_instance = interaction_id()
            if isinstance(interaction_instance, Interaction):
                # noinspection PyTypeChecker
                return interaction_id
        except:
            pass
        # noinspection PyBroadException
        try:
            interaction_id: int = int(interaction_id)
        except:
            # noinspection PyTypeChecker
            interaction_id: Interaction = interaction_id
            return interaction_id

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.INTERACTION, interaction_id)

    @staticmethod
    def get_instance_manager() -> InteractionInstanceManager:
        """get_instance_manager()

        Retrieve the instance manager that manages all tunables for interactions.

        :return: The instance manager that manages all tunables for interactions.
        :rtype: InteractionInstanceManager
        """
        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        # noinspection PyTypeChecker
        return CommonResourceUtils.get_instance_manager(Types.INTERACTION)
