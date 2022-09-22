"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from statistics.skill import SkillEffectiveness


class CommonSkillEffectiveness(CommonInt):
    """Various Skill Effectiveness."""
    HUGE: 'CommonSkillEffectiveness' = ...
    LARGE: 'CommonSkillEffectiveness' = ...
    PERIODIC_LARGE: 'CommonSkillEffectiveness' = ...
    PERIODIC_SMALL: 'CommonSkillEffectiveness' = ...
    PERIODIC_STANDARD: 'CommonSkillEffectiveness' = ...
    PERIODIC_STANDARD_TODDLER: 'CommonSkillEffectiveness' = ...
    PERIODIC_TONE: 'CommonSkillEffectiveness' = ...
    PERIODIC_VERY_SMALL: 'CommonSkillEffectiveness' = ...
    SMALL: 'CommonSkillEffectiveness' = ...
    TINY: 'CommonSkillEffectiveness' = ...
    TODDLER: 'CommonSkillEffectiveness' = ...

    @staticmethod
    def convert_to_vanilla(value: 'CommonSkillEffectiveness') -> SkillEffectiveness:
        """convert_to_vanilla(value)

        Convert a value into a vanilla SkillEffectiveness value.

        :param value: An instance of CommonSkillEffectiveness
        :type value: CommonSkillEffectiveness
        :return: The specified value translated to an SkillEffectiveness or StandardPeriodic if the value could not be translated.
        :rtype: SkillEffectiveness
        """
        if value is None:
            # noinspection PyUnresolvedReferences
            return SkillEffectiveness.StandardPeriodic
        if isinstance(value, SkillEffectiveness):
            return value
        mapping = dict()
        if hasattr(SkillEffectiveness, 'Small'):
            mapping[CommonSkillEffectiveness.SMALL] = SkillEffectiveness.Small
        if hasattr(SkillEffectiveness, 'Large'):
            mapping[CommonSkillEffectiveness.LARGE] = SkillEffectiveness.Large
        if hasattr(SkillEffectiveness, 'SmallPeriodic'):
            mapping[CommonSkillEffectiveness.PERIODIC_SMALL] = SkillEffectiveness.SmallPeriodic
        if hasattr(SkillEffectiveness, 'StandardPeriodic'):
            mapping[CommonSkillEffectiveness.PERIODIC_STANDARD] = SkillEffectiveness.StandardPeriodic
        if hasattr(SkillEffectiveness, 'LargePeriodic'):
            mapping[CommonSkillEffectiveness.PERIODIC_LARGE] = SkillEffectiveness.LargePeriodic
        if hasattr(SkillEffectiveness, 'Tiny'):
            mapping[CommonSkillEffectiveness.TINY] = SkillEffectiveness.Tiny
        if hasattr(SkillEffectiveness, 'Huge'):
            mapping[CommonSkillEffectiveness.HUGE] = SkillEffectiveness.Huge
        if hasattr(SkillEffectiveness, 'VerySmallPeriodic'):
            mapping[CommonSkillEffectiveness.PERIODIC_VERY_SMALL] = SkillEffectiveness.VerySmallPeriodic
        if hasattr(SkillEffectiveness, 'TonePeriodic'):
            mapping[CommonSkillEffectiveness.PERIODIC_TONE] = SkillEffectiveness.TonePeriodic
        if hasattr(SkillEffectiveness, 'Toddler'):
            mapping[CommonSkillEffectiveness.TODDLER] = SkillEffectiveness.Toddler
        if hasattr(SkillEffectiveness, 'ToddlerStandardPeriodic'):
            mapping[CommonSkillEffectiveness.PERIODIC_STANDARD_TODDLER] = SkillEffectiveness.ToddlerStandardPeriodic

        return mapping.get(value, getattr(SkillEffectiveness, 'StandardPeriodic', None))

    @staticmethod
    def convert_from_vanilla(value: SkillEffectiveness) -> 'CommonSkillEffectiveness':
        """convert_from_vanilla(value)

        Convert a vanilla value to a CommonSkillEffectiveness value.

        :param value: An instance of SkillEffectiveness
        :type value: SkillEffectiveness
        :return: The specified value translated to a CommonSkillEffectiveness or PERIODIC_STANDARD if the value could not be translated.
        :rtype: CommonSkillEffectiveness
        """
        if value is None:
            return CommonSkillEffectiveness.PERIODIC_STANDARD
        if isinstance(value, CommonSkillEffectiveness):
            return value
        mapping = dict()
        if hasattr(SkillEffectiveness, 'Small'):
            mapping[SkillEffectiveness.Small] = CommonSkillEffectiveness.SMALL
        if hasattr(SkillEffectiveness, 'Large'):
            mapping[SkillEffectiveness.Large] = CommonSkillEffectiveness.LARGE
        if hasattr(SkillEffectiveness, 'SmallPeriodic'):
            mapping[SkillEffectiveness.SmallPeriodic] = CommonSkillEffectiveness.PERIODIC_SMALL
        if hasattr(SkillEffectiveness, 'StandardPeriodic'):
            mapping[SkillEffectiveness.StandardPeriodic] = CommonSkillEffectiveness.PERIODIC_STANDARD
        if hasattr(SkillEffectiveness, 'LargePeriodic'):
            mapping[SkillEffectiveness.LargePeriodic] = CommonSkillEffectiveness.PERIODIC_LARGE
        if hasattr(SkillEffectiveness, 'Tiny'):
            mapping[SkillEffectiveness.Tiny] = CommonSkillEffectiveness.TINY
        if hasattr(SkillEffectiveness, 'Huge'):
            mapping[SkillEffectiveness.Huge] = CommonSkillEffectiveness.HUGE
        if hasattr(SkillEffectiveness, 'VerySmallPeriodic'):
            mapping[SkillEffectiveness.VerySmallPeriodic] = CommonSkillEffectiveness.PERIODIC_VERY_SMALL
        if hasattr(SkillEffectiveness, 'TonePeriodic'):
            mapping[SkillEffectiveness.TonePeriodic] = CommonSkillEffectiveness.PERIODIC_TONE
        if hasattr(SkillEffectiveness, 'Toddler'):
            mapping[SkillEffectiveness.Toddler] = CommonSkillEffectiveness.TODDLER
        if hasattr(SkillEffectiveness, 'ToddlerStandardPeriodic'):
            mapping[SkillEffectiveness.ToddlerStandardPeriodic] = CommonSkillEffectiveness.PERIODIC_STANDARD_TODDLER

        return mapping.get(value, CommonSkillEffectiveness.PERIODIC_STANDARD)
