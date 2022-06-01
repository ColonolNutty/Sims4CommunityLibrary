"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from collections import OrderedDict
from typing import Iterator, Union, Tuple

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # Created from example provided at https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
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
    class Int:
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

        def __sub__(self, other: Union['Int', int]) -> int:
            pass

        def __invert__(self) -> int:
            pass

        def __add__(self, other: Union['Int', int]) -> int:
            pass

        def __divmod__(self, other: Union['Int', int]) -> Tuple[int, int]:
            pass

        def __mod__(self, other: Union['Int', int]) -> int:
            pass

        def __mul__(self, other: Union['Int', int]) -> int:
            pass

        def __neg__(self) -> int:
            pass

        def __ge__(self, other: Union['Int', int]) -> bool:
            pass

        def __le__(self, other: Union['Int', int]) -> bool:
            pass

        def __lt__(self, other: Union['Int', int]) -> bool:
            pass

        def __gt__(self, other: Union['Int', int]) -> bool:
            pass

        def __eq__(self, other: Union['Int', int]) -> bool:
            pass

        def __hash__(self) -> int:
            pass


class CommonInt(Int):
    """An inheritable class that inherits from the vanilla Sims 4 enum.Int class so you don't have to.

    """
    pass
