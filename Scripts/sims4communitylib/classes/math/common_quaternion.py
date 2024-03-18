"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, TYPE_CHECKING, Dict, Type
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

    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if z is None:
            z = 0.0
        if w is None:
            w = 1.0
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

    def __new__(cls, x: float, y: float, z: float, w: float) -> 'CommonQuaternion':
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if z is None:
            z = 0.0
        if w is None:
            w = 1.0
        # noinspection PyTypeChecker
        return Quaternion(x, y, z, w)

    @staticmethod
    def empty() -> 'CommonQuaternion':
        """empty()

        Deprecated, use "identity" instead.

        Create an empty quaternion.

        :return: An empty quaternion.
        :rtype: CommonQuaternion
        """
        return CommonQuaternion.identity()

    @staticmethod
    def identity() -> 'CommonQuaternion':
        """identity()

        Create an identity quaternion.

        :return: An identity quaternion.
        :rtype: CommonQuaternion
        """
        return CommonQuaternion(0.0, 0.0, 0.0, 1.0)

    @staticmethod
    def is_empty(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> bool:
        """is_empty(quaternion)

        Determine if a quaternion is empty or not.

        :param quaternion: The quaternion to check.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: True, if the quaternion is empty. False, if not.
        :rtype: bool
        """
        quaternion_identity = CommonQuaternion.empty()
        return quaternion.x == quaternion_identity.x and quaternion.y == quaternion_identity.y and quaternion.z == quaternion_identity.z and quaternion.w == quaternion_identity.w

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

    def __add__(self, other: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion', float]) -> 'CommonQuaternion':
        # The functionality lies inside Quaternion
        pass

    def __sub__(self, other: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion', float]) -> 'CommonQuaternion':
        # The functionality lies inside Quaternion
        pass

    @staticmethod
    def rotate_vector(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion'], vector: 'CommonVector3') -> Any:
        """rotate_vector(quaternion, vector)

        Rotate a vector with a quaternion.

        :param quaternion: The quaternion to use for rotation.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :param vector: The vector to rotate.
        :type vector: CommonVector3
        :return: A normalized Quaternion.
        :rtype: CommonQuaternion
        """
        from sims4communitylib.classes.math.common_vector3 import CommonVector3
        q = CommonQuaternion.multiply(CommonQuaternion.multiply(quaternion, CommonQuaternion(vector.x, vector.y, vector.z, 0.0)), CommonQuaternion.conjugate(quaternion))  # q.w will be zero.
        return CommonVector3(q.x, q.y, q.z)

    @staticmethod
    def normalize(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion'], tolerance: float = 0.00001) -> 'CommonQuaternion':
        """normalize(quaternion, tolerance=0.00001)

        Normalize a quaternion.

        :param quaternion: The quaternion to normalize.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :param tolerance: The tolerance level for normalization. Default is 0.00001.
        :type tolerance: float, optional
        :return: A normalized Quaternion.
        :rtype: CommonQuaternion
        """
        import math
        mag2 = (quaternion.x * quaternion.x) + (quaternion.y * quaternion.y) + (quaternion.z * quaternion.z) + (quaternion.w * quaternion.w)
        if mag2 == 0:
            return quaternion
        mag3 = abs(1 - mag2)
        if mag3 > tolerance:
            mag = math.sqrt(mag2)
            new_x = (quaternion.x / mag)
            new_y = (quaternion.y / mag)
            new_z = (quaternion.z / mag)
            new_w = (quaternion.w / mag)
            return CommonQuaternion(new_x, new_y, new_z, new_w)
        return quaternion

    @staticmethod
    def conjugate(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> 'CommonQuaternion':
        """conjugate(quaternion)

        Conjugate a quaternion.

        :param quaternion: The quaternion to conjugate.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: A conjugated Quaternion.
        :rtype: CommonQuaternion
        """
        return CommonQuaternion(-quaternion.x, -quaternion.y, -quaternion.z, quaternion.w)

    @staticmethod
    def __truediv__(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion'], quaternion_other: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> 'CommonQuaternion':
        return CommonQuaternion.normalize(CommonQuaternion.divide(quaternion, quaternion_other))

    @staticmethod
    def __mul__(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion'], quaternion_other: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> 'CommonQuaternion':
        return CommonQuaternion.normalize(CommonQuaternion.multiply(quaternion, quaternion_other))

    @staticmethod
    def divide(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion'], quaternion_other: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']):
        """divide(quaternion, quaternion_other)

        Divides two quaternions without normalizing the result. Use `q = q1 / q2` for a normalized result.

        :param quaternion: The quaternion to be divided.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :param quaternion_other: The quaternion to divide with.
        :type quaternion_other: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: A divided Quaternion.
        :rtype: CommonQuaternion
        """
        return CommonQuaternion.multiply(quaternion, CommonQuaternion.conjugate(quaternion_other))

    @staticmethod
    def multiply(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion'], quaternion_other: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> 'CommonQuaternion':
        """multiply(quaternion, quaternion_other)

        Multiplies two quaternions without normalizing the result.  Use `q = q1 * q2` for a normalized result.

        :param quaternion: The quaternion to be multiplied.
        :type quaternion: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :param quaternion_other: The quaternion to multiply with.
        :type quaternion_other: Union[Quaternion, MathPb2Quaternion, CommonQuaternion]
        :return: A divided Quaternion.
        :rtype: CommonQuaternion
        """
        x = (quaternion.w * quaternion_other.x) + (quaternion.x * quaternion_other.w) + (quaternion.y * quaternion_other.z) - (quaternion.z * quaternion_other.y)
        y = (quaternion.w * quaternion_other.y) - (quaternion.x * quaternion_other.z) + (quaternion.y * quaternion_other.w) + (quaternion.z * quaternion_other.x)
        z = (quaternion.w * quaternion_other.z) + (quaternion.x * quaternion_other.y) - (quaternion.y * quaternion_other.x) + (quaternion.z * quaternion_other.w)
        w = (quaternion.w * quaternion_other.w) - (quaternion.x * quaternion_other.x) - (quaternion.y * quaternion_other.y) - (quaternion.z * quaternion_other.z)
        return CommonQuaternion(x, y, z, w)

    # noinspection PyMissingOrEmptyDocstring
    @staticmethod
    def serialize(quaternion: Union[Quaternion, MathPb2Quaternion, 'CommonQuaternion']) -> Union[str, Dict[str, Any]]:
        data = dict()
        data['x'] = quaternion.x
        data['y'] = quaternion.y
        data['z'] = quaternion.z
        data['w'] = quaternion.w
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls: Type['CommonQuaternion'], data: Union[str, Dict[str, Any]]) -> Union['CommonQuaternion', None]:
        x = data.get('x', 0.0)
        y = data.get('y', 0.0)
        z = data.get('z', 0.0)
        w = data.get('w', 1.0)
        return CommonQuaternion(x, y, z, w)
