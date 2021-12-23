"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union

from interactions.constraints import Constraint, _ConstraintSet, Nowhere
from sims4communitylib.services.common_service import CommonService


class CommonPostureConstraintService(CommonService):
    """CommonPostureConstraintService()

    Utilities for providing and manipulating posture constraints of Sims.
    """

    def __init__(self) -> None:
        self._stand_or_swim = None

    @property
    def stand(self) -> Constraint:
        """ A posture constraint for a Sim to stand at a target.

        :return: An instance of a Constraint.
        :rtype: Constraint
        """
        from animation.posture_manifest_constants import STAND_AT_NONE_CONSTRAINT
        return STAND_AT_NONE_CONSTRAINT

    @property
    def stand_at_none(self) -> Constraint:
        """ A posture constraint for a Sim to stand at no target.

        :return: An instance of a Constraint.
        :rtype: Constraint
        """
        from animation.posture_manifest_constants import STAND_AT_NONE_CONSTRAINT
        return STAND_AT_NONE_CONSTRAINT

    @property
    def swim_at_none(self) -> Constraint:
        """ A posture constraint for a Sim to swim at no target.

        :return: An instance of a Constraint.
        :rtype: Constraint
        """
        from animation.posture_manifest_constants import SWIM_AT_NONE_CONSTRAINT
        return SWIM_AT_NONE_CONSTRAINT

    @property
    def stand_or_swim_at_none(self) -> Constraint:
        """ A posture constraint for a Sim to stand at a target or to swim at no target.

        :return: An instance of a Constraint.
        :rtype: Constraint
        """
        if self._stand_or_swim is None:
            self._stand_or_swim = CommonPostureConstraintService.combine_constraints((self.stand_at_none, self.swim_at_none), debug_name='Stand-Or-Swim@None')
        return self._stand_or_swim

    @staticmethod
    def combine_constraints(constraints: Iterator[Constraint], fallback_constraints: Iterator[Constraint]=(), debug_name: str='Combined') -> Union[_ConstraintSet, Constraint, Nowhere]:
        """combine_constraints(constraints, fallback_constraints=(), debug_name='Combined')

        Attempt to combine similar constraints into a constraint set.

        :param constraints: A collection of Constraints.
        :type constraints: Iterator[Constraint]
        :param fallback_constraints: A collection of Constraints to choose from as a fallback when the primary constraints fail to combine. Default is an empty collection.
        :type fallback_constraints: Iterator[Constraint], optional
        :param debug_name: The name of the constraint set being created. Default is 'Combined'.
        :type debug_name: str, optional
        :return: A constraint set containing the specified constraints, a Constraint chosen from one of the specified fallback constraints, or Nowhere when everything else fails.
        :rtype: Union[_ConstraintSet, Constraint, Nowhere]
        """
        from interactions.constraints import create_constraint_set
        return create_constraint_set(tuple(constraints), invalid_constraints=tuple(fallback_constraints), debug_name=debug_name)
