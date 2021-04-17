"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.utils import classproperty
from collections import OrderedDict
from typing import Iterator, Union, Tuple

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        # noinspection PyPropertyDefinition
        @property
        def name(self) -> str:
            pass

        # noinspection PyPropertyDefinition
        @property
        def value(self) -> int:
            pass

        # noinspection PyPropertyDefinition,PyMethodParameters
        @classproperty
        def values(cls) -> Iterator[int]:
            pass

        # noinspection PyPropertyDefinition,PyMethodParameters
        @classproperty
        def name_to_value(cls) -> OrderedDict:
            pass

        # noinspection PyPropertyDefinition,PyMethodParameters
        @classproperty
        def value_to_name(cls) -> OrderedDict:
            pass

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
