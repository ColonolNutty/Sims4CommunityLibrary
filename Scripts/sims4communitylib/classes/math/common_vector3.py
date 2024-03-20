"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Type, Dict, Any
from protocolbuffers.Math_pb2 import Vector3 as MathPb2Vector3

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from sims4.math import Vector3, Vector3Immutable
except:
    # noinspection PyMissingOrEmptyDocstring
    class Vector3Immutable:
        # noinspection PyUnusedLocal
        def __init__(self, x: float, y: float, z: float):
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

    # noinspection PyMissingOrEmptyDocstring
    class Vector3:
        # noinspection PyUnusedLocal
        def __init__(self, x: float, y: float, z: float):
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


class CommonVector3:
    """ A class that contains positional data with three coordinates. """
    def __init__(self, x: float, y: float, z: float):
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if z is None:
            z = 0.0
        self._x = x
        self._y = y
        self._z = z

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

    @z.setter
    def z(self, value: float):
        self._z = value

    def __new__(cls, x: float, y: float, z: float) -> 'CommonVector3':
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if z is None:
            z = 0.0
        # noinspection PyTypeChecker
        return Vector3(x, y, z)

    @staticmethod
    def empty() -> 'CommonVector3':
        """empty()

        Create an empty vector.

        :return: An empty vector.
        :rtype: CommonVector3
        """
        return CommonVector3(0.0, 0.0, 0.0)

    @staticmethod
    def is_empty(vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        """is_empty(vector)

        Determine if a vector is empty or not.

        :param vector: The vector to check.
        :type vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, CommonVector3]
        :return: True, if the vector is empty. False, if not.
        :rtype: bool
        """
        empty_vector = CommonVector3.empty()
        return vector.x == empty_vector.x and vector.y == empty_vector.y and vector.z == empty_vector.z

    @staticmethod
    def from_vector3(vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> Union['CommonVector3', None]:
        """from_vector3(vector)

        Convert a Vector into a CommonVector3.

        :param vector: An instance of a vector.
        :type vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, CommonVector3]
        :return: An instance of a CommonVector3 or None if it failed to convert.
        :rtype: Union[CommonVector3, None]
        """
        if vector is None:
            raise ValueError('Cannot convert {} to {}.'.format(vector, CommonVector3.__name__))
        if isinstance(vector, CommonVector3):
            return vector
        if not isinstance(vector, Vector3) and not isinstance(vector, Vector3Immutable) and not isinstance(vector, MathPb2Vector3):
            raise Exception('Failed to convert {} with type {} was not of type {}.'.format(vector, type(vector), type(Vector3)))
        # noinspection PyUnresolvedReferences
        return CommonVector3(vector.x, vector.y, vector.z)

    @staticmethod
    def flatten(vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> 'CommonVector3':
        """flatten(vector)

        Flatten a Vector.

        :param vector: An instance of a vector.
        :type vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, CommonVector3]
        :return: An instance of a flattened CommonVector3.
        :rtype: CommonVector3
        """
        if vector is None:
            raise AttributeError('{} was called with vector as None!'.format(CommonVector3.flatten.__name__))
        from sims4.math import vector_flatten
        return CommonVector3.from_vector3(vector_flatten(vector))

    @staticmethod
    def normalize(vector: 'CommonVector3') -> float:
        """normalize(vector)

        Normalize a Vector.

        :param vector: An instance of a vector.
        :type vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, CommonVector3]
        :return: An instance of a normalized CommonVector3.
        :rtype: float
        """
        from sims4.math import vector_normalize
        return vector_normalize(vector)

    @staticmethod
    def distance_between(
        position_one: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3'],
        position_two: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']
    ) -> float:
        """distance_between(position_one, position_two)

        Calculate the distance between two vectors.

        :param position_one: An instance of a Vector.
        :type position_one: CommonVector3
        :param position_two: An instance of a Vector.
        :type position_two: CommonVector3
        :return: The distance between the two specified vectors.
        :rtype: float
        """
        if position_one is None:
            raise AttributeError('{} was called with position_one as None!'.format(CommonVector3.distance_between.__name__))
        if position_two is None:
            raise AttributeError('{} was called with position_two as None!'.format(CommonVector3.distance_between.__name__))
        from math import sqrt
        return sqrt((position_one - position_two).magnitude_squared())

    # noinspection PyMissingOrEmptyDocstring
    def magnitude_squared(self) -> float:
        # The functionality lies inside Vector3
        pass

    def __add__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3', float]) -> 'CommonVector3':
        # The functionality lies inside Vector3
        pass

    def __sub__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3', float]) -> 'CommonVector3':
        # The functionality lies inside Vector3
        pass

    def __mul__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3', float]) -> 'CommonVector3':
        # The functionality lies inside Vector3
        pass

    def __le__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        # The functionality lies inside Vector3
        pass

    def __lt__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        # The functionality lies inside Vector3
        pass

    def __ge__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        # The functionality lies inside Vector3
        pass

    def __gt__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        # The functionality lies inside Vector3
        pass

    def __hash__(self) -> int:
        # The functionality lies inside Vector3
        pass

    def __ne__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        # The functionality lies inside Vector3
        pass

    def __eq__(self, other: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> bool:
        # The functionality lies inside Vector3
        pass

    def __repr__(self) -> str:
        # The functionality lies inside Vector3
        pass

    def __str__(self) -> str:
        pass

    # noinspection PyMissingOrEmptyDocstring
    @staticmethod
    def serialize(vector: Union[Vector3, Vector3Immutable, MathPb2Vector3, 'CommonVector3']) -> Union[str, Dict[str, Any]]:
        data = dict()
        data['x'] = vector.x
        data['y'] = vector.y
        data['z'] = vector.z
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls: Type['CommonVector3'], data: Union[str, Dict[str, Any]]) -> Union['CommonVector3', None]:
        x = data.get('x', 0.0)
        y = data.get('y', 0.0)
        z = data.get('z', 0.0)
        return CommonVector3(x, y, z)
