"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 international public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from collections import OrderedDict
from typing import Iterator, Union, Tuple, List

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import IntFlags
except:
    # noinspection PyMissingOrEmptyDocstring
    class _ClassPropertyDescriptor(object):

        # noinspection PyMissingTypeHints,SpellCheckingInspection
        def __init__(self, fget, fset=None):
            self.fget = fget
            self.fset = fset

        # noinspection PyMissingTypeHints,SpellCheckingInspection
        def __get__(self, obj, klass=None):
            if klass is None:
                # noinspection SpellCheckingInspection
                klass = type(obj)
            return self.fget.__get__(obj, klass)()

        # noinspection PyMissingTypeHints
        def __set__(self, obj, value):
            if not self.fset:
                raise AttributeError("can't set attribute")
            type_ = type(obj)
            return self.fset.__get__(obj, type_)(value)

        # noinspection PyMissingTypeHints
        def setter(self, func):
            if not isinstance(func, (classmethod, staticmethod)):
                func = classmethod(func)
            # noinspection SpellCheckingInspection
            self.fset = func
            return self


    # noinspection PyMissingTypeHints,SpellCheckingInspection
    def _classproperty(func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        return _ClassPropertyDescriptor(func)

    # noinspection PyMissingOrEmptyDocstring
    class IntFlags:
        # From Int
        # noinspection PyPropertyDefinition
        @property
        def name(self) -> str:
            return ''

        # noinspection PyPropertyDefinition
        @property
        def value(self) -> int:
            return 0

        # noinspection PyPropertyDefinition,PyMethodParameters
        @_classproperty
        def values(cls) -> Iterator[int]:
            return tuple()

        # noinspection PyPropertyDefinition,PyMethodParameters
        @_classproperty
        def name_to_value(cls) -> OrderedDict:
            return OrderedDict()

        # noinspection PyPropertyDefinition,PyMethodParameters
        @_classproperty
        def value_to_name(cls) -> OrderedDict:
            return OrderedDict()

        def __int__(self) -> int:
            pass

        def __float__(self) -> float:
            pass

        def __sub__(self, other: Union['IntFlags', int]) -> int:
            pass

        def __invert__(self) -> int:
            pass

        def __add__(self, other: Union['IntFlags', int]) -> int:
            pass

        # noinspection SpellCheckingInspection
        def __divmod__(self, other: Union['IntFlags', int]) -> Tuple[int, int]:
            pass

        def __mod__(self, other: Union['IntFlags', int]) -> int:
            pass

        def __mul__(self, other: Union['IntFlags', int]) -> int:
            pass

        def __neg__(self) -> int:
            pass

        def __ge__(self, other: Union['IntFlags', int]) -> bool:
            pass

        def __le__(self, other: Union['IntFlags', int]) -> bool:
            pass

        def __lt__(self, other: Union['IntFlags', int]) -> bool:
            pass

        def __gt__(self, other: Union['IntFlags', int]) -> bool:
            pass

        def __eq__(self, other: Union['IntFlags', int]) -> bool:
            pass

        def __hash__(self) -> int:
            pass

        # From IntFlags
        @classmethod
        def _get_unknown_value(cls, value: 'IntFlags') -> 'IntFlags':
            pass

        @staticmethod
        def _next_auto_value(value: 'IntFlags') -> 'IntFlags':
            pass

        def _get_bits(self) -> Tuple[List[int], 'IntFlags']:
            pass

        @classmethod
        def list_values_from_flags(cls, value: 'IntFlags') -> List['IntFlags']:
            pass

        def __iter__(self) -> Iterator['IntFlags']:
            pass

        def __contains__(self, value: 'IntFlags'):
            pass

        def __and__(self, other: 'IntFlags'):
            pass

        def __or__(self, other: 'IntFlags'):
            pass


class CommonIntFlags(IntFlags):
    """An inheritable class that inherits from the vanilla Sims 4 enum.IntFlags class so you don't have to.

    """
    pass
