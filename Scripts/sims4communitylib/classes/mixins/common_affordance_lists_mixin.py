"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple


class CommonAffordanceListsMixin:
    """A mixin that will do something with affordance lists."""

    @property
    def affordance_list_ids(self) -> Tuple[int]:
        """A collection of identifiers for affordance lists.

        :return: A collection of identifiers for affordance lists.
        :rtype: Tuple[int]
        """
        raise NotImplementedError()
