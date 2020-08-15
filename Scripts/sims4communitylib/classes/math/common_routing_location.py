"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, TYPE_CHECKING
from sims4.math import Location as Math_Location
from routing import Location
from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3

if TYPE_CHECKING:
    from sims4communitylib.classes.math.common_location import CommonLocation


class CommonRoutingLocation:
    """CommonRoutingLocation(position, orientation=None, routing_surface=None)

    A Location used for routing.

    :param position: The position of the location.
    :type position: CommonVector3
    :param orientation: The orientation of the location. Default is None.
    :type orientation: CommonQuaternion, optional
    :param routing_surface: The routing surface of the location. Default is None.
    :type routing_surface: CommonSurfaceIdentifier, optional
    """
    def __init__(self, position: CommonVector3, orientation: CommonQuaternion=None, routing_surface: CommonSurfaceIdentifier=None):
        super().__init__(position, orientation, routing_surface)
        self._position = position
        self._orientation = orientation
        self._routing_surface = routing_surface

    @property
    def position(self) -> CommonVector3:
        """The translation and orientation of the location.

        :return: The translation and orientation of the location.
        :rtype: CommonTransform
        """
        return self._position

    @property
    def orientation(self) -> CommonQuaternion:
        """The orientation of the location.

        :return: The orientation of the Location.
        :rtype: CommonQuaternion
        """
        return self._orientation

    @property
    def routing_surface(self) -> CommonSurfaceIdentifier:
        """The routing surface the location is located on.

        :return: The routing surface the location is located on.
        :rtype: CommonSurfaceIdentifier
        """
        return self._routing_surface

    def __new__(cls, position: CommonVector3, orientation: CommonQuaternion=None, routing_surface: CommonSurfaceIdentifier=None) -> 'CommonRoutingLocation':
        # noinspection PyTypeChecker
        return Location(position, orientation, routing_surface)

    @staticmethod
    def empty() -> 'CommonRoutingLocation':
        """empty()

        Create an empty location.

        :return: An empty location.
        :rtype: CommonRoutingLocation
        """
        return CommonRoutingLocation(CommonVector3.empty(), orientation=CommonQuaternion.empty(), routing_surface=CommonSurfaceIdentifier.empty())

    @staticmethod
    def from_location(location: Union[Location, Math_Location, 'CommonLocation', 'CommonRoutingLocation']) -> Union['CommonRoutingLocation', None]:
        """from_location(location)

        Convert a vanilla Location object into a CommonRoutingLocation.

        :param location: An instance of a Location.
        :type location: Union[routing.Location, sims4.math.Location, CommonLocation, CommonRoutingLocation]
        :return: An instance of a CommonRoutingLocation or None if the object failed to convert.
        :rtype: Union[CommonRoutingLocation, None]
        """
        from sims4communitylib.classes.math.common_location import CommonLocation
        if location is None:
            return None
        if isinstance(location, CommonRoutingLocation):
            return location
        if isinstance(location, Location):
            return CommonRoutingLocation(location.position, location.orientation, location.routing_surface)
        if not isinstance(location, Math_Location) and not isinstance(location, CommonLocation):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(location, type(location), type(Math_Location)))
        routing_surface = location.routing_surface if location.routing_surface is not None else CommonSurfaceIdentifier.empty()
        return CommonRoutingLocation(CommonVector3.from_vector3(location.transform.translation), orientation=CommonQuaternion.from_quaternion(location.transform.orientation), routing_surface=CommonSurfaceIdentifier.from_surface_identifier(routing_surface))

    def get_world_surface_location(self) -> 'CommonRoutingLocation':
        """get_world_surface_location(self)

        Retrieve the Location as a world surface location.

        :return: A world surface location.
        :rtype: CommonRoutingLocation
        """
        pass
