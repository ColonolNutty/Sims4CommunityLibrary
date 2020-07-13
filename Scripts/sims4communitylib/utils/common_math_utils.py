"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import math


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
