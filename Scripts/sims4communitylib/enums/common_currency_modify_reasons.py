"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from protocolbuffers import Consts_pb2
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonCurrencyModifyReason(CommonInt):
    """Various reasons for currencies to be modified."""
    # Change reasons
    CHEAT: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_CHEAT
    SPLIT_HOUSEHOLD: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_SPLIT_HOUSEHOLD

    # Add reasons
    INTERACTION_REWARD: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_INTERACTION_REWARD
    EVENT_REWARD: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_EVENET_REWARD
    OBJECT_SELL: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_OBJECT_SELL
    STRUCTURE_SELL: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_STRUCTURE_SELL
    LOT_SELL: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_LOT_SELL
    HOUSEHOLD_TRANSFER_GAIN: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_HOUSEHOLD_TRANSFER_GAIN
    SIM_POINTS_EXCHANGED: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_SIM_POINTS_EXCHANGED
    SIM_WALLET_FUNDED: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_SIM_WALLET_FUNDED
    CAREER: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_CAREER
    ASPIRATION_REWARD: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_ASPIRATION_REWARD
    ROYALTY: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_ROYALTY
    FIRE_INSURANCE: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_FIREINSURANCE
    RETAIL_PROFITS: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_RETAIL_PROFITS
    RETAIL_TRANSFER_GAIN: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_RETAIL_TRANSFER_GAIN
    HOLIDAY_LOTTERY: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_HOLIDAY_LOTTERY
    LIFESTYLE_BRAND: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_LIFESTYLE_BRAND
    ROOMMATE_RENT: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_ROOMMATE_RENT
    SCHOLARSHIP_SURPLUS: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_SCHOLARSHIP_SURPLUS
    MARKETPLACE_OBJECT_SALE: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_MONEY_OBJECT_MARKETPLACE_SALE

    # Remove reasons
    INTERACTION_COST: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_INTERACTION_COST
    EVENT_COST: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_EVENT_COST
    OBJECT_BUY: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_OBJECT_BUY
    STRUCTURE_BUY: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_STRUCTURE_BUY
    CAS_ITEM_BUY: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_CAS_BUY
    BLUEPRINT_CONSTRUCTED: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_LOT_BUY
    LOT_BUY: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_LOT_BUY
    HOUSEHOLD_TRANSFER_LOSS: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_HOUSEHOLD_TRANSFER_LOSS
    SIM_WALLET_EMPTIED: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_SIM_WALLET_EMPTIED
    CRAFTING_COST: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_CRAFTING_COST
    VACATION: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_MONEY_VACATION
    RETAIL_ITEM_BUY: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_RETAIL_ITEM_BUY
    RETAIL_TRANSFER_LOSS: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_RETAIL_TRANSFER_LOSS
    TUITION_COST: 'CommonCurrencyModifyReason' = Consts_pb2.FUNDS_TUITION_COST
    SIM_DEATH_COST: 'CommonCurrencyModifyReason' = Consts_pb2.TELEMETRY_LOANS_SIM_DEATH
