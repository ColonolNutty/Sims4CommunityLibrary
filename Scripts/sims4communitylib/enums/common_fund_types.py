"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict

from sims.funds import FundsSource
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonFundType(CommonInt):
    """Types of funds."""
    HOUSEHOLD: 'CommonFundType' = ...
    RETAIL: 'CommonFundType' = ...
    BUSINESS: 'CommonFundType' = ...
    STATISTIC: 'CommonFundType' = ...
    BUCKS: 'CommonFundType' = ...
    NO_SOURCE: 'CommonFundType' = ...

    @staticmethod
    def convert_to_vanilla(value: 'CommonFundType') -> FundsSource:
        """convert_to_vanilla(value)

        Convert a CommonFundType into the vanilla FundsSource enum.

        :param value: An instance of CommonFundType
        :type value: CommonFundType
        :return: The specified CommonFundType translated to FundsSource or HOUSEHOLD if the CommonFundType could not be translated.
        :rtype: Union[FundsSource, None]
        """
        mapping: Dict[CommonFundType, FundsSource] = {
            CommonFundType.HOUSEHOLD: FundsSource.HOUSEHOLD,
            CommonFundType.RETAIL: FundsSource.RETAIL,
            CommonFundType.BUSINESS: FundsSource.BUSINESS,
            CommonFundType.STATISTIC: FundsSource.STATISTIC,
            CommonFundType.BUCKS: FundsSource.BUCKS,
            CommonFundType.NO_SOURCE: FundsSource.NO_SOURCE,
        }
        return mapping.get(value, FundsSource.HOUSEHOLD)

    @staticmethod
    def convert_from_vanilla(value: FundsSource) -> 'CommonFundType':
        """convert_from_vanilla(value)

        Convert a vanilla FundsSource to CommonFundType.

        :param value: An instance of FundsSource
        :type value: FundsSource
        :return: The specified FundsSource translated to CommonFundType or HOUSEHOLD if the FundsSource could not be translated.
        :rtype: CommonFundType
        """
        mapping: Dict[FundsSource, CommonFundType] = {
            FundsSource.HOUSEHOLD: CommonFundType.HOUSEHOLD,
            FundsSource.RETAIL: CommonFundType.RETAIL,
            FundsSource.BUSINESS: CommonFundType.BUSINESS,
            FundsSource.STATISTIC: CommonFundType.STATISTIC,
            FundsSource.BUCKS: CommonFundType.BUCKS,
            FundsSource.NO_SOURCE: CommonFundType.NO_SOURCE,
        }
        return mapping.get(value, CommonFundType.HOUSEHOLD)
