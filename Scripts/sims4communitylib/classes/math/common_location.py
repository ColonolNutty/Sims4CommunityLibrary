"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union
from sims4.math import Location
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_transform import CommonTransform


class CommonLocation:
    """ A class that contains locational data. """

    def __init__(self, transform: CommonTransform, routing_surface: CommonSurfaceIdentifier, parent_ref: Any=None, joint_name_or_hash: Any=None, slot_hash: int=0):
        self._transform = transform
        self._routing_surface = routing_surface
        self._parent_ref = parent_ref
        self._joint_name_or_hash = joint_name_or_hash
        self._slot_hash = slot_hash

    @property
    def transform(self) -> CommonTransform:
        """ The translation and orientation of the location.

        :return: The translation and orientation of the location.
        :rtype: CommonTransform
        """
        return self._transform

    @property
    def routing_surface(self) -> CommonSurfaceIdentifier:
        """ The routing surface the location is located on.

        :return: The routing surface the location is located on.
        :rtype: CommonSurfaceIdentifier
        """
        return self._routing_surface

    @property
    def parent_ref(self) -> Any:
        """ The parent reference of the location.

        :return: The parent reference of the location.
        :rtype: Any
        """
        return self._parent_ref

    @property
    def joint_name_or_hash(self) -> Union[str, int]:
        """ The name or hash identifier of the joint the location is located at.

        :return: The name or hash identifier of the joint the location is located at.
        :rtype: Union[str, int]
        """
        return self._joint_name_or_hash

    @property
    def slot_hash(self) -> int:
        """ The hash identifier of the Slot the location is located at.

        :return: The hash identifier of the Slot the location is located at.
        :rtype: int
        """
        return self._slot_hash

    def __new__(cls, transform: CommonTransform, routing_surface: CommonSurfaceIdentifier, parent_ref: Any=None, joint_name_or_hash: Any=None, slot_hash: int=0) -> 'CommonLocation':
        # noinspection PyTypeChecker, PyArgumentList
        return Location(transform, routing_surface, parent_ref, joint_name_or_hash, slot_hash)

    @staticmethod
    def empty() -> 'CommonLocation':
        """empty()

        Create an empty location.

        :return: An empty location.
        :rtype: CommonLocation
        """
        return CommonLocation(CommonTransform.empty(), CommonSurfaceIdentifier.empty())

    @staticmethod
    def from_location(location: Union[Location, 'CommonLocation']) -> Union['CommonLocation', None]:
        """from_location(location)

        Convert a vanilla Location object into a CommonLocation.

        :param location: An instance of a Location.
        :type location: Union[Location, CommonLocation]
        :return: An instance of a CommonLocation or None if the object failed to convert.
        :rtype: Union[CommonLocation, None]
        """
        if location is None:
            return None
        if isinstance(location, CommonLocation):
            return location
        if not isinstance(location, Location):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(location, type(location), type(Location)))
        routing_surface = location.routing_surface if location.routing_surface is not None else CommonSurfaceIdentifier.empty(
            secondary_id=location.level)
        parent_ref = None
        if location.parent_ref is not None and hasattr(location.parent_ref, 'provided_routing_surface'):
            parent_ref = location.parent_ref
        return CommonLocation(
            CommonTransform.from_transform(location.transform),
            CommonSurfaceIdentifier.from_surface_identifier(routing_surface),
            parent_ref=parent_ref,
            joint_name_or_hash=location.joint_name_or_hash,
            slot_hash=location.slot_hash
        )
