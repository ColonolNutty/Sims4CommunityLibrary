"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, TYPE_CHECKING
from protocolbuffers.Math_pb2 import Quaternion as MathPb2Quaternion
if TYPE_CHECKING:
    from sims4communitylib.classes.math.common_vector3 import CommonVector3

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from sims4.math import Quaternion, QuaternionImmutable
except:
    # noinspection PyMissingOrEmptyDocstring
    class QuaternionImmutable:
        # noinspection PyUnusedLocal
        def __init__(self, x: float, y: float, z: float, w: float):
            pass

        # noinspection PyPropertyDefinition
        @property
        def x(self) -> float:
            pass

        # noinspection PyPropertyDefinition
        @property
        def y(self) -> float:
            pass

        # noinspection PyPropertyDefinition
        @property
        def z(self) -> float:
            pass

        # noinspection PyPropertyDefinition
        @property
        def w(self) -> float:
            pass

        # noinspection PyMissingOrEmptyDocstring
        def transform_vector(self, vector: 'CommonVector3') -> 'CommonVector3':
            pass

    # noinspection PyMissingOrEmptyDocstring
    class Quaternion:
        # noinspection PyUnusedLocal
        def __init__(self, x: float, y: float, z: float, w: float):
            pass

        # noinspection PyPropertyDefinition
        @property
        def x(self) -> float:
            pass

        @x.setter
        def x(self, value: float):
            pass

        # noinspection PyPropertyDefinition
        @property
        def y(self) -> float:
            pass

        @y.setter
        def y(self, value: float):
            pass

        # noinspection PyPropertyDefinition
        @property
        def z(self) -> float:
            pass

        @z.setter
        def z(self, value: float):
            pass

        # noinspection PyPropertyDefinition
        @property
        def w(self) -> float:
            pass

        @w.setter
        def w(self, value: float):
            pass

        # noinspection PyMissingOrEmptyDocstring
        def transform_vector(self, vector: 'CommonVector3') -> 'CommonVector3':
            pass


class CommonQuaternion:
    """ A class that contains orientation data. """
    def __init__(self, x: float, y: float, z: float, w: Any) -> None:
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if z is None:
            z = 0.0
        if w is None:
            w = 0.0
        self._x = x
        self._y = y
        self._z = z
        self._w = w

    @property
    def x(self) -> float:
        """ The x position.

        :return: The x position.
        :rtype: float
        """
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value

    @property
    def y(self) -> float:
        """ The y position.

        :return: The y position.
        :rtype: float
        """
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value

    @property
    def z(self) -> float:
        """ The z position.

        :return: The z position.
        :rtype: float
        """
        return self._z

    @property
    def w(self) -> Any:
        """ The rotation.

        :return: The rotation.
        :rtype: Any
        """
        return self._w

    @w.setter
    def w(self, value: float):
        self._w = value

    def __new__(cls, x: float, y: float, z: float, w: Any) -> 'CommonQuaternion':
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if z is None:
            z = 0.0
        if w is None:
            w = 0.0
        # noinspection PyTypeChecker
        return Quaternion(x, y, z, w)

    @staticmethod
    def empty() -> 'CommonQuaternion':
        """empty()

        Create an empty quaternion.

        :return: An empty quaternion.
        :rtype: CommonQuaternion
        """
        return CommonQuaternion(0.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_quaternion(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> Union['CommonQuaternion', None]:
        """from_quaternion(quaternion)

        Convert a Quaternion into a CommonQuaternion.

        :param quaternion: An instance of a Quaternion.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: An instance of a CommonQuaternion or None if the object failed to convert.
        :rtype: Union[CommonQuaternion, None]
        """
        if quaternion is None:
            return None
        if isinstance(quaternion, CommonQuaternion):
            return quaternion
        if not isinstance(quaternion, Quaternion) and not isinstance(quaternion, QuaternionImmutable):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(quaternion, type(quaternion), type(Quaternion)))
        # noinspection PyUnresolvedReferences
        return CommonQuaternion(quaternion.x, quaternion.y, quaternion.z, quaternion.w)

    @staticmethod
    def from_radian(radian: float) -> 'CommonQuaternion':
        """from_radian(radian)

        Convert a radian value into a CommonQuaternion.

        :param radian: An angle in radians
        :type radian: float
        :return: An instance of a CommonQuaternion.
        :rtype: CommonQuaternion
        """
        from sims4.math import angle_to_yaw_quaternion
        return CommonQuaternion.from_quaternion(angle_to_yaw_quaternion(radian))

    @staticmethod
    def from_degrees(degrees: float) -> 'CommonQuaternion':
        """from_degrees(degrees)

        Convert an angle in degrees into a CommonQuaternion.

        :param degrees: An angle in degrees
        :type degrees: float
        :return: An instance of a CommonQuaternion.
        :rtype: CommonQuaternion
        """
        from sims4communitylib.utils.common_math_utils import CommonMathUtils
        return CommonQuaternion.from_radian(CommonMathUtils.degrees_to_radian(degrees))

    @staticmethod
    def to_radian(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> float:
        """to_radian(quaternion)

        Convert a Quaternion into radians.

        :param quaternion: An instance of a Quaternion.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: The quaternion represented in radians.
        :rtype: float
        """
        if quaternion is None:
            return 0.0
        from sims4.math import yaw_quaternion_to_angle
        return yaw_quaternion_to_angle(quaternion)

    @staticmethod
    def to_degrees(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> float:
        """to_degrees(quaternion)

        Convert a Quaternion into degrees.

        :param quaternion: An instance of a Quaternion.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: The quaternion represented in degrees.
        :rtype: float
        """
        if quaternion is None:
            return 0.0
        from sims4communitylib.utils.common_math_utils import CommonMathUtils
        return CommonMathUtils.radian_to_degrees(CommonQuaternion.to_radian(quaternion))

    # noinspection PyMissingOrEmptyDocstring
    def transform_vector(self, vector: 'CommonVector3') -> 'CommonVector3':
        pass
