"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict

from sims.funds import FundsSource
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonFundsSource(CommonInt):
    """Sources of funds."""
    HOUSEHOLD: 'CommonFundsSource' = ...
    RETAIL: 'CommonFundsSource' = ...
    BUSINESS: 'CommonFundsSource' = ...
    STATISTIC: 'CommonFundsSource' = ...
    BUCKS: 'CommonFundsSource' = ...
    NO_SOURCE: 'CommonFundsSource' = ...

    @staticmethod
    def convert_to_vanilla(value: 'CommonFundsSource') -> FundsSource:
        """convert_to_vanilla(value)

        Convert a value into the vanilla FundsSource enum.

        :param value: An instance of the enum.
        :type value: CommonFundsSource
        :return: The specified value translated to FundsSource or HOUSEHOLD if the value could not be translated.
        :rtype: Union[FundsSource, None]
        """
        mapping: Dict[CommonFundsSource, FundsSource] = {
            CommonFundsSource.HOUSEHOLD: FundsSource.HOUSEHOLD,
            CommonFundsSource.RETAIL: FundsSource.RETAIL,
            CommonFundsSource.BUSINESS: FundsSource.BUSINESS,
            CommonFundsSource.STATISTIC: FundsSource.STATISTIC,
            CommonFundsSource.BUCKS: FundsSource.BUCKS,
            CommonFundsSource.NO_SOURCE: FundsSource.NO_SOURCE,
        }
        return mapping.get(value, FundsSource.HOUSEHOLD)

    @staticmethod
    def convert_from_vanilla(value: FundsSource) -> 'CommonFundsSource':
        """convert_from_vanilla(value)

        Convert a vanilla FundsSource to value.

        :param value: An instance of the enum.
        :type value: FundsSource
        :return: The specified value translated to CommonFundsSource or HOUSEHOLD if the value could not be translated.
        :rtype: CommonFundsSource
        """
        mapping: Dict[FundsSource, CommonFundsSource] = {
            FundsSource.HOUSEHOLD: CommonFundsSource.HOUSEHOLD,
            FundsSource.RETAIL: CommonFundsSource.RETAIL,
            FundsSource.BUSINESS: CommonFundsSource.BUSINESS,
            FundsSource.STATISTIC: CommonFundsSource.STATISTIC,
            FundsSource.BUCKS: CommonFundsSource.BUCKS,
            FundsSource.NO_SOURCE: CommonFundsSource.NO_SOURCE,
        }
        return mapping.get(value, CommonFundsSource.HOUSEHOLD)
