"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from routing import SurfaceType, SurfaceIdentifier


class CommonSurfaceIdentifier:
    """ A class that contains surface data. """

    def __init__(self, primary_id: int, secondary_id: int=None, surface_type: SurfaceType=SurfaceType.SURFACETYPE_WORLD):
        self._primary_id = primary_id
        self._secondary_id = secondary_id
        self._surface_type = surface_type

    @property
    def primary_id(self) -> int:
        """ The primary identifier for the surface. This value is usually the identifier of a Zone.

        :return: The primary identifier.
        :rtype: int
        """
        return self._primary_id

    @primary_id.setter
    def primary_id(self, value: int):
        self._primary_id = value

    @property
    def secondary_id(self) -> Union[int, None]:
        """ The secondary identifier for the surface. This value is usually the level at which the surface is.

        :return: The secondary identifier.
        :rtype: Union[int, None]
        """
        return self._secondary_id

    @secondary_id.setter
    def secondary_id(self, value: Union[int, None]):
        self._secondary_id = value

    @property
    def type(self) -> Union[SurfaceType, None]:
        """ The type of surface.

        :return: The type of surface.
        :rtype: Union[SurfaceType, None]
        """
        return self._surface_type

    @type.setter
    def type(self, value: Union[SurfaceType, None]):
        self._surface_type = value

    def __new__(cls, primary_id: int, secondary_id: int=None, surface_type: SurfaceType=SurfaceType.SURFACETYPE_WORLD) -> 'CommonSurfaceIdentifier':
        # noinspection PyTypeChecker
        return SurfaceIdentifier(primary_id, secondary_id, surface_type)

    @staticmethod
    def empty(secondary_id: int=0) -> 'CommonSurfaceIdentifier':
        """empty(secondary_id=0)

        Create an empty surface identifier for the current zone.

        :param secondary_id: The secondary id to give to the surface identifier. Default is 0.
        :type secondary_id: int, optional
        :return: An empty surface identifier.
        :rtype: CommonSurfaceIdentifier
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        return CommonSurfaceIdentifier(CommonLocationUtils.get_current_zone_id(), secondary_id=secondary_id)

    @staticmethod
    def from_surface_identifier(surface_identifier: Union[SurfaceIdentifier, 'CommonSurfaceIdentifier']) -> Union['CommonSurfaceIdentifier', None]:
        """from_surface_identifier(surface_identifier)

        Convert a SurfaceIdentifier into a CommonSurfaceIdentifier.

        :param surface_identifier: An instance of a surface identifier.
        :type surface_identifier: Union[SurfaceIdentifier, CommonSurfaceIdentifier]
        :return: An instance of a CommonSurfaceIdentifier or None if it failed to convert.
        :rtype: Union[CommonSurfaceIdentifier, None]
        """
        if surface_identifier is None:
            return None
        if isinstance(surface_identifier, CommonSurfaceIdentifier):
            return surface_identifier
        if not isinstance(surface_identifier, SurfaceIdentifier):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(surface_identifier, type(surface_identifier), type(SurfaceIdentifier)))
        return CommonSurfaceIdentifier(surface_identifier.primary_id, secondary_id=surface_identifier.secondary_id, surface_type=surface_identifier.type)
