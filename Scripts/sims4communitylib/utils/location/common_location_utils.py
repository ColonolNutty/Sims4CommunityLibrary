"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services

from typing import Tuple

import build_buy
from sims4.resources import Types
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from venues.venue_tuning import Venue, VenueTypes
from world.lot import Lot
from zone import Zone
from zone_modifier.zone_modifier import ZoneModifier
from protocolbuffers.Math_pb2 import Vector3
from sims4.math import Location


class CommonLocationUtils:
    """Utilities for manipulating locations and lots.

    """

    @staticmethod
    def get_zone_id(zone: Zone) -> int:
        """Retrieve the identifier of the specified Zone.

        """
        return zone.id

    @staticmethod
    def get_current_zone() -> Zone:
        """Retrieve the current zone.

        """
        return services.current_zone()

    @staticmethod
    def get_current_zone_id() -> int:
        """Retrieve the current zone id.

        """
        return services.current_zone_id()

    @staticmethod
    def get_current_lot() -> Lot:
        """Retrieve the current lot.

        """
        return CommonLocationUtils.get_current_zone().lot

    @staticmethod
    def is_location_outside_current_lot(location: Location) -> bool:
        """Determine if a location is outside of the current lot or not.

        """
        return CommonLocationUtils.is_location_outside_lot(location, CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def is_location_outside_lot(location: Location, lot_id: int) -> bool:
        """Determine if a location is outside of the Lot with the specified identifier.

        """
        try:
            return build_buy.is_location_outside(lot_id, location.transform.translation, location.level)
        except RuntimeError:
            return False

    @staticmethod
    def is_position_on_current_lot(position: Vector3) -> bool:
        """Determine if a sim is on the current lot.

        """
        return position is not None and services.active_lot().is_position_on_lot(position)

    @staticmethod
    def get_current_lot_id() -> int:
        """Retrieve the identifier for the Current Lot.

        """
        return services.current_zone_id()

    @staticmethod
    def get_lot_traits(lot_id: int) -> Tuple[ZoneModifier]:
        """Retrieve the Lot Traits of a Lot with the specified identifier.

        """
        return tuple(services.get_zone_modifier_service().get_zone_modifiers(lot_id))

    @staticmethod
    def get_lot_traits_of_current_lot() -> Tuple[ZoneModifier]:
        """Retrieve the Lot Traits of the Current Lot.

        """
        return CommonLocationUtils.get_lot_traits(CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def current_lot_has_trait(lot_trait_id: int) -> bool:
        """Determine if the Current Lot has the specified Lot Trait.

        """
        return CommonLocationUtils.current_lot_has_all_traits((lot_trait_id,))

    @staticmethod
    def current_lot_has_any_traits(lot_trait_ids: Tuple[int]) -> bool:
        """Determine if the Current Lot has any of the specified Lot Traits.

        """
        current_lot_traits = CommonLocationUtils.get_lot_traits_of_current_lot()
        for current_lot_trait in current_lot_traits:
            lot_trait_id = getattr(current_lot_trait, 'guid64', None)
            if lot_trait_id in lot_trait_ids:
                return True
        return False

    @staticmethod
    def current_lot_has_all_traits(lot_trait_ids: Tuple[int]) -> bool:
        """Determine if the Current Lot has all of the specified Lot Traits.

        """
        current_lot_traits = CommonLocationUtils.get_lot_traits_of_current_lot()
        for current_lot_trait in current_lot_traits:
            lot_trait_id = getattr(current_lot_trait, 'guid64', None)
            if lot_trait_id not in lot_trait_ids:
                return False
        return True

    @staticmethod
    def get_current_venue_type() -> VenueTypes:
        """Retrieve the type of the current venue.

        """
        return build_buy.get_current_venue(CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def get_venue_of_current_lot() -> Venue:
        """Retrieve a Venue for the current lot.

        """
        return CommonResourceUtils.load_instance(Types.VENUE, CommonLocationUtils.get_current_venue_type())

    @staticmethod
    def is_current_venue_residential() -> bool:
        """Determine if a venue is residential.

        """
        venue_instance = CommonLocationUtils.get_venue_of_current_lot()
        if venue_instance is None:
            return False
        # noinspection PyUnresolvedReferences
        return venue_instance.residential

    @staticmethod
    def current_venue_requires_player_greeting() -> bool:
        """Determine if the current venue requires player greeting.

        """
        venue_instance = CommonLocationUtils.get_venue_of_current_lot()
        if venue_instance is None:
            return False
        return venue_instance.requires_visitation_rights

    @staticmethod
    def current_venue_allows_role_state_routing() -> bool:
        """Determine if the current venue allows routing for role states.

        """
        venue_instance = CommonLocationUtils.get_venue_of_current_lot()
        if venue_instance is None:
            return False
        # noinspection PyUnresolvedReferences
        return venue_instance.allow_rolestate_routing_on_navmesh
