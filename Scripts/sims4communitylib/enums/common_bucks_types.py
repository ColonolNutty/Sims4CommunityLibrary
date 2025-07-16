"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from bucks.bucks_enums import BucksType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonBucksType(CommonInt):
    """Variants of Bucks Types."""
    INVALID: 'CommonBucksType' = ...
    RETAIL: 'CommonBucksType' = ...
    VAMPIRE_POWER: 'CommonBucksType' = ...
    VAMPIRE_WEAKNESS: 'CommonBucksType' = ...
    VET: 'CommonBucksType' = ...
    CLUB: 'CommonBucksType' = ...
    RESTAURANT: 'CommonBucksType' = ...
    RECYCLE_BITS: 'CommonBucksType' = ...
    RECYCLE_PIECES: 'CommonBucksType' = ...
    FAME_PERK: 'CommonBucksType' = ...
    FAME_QUIRK: 'CommonBucksType' = ...
    WITCH_PERK: 'CommonBucksType' = ...
    INFLUENCE: 'CommonBucksType' = ...
    GALACTIC_CREDIT: 'CommonBucksType' = ...
    WEREWOLF_ABILITY: 'CommonBucksType' = ...
    WEREWOLF_ABILITY_QUEST: 'CommonBucksType' = ...
    GHOST_POWERS_ABILITY: 'CommonBucksType' = ...
    BUSINESS_PERK: 'CommonBucksType' = ...
    CUSTOMER_SATISFACTION: 'CommonBucksType' = ...
    FAIRY_PERK: 'CommonBucksType' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonBucksType'] = None) -> Tuple['CommonBucksType']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBucksType], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonBucksType]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonBucksType, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonBucksType'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBucksType], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonBucksType'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBucksType], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonBucksType') -> Union[BucksType, None]:
        """convert_to_vanilla(value)

        Convert a value into the vanilla BucksType enum.

        :param value: An instance of CommonBucksType
        :type value: CommonBucksType
        :return: The specified value translated to BucksType or None if the value could not be translated.
        :rtype: Union[BucksType, None]
        """
        if value is None or value == CommonBucksType.INVALID:
            return None
        if isinstance(value, BucksType):
            return value
        mapping = dict()
        if hasattr(BucksType, 'RetailBucks'):
            mapping[CommonBucksType.RETAIL] = BucksType.RetailBucks
        if hasattr(BucksType, 'VampirePowerBucks'):
            mapping[CommonBucksType.VAMPIRE_POWER] = BucksType.VampirePowerBucks
        if hasattr(BucksType, 'VampireWeaknessBucks'):
            mapping[CommonBucksType.VAMPIRE_WEAKNESS] = BucksType.VampireWeaknessBucks
        if hasattr(BucksType, 'VetBucks'):
            mapping[CommonBucksType.VET] = BucksType.VetBucks
        if hasattr(BucksType, 'ClubBucks'):
            mapping[CommonBucksType.CLUB] = BucksType.ClubBucks
        if hasattr(BucksType, 'RestaurantBucks'):
            mapping[CommonBucksType.RESTAURANT] = BucksType.RestaurantBucks
        if hasattr(BucksType, 'RecycleBitsBucks'):
            mapping[CommonBucksType.RECYCLE_BITS] = BucksType.RecycleBitsBucks
        if hasattr(BucksType, 'RecyclePiecesBucks'):
            mapping[CommonBucksType.RECYCLE_PIECES] = BucksType.RecyclePiecesBucks
        if hasattr(BucksType, 'FamePerkBucks'):
            mapping[CommonBucksType.FAME_PERK] = BucksType.FamePerkBucks
        if hasattr(BucksType, 'FameQuirkBucks'):
            mapping[CommonBucksType.FAME_QUIRK] = BucksType.FameQuirkBucks
        if hasattr(BucksType, 'WitchPerkBucks'):
            mapping[CommonBucksType.WITCH_PERK] = BucksType.WitchPerkBucks
        if hasattr(BucksType, 'InfluenceBuck'):
            mapping[CommonBucksType.INFLUENCE] = BucksType.InfluenceBuck
        if hasattr(BucksType, 'GalacticCredits'):
            mapping[CommonBucksType.GALACTIC_CREDIT] = BucksType.GalacticCredits
        if hasattr(BucksType, 'WerewolfAbilityBucks'):
            mapping[CommonBucksType.WEREWOLF_ABILITY] = BucksType.WerewolfAbilityBucks
        if hasattr(BucksType, 'WerewolfQuestAbilityBucks'):
            mapping[CommonBucksType.WEREWOLF_ABILITY_QUEST] = BucksType.WerewolfQuestAbilityBucks
        if hasattr(BucksType, 'GhostPowersAbilityBucks'):
            mapping[CommonBucksType.GHOST_POWERS_ABILITY] = BucksType.GhostPowersAbilityBucks
        if hasattr(BucksType, 'BusinessPerkBucks'):
            mapping[CommonBucksType.BUSINESS_PERK] = BucksType.BusinessPerkBucks
        if hasattr(BucksType, 'CustomerSatisfactionBucks'):
            mapping[CommonBucksType.CUSTOMER_SATISFACTION] = BucksType.CustomerSatisfactionBucks
        if hasattr(BucksType, 'FairyPerkBucks'):
            mapping[CommonBucksType.FAIRY_PERK] = BucksType.FairyPerkBucks
        return mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: Union[int, BucksType]) -> 'CommonBucksType':
        """convert_from_vanilla(value)

        Convert a value into a CommonBucksType enum.

        :param value: An instance of BucksType
        :type value: BucksType
        :return: The specified value translated to CommonBucksType or INVALID if the value could not be translated.
        :rtype: Union[BucksType, None]
        """
        if value is None:
            return CommonBucksType.INVALID
        if isinstance(value, CommonBucksType):
            return value
        mapping = dict()
        if hasattr(BucksType, 'RetailBucks'):
            mapping[BucksType.RetailBucks] = CommonBucksType.RETAIL
        if hasattr(BucksType, 'VampirePowerBucks'):
            mapping[BucksType.VampirePowerBucks] = CommonBucksType.VAMPIRE_POWER
        if hasattr(BucksType, 'VampireWeaknessBucks'):
            mapping[BucksType.VampireWeaknessBucks] = CommonBucksType.VAMPIRE_WEAKNESS
        if hasattr(BucksType, 'VetBucks'):
            mapping[BucksType.VetBucks] = CommonBucksType.VET
        if hasattr(BucksType, 'ClubBucks'):
            mapping[BucksType.ClubBucks] = CommonBucksType.CLUB
        if hasattr(BucksType, 'RestaurantBucks'):
            mapping[BucksType.RestaurantBucks] = CommonBucksType.RESTAURANT
        if hasattr(BucksType, 'RecycleBitsBucks'):
            mapping[BucksType.RecycleBitsBucks] = CommonBucksType.RECYCLE_BITS
        if hasattr(BucksType, 'RecyclePiecesBucks'):
            mapping[BucksType.RecyclePiecesBucks] = CommonBucksType.RECYCLE_PIECES
        if hasattr(BucksType, 'FamePerkBucks'):
            mapping[BucksType.FamePerkBucks] = CommonBucksType.FAME_PERK
        if hasattr(BucksType, 'FameQuirkBucks'):
            mapping[BucksType.FameQuirkBucks] = CommonBucksType.FAME_QUIRK
        if hasattr(BucksType, 'WitchPerkBucks'):
            mapping[BucksType.WitchPerkBucks] = CommonBucksType.WITCH_PERK
        if hasattr(BucksType, 'InfluenceBuck'):
            mapping[BucksType.InfluenceBuck] = CommonBucksType.INFLUENCE
        if hasattr(BucksType, 'GalacticCredits'):
            mapping[BucksType.GalacticCredits] = CommonBucksType.GALACTIC_CREDIT
        if hasattr(BucksType, 'WerewolfAbilityBucks'):
            mapping[BucksType.WerewolfAbilityBucks] = CommonBucksType.WEREWOLF_ABILITY
        if hasattr(BucksType, 'WerewolfQuestAbilityBucks'):
            mapping[BucksType.WerewolfQuestAbilityBucks] = CommonBucksType.WEREWOLF_ABILITY_QUEST
        if hasattr(BucksType, 'GhostPowersAbilityBucks'):
            mapping[BucksType.GhostPowersAbilityBucks] = CommonBucksType.GHOST_POWERS_ABILITY
        if hasattr(BucksType, 'BusinessPerkBucks'):
            mapping[BucksType.BusinessPerkBucks] = CommonBucksType.BUSINESS_PERK
        if hasattr(BucksType, 'CustomerSatisfactionBucks'):
            mapping[BucksType.CustomerSatisfactionBucks] = CommonBucksType.CUSTOMER_SATISFACTION
        if hasattr(BucksType, 'FairyPerkBucks'):
            mapping[BucksType.FairyPerkBucks] = CommonBucksType.FAIRY_PERK
        return mapping.get(value, value)

    @staticmethod
    def convert_to_localized_string_id(value: 'CommonBucksType') -> Union[int, str]:
        """convert_to_localized_string_id(value)

        Convert a CommonBucksType into a Localized String identifier.

        :param value: An instance of a CommonBucksType
        :type value: CommonBucksType
        :return: The specified CommonBucksType translated to a localized string identifier. If no localized string id is found, the name property of the value will be used instead.
        :rtype: Union[int, str]
        """
        display_name_mapping = {
            # CommonBucksType.RETAIL: 0,
            # CommonBucksType.VAMPIRE_POWER: 0,
            # CommonBucksType.VAMPIRE_WEAKNESS: 0,
            # CommonBucksType.VET: 0,
            # CommonBucksType.CLUB: 0,
            # CommonBucksType.RESTAURANT: 0,
            # CommonBucksType.RECYCLE_BITS: 0,
            # CommonBucksType.RECYCLE_PIECES: 0,
            # CommonBucksType.FAME_PERK: 0,
            # CommonBucksType.FAME_QUIRK: 0,
            # CommonBucksType.WITCH_PERK: 0,
            # CommonBucksType.INFLUENCE: 0,
            # CommonBucksType.GALACTIC_CREDIT: 0,
            # CommonBucksType.WEREWOLF_ABILITY: 0,
            # CommonBucksType.WEREWOLF_ABILITY_QUEST: 0,
        }
        if isinstance(value, int) and not isinstance(value, CommonBucksType):
            value = CommonBucksType.convert_from_vanilla(value)
        return display_name_mapping.get(value, value.name if hasattr(value, 'name') else str(value))
