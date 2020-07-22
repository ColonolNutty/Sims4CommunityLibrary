"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator

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

        # noinspection PyPropertyDefinition
        @property
        def values(self) -> Iterator[int]:
            pass


class CommonInt(Int):
    """An inheritable class that inherits from the vanilla Sims 4 enum.Int class so you don't have to.

    """
    pass
