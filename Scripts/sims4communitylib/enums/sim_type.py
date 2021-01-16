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

    ADULT_HUMAN: 'CommonSimType' = 8
    ADULT_HUMAN_VAMPIRE: 'CommonSimType' = 9
    ADULT_HUMAN_GHOST: 'CommonSimType' = 10
    ADULT_HUMAN_ALIEN: 'CommonSimType' = 11
    ADULT_HUMAN_MERMAID: 'CommonSimType' = 12
    ADULT_HUMAN_WITCH: 'CommonSimType' = 13
    ADULT_HUMAN_ROBOT: 'CommonSimType' = 14

    YOUNG_ADULT_HUMAN: 'CommonSimType' = 15
    YOUNG_ADULT_HUMAN_VAMPIRE: 'CommonSimType' = 16
    YOUNG_ADULT_HUMAN_GHOST: 'CommonSimType' = 17
    YOUNG_ADULT_HUMAN_ALIEN: 'CommonSimType' = 18
    YOUNG_ADULT_HUMAN_MERMAID: 'CommonSimType' = 19
    YOUNG_ADULT_HUMAN_WITCH: 'CommonSimType' = 20
    YOUNG_ADULT_HUMAN_ROBOT: 'CommonSimType' = 21

    TEEN_HUMAN: 'CommonSimType' = 22
    TEEN_HUMAN_VAMPIRE: 'CommonSimType' = 23
    TEEN_HUMAN_GHOST: 'CommonSimType' = 24
    TEEN_HUMAN_ALIEN: 'CommonSimType' = 25
    TEEN_HUMAN_MERMAID: 'CommonSimType' = 26
    TEEN_HUMAN_WITCH: 'CommonSimType' = 27
    TEEN_HUMAN_ROBOT: 'CommonSimType' = 28

    CHILD_HUMAN: 'CommonSimType' = 29
    CHILD_HUMAN_VAMPIRE: 'CommonSimType' = 30
    CHILD_HUMAN_GHOST: 'CommonSimType' = 31
    CHILD_HUMAN_ALIEN: 'CommonSimType' = 32
    CHILD_HUMAN_MERMAID: 'CommonSimType' = 33
    CHILD_HUMAN_WITCH: 'CommonSimType' = 34
    CHILD_HUMAN_ROBOT: 'CommonSimType' = 35

    TODDLER_HUMAN: 'CommonSimType' = 36
    TODDLER_HUMAN_VAMPIRE: 'CommonSimType' = 37
    TODDLER_HUMAN_GHOST: 'CommonSimType' = 38
    TODDLER_HUMAN_ALIEN: 'CommonSimType' = 39
    TODDLER_HUMAN_MERMAID: 'CommonSimType' = 40
    TODDLER_HUMAN_WITCH: 'CommonSimType' = 41
    TODDLER_HUMAN_ROBOT: 'CommonSimType' = 42

    BABY_HUMAN: 'CommonSimType' = 43
    BABY_HUMAN_VAMPIRE: 'CommonSimType' = 44
    BABY_HUMAN_GHOST: 'CommonSimType' = 45
    BABY_HUMAN_ALIEN: 'CommonSimType' = 46
    BABY_HUMAN_MERMAID: 'CommonSimType' = 47
    BABY_HUMAN_WITCH: 'CommonSimType' = 48
    BABY_HUMAN_ROBOT: 'CommonSimType' = 49

    ELDER_SMALL_DOG: 'CommonSimType' = 200
    ELDER_SMALL_DOG_VAMPIRE: 'CommonSimType' = 201
    ELDER_SMALL_DOG_GHOST: 'CommonSimType' = 202
    ELDER_SMALL_DOG_ALIEN: 'CommonSimType' = 203
    ELDER_SMALL_DOG_MERMAID: 'CommonSimType' = 204
    ELDER_SMALL_DOG_WITCH: 'CommonSimType' = 205
    ELDER_SMALL_DOG_ROBOT: 'CommonSimType' = 206

    ADULT_SMALL_DOG: 'CommonSimType' = 207
    ADULT_SMALL_DOG_VAMPIRE: 'CommonSimType' = 208
    ADULT_SMALL_DOG_GHOST: 'CommonSimType' = 209
    ADULT_SMALL_DOG_ALIEN: 'CommonSimType' = 210
    ADULT_SMALL_DOG_MERMAID: 'CommonSimType' = 211
    ADULT_SMALL_DOG_WITCH: 'CommonSimType' = 212
    ADULT_SMALL_DOG_ROBOT: 'CommonSimType' = 213

    CHILD_SMALL_DOG: 'CommonSimType' = 214
    CHILD_SMALL_DOG_VAMPIRE: 'CommonSimType' = 215
    CHILD_SMALL_DOG_GHOST: 'CommonSimType' = 216
    CHILD_SMALL_DOG_ALIEN: 'CommonSimType' = 217
    CHILD_SMALL_DOG_MERMAID: 'CommonSimType' = 218
    CHILD_SMALL_DOG_WITCH: 'CommonSimType' = 219
    CHILD_SMALL_DOG_ROBOT: 'CommonSimType' = 220

    ELDER_LARGE_DOG: 'CommonSimType' = 300
    ELDER_LARGE_DOG_VAMPIRE: 'CommonSimType' = 301
    ELDER_LARGE_DOG_GHOST: 'CommonSimType' = 302
    ELDER_LARGE_DOG_ALIEN: 'CommonSimType' = 303
    ELDER_LARGE_DOG_MERMAID: 'CommonSimType' = 304
    ELDER_LARGE_DOG_WITCH: 'CommonSimType' = 305
    ELDER_LARGE_DOG_ROBOT: 'CommonSimType' = 306

    ADULT_LARGE_DOG: 'CommonSimType' = 307
    ADULT_LARGE_DOG_VAMPIRE: 'CommonSimType' = 308
    ADULT_LARGE_DOG_GHOST: 'CommonSimType' = 309
    ADULT_LARGE_DOG_ALIEN: 'CommonSimType' = 310
    ADULT_LARGE_DOG_MERMAID: 'CommonSimType' = 311
    ADULT_LARGE_DOG_WITCH: 'CommonSimType' = 312
    ADULT_LARGE_DOG_ROBOT: 'CommonSimType' = 313

    CHILD_LARGE_DOG: 'CommonSimType' = 314
    CHILD_LARGE_DOG_VAMPIRE: 'CommonSimType' = 315
    CHILD_LARGE_DOG_GHOST: 'CommonSimType' = 316
    CHILD_LARGE_DOG_ALIEN: 'CommonSimType' = 317
    CHILD_LARGE_DOG_MERMAID: 'CommonSimType' = 318
    CHILD_LARGE_DOG_WITCH: 'CommonSimType' = 319
    CHILD_LARGE_DOG_ROBOT: 'CommonSimType' = 320

    ELDER_CAT: 'CommonSimType' = 400
    ELDER_CAT_VAMPIRE: 'CommonSimType' = 401
    ELDER_CAT_GHOST: 'CommonSimType' = 402
    ELDER_CAT_ALIEN: 'CommonSimType' = 403
    ELDER_CAT_MERMAID: 'CommonSimType' = 404
    ELDER_CAT_WITCH: 'CommonSimType' = 405
    ELDER_CAT_ROBOT: 'CommonSimType' = 406

    ADULT_CAT: 'CommonSimType' = 407
    ADULT_CAT_VAMPIRE: 'CommonSimType' = 408
    ADULT_CAT_GHOST: 'CommonSimType' = 409
    ADULT_CAT_ALIEN: 'CommonSimType' = 410
    ADULT_CAT_MERMAID: 'CommonSimType' = 411
    ADULT_CAT_WITCH: 'CommonSimType' = 412
    ADULT_CAT_ROBOT: 'CommonSimType' = 413

    CHILD_CAT: 'CommonSimType' = 414
    CHILD_CAT_VAMPIRE: 'CommonSimType' = 415
    CHILD_CAT_GHOST: 'CommonSimType' = 416
    CHILD_CAT_ALIEN: 'CommonSimType' = 417
    CHILD_CAT_MERMAID: 'CommonSimType' = 418
    CHILD_CAT_WITCH: 'CommonSimType' = 419
    CHILD_CAT_ROBOT: 'CommonSimType' = 420

    @staticmethod
    def get_all(include_teen_young_adult_and_elder: bool=False, include_baby: bool=False) -> Tuple['CommonSimType']:
        """get_all(include_teen_young_adult_and_elder=False, include_baby=False)

        Retrieve a collection of all Sim Types.

        :param include_teen_young_adult_and_elder: If set to True, the TEEN, YOUNG_ADULT, and ELDER Sim Types will be returned. If False, they will be excluded. Default is False.
        :type include_teen_young_adult_and_elder: bool, optional
        :param include_baby: If set to True, the BABY Sim Type will be included in the result. If False, the BABY Sim Type will not be included. Default is False.
        :type include_baby: bool, optional
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

            CommonSimType.CHILD_HUMAN,
            CommonSimType.CHILD_HUMAN_VAMPIRE,
            CommonSimType.CHILD_HUMAN_GHOST,
            CommonSimType.CHILD_HUMAN_ALIEN,
            CommonSimType.CHILD_HUMAN_MERMAID,
            CommonSimType.CHILD_HUMAN_WITCH,
            CommonSimType.CHILD_HUMAN_ROBOT,

            CommonSimType.TODDLER_HUMAN,
            CommonSimType.TODDLER_HUMAN_VAMPIRE,
            CommonSimType.TODDLER_HUMAN_GHOST,
            CommonSimType.TODDLER_HUMAN_ALIEN,
            CommonSimType.TODDLER_HUMAN_MERMAID,
            CommonSimType.TODDLER_HUMAN_WITCH,
            CommonSimType.TODDLER_HUMAN_ROBOT,

            CommonSimType.ADULT_SMALL_DOG,
            CommonSimType.ADULT_SMALL_DOG_VAMPIRE,
            CommonSimType.ADULT_SMALL_DOG_GHOST,
            CommonSimType.ADULT_SMALL_DOG_ALIEN,
            CommonSimType.ADULT_SMALL_DOG_MERMAID,
            CommonSimType.ADULT_SMALL_DOG_WITCH,
            CommonSimType.ADULT_SMALL_DOG_ROBOT,

            CommonSimType.CHILD_SMALL_DOG,
            CommonSimType.CHILD_SMALL_DOG_VAMPIRE,
            CommonSimType.CHILD_SMALL_DOG_GHOST,
            CommonSimType.CHILD_SMALL_DOG_ALIEN,
            CommonSimType.CHILD_SMALL_DOG_MERMAID,
            CommonSimType.CHILD_SMALL_DOG_WITCH,
            CommonSimType.CHILD_SMALL_DOG_ROBOT,

            CommonSimType.ADULT_LARGE_DOG,
            CommonSimType.ADULT_LARGE_DOG_VAMPIRE,
            CommonSimType.ADULT_LARGE_DOG_GHOST,
            CommonSimType.ADULT_LARGE_DOG_ALIEN,
            CommonSimType.ADULT_LARGE_DOG_MERMAID,
            CommonSimType.ADULT_LARGE_DOG_WITCH,
            CommonSimType.ADULT_LARGE_DOG_ROBOT,

            CommonSimType.CHILD_LARGE_DOG,
            CommonSimType.CHILD_LARGE_DOG_VAMPIRE,
            CommonSimType.CHILD_LARGE_DOG_GHOST,
            CommonSimType.CHILD_LARGE_DOG_ALIEN,
            CommonSimType.CHILD_LARGE_DOG_MERMAID,
            CommonSimType.CHILD_LARGE_DOG_WITCH,
            CommonSimType.CHILD_LARGE_DOG_ROBOT,

            CommonSimType.ADULT_CAT,
            CommonSimType.ADULT_CAT_VAMPIRE,
            CommonSimType.ADULT_CAT_GHOST,
            CommonSimType.ADULT_CAT_ALIEN,
            CommonSimType.ADULT_CAT_MERMAID,
            CommonSimType.ADULT_CAT_WITCH,
            CommonSimType.ADULT_CAT_ROBOT,

            CommonSimType.CHILD_CAT,
            CommonSimType.CHILD_CAT_VAMPIRE,
            CommonSimType.CHILD_CAT_GHOST,
            CommonSimType.CHILD_CAT_ALIEN,
            CommonSimType.CHILD_CAT_MERMAID,
            CommonSimType.CHILD_CAT_WITCH,
            CommonSimType.CHILD_CAT_ROBOT,
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

                CommonSimType.YOUNG_ADULT_HUMAN,
                CommonSimType.YOUNG_ADULT_HUMAN_VAMPIRE,
                CommonSimType.YOUNG_ADULT_HUMAN_GHOST,
                CommonSimType.YOUNG_ADULT_HUMAN_ALIEN,
                CommonSimType.YOUNG_ADULT_HUMAN_MERMAID,
                CommonSimType.YOUNG_ADULT_HUMAN_WITCH,
                CommonSimType.YOUNG_ADULT_HUMAN_ROBOT,

                CommonSimType.TEEN_HUMAN,
                CommonSimType.TEEN_HUMAN_VAMPIRE,
                CommonSimType.TEEN_HUMAN_GHOST,
                CommonSimType.TEEN_HUMAN_ALIEN,
                CommonSimType.TEEN_HUMAN_MERMAID,
                CommonSimType.TEEN_HUMAN_WITCH,
                CommonSimType.TEEN_HUMAN_ROBOT,

                CommonSimType.ELDER_SMALL_DOG,
                CommonSimType.ELDER_SMALL_DOG_VAMPIRE,
                CommonSimType.ELDER_SMALL_DOG_GHOST,
                CommonSimType.ELDER_SMALL_DOG_ALIEN,
                CommonSimType.ELDER_SMALL_DOG_MERMAID,
                CommonSimType.ELDER_SMALL_DOG_WITCH,
                CommonSimType.ELDER_SMALL_DOG_ROBOT,

                CommonSimType.ELDER_LARGE_DOG,
                CommonSimType.ELDER_LARGE_DOG_VAMPIRE,
                CommonSimType.ELDER_LARGE_DOG_GHOST,
                CommonSimType.ELDER_LARGE_DOG_ALIEN,
                CommonSimType.ELDER_LARGE_DOG_MERMAID,
                CommonSimType.ELDER_LARGE_DOG_WITCH,
                CommonSimType.ELDER_LARGE_DOG_ROBOT,

                CommonSimType.ELDER_CAT,
                CommonSimType.ELDER_CAT_VAMPIRE,
                CommonSimType.ELDER_CAT_GHOST,
                CommonSimType.ELDER_CAT_ALIEN,
                CommonSimType.ELDER_CAT_MERMAID,
                CommonSimType.ELDER_CAT_WITCH,
                CommonSimType.ELDER_CAT_ROBOT,
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
                CommonSimType.BABY_HUMAN_ROBOT
            )
        return sim_types
