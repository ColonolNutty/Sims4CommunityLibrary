"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services

from typing import Tuple

import build_buy

try:
    import _buildbuy
except ImportError:
    # noinspection SpellCheckingInspection
    _buildbuy = build_buy
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

    To manipulate the location of Sims, see :class:`.CommonSimLocationUtils`.

    """

    @staticmethod
    def get_zone_id(zone: Zone) -> int:
        """get_zone_id(zone)

        Retrieve the identifier of the specified Zone.

        :param zone: The Zone to get the identifier of.
        :type zone: Zone
        :return: The identifier of the specified Zone.
        :rtype: int
        """
        return zone.id

    @staticmethod
    def get_current_zone() -> Zone:
        """get_current_zone()

        Retrieve the current zone.

        :return: The current Zone
        :rtype: Zone
        """
        return services.current_zone()

    @staticmethod
    def get_current_zone_id() -> int:
        """get_current_zone_id()

        Retrieve the current zone id.

        :return: The identifier of the current Zone.
        :rtype: int
        """
        return services.current_zone_id()

    @staticmethod
    def get_current_lot_id() -> int:
        """get_current_lot_id()

        Retrieve the identifier for the Current Lot.

        :return: The identifier of the current lot.
        :rtype: int
        """
        return services.current_zone_id()

    @staticmethod
    def get_current_lot() -> Lot:
        """get_current_lot()

        Retrieve the current lot.

        :return: The current Lot.
        :rtype: Lot
        """
        return CommonLocationUtils.get_current_zone().lot

    @staticmethod
    def is_location_outside_current_lot(location: Location) -> bool:
        """is_location_outside_current_lot(location)

        Determine if a location is outside of the current lot or not.

        :param location: The Location to check.
        :type location: Location
        :return: True, if the location is outside of the current lot. False, if not.
        :rtype: bool
        """
        return CommonLocationUtils.is_location_outside_lot(location, CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def is_location_outside_lot(location: Location, lot_id: int) -> bool:
        """is_location_outside_lot(location, lot_id)

        Determine if a location is outside of the Lot with the specified identifier.

        :param location: The Location to check.
        :type location: Location
        :param lot_id: The identifier of the Lot to check for the Location to be outside of.
        :type lot_id: int
        :return: True, if location is outside of the Lot with the specified lot_id. False, if not.
        :rtype: bool
        """
        try:
            # noinspection PyTypeChecker
            return _buildbuy.is_location_outside(lot_id, location.transform.translation, location.level)
        except RuntimeError:
            return False

    @staticmethod
    def is_position_on_current_lot(position: Vector3) -> bool:
        """is_position_on_current_lot(position)

        Determine if a sim is on the current lot.

        :param position: The position to check.
        :type position: Vector3
        :return: True, if the specified position is within the bounds of the current lot. False, if not.
        :rtype: bool
        """
        return position is not None and services.active_lot().is_position_on_lot(position)

    @staticmethod
    def get_lot_traits(lot_id: int) -> Tuple[ZoneModifier]:
        """get_lot_traits(lot_id)

        Retrieve the Lot Traits of a Lot with the specified identifier.

        :param lot_id: The lot to retrieve the traits of.
        :type lot_id: int
        :return: A collection of Lot Traits for the specified lot.
        :rtype: Tuple[ZoneModifier]
        """
        return tuple(services.get_zone_modifier_service().get_zone_modifiers(lot_id))

    @staticmethod
    def get_lot_traits_of_current_lot() -> Tuple[ZoneModifier]:
        """get_lot_traits_of_current_lot()

        Retrieve the Lot Traits of the Current Lot.

        :return: A collection of Lot Traits for the current lot.
        :rtype: Tuple[ZoneModifier]
        """
        return CommonLocationUtils.get_lot_traits(CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def current_lot_has_trait(lot_trait_id: int) -> bool:
        """current_lot_has_trait(lot_trait_id)

        Determine if the Current Lot has the specified Lot Trait.

        :param lot_trait_id: The trait to look for.
        :type lot_trait_id: int
        :return: True, if the current lot has the specified trait. False, if not.
        :rtype: bool
        """
        return CommonLocationUtils.current_lot_has_all_traits((lot_trait_id,))

    @staticmethod
    def current_lot_has_any_traits(lot_trait_ids: Tuple[int]) -> bool:
        """current_lot_has_any_traits(lot_trait_ids)

        Determine if the Current Lot has any of the specified Lot Traits.

        :param lot_trait_ids: A collection of traits to look for.
        :type lot_trait_ids: Tuple[int]
        :return: True, if the current lot has any of the specified traits. False, if not.
        :rtype: bool
        """
        current_lot_trait_ids = [getattr(current_lot_trait, 'guid64', None) for current_lot_trait in CommonLocationUtils.get_lot_traits_of_current_lot()]
        for lot_trait_id in lot_trait_ids:
            if lot_trait_id in current_lot_trait_ids:
                return True
        return False

    @staticmethod
    def current_lot_has_all_traits(lot_trait_ids: Tuple[int]) -> bool:
        """current_lot_has_all_traits(lot_trait_ids)

        Determine if the Current Lot has all of the specified Lot Traits.

        :param lot_trait_ids: A collection of traits to look for.
        :type lot_trait_ids: Tuple[int]
        :return: True, if the current lot has all of the specified traits. False, if not.
        :rtype: bool
        """
        current_lot_trait_ids = [getattr(current_lot_trait, 'guid64', None) for current_lot_trait in CommonLocationUtils.get_lot_traits_of_current_lot()]
        if len(current_lot_trait_ids) == 0:
            return False
        for lot_trait_id in lot_trait_ids:
            if lot_trait_id in current_lot_trait_ids:
                continue
            return False
        return True

    @staticmethod
    def get_current_venue_type() -> VenueTypes:
        """get_current_venue_type()

        Retrieve the type of the current venue.

        :return: The VenueType of the current lot.
        :rtype: VenueTypes
        """
        return build_buy.get_current_venue(CommonLocationUtils.get_current_lot_id())

    @staticmethod
    def get_venue_of_current_lot() -> Venue:
        """get_venue_of_current_lot()

        Retrieve a Venue for the current lot.

        :return: The Venue of the current lot.
        :rtype: Venue
        """
        return CommonResourceUtils.load_instance(Types.VENUE, CommonLocationUtils.get_current_venue_type())

    @staticmethod
    def is_current_venue_residential() -> bool:
        """is_current_venue_residential()

        Determine if a venue is residential.

        :return: True, if the venue of the current lot is residential. False, if not.
        :rtype: bool
        """
        venue_instance = CommonLocationUtils.get_venue_of_current_lot()
        if venue_instance is None:
            return False
        # noinspection PyUnresolvedReferences
        return venue_instance.residential

    @staticmethod
    def current_venue_requires_player_greeting() -> bool:
        """current_venue_requires_player_greeting()

        Determine if the current venue requires player greeting.

        :return: True, if the venue of the current lot requires the player to be greeted. False, if not.
        :rtype: bool
        """
        venue_instance = CommonLocationUtils.get_venue_of_current_lot()
        if venue_instance is None:
            return False
        return venue_instance.requires_visitation_rights

    @staticmethod
    def current_venue_allows_role_state_routing() -> bool:
        """current_venue_allows_role_state_routing()

        Determine if the current venue allows routing for role states.

        :return: True, if the venue of the current lot allows routing by role state. False, if not.
        :rtype: bool
        """
        venue_instance = CommonLocationUtils.get_venue_of_current_lot()
        if venue_instance is None:
            return False
        # noinspection PyUnresolvedReferences
        return venue_instance.allow_rolestate_routing_on_navmesh
