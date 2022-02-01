"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 international public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.utils import classproperty
from collections import OrderedDict
from typing import Iterator, Union, Tuple, List

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import IntFlags
except:
    # noinspection PyMissingOrEmptyDocstring
    class IntFlags:
        # From Int
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
