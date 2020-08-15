"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services

from typing import Tuple, Union, Any, Dict, List

import build_buy
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3

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


class CommonLocationUtils:
    """Utilities for manipulating locations and lots.

    To manipulate the location of Sims, see :class:`.CommonSimLocationUtils`.
    To manipulate the location of Objects, see :class:`.CommonObjectLocationUtils`.

    """

    @staticmethod
    def get_lot_corners(lot: Lot) -> Tuple[Any]:
        """get_lot_corners(lot)

        Retrieve the lot corners of the specified Lot.

        :return: A collection of corners of the specified Lot.
        :rtype: Tuple[Any]
        """
        return tuple(lot.corners)

    @staticmethod
    def get_lot_corners_of_current_lot() -> Tuple[Any]:
        """get_lot_corners_of_current_lot()

        Retrieve the lot corners of the current Lot.

        :return: A collection of corners on the current Lot.
        :rtype: Tuple[Any]
        """
        return CommonLocationUtils.get_lot_corners(CommonLocationUtils.get_current_lot())

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
    def get_zone(zone_id: int, allow_unloaded_zones: bool=False) -> Zone:
        """get_zone(zone_id, allow_unloaded_zones=False)

        Retrieve the Zone matching an identifier.

        :param zone_id: The decimal identifier of a Zone.
        :type zone_id: int
        :param allow_unloaded_zones: If set to True, Zones that are currently not loaded (or have not been loaded) will be considered. If set to False, Zones that have yet to be loaded will not be considered. Default is False.
        :type allow_unloaded_zones: bool, optional
        :return: The Zone with the specified zone id or None if it was not found.
        :rtype: Zone
        """
        return services.get_zone(zone_id, allow_uninstantiated_zones=allow_unloaded_zones)

    @staticmethod
    def get_zone_lot(zone: Zone) -> Union[Lot, None]:
        """get_zone_lot(zone)

        Retrieve the lot of a Zone.

        :param zone: An instance of a Zone.
        :type zone: Zone
        :return: The Lot belonging to the specified Zone or None if a problem occurs.
        :rtype: Union[Lot, None]
        """
        if zone is None:
            return None
        return zone.lot

    @staticmethod
    def get_current_zone_plex_id() -> int:
        """get_current_zone_plex_id()

        Retrieve the plex id of the current zone.

        .. note:: A plex id is basically a Room location.

        :return: The decimal identifier of the current zone or 0 if the current zone does not have a plex id.
        :rtype: int
        """
        from services import get_plex_service
        return get_plex_service().get_active_zone_plex_id() or 0

    @staticmethod
    def get_plex_id_for_zone(zone: Zone) -> int:
        """get_plex_id_for_zone(zone)

        Retrieve the plex id for a Zone.

        :return: The Plex Id of the specified zone or -1 if it was not found.
        :rtype: int
        """
        zone_id = CommonLocationUtils.get_zone_id(zone)
        return CommonLocationUtils.get_plex_id(zone_id)

    @staticmethod
    def get_plex_id(zone_id: int) -> int:
        """get_plex_id(zone_id)

        Retrieve the plex id of a Zone.

        :return: The Plex Id of the specified zone or -1 if it was not found.
        :rtype: int
        """
        plex_service = services.get_plex_service()
        if zone_id not in plex_service._zone_to_master_map:
            return 0
        (_, plex_id) = plex_service._zone_to_master_map[zone_id]
        return plex_id

    @staticmethod
    def get_all_block_ids(zone_id: int) -> Tuple[int]:
        """get_all_block_ids(zone_id)

        Retrieve a collection of all Block Identifiers for a Zone.

        :param zone_id: The decimal identifier of the Zone to retrieve the block ids of.
        :type zone_id: int
        :return: A collection of block identifiers.
        :rtype: Tuple[int]
        """
        plex_id = CommonLocationUtils.get_plex_id(zone_id)
        if plex_id == -1:
            return tuple()
        # noinspection PyArgumentList
        return tuple(_buildbuy.get_all_block_polygons(zone_id, plex_id).keys())

    @staticmethod
    def get_block_id_in_current_zone(position: CommonVector3, surface_level: int) -> int:
        """get_block_id_in_current_zone(position, level)

        Retrieve the decimal identifier of the block containing the position.

        :param position: An instance of a vector.
        :type position: CommonVector3
        :param surface_level: The surface level of the position.
        :type surface_level: int
        :return: A decimal identifier of the block containing the position.
        :rtype: int
        """
        return CommonLocationUtils.get_block_id(CommonLocationUtils.get_current_zone_id(), position, surface_level)

    @staticmethod
    def get_all_block_ids_in_current_zone() -> Tuple[int]:
        """get_all_block_ids_in_current_zone()

        Retrieve a collection of all Block Identifiers for the current zone.

        .. note:: A Block Id is essentially an identifier for a Room.

        :return: A collection of block decimal identifiers.
        :rtype: Tuple[int]
        """
        return tuple(CommonLocationUtils.get_all_block_polygons_of_current_zone().keys())

    @staticmethod
    def get_all_block_polygons_of_current_zone() -> Dict[int, Tuple[Tuple[List[CommonVector3]]]]:
        """get_all_block_polygons_of_current_zone()

        Retrieve all block polygons for the current Zone.

        :return: A dictionary of polygons for the current Zone with the Block Ids as the key.
        :rtype: Dict[int, Tuple[Tuple[Polygon]]]
        """
        # noinspection PyArgumentList
        return _buildbuy.get_all_block_polygons(CommonLocationUtils.get_current_zone_id(), CommonLocationUtils.get_current_zone_plex_id())

    @staticmethod
    def get_all_block_polygons(zone_id: int) -> Dict[int, Tuple[Tuple[List[CommonVector3]]]]:
        """get_all_block_polygons(zone_id)

        Retrieve all block polygons for a Zone.

        .. note:: A Block is essentially just a Room.

        :param zone_id: A decimal identifier of a Zone.
        :type zone_id: int
        :return: A collection of polygons for the specified Zone.
        :rtype: Dict[int, Tuple[Tuple[List[CommonVector3]]]]
        """
        plex_id = CommonLocationUtils.get_plex_id(zone_id)
        if plex_id == -1:
            return dict()
        # noinspection PyArgumentList
        return _buildbuy.get_all_block_polygons(zone_id, plex_id)

    @staticmethod
    def get_block_id(zone_id: int, position: CommonVector3, surface_level: int) -> int:
        """get_block_id(zone_id, position, surface_level)

        Retrieve the decimal identifier of the block containing the position.

        :param zone_id: The decimal identifier of a Zone.
        :type zone_id: int
        :param position: An instance of a vector.
        :type position: CommonVector3
        :param surface_level: The surface level of the position.
        :type surface_level: int
        :return: A decimal identifier of the block containing the position.
        :rtype: int
        """
        return build_buy.get_block_id(zone_id, position, surface_level)

    @staticmethod
    def get_lot_id(lot: Lot) -> int:
        """get_lot_id(lot)

        Retrieve the decimal identifier of a Lot.

        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: The decimal identifier of the specified lot or -1 if a problem occurs.
        :rtype: int
        """
        if lot is None:
            return -1
        return lot.lot_id

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
    def get_current_lot() -> Lot:
        """get_current_lot()

        Retrieve the current lot.

        :return: The current Lot.
        :rtype: Lot
        """
        return services.active_lot()

    @staticmethod
    def get_current_lot_id() -> int:
        """get_current_lot_id()

        Retrieve the decimal identifier of the current Lot.

        :return: The decimal identifier of the current Lot or -1 if a problem occurs.
        :rtype: int
        """
        return services.active_lot_id() or -1

    @staticmethod
    def is_location_outside_current_lot(location: CommonLocation) -> bool:
        """is_location_outside_current_lot(location)

        Determine if a location is outside of the current lot or not.

        :param location: The Location to check.
        :type location: CommonLocation
        :return: True, if the location is outside of the current lot. False, if not.
        :rtype: bool
        """
        return CommonLocationUtils.is_location_outside_lot(location, CommonLocationUtils.get_current_zone_id())

    @staticmethod
    def is_location_outside_lot(location: CommonLocation, zone_id: int) -> bool:
        """is_location_outside_lot(location, lot_id)

        Determine if a location is outside of the Lot with the specified identifier.

        :param location: The Location to check.
        :type location: CommonLocation
        :param zone_id: The identifier of a Zone to check for the Location to be outside of.
        :type zone_id: int
        :return: True, if location is outside of the Lot with the specified lot_id. False, if not.
        :rtype: bool
        """
        try:
            # noinspection PyTypeChecker,PyArgumentList
            return _buildbuy.is_location_outside(zone_id, location.transform.translation, location.routing_surface.secondary_id)
        except RuntimeError:
            return False

    @staticmethod
    def is_position_on_current_lot(position: CommonVector3) -> bool:
        """is_position_on_current_lot(position)

        Determine if a sim is on the current lot.

        :param position: The position to check.
        :type position: CommonVector3
        :return: True, if the specified position is within the bounds of the current lot. False, if not.
        :rtype: bool
        """
        return position is not None and services.active_lot().is_position_on_lot(position)

    @staticmethod
    def get_lot_traits(zone_id: int) -> Tuple[ZoneModifier]:
        """get_lot_traits(lot_id)

        Retrieve the Lot Traits of a Lot with the specified identifier.

        :param zone_id: The lot to retrieve the traits of.
        :type zone_id: int
        :return: A collection of Lot Traits for the specified lot.
        :rtype: Tuple[ZoneModifier]
        """
        return tuple(services.get_zone_modifier_service().get_zone_modifiers(zone_id))

    @staticmethod
    def get_lot_traits_of_current_lot() -> Tuple[ZoneModifier]:
        """get_lot_traits_of_current_lot()

        Retrieve the Lot Traits of the Current Lot.

        :return: A collection of Lot Traits for the current lot.
        :rtype: Tuple[ZoneModifier]
        """
        return CommonLocationUtils.get_lot_traits(CommonLocationUtils.get_current_zone_id())

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
        return build_buy.get_current_venue(CommonLocationUtils.get_current_zone_id())

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

    @staticmethod
    def is_position_on_lot(position: CommonVector3, lot: Lot) -> bool:
        """is_position_on_lot(position, lot)

        Determine if a Position is located on a Lot.

        :param position: An instance of a CommonVector
        :type position: CommonVector3
        :param lot: An instance of a Lot.
        :type lot: Lot
        :return: True, if the Sim is on the specified Lot. False, if not.
        :rtype: bool
        """
        return position is not None and lot.is_position_on_lot(position)

    @staticmethod
    def can_location_be_routed_to(location: CommonLocation) -> bool:
        """can_location_be_routed_to(location)

        Determine if a location can be routed to by a Sim.

        :param location: The location to check.
        :type location: CommonLocation
        :return: True, if the location can be routed to by a Sim. False, it not.
        :rtype: bool
        """
        return CommonLocationUtils.can_position_be_routed_to(location.transform.translation, location.routing_surface)

    @staticmethod
    def can_position_be_routed_to(position: CommonVector3, surface_identifier: CommonSurfaceIdentifier) -> bool:
        """can_position_be_routed_to(position, surface_identifier)

        Determine if a position and surface can be routed to by a Sim.

        :param position: The position to check.
        :type position: CommonVector3
        :param surface_identifier: The surface to check.
        :type surface_identifier: CommonSurfaceIdentifier
        :return: True, if the position can be routed to by a Sim. False, it not.
        :rtype: bool
        """
        from routing import test_point_placement_in_navmesh
        return test_point_placement_in_navmesh(surface_identifier, position)

    @staticmethod
    def get_surface_height_at(x: float, z: float, routing_surface: CommonSurfaceIdentifier) -> float:
        """get_surface_height_at(x, z, routing_surface)

        Calculate the height of a surface.

        :param x: The x position of the surface.
        :type x: float
        :param z: The z position of the surface.
        :type z: float
        :param routing_surface: The surface.
        :type routing_surface: CommonSurfaceIdentifier
        :return: The height of the surface.
        :rtype: float
        """
        # noinspection PyUnresolvedReferences
        return services.terrain_service.terrain_object().get_routing_surface_height_at(x, z, routing_surface)

    @staticmethod
    def get_current_zone_world_id() -> int:
        """get_current_zone_world_id()

        Retrieve the world id of the current Zone.

        :return: The world id of the current Zone.
        :rtype: int
        """
        return CommonLocationUtils.get_zone_world_id(CommonLocationUtils.get_current_zone_id())

    @staticmethod
    def get_current_zone_world_description_id() -> int:
        """get_current_zone_world_description_id()

        Retrieve the world description id of the current Zone.

        :return: The world description id of the current Zone.
        :rtype: int
        """
        return CommonLocationUtils.get_zone_world_description_id(CommonLocationUtils.get_current_zone_id())

    @staticmethod
    def get_zone_world_id(zone_id: int) -> int:
        """get_zone_world_id(zone_id)

        Retrieve the world id of the a Zone.

        :param zone_id: The decimal identifier of a Zone.
        :type zone_id: int
        :return: The world id of the specified Zone.
        :rtype: int
        """
        return services.get_persistence_service().get_world_id_from_zone(zone_id)

    @staticmethod
    def get_zone_world_description_id(zone_id: int) -> int:
        """get_zone_world_description_id(zone_id)

        Retrieve the world description id of the a Zone.

        :param zone_id: The decimal identifier of a Zone.
        :type zone_id: int
        :return: The world description id of the the specified Zone.
        :rtype: int
        """
        return services.get_world_description_id(CommonLocationUtils.get_zone_world_id(zone_id))
