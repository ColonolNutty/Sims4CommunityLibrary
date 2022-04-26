"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonStringId(CommonInt):
    """Identifiers for localization strings.

    .. note:: These identifiers point to strings within String Tables within package files.

    """
    INVALID: 'CommonStringId' = 0
    # Notifications
    EXCEPTION_OCCURRED_TITLE: 'CommonStringId' = 3506527463
    EXCEPTION_OCCURRED_TITLE_FOR_MOD: 'CommonStringId' = 1541569535
    # 0.String
    EXCEPTION_OCCURRED_TEXT: 'CommonStringId' = 1656389837

    # Dialog
    OK: 'CommonStringId' = 3648501874
    OK_ALL_CAPS: 'CommonStringId' = 1102906806
    CANCEL: 'CommonStringId' = 3497542682
    CANCEL_ALL_CAPS: 'CommonStringId' = 1249800636

    # Navigation
    NEXT: 'CommonStringId' = 982796106
    PREVIOUS: 'CommonStringId' = 4210670582
    # Tokens: {0.String}
    GO_TO_STRING: 'CommonStringId' = 3934117375

    # Text
    # Tokens: {0.String}
    TEXT_WITH_GREEN_COLOR: 'CommonStringId' = 3458194999
    # Tokens: {0.String}
    TEXT_WITH_RED_COLOR: 'CommonStringId' = 835489330
    # Tokens: {0.String}
    TEXT_WITH_BLUE_COLOR: 'CommonStringId' = 1505840180
    # Tokens: {0.String}
    TEXT_WITH_YELLOW_COLOR: 'CommonStringId' = 3457894271
    # Tokens: {0.String}
    TEXT_WITH_ORANGE_COLOR: 'CommonStringId' = 2567694686

    # Ages
    BABY: 'CommonStringId' = 4016862175
    TODDLER: 'CommonStringId' = 3252370736
    CHILD: 'CommonStringId' = 2993678259
    TEEN: 'CommonStringId' = 1166433319
    YOUNG_ADULT: 'CommonStringId' = 2053658442
    ADULT: 'CommonStringId' = 1747466136
    ELDER: 'CommonStringId' = 685867388

    # Gender
    MALE: 'CommonStringId' = 434606820
    FEMALE: 'CommonStringId' = 2933657479

    # Species
    HUMAN: 'CommonStringId' = 3519680994
    SMALL_DOG: 'CommonStringId' = 698804483
    LARGE_DOG: 'CommonStringId' = 1545624565
    CAT: 'CommonStringId' = 1720023562
    FOX: 'CommonStringId' = 0xCE739947

    # Pregnancy
    GET_PREGNANT: 'CommonStringId' = 3694037554
    GET_OTHER_PREGNANT: 'CommonStringId' = 3780444441
    CANNOT_EDIT_PREGNANT_SIMS: 'CommonStringId' = 1715308569
    PREGNANT_OUTCOME: 'CommonStringId' = 3717297329

    # Gender Options
    TOILET_USE_STANDING: 'CommonStringId' = 3730566822
    TOILET_USE_SITTING: 'CommonStringId' = 4265081704

    # Misc Text
    CUSTOM_GENDER_SETTINGS: 'CommonStringId' = 2156245727
    CLOTHING_PREFERENCE: 'CommonStringId' = 611620004
    MASCULINE: 'CommonStringId' = 585998164
    FEMININE: 'CommonStringId' = 667254132
    PHYSICAL_FRAME: 'CommonStringId' = 2574825855

    # Text
    # Tokens: {0.String}
    STRING_NOT_FOUND_WITH_IDENTIFIER: 'CommonStringId' = 3037244137

    # Test
    TESTING_TEST_BUTTON_ONE: 'CommonStringId' = 367590350
    TESTING_TEST_BUTTON_TWO: 'CommonStringId' = 367590349
    TESTING_SOME_TEXT_FOR_TESTING: 'CommonStringId' = 1352970207
    TESTING_TEST_TEXT_NO_TOKENS: 'CommonStringId' = 3987872118
    # Tokens: {0.SimFirstName} {0.SimLastName}
    TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME: 'CommonStringId' = 4280406738
    # Tokens: {0.String}
    TESTING_TEST_TEXT_WITH_STRING_TOKEN: 'CommonStringId' = 2977195159
    # Tokens: {0.Number}
    TESTING_TEST_TEXT_WITH_NUMBER_TOKEN: 'CommonStringId' = 4138001347

    # S4CL
    S4CL_SIMS_4_COMMUNITY_LIBRARY: 'CommonStringId' = 1638558923
    S4CL_LOG_ALL_INTERACTIONS: 'CommonStringId' = 3133049591
    # Tokens: {0.String}
    S4CL_DONE_LOGGING_ALL_INTERACTIONS: 'CommonStringId' = 207690817

    # Sim Actions.
    S4CL_OBJECT_IS_IN_USE = 0x7EC77EF6
    # Tokens: {0.SimFirstName}
    S4CL_SIM_NOT_ALLOWED_THERE = 0x48245F2A
    # Tokens: {0.SimFirstName}
    S4CL_SIM_CANNOT_REACH_THAT_SPOT = 0x6B324A52
    # Tokens: {0.SimFirstName}
    S4CL_NOT_ENOUGH_ROOM_FOR_SIM_HERE = 0x36EB7A72
    # Tokens: {0.SimFirstName}
    S4CL_SIM_IS_NOT_PREGNANT: 'CommonStringId' = 0x4992E851

    S4CL_YES: 'CommonStringId' = 0x3A6189A6
    S4CL_NO: 'CommonStringId' = 0x6377188C
    S4CL_RANDOM: 'CommonStringId' = 0xB5ADADF0
    S4CL_CONFIRMATION: 'CommonStringId' = 0x963ACF86
    S4CL_GO_BACK = 0xD74B6B28
    S4CL_NONE = 0x2CA33BDB
    S4CL_ALL = 0x419C2C6E
    S4CL_ANY = 0x3F9C28A5
    S4CL_DECLINED = 0x5FD633CB
    S4CL_ACCEPTED = 0xB667ABF6
    S4CL_ACCEPT = 0xD0F420D1
    S4CL_DECLINE = 0xA60FC6F5
    S4CL_DEFAULT = 0x2EA8FB98
    S4CL_REMOVE_ALL = 0x5C6C2580
    S4CL_REMOVE = 0x8B3681B1

    # Species
    S4CL_DOG: 'CommonStringId' = 0x20953C2D

    # Separators
    # {0.String}{1.String}
    S4CL_COMBINE_TWO_STRINGS: 'CommonStringId' = 4217460952
    # Tokens: {0.String}: {1.String}
    STRING_COLON_SPACE_STRING = 0x6284ACBA
    # Tokens: {0.String}, {1.String}
    STRING_COMMA_SPACE_STRING = 0x1429B07C
    # Tokens: {0.String} {1.String}
    STRING_SPACE_STRING = 0x0699D5F4
    # Tokens: {0.String} ({1.String})
    STRING_SPACE_PARENTHESIS_SURROUNDED_STRING = 0x1A406429
    # Tokens: {0.String}\n{1.String}
    STRING_NEWLINE_STRING = 0xCE1E042E
    # Tokens: {0.String}\n\n{1.String}
    STRING_NEWLINE_NEWLINE_STRING = 0xBA331D00
    # Tokens: {0.String}-{1.String}
    STRING_HYPHEN_STRING = 0x032A81F9
    # Tokens: {0.String} are {1.String}
    S4CL_STRING_ARE_STRING = 0x92AF2862
    # Tokens: {0.String} is {1.String}
    S4CL_STRING_IS_STRING = 0xC1166AC4
    # Tokens: {0.String}+{1.String}
    S4CL_STRING_PLUS_STRING = 0x82ED46EB
    # Tokens: {0.String} or {1.String}
    S4CL_STRING_OR_STRING = 0x1DC61DF5
    # Tokens: {0.String}, or {1.String}
    S4CL_STRING_COMMA_SPACE_OR_STRING = 0x34E0269D
    # Tokens: {0.String} and {1.String}
    S4CL_STRING_AND_STRING = 0xCFB35A51
    # Tokens: {0.String}, and {1.String}
    S4CL_STRING_COMMA_SPACE_AND_STRING = 0x419E6969

    # String Modifiers
    # Tokens: ({0.String})
    S4CL_PARENTHESIS_SURROUNDED_STRING = 0xD7FDCAF5

    S4CL_PLEASE_WAIT = 0xF2237D1E
    S4CL_RANDOMIZATION_COMPLETE = 0x8ABA94C5

    S4CL_PREGNANCY = 0x3F70BCAA

    S4CL_RESTART_REQUIRED = 0x955D0179
    S4CL_CHANGES_MADE_RESTART_REQUIRED_DESCRIPTION = 0x6B5119FB
    # (From Debug)
    S4CL_BUFF_REASON_FROM_DEBUG = 0x38C2E6F7

    # Purchase
    S4CL_PURCHASE_SUCCESSFUL = 0xF3C59252
    S4CL_YOUR_PURCHASED_ITEMS_ARE_ON_THE_WAY = 0x5A8D580D
    S4CL_YOUR_PURCHASED_ITEMS_ARE_IN_YOUR_INVENTORY = 0xF33F9A95
    S4CL_TOO_EXPENSIVE = 0x59F9C698

    S4CL_THIS_FEATURE_IS_NOT_YET_IMPLEMENTED = 0x556801EE

    # Sim Name
    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim One)
    S4CL_SIM_NAME = 0xAC8F626F
    # Tokens: {0.SimFirstName} {0.SimLastName} (Sim One) {1.SimFirstName} {1.SimLastName} (Sim Two)
    S4CL_SIM_NAME_AND_SIM_NAME = 0xD8740FE4
    # Tokens: {0.String} (A String) {1.SimFirstName} {1.SimLastName} (The Last Sim)
    S4CL_STRING_COMMA_SPACE_AND_SIM_NAME = 0x2EACE203
    # Tokens: {0.SimFirstName} {0.SimLastName} (The First Sim) {1.String} (A String)
    S4CL_SIM_NAME_COMMA_SPACE_AND_STRING = 0x2A8148D8

    # Tokens: {0.String}
    S4CL_UID_STRING = 0x0313D2A0
    # Tokens: {0.String} (Current)
    S4CL_CURRENT_STRING = 0x860F13B5
    # Tokens: {0.String} (Count)
    S4CL_COUNT_STRING = 0x423122EB
    # Tokens: {0.String} (Error Message)
    S4CL_ERROR_STRING = 0xA1C925BC
    # Tokens: {0.String} (Failed Message)
    S4CL_FAILED_STRING = 0x0F818D6F
    # Tokens: {0.String} (Failure Message)
    S4CL_FAILURE_STRING = 0x33A94544
    # Tokens: {0.String} (Success Message)
    S4CL_SUCCESS_STRING = 0xC6D15497
    # Tokens: {0.String} (String Message)
    S4CL_EXCLAMATION_EXCLAMATION_STRING = 0xA07FA6C6
