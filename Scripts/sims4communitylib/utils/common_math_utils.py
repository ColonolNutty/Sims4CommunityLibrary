"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import math
import sims4.math as sims_math

from sims4communitylib.classes.math.common_vector3 import CommonVector3


class CommonMathUtils:
    """ Utilities for math operations. """

    @staticmethod
    def calculate_degrees_between_positions(position_one: CommonVector3, position_two: CommonVector3) -> float:
        """calculate_degrees_between_positions(position_one, position_two)

        Calculate the degrees between two positions.

        :param position_one: An instance of a Vector.
        :type position_one: CommonVector3
        :param position_two: An instance of a Vector.
        :type position_two: CommonVector3
        :return: The degrees between the specified Vectors.
        :rtype: float
        """
        return CommonMathUtils.radian_to_degrees(math.atan2(position_two.x - position_one.x, position_two.z - position_one.z))

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

    @staticmethod
    def calculate_offset_from_degrees(position: CommonVector3, degrees: float, length: float) -> CommonVector3:
        """calculate_offset_from_degrees(position, degrees, length)

        Calculate an offset vector based on the forward axis from a vector.

        :param position: The original position.
        :type position: CommonVector3
        :param degrees: Amount of degrees to offset.
        :type degrees: float
        :param length: The length of the offset.
        :type length: float
        :return: The vector offset.
        :rtype: CommonVector3
        """
        offset_vector = sims_math.FORWARD_AXIS
        # noinspection PyUnresolvedReferences
        offset_vector = CommonQuaternion.from_degrees(degrees).transform_vector(offset_vector)
        offset_vector = sims_math.vector_normalize(offset_vector) * length
        return position + offset_vector
