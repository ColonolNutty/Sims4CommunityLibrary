"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import math

from sims4communitylib.classes.math.common_vector3 import CommonVector3


class CommonMathUtils:
    """ Utilities for math operations. """

    @staticmethod
    def radian_to_degrees(radian: float) -> float:
        """radian_to_degrees(radian)

        Translate Radian to Degrees.

        :param radian: The value to convert.
        :type radian: float
        :return: The value as Degrees.
        :rtype: float
        """
        return radian * 180.0 / math.pi

    @staticmethod
    def degrees_to_radian(degrees: float) -> float:
        """degrees_to_radian(degrees)

        Translate Degrees to Radian.

        :param degrees: The value to convert.
        :type degrees: float
        :return: The value as Radian.
        :rtype: float
        """
        return degrees * math.pi / 180.0

    @staticmethod
    def calculate_distance(position_one: CommonVector3, position_two: CommonVector3, flatten_positions: bool=True) -> float:
        """calculate_distance(position_one, position_two, flatten_positions=True)

        Calculate the distance between two vectors.

        :param position_one: An instance of a Vector.
        :type position_one: CommonVector3
        :param position_two: An instance of a Vector.
        :type position_two: CommonVector3
        :param flatten_positions: If True, both Vectors will be flattened before calculations will occur. Default is True.
        :type flatten_positions: bool, optional
        :return: The distance between the two specified vectors.
        :rtype: float
        """
        if flatten_positions:
            position_one = CommonVector3.flatten(position_one)
            position_two = CommonVector3.flatten(position_one)
        return CommonVector3.distance_between(position_one, position_two)
