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
    # Tokens: {0.SimFirstName}
    S4CL_SIM_IS_NOT_PREGNANT: 'CommonStringId' = 1234364497
    S4CL_YES: 'CommonStringId' = 979470758
    S4CL_NO: 'CommonStringId' = 1668749452
    S4CL_RANDOM: 'CommonStringId' = 3048058352
    S4CL_CONFIRMATION: 'CommonStringId' = 2520436614
    # {0.String}{1.String}
    S4CL_COMBINE_TWO_STRINGS: 'CommonStringId' = 4217460952
