"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSimType(CommonInt):
    """Various Sim Types that describe the Age, Species, and Occult Type of a Sim in a single value."""
    NONE: 'CommonSimType' = 0

    ELDER_HUMAN: 'CommonSimType' = 1
    ELDER_HUMAN_VAMPIRE: 'CommonSimType' = 2
    ELDER_HUMAN_GHOST: 'CommonSimType' = 3
    ELDER_HUMAN_ALIEN: 'CommonSimType' = 4
    ELDER_HUMAN_MERMAID: 'CommonSimType' = 5
    ELDER_HUMAN_WITCH: 'CommonSimType' = 6
    ELDER_HUMAN_ROBOT: 'CommonSimType' = 7
    ELDER_HUMAN_SKELETON: 'CommonSimType' = 8
    ELDER_HUMAN_PLANT_SIM: 'CommonSimType' = 9

    ADULT_HUMAN: 'CommonSimType' = 15
    ADULT_HUMAN_VAMPIRE: 'CommonSimType' = 16
    ADULT_HUMAN_GHOST: 'CommonSimType' = 17
    ADULT_HUMAN_ALIEN: 'CommonSimType' = 18
    ADULT_HUMAN_MERMAID: 'CommonSimType' = 19
    ADULT_HUMAN_WITCH: 'CommonSimType' = 20
    ADULT_HUMAN_ROBOT: 'CommonSimType' = 21
    ADULT_HUMAN_SKELETON: 'CommonSimType' = 22
    ADULT_HUMAN_PLANT_SIM: 'CommonSimType' = 23

    YOUNG_ADULT_HUMAN: 'CommonSimType' = 30
    YOUNG_ADULT_HUMAN_VAMPIRE: 'CommonSimType' = 31
    YOUNG_ADULT_HUMAN_GHOST: 'CommonSimType' = 32
    YOUNG_ADULT_HUMAN_ALIEN: 'CommonSimType' = 33
    YOUNG_ADULT_HUMAN_MERMAID: 'CommonSimType' = 34
    YOUNG_ADULT_HUMAN_WITCH: 'CommonSimType' = 35
    YOUNG_ADULT_HUMAN_ROBOT: 'CommonSimType' = 36
    YOUNG_ADULT_HUMAN_SKELETON: 'CommonSimType' = 37
    YOUNG_ADULT_HUMAN_PLANT_SIM: 'CommonSimType' = 38

    TEEN_HUMAN: 'CommonSimType' = 45
    TEEN_HUMAN_VAMPIRE: 'CommonSimType' = 46
    TEEN_HUMAN_GHOST: 'CommonSimType' = 47
    TEEN_HUMAN_ALIEN: 'CommonSimType' = 48
    TEEN_HUMAN_MERMAID: 'CommonSimType' = 49
    TEEN_HUMAN_WITCH: 'CommonSimType' = 50
    TEEN_HUMAN_ROBOT: 'CommonSimType' = 51
    TEEN_HUMAN_SKELETON: 'CommonSimType' = 52
    TEEN_HUMAN_PLANT_SIM: 'CommonSimType' = 53

    CHILD_HUMAN: 'CommonSimType' = 58
    CHILD_HUMAN_VAMPIRE: 'CommonSimType' = 59
    CHILD_HUMAN_GHOST: 'CommonSimType' = 60
    CHILD_HUMAN_ALIEN: 'CommonSimType' = 61
    CHILD_HUMAN_MERMAID: 'CommonSimType' = 62
    CHILD_HUMAN_WITCH: 'CommonSimType' = 63
    CHILD_HUMAN_ROBOT: 'CommonSimType' = 64
    CHILD_HUMAN_SKELETON: 'CommonSimType' = 65
    CHILD_HUMAN_PLANT_SIM: 'CommonSimType' = 66

    TODDLER_HUMAN: 'CommonSimType' = 70
    TODDLER_HUMAN_VAMPIRE: 'CommonSimType' = 71
    TODDLER_HUMAN_GHOST: 'CommonSimType' = 72
    TODDLER_HUMAN_ALIEN: 'CommonSimType' = 73
    TODDLER_HUMAN_MERMAID: 'CommonSimType' = 74
    TODDLER_HUMAN_WITCH: 'CommonSimType' = 75
    TODDLER_HUMAN_ROBOT: 'CommonSimType' = 76
    TODDLER_HUMAN_SKELETON: 'CommonSimType' = 77
    TODDLER_HUMAN_PLANT_SIM: 'CommonSimType' = 78

    BABY_HUMAN: 'CommonSimType' = 82
    BABY_HUMAN_VAMPIRE: 'CommonSimType' = 83
    BABY_HUMAN_GHOST: 'CommonSimType' = 84
    BABY_HUMAN_ALIEN: 'CommonSimType' = 85
    BABY_HUMAN_MERMAID: 'CommonSimType' = 86
    BABY_HUMAN_WITCH: 'CommonSimType' = 87
    BABY_HUMAN_ROBOT: 'CommonSimType' = 88
    BABY_HUMAN_SKELETON: 'CommonSimType' = 89
    BABY_HUMAN_PLANT_SIM: 'CommonSimType' = 90

    CHILD_DOG: 'CommonSimType' = 100
    CHILD_DOG_VAMPIRE: 'CommonSimType' = 101
    CHILD_DOG_GHOST: 'CommonSimType' = 102
    CHILD_DOG_ALIEN: 'CommonSimType' = 103
    CHILD_DOG_MERMAID: 'CommonSimType' = 104
    CHILD_DOG_WITCH: 'CommonSimType' = 105
    CHILD_DOG_ROBOT: 'CommonSimType' = 106
    CHILD_DOG_SKELETON: 'CommonSimType' = 107
    CHILD_DOG_PLANT_SIM: 'CommonSimType' = 108

    ELDER_SMALL_DOG: 'CommonSimType' = 200
    ELDER_SMALL_DOG_VAMPIRE: 'CommonSimType' = 201
    ELDER_SMALL_DOG_GHOST: 'CommonSimType' = 202
    ELDER_SMALL_DOG_ALIEN: 'CommonSimType' = 203
    ELDER_SMALL_DOG_MERMAID: 'CommonSimType' = 204
    ELDER_SMALL_DOG_WITCH: 'CommonSimType' = 205
    ELDER_SMALL_DOG_ROBOT: 'CommonSimType' = 206
    ELDER_SMALL_DOG_SKELETON: 'CommonSimType' = 207
    ELDER_SMALL_DOG_PLANT_SIM: 'CommonSimType' = 208

    ADULT_SMALL_DOG: 'CommonSimType' = 215
    ADULT_SMALL_DOG_VAMPIRE: 'CommonSimType' = 216
    ADULT_SMALL_DOG_GHOST: 'CommonSimType' = 217
    ADULT_SMALL_DOG_ALIEN: 'CommonSimType' = 218
    ADULT_SMALL_DOG_MERMAID: 'CommonSimType' = 219
    ADULT_SMALL_DOG_WITCH: 'CommonSimType' = 220
    ADULT_SMALL_DOG_ROBOT: 'CommonSimType' = 221
    ADULT_SMALL_DOG_SKELETON: 'CommonSimType' = 222
    ADULT_SMALL_DOG_PLANT_SIM: 'CommonSimType' = 223

    CHILD_SMALL_DOG: 'CommonSimType' = 227
    CHILD_SMALL_DOG_VAMPIRE: 'CommonSimType' = 228
    CHILD_SMALL_DOG_GHOST: 'CommonSimType' = 229
    CHILD_SMALL_DOG_ALIEN: 'CommonSimType' = 230
    CHILD_SMALL_DOG_MERMAID: 'CommonSimType' = 231
    CHILD_SMALL_DOG_WITCH: 'CommonSimType' = 232
    CHILD_SMALL_DOG_ROBOT: 'CommonSimType' = 233
    CHILD_SMALL_DOG_SKELETON: 'CommonSimType' = 234
    CHILD_SMALL_DOG_PLANT_SIM: 'CommonSimType' = 235

    ELDER_LARGE_DOG: 'CommonSimType' = 300
    ELDER_LARGE_DOG_VAMPIRE: 'CommonSimType' = 301
    ELDER_LARGE_DOG_GHOST: 'CommonSimType' = 302
    ELDER_LARGE_DOG_ALIEN: 'CommonSimType' = 303
    ELDER_LARGE_DOG_MERMAID: 'CommonSimType' = 304
    ELDER_LARGE_DOG_WITCH: 'CommonSimType' = 305
    ELDER_LARGE_DOG_ROBOT: 'CommonSimType' = 306
    ELDER_LARGE_DOG_SKELETON: 'CommonSimType' = 307
    ELDER_LARGE_DOG_PLANT_SIM: 'CommonSimType' = 308

    ADULT_LARGE_DOG: 'CommonSimType' = 315
    ADULT_LARGE_DOG_VAMPIRE: 'CommonSimType' = 316
    ADULT_LARGE_DOG_GHOST: 'CommonSimType' = 317
    ADULT_LARGE_DOG_ALIEN: 'CommonSimType' = 318
    ADULT_LARGE_DOG_MERMAID: 'CommonSimType' = 319
    ADULT_LARGE_DOG_WITCH: 'CommonSimType' = 320
    ADULT_LARGE_DOG_ROBOT: 'CommonSimType' = 321
    ADULT_LARGE_DOG_SKELETON: 'CommonSimType' = 322
    ADULT_LARGE_DOG_PLANT_SIM: 'CommonSimType' = 323

    CHILD_LARGE_DOG: 'CommonSimType' = 327
    CHILD_LARGE_DOG_VAMPIRE: 'CommonSimType' = 328
    CHILD_LARGE_DOG_GHOST: 'CommonSimType' = 329
    CHILD_LARGE_DOG_ALIEN: 'CommonSimType' = 330
    CHILD_LARGE_DOG_MERMAID: 'CommonSimType' = 331
    CHILD_LARGE_DOG_WITCH: 'CommonSimType' = 332
    CHILD_LARGE_DOG_ROBOT: 'CommonSimType' = 333
    CHILD_LARGE_DOG_SKELETON: 'CommonSimType' = 334
    CHILD_LARGE_DOG_PLANT_SIM: 'CommonSimType' = 335

    ELDER_CAT: 'CommonSimType' = 400
    ELDER_CAT_VAMPIRE: 'CommonSimType' = 401
    ELDER_CAT_GHOST: 'CommonSimType' = 402
    ELDER_CAT_ALIEN: 'CommonSimType' = 403
    ELDER_CAT_MERMAID: 'CommonSimType' = 404
    ELDER_CAT_WITCH: 'CommonSimType' = 405
    ELDER_CAT_ROBOT: 'CommonSimType' = 406
    ELDER_CAT_SKELETON: 'CommonSimType' = 407
    ELDER_CAT_PLANT_SIM: 'CommonSimType' = 408

    ADULT_CAT: 'CommonSimType' = 415
    ADULT_CAT_VAMPIRE: 'CommonSimType' = 416
    ADULT_CAT_GHOST: 'CommonSimType' = 417
    ADULT_CAT_ALIEN: 'CommonSimType' = 418
    ADULT_CAT_MERMAID: 'CommonSimType' = 419
    ADULT_CAT_WITCH: 'CommonSimType' = 420
    ADULT_CAT_ROBOT: 'CommonSimType' = 421
    ADULT_CAT_SKELETON: 'CommonSimType' = 422
    ADULT_CAT_PLANT_SIM: 'CommonSimType' = 423

    CHILD_CAT: 'CommonSimType' = 427
    CHILD_CAT_VAMPIRE: 'CommonSimType' = 428
    CHILD_CAT_GHOST: 'CommonSimType' = 429
    CHILD_CAT_ALIEN: 'CommonSimType' = 430
    CHILD_CAT_MERMAID: 'CommonSimType' = 431
    CHILD_CAT_WITCH: 'CommonSimType' = 432
    CHILD_CAT_ROBOT: 'CommonSimType' = 433
    CHILD_CAT_SKELETON: 'CommonSimType' = 434
    CHILD_CAT_PLANT_SIM: 'CommonSimType' = 435

    @staticmethod
    def get_all(include_teen_young_adult_and_elder: bool=False, include_baby: bool=False, include_separate_child_dog_types: bool=False) -> Tuple['CommonSimType']:
        """get_all(include_teen_young_adult_and_elder=False, include_baby=False, include_separate_child_dog_types=False)

        Retrieve a collection of all Sim Types.

        :param include_teen_young_adult_and_elder: If set to True, the TEEN, YOUNG_ADULT, and ELDER Sim Types will be returned. If False, they will be excluded. Default is False.
        :type include_teen_young_adult_and_elder: bool, optional
        :param include_baby: If set to True, the BABY Sim Type will be included in the result. If False, the BABY Sim Type will not be included. Default is False.
        :type include_baby: bool, optional
        :param include_separate_child_dog_types: If set to True, the Child Dog Sim Types (CHILD_LARGE_DOG, CHILD_SMALL_DOG, etc.) will be included in the result. If False, they will not be included. Default is False.
        :type include_separate_child_dog_types: bool, optional
        :return: A collection of all Sim Types.
        :rtype: Tuple[CommonSimType]
        """
        sim_types: Tuple[CommonSimType] = (
            CommonSimType.ADULT_HUMAN,
            CommonSimType.ADULT_HUMAN_VAMPIRE,
            CommonSimType.ADULT_HUMAN_GHOST,
            CommonSimType.ADULT_HUMAN_ALIEN,
            CommonSimType.ADULT_HUMAN_MERMAID,
            CommonSimType.ADULT_HUMAN_WITCH,
            CommonSimType.ADULT_HUMAN_ROBOT,
            CommonSimType.ADULT_HUMAN_SKELETON,
            CommonSimType.ADULT_HUMAN_PLANT_SIM,

            CommonSimType.CHILD_HUMAN,
            CommonSimType.CHILD_HUMAN_VAMPIRE,
            CommonSimType.CHILD_HUMAN_GHOST,
            CommonSimType.CHILD_HUMAN_ALIEN,
            CommonSimType.CHILD_HUMAN_MERMAID,
            CommonSimType.CHILD_HUMAN_WITCH,
            CommonSimType.CHILD_HUMAN_ROBOT,
            CommonSimType.CHILD_HUMAN_SKELETON,
            CommonSimType.CHILD_HUMAN_PLANT_SIM,

            CommonSimType.TODDLER_HUMAN,
            CommonSimType.TODDLER_HUMAN_VAMPIRE,
            CommonSimType.TODDLER_HUMAN_GHOST,
            CommonSimType.TODDLER_HUMAN_ALIEN,
            CommonSimType.TODDLER_HUMAN_MERMAID,
            CommonSimType.TODDLER_HUMAN_WITCH,
            CommonSimType.TODDLER_HUMAN_ROBOT,
            CommonSimType.TODDLER_HUMAN_SKELETON,
            CommonSimType.TODDLER_HUMAN_PLANT_SIM,

            CommonSimType.ADULT_SMALL_DOG,
            CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
            CommonSimType.ADULT_SMALL_DOG_GHOST,
            CommonSimType.ADULT_SMALL_DOG_ALIEN,
            CommonSimType.ADULT_SMALL_DOG_MERMAID,
            CommonSimType.ADULT_SMALL_DOG_WITCH,
            CommonSimType.ADULT_SMALL_DOG_ROBOT,
            CommonSimType.ADULT_SMALL_DOG_SKELETON,
            CommonSimType.ADULT_SMALL_DOG_PLANT_SIM,

            CommonSimType.ADULT_LARGE_DOG,
            CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
            CommonSimType.ADULT_LARGE_DOG_GHOST,
            CommonSimType.ADULT_LARGE_DOG_ALIEN,
            CommonSimType.ADULT_LARGE_DOG_MERMAID,
            CommonSimType.ADULT_LARGE_DOG_WITCH,
            CommonSimType.ADULT_LARGE_DOG_ROBOT,
            CommonSimType.ADULT_LARGE_DOG_SKELETON,
            CommonSimType.ADULT_LARGE_DOG_PLANT_SIM,

            CommonSimType.ADULT_CAT,
            CommonSimType.ADULT_CAT_VAMPIRE,
            CommonSimType.ADULT_CAT_GHOST,
            CommonSimType.ADULT_CAT_ALIEN,
            CommonSimType.ADULT_CAT_MERMAID,
            CommonSimType.ADULT_CAT_WITCH,
            CommonSimType.ADULT_CAT_ROBOT,
            CommonSimType.ADULT_CAT_SKELETON,
            CommonSimType.ADULT_CAT_PLANT_SIM,

            CommonSimType.CHILD_CAT,
            CommonSimType.CHILD_CAT_VAMPIRE,
            CommonSimType.CHILD_CAT_GHOST,
            CommonSimType.CHILD_CAT_ALIEN,
            CommonSimType.CHILD_CAT_MERMAID,
            CommonSimType.CHILD_CAT_WITCH,
            CommonSimType.CHILD_CAT_ROBOT,
            CommonSimType.CHILD_CAT_SKELETON,
            CommonSimType.CHILD_CAT_PLANT_SIM,

            CommonSimType.CHILD_DOG,
            CommonSimType.CHILD_DOG_VAMPIRE,
            CommonSimType.CHILD_DOG_GHOST,
            CommonSimType.CHILD_DOG_ALIEN,
            CommonSimType.CHILD_DOG_MERMAID,
            CommonSimType.CHILD_DOG_WITCH,
            CommonSimType.CHILD_DOG_ROBOT,
            CommonSimType.CHILD_DOG_SKELETON,
            CommonSimType.CHILD_DOG_PLANT_SIM,
        )
        if include_teen_young_adult_and_elder:
            sim_types: Tuple[CommonSimType] = (
                *sim_types,
                CommonSimType.ELDER_HUMAN,
                CommonSimType.ELDER_HUMAN_VAMPIRE,
                CommonSimType.ELDER_HUMAN_GHOST,
                CommonSimType.ELDER_HUMAN_ALIEN,
                CommonSimType.ELDER_HUMAN_MERMAID,
                CommonSimType.ELDER_HUMAN_WITCH,
                CommonSimType.ELDER_HUMAN_ROBOT,
                CommonSimType.ELDER_HUMAN_SKELETON,
                CommonSimType.ELDER_HUMAN_PLANT_SIM,

                CommonSimType.YOUNG_ADULT_HUMAN,
                CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE,
                CommonSimType.YOUNG_ADULT_HUMAN_GHOST,
                CommonSimType.YOUNG_ADULT_HUMAN_ALIEN,
                CommonSimType.YOUNG_ADULT_HUMAN_MERMAID,
                CommonSimType.YOUNG_ADULT_HUMAN_WITCH,
                CommonSimType.YOUNG_ADULT_HUMAN_ROBOT,
                CommonSimType.YOUNG_ADULT_HUMAN_SKELETON,
                CommonSimType.YOUNG_ADULT_HUMAN_PLANT_SIM,

                CommonSimType.TEEN_HUMAN,
                CommonSimType.TEEN_HUMAN_VAMPIRE,
                CommonSimType.TEEN_HUMAN_GHOST,
                CommonSimType.TEEN_HUMAN_ALIEN,
                CommonSimType.TEEN_HUMAN_MERMAID,
                CommonSimType.TEEN_HUMAN_WITCH,
                CommonSimType.TEEN_HUMAN_ROBOT,
                CommonSimType.TEEN_HUMAN_SKELETON,
                CommonSimType.TEEN_HUMAN_PLANT_SIM,

                CommonSimType.ELDER_SMALL_DOG,
                CommonSimType.ELDER_SMALL_DOG_VAMPIRE,
                CommonSimType.ELDER_SMALL_DOG_GHOST,
                CommonSimType.ELDER_SMALL_DOG_ALIEN,
                CommonSimType.ELDER_SMALL_DOG_MERMAID,
                CommonSimType.ELDER_SMALL_DOG_WITCH,
                CommonSimType.ELDER_SMALL_DOG_ROBOT,
                CommonSimType.ELDER_SMALL_DOG_SKELETON,
                CommonSimType.ELDER_SMALL_DOG_PLANT_SIM,

                CommonSimType.ELDER_LARGE_DOG,
                CommonSimType.ELDER_LARGE_DOG_VAMPIRE,
                CommonSimType.ELDER_LARGE_DOG_GHOST,
                CommonSimType.ELDER_LARGE_DOG_ALIEN,
                CommonSimType.ELDER_LARGE_DOG_MERMAID,
                CommonSimType.ELDER_LARGE_DOG_WITCH,
                CommonSimType.ELDER_LARGE_DOG_ROBOT,
                CommonSimType.ELDER_LARGE_DOG_SKELETON,
                CommonSimType.ELDER_LARGE_DOG_PLANT_SIM,

                CommonSimType.ELDER_CAT,
                CommonSimType.ELDER_CAT_VAMPIRE,
                CommonSimType.ELDER_CAT_GHOST,
                CommonSimType.ELDER_CAT_ALIEN,
                CommonSimType.ELDER_CAT_MERMAID,
                CommonSimType.ELDER_CAT_WITCH,
                CommonSimType.ELDER_CAT_ROBOT,
                CommonSimType.ELDER_CAT_SKELETON,
                CommonSimType.ELDER_CAT_PLANT_SIM,
            )
        if include_baby:
            sim_types: Tuple[CommonSimType] = (
                *sim_types,
                CommonSimType.BABY_HUMAN,
                CommonSimType.BABY_HUMAN_VAMPIRE,
                CommonSimType.BABY_HUMAN_GHOST,
                CommonSimType.BABY_HUMAN_ALIEN,
                CommonSimType.BABY_HUMAN_MERMAID,
                CommonSimType.BABY_HUMAN_WITCH,
                CommonSimType.BABY_HUMAN_ROBOT,
                CommonSimType.BABY_HUMAN_SKELETON,
                CommonSimType.BABY_HUMAN_PLANT_SIM
            )
        if include_separate_child_dog_types:
            sim_types: Tuple[CommonSimType] = (
                *sim_types,
                CommonSimType.CHILD_SMALL_DOG,
                CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
                CommonSimType.CHILD_SMALL_DOG_GHOST,
                CommonSimType.CHILD_SMALL_DOG_ALIEN,
                CommonSimType.CHILD_SMALL_DOG_MERMAID,
                CommonSimType.CHILD_SMALL_DOG_WITCH,
                CommonSimType.CHILD_SMALL_DOG_ROBOT,
                CommonSimType.CHILD_SMALL_DOG_SKELETON,
                CommonSimType.CHILD_SMALL_DOG_PLANT_SIM,

                CommonSimType.CHILD_LARGE_DOG,
                CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
                CommonSimType.CHILD_LARGE_DOG_GHOST,
                CommonSimType.CHILD_LARGE_DOG_ALIEN,
                CommonSimType.CHILD_LARGE_DOG_MERMAID,
                CommonSimType.CHILD_LARGE_DOG_WITCH,
                CommonSimType.CHILD_LARGE_DOG_ROBOT,
                CommonSimType.CHILD_LARGE_DOG_SKELETON,
                CommonSimType.CHILD_LARGE_DOG_PLANT_SIM,
            )
        return sim_types
