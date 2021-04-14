"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, List, Union

from interactions.constraints import Constraint
from sims4.geometry import Polygon
from sims4communitylib.classes.math.common_vector3 import CommonVector3


class CommonPolygon:
    """ A class that contains polygonal data. """

    def __init__(self, polygon_vertices: Tuple[CommonVector3]):
        self._polygon_vertices = polygon_vertices

    def __new__(cls, corners: Tuple[CommonVector3]) -> 'CommonPolygon':
        return Polygon(corners)

    def __iter__(self) -> Iterator[CommonVector3]:
        pass

    def __len__(self) -> int:
        pass

    def __getitem__(self, item: int) -> CommonVector3:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def normalize(self) -> None:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def centroid(self) -> 'CommonVector3':
        pass

    # noinspection PyMissingOrEmptyDocstring
    def radius(self) -> float:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def area(self) -> float:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def bounds(self) -> Tuple[CommonVector3, CommonVector3]:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def contains(self, point: CommonVector3) -> bool:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def intersect(self, polygon: 'CommonPolygon') -> Constraint:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def union(self, polygon: 'CommonPolygon') -> Constraint:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def subtract(self, polygon: 'CommonPolygon') -> List[CommonVector3]:
        pass

    # noinspection PyMissingOrEmptyDocstring
    def get_convex_hull(self) -> 'CommonPolygon':
        pass

    @staticmethod
    def empty() -> 'CommonPolygon':
        """empty()

        Create an empty Polygon.

        :return: An empty Polygon.
        :rtype: CommonPolygon
        """
        return CommonPolygon(tuple())

    @staticmethod
    def from_polygon(polygon: Union[Polygon, 'CommonPolygon']) -> Union['CommonPolygon', None]:
        """from_polygon(polygon)

        Convert a vanilla Polygon object into a CommonPolygon.

        :param polygon: An instance of a Polygon
        :type polygon: Union[Polygon, CommonPolygon]
        :return: An instance of a CommonPolygon or None if the object failed to convert.
        :rtype: Union[CommonLocation, None]
        """
        if polygon is None:
            return None
        if isinstance(polygon, CommonPolygon):
            return polygon
        if not isinstance(polygon, Polygon):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(polygon, type(polygon), type(Polygon)))
        return CommonPolygon(tuple(polygon))
