"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from statistics.skill import SkillEffectiveness


class CommonSkillEffectiveness(CommonInt):
    """Various Skill Effectiveness."""
    HUGE: 'CommonSkillEffectiveness' = 7
    LARGE: 'CommonSkillEffectiveness' = 2
    SMALL: 'CommonSkillEffectiveness' = 1
    TINY: 'CommonSkillEffectiveness' = 6
    TODDLER: 'CommonSkillEffectiveness' = 10
    PERIODIC_LARGE: 'CommonSkillEffectiveness' = 5
    PERIODIC_SMALL: 'CommonSkillEffectiveness' = 3
    PERIODIC_STANDARD: 'CommonSkillEffectiveness' = 4
    PERIODIC_STANDARD_TODDLER: 'CommonSkillEffectiveness' = 11
    PERIODIC_TONE: 'CommonSkillEffectiveness' = 9
    PERIODIC_VERY_SMALL: 'CommonSkillEffectiveness' = 8

    @staticmethod
    def convert_to_vanilla(value: 'CommonSkillEffectiveness') -> SkillEffectiveness:
        """convert_to_vanilla(value)

        Convert a CommonSkillEffectiveness value into a vanilla SkillEffectiveness value.

        :param value: An instance of CommonSkillEffectiveness
        :type value: CommonSkillEffectiveness
        :return: The specified CommonSkillEffectiveness translated to an SkillEffectiveness or SkillEffectiveness.StandardPeriodic if the CommonSkillEffectiveness could not be translated.
        :rtype: Union[SkillEffectiveness, None]
        """
        if value is None:
            # noinspection PyUnresolvedReferences
            return SkillEffectiveness.StandardPeriodic

        if isinstance(value, SkillEffectiveness):
            return value
        # noinspection PyUnresolvedReferences
        mapping: Dict[CommonSkillEffectiveness, SkillEffectiveness] = {
            CommonSkillEffectiveness.HUGE: SkillEffectiveness.Huge,
            CommonSkillEffectiveness.LARGE: SkillEffectiveness.Large,
            CommonSkillEffectiveness.SMALL: SkillEffectiveness.Small,
            CommonSkillEffectiveness.TINY: SkillEffectiveness.Tiny,
            CommonSkillEffectiveness.TODDLER: SkillEffectiveness.Toddler,
            CommonSkillEffectiveness.PERIODIC_LARGE: SkillEffectiveness.LargePeriodic,
            CommonSkillEffectiveness.PERIODIC_SMALL: SkillEffectiveness.SmallPeriodic,
            CommonSkillEffectiveness.PERIODIC_STANDARD: SkillEffectiveness.StandardPeriodic,
            CommonSkillEffectiveness.PERIODIC_STANDARD_TODDLER: SkillEffectiveness.ToddlerStandardPeriodic,
            CommonSkillEffectiveness.PERIODIC_TONE: SkillEffectiveness.TonePeriodic,
            CommonSkillEffectiveness.PERIODIC_VERY_SMALL: SkillEffectiveness.VerySmallPeriodic,
        }
        if value not in mapping:
            # noinspection PyUnresolvedReferences
            return CommonResourceUtils.get_enum_by_int_value(int(value), SkillEffectiveness, default_value=SkillEffectiveness.StandardPeriodic)
        # noinspection PyUnresolvedReferences
        return mapping.get(value, SkillEffectiveness.StandardPeriodic)

    @staticmethod
    def convert_from_vanilla(value: SkillEffectiveness) -> 'CommonSkillEffectiveness':
        """convert_from_vanilla(value)

        Convert a vanilla SkillEffectiveness value to a CommonSkillEffectiveness value.

        :param value: An instance of SkillEffectiveness
        :type value: SkillEffectiveness
        :return: The specified SkillEffectiveness translated to a CommonSkillEffectiveness or CommonSkillEffectiveness.PERIODIC_STANDARD if the SkillEffectiveness could not be translated.
        :rtype: CommonSkillEffectiveness
        """
        if value is None:
            return CommonSkillEffectiveness.PERIODIC_STANDARD
        if isinstance(value, CommonSkillEffectiveness):
            return value
        # noinspection PyUnresolvedReferences
        mapping: Dict[SkillEffectiveness, CommonSkillEffectiveness] = {
            SkillEffectiveness.Huge: CommonSkillEffectiveness.HUGE,
            SkillEffectiveness.Large: CommonSkillEffectiveness.LARGE,
            SkillEffectiveness.Small: CommonSkillEffectiveness.SMALL,
            SkillEffectiveness.Tiny: CommonSkillEffectiveness.TINY,
            SkillEffectiveness.Toddler: CommonSkillEffectiveness.TODDLER,
            SkillEffectiveness.LargePeriodic: CommonSkillEffectiveness.PERIODIC_LARGE,
            SkillEffectiveness.SmallPeriodic: CommonSkillEffectiveness.PERIODIC_SMALL,
            SkillEffectiveness.StandardPeriodic: CommonSkillEffectiveness.PERIODIC_STANDARD,
            SkillEffectiveness.ToddlerStandardPeriodic: CommonSkillEffectiveness.PERIODIC_STANDARD_TODDLER,
            SkillEffectiveness.TonePeriodic: CommonSkillEffectiveness.PERIODIC_TONE,
            SkillEffectiveness.VerySmallPeriodic: CommonSkillEffectiveness.PERIODIC_VERY_SMALL,
        }
        if value not in mapping:
            # noinspection PyUnresolvedReferences
            return CommonResourceUtils.get_enum_by_int_value(int(value), CommonSkillEffectiveness, default_value=CommonSkillEffectiveness.PERIODIC_STANDARD)
        return mapping.get(value, CommonSkillEffectiveness.PERIODIC_STANDARD)
