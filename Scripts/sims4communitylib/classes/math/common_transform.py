"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any
from protocolbuffers.Math_pb2 import Transform as MathPb2Transform

from sims4communitylib.classes.math.common_quaternion import CommonQuaternion
from sims4communitylib.classes.math.common_vector3 import CommonVector3

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from sims4.math import Transform
except:
    # noinspection PyMissingOrEmptyDocstring
    class Transform:
        # noinspection PyUnusedLocal
        def __init__(self, translation: Any, orientation: Any):
            pass

        # noinspection PyPropertyDefinition
        @property
        def translation(self) -> Any:
            pass

        # noinspection PyPropertyDefinition
        @property
        def orientation(self) -> Any:
            pass


class CommonTransform:
    """ A class that contains transformational data. """

    def __init__(self, translation: CommonVector3, orientation: CommonQuaternion):
        self._translation = translation
        self._orientation = orientation

    @property
    def translation(self) -> CommonVector3:
        """ The translation.

        :return: The translation.
        :rtype: CommonVector3
        """
        return self._translation

    @translation.setter
    def translation(self, value: CommonVector3):
        self._translation = value

    @property
    def orientation(self) -> CommonQuaternion:
        """ The orientation.

        :return: The orientation.
        :rtype: CommonQuaternion
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value: CommonQuaternion):
        self._orientation = value

    def __new__(cls, translation: CommonVector3, orientation: CommonQuaternion) -> 'CommonTransform':
        # noinspection PyTypeChecker
        return Transform(translation, orientation)

    @staticmethod
    def empty() -> 'CommonTransform':
        """empty()

        Create an empty transform.

        :return: An empty transform.
        :rtype: CommonTransform
        """
        return CommonTransform(CommonVector3.empty(), CommonQuaternion.empty())

    @staticmethod
    def from_transform(transform: Union[Transform, MathPb2Transform, 'CommonTransform']) -> Union['CommonTransform', None]:
        """from_transform(transform)

        Convert a Transform into a CommonTransform.

        :param transform: An instance of a transform.
        :type transform: Union[Transform, MathPb2Transform, CommonTransform]
        :return: An instance of a CommonTransform or None if it failed to convert.
        :rtype: Union[CommonTransform, None]
        """
        if transform is None:
            return None
        if isinstance(transform, CommonTransform):
            return transform
        if not isinstance(transform, Transform) and not isinstance(transform, MathPb2Transform):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(transform, type(transform), type(Transform)))
        # noinspection PyUnresolvedReferences
        return CommonTransform(CommonVector3.from_vector3(transform.translation), CommonQuaternion.from_quaternion(transform.orientation))
