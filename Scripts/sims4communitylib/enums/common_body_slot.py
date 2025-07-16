"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple

from sims.outfits.outfit_enums import BodyType
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags


class CommonBodySlot(CommonIntFlags):
    """Slots on the body of Sims that CAS Parts can be attached to."""
    NONE: 'CommonBodySlot' = 0
    ACNE: 'CommonBodySlot' = 72
    ATTACHMENT_BACK: 'CommonBodySlot' = 88
    BIRTHMARK_ARMS: 'CommonBodySlot' = 94
    BIRTHMARK_FACE: 'CommonBodySlot' = 91
    BIRTHMARK_LEGS: 'CommonBodySlot' = 98
    BIRTHMARK_TORSO_BACK: 'CommonBodySlot' = 92
    BIRTHMARK_TORSO_FRONT: 'CommonBodySlot' = 93
    BITE: 'CommonBodySlot' = 76
    BLANKET: 'CommonBodySlot' = 104
    BLUSH: 'CommonBodySlot' = 32
    BODY_FRECKLES: 'CommonBodySlot' = 77
    BODY_HAIR_ARM: 'CommonBodySlot' = 78
    BODY_HAIR_LEG: 'CommonBodySlot' = 79
    BODY_HAIR_TORSO_BACK: 'CommonBodySlot' = 81
    BODY_HAIR_TORSO_FRONT: 'CommonBodySlot' = 80
    BODY_SCAR_ARM_LEFT: 'CommonBodySlot' = 82
    BODY_SCAR_ARM_RIGHT: 'CommonBodySlot' = 83
    BODY_SCAR_LEG_LEFT: 'CommonBodySlot' = 86
    BODY_SCAR_LEG_RIGHT: 'CommonBodySlot' = 87
    BODY_SCAR_TORSO_BACK: 'CommonBodySlot' = 85
    BODY_SCAR_TORSO_FRONT: 'CommonBodySlot' = 84
    BRIDLE: 'CommonBodySlot' = 102
    BROW_RING_LEFT: 'CommonBodySlot' = 20
    BROW_RING_RIGHT: 'CommonBodySlot' = 21
    CUMMERBUND: 'CommonBodySlot' = 9
    EARRINGS: 'CommonBodySlot' = 10
    EARS: 'CommonBodySlot' = 60
    EYE_COLOR: 'CommonBodySlot' = 35
    EYE_COLOR_SECONDARY: 'CommonBodySlot' = 63
    EYE_LINER: 'CommonBodySlot' = 31
    EYE_SHADOW: 'CommonBodySlot' = 30
    EYEBROWS: 'CommonBodySlot' = 34
    FACE_PAINT: 'CommonBodySlot' = 33
    FACE_SCAR: 'CommonBodySlot' = 90
    FACIAL_HAIR: 'CommonBodySlot' = 28
    FINGERNAIL: 'CommonBodySlot' = 73
    FOREARM_SCAR: 'CommonBodySlot' = 71
    FULL_BODY: 'CommonBodySlot' = 5
    FUR_BODY: 'CommonBodySlot' = 59
    GLASSES: 'CommonBodySlot' = 11
    GLOVES: 'CommonBodySlot' = 13
    HAIR: 'CommonBodySlot' = 2
    HAIR_COLOR_OVERRIDE: 'CommonBodySlot' = 75
    HAIR_FEATHERS: 'CommonBodySlot' = 109
    HAIR_FORELOCK: 'CommonBodySlot' = 108
    HAIR_MANE: 'CommonBodySlot' = 106
    HAIR_TAIL: 'CommonBodySlot' = 107
    HAT: 'CommonBodySlot' = 1
    HEAD: 'CommonBodySlot' = 3
    HORN: 'CommonBodySlot' = 110
    INDEX_FINGER_LEFT: 'CommonBodySlot' = 22
    INDEX_FINGER_RIGHT: 'CommonBodySlot' = 23
    LIP_RING_LEFT: 'CommonBodySlot' = 16
    LIP_RING_RIGHT: 'CommonBodySlot' = 17
    LIPSTICK: 'CommonBodySlot' = 29
    LOWER_BODY: 'CommonBodySlot' = 7
    EYELASHES: 'CommonBodySlot' = 37
    MIDDLE_FINGER_LEFT: 'CommonBodySlot' = 26
    MIDDLE_FINGER_RIGHT: 'CommonBodySlot' = 27
    MOLE_BACK_UPPER: 'CommonBodySlot' = 97
    MOLE_CHEST_UPPER: 'CommonBodySlot' = 96
    MOLE_FACE: 'CommonBodySlot' = 95
    NECKLACE: 'CommonBodySlot' = 12
    NOSE_RING_LEFT: 'CommonBodySlot' = 18
    NOSE_RING_RIGHT: 'CommonBodySlot' = 19
    OCCULT_BROW: 'CommonBodySlot' = 64
    OCCULT_EYE_SOCKET: 'CommonBodySlot' = 65
    OCCULT_EYELID: 'CommonBodySlot' = 66
    OCCULT_LEFT_CHEEK: 'CommonBodySlot' = 68
    OCCULT_MOUTH: 'CommonBodySlot' = 67
    OCCULT_NECK_SCAR: 'CommonBodySlot' = 70
    OCCULT_RIGHT_CHEEK: 'CommonBodySlot' = 69
    REINS: 'CommonBodySlot' = 103
    RING_FINGER_LEFT: 'CommonBodySlot' = 24
    RING_FINGER_RIGHT: 'CommonBodySlot' = 25
    SADDLE: 'CommonBodySlot' = 101
    SHOES: 'CommonBodySlot' = 8
    SKIN_DETAIL_ACNE_PUBERTY: 'CommonBodySlot' = 89
    SKIN_DETAIL_CREASE_FOREHEAD: 'CommonBodySlot' = 38
    SKIN_DETAIL_CREASE_MOUTH: 'CommonBodySlot' = 57
    SKIN_DETAIL_DIMPLE_LEFT: 'CommonBodySlot' = 40
    SKIN_DETAIL_DIMPLE_RIGHT: 'CommonBodySlot' = 41
    SKIN_DETAIL_FRECKLES: 'CommonBodySlot' = 39
    SKIN_DETAIL_HOOF_COLOR: 'CommonBodySlot' = 105
    SKIN_DETAIL_MOLE_CHEEK_LEFT: 'CommonBodySlot' = 55
    SKIN_DETAIL_MOLE_CHEEK_RIGHT: 'CommonBodySlot' = 56
    SKIN_DETAIL_MOLE_LIP_LEFT: 'CommonBodySlot' = 43
    SKIN_DETAIL_MOLE_LIP_RIGHT: 'CommonBodySlot' = 44
    SKIN_DETAIL_NOSE_COLOR: 'CommonBodySlot' = 62
    SKIN_OVERLAY: 'CommonBodySlot' = 58
    SOCKS: 'CommonBodySlot' = 36
    STRETCH_MARKS_BACK: 'CommonBodySlot' = 100
    STRETCH_MARKS_FRONT: 'CommonBodySlot' = 99
    TAIL: 'CommonBodySlot' = 61
    TAIL_BASE: 'CommonBodySlot' = 111
    TATTOO_ARM_LOWER_LEFT: 'CommonBodySlot' = 45
    TATTOO_ARM_LOWER_RIGHT: 'CommonBodySlot' = 47
    TATTOO_ARM_UPPER_LEFT: 'CommonBodySlot' = 46
    TATTOO_ARM_UPPER_RIGHT: 'CommonBodySlot' = 48
    TATTOO_LEG_LEFT: 'CommonBodySlot' = 49
    TATTOO_LEG_RIGHT: 'CommonBodySlot' = 50
    TATTOO_TORSO_BACK_LOWER: 'CommonBodySlot' = 51
    TATTOO_TORSO_BACK_UPPER: 'CommonBodySlot' = 52
    TATTOO_TORSO_FRONT_LOWER: 'CommonBodySlot' = 53
    TATTOO_TORSO_FRONT_UPPER: 'CommonBodySlot' = 54
    TEETH: 'CommonBodySlot' = 4
    TIGHTS: 'CommonBodySlot' = 42
    TOENAIL: 'CommonBodySlot' = 74
    UPPER_BODY: 'CommonBodySlot' = 6
    WRIST_LEFT: 'CommonBodySlot' = 14
    WRIST_RIGHT: 'CommonBodySlot' = 15
    WINGS: 'CommonBodySlot' = 114
    HEAD_DECORATION = 115
    SKIN_SPECULARITY = 116

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonBodySlot'] = None) -> Tuple['CommonBodySlot']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBodySlot], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonBodySlot]
        """
        if exclude_values is None:
            exclude_values = (cls.NONE,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonBodySlot, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonBodySlot'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBodySlot], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonBodySlot'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonBodySlot], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: Union['CommonBodySlot', BodyType, int]) -> Union[BodyType, 'CommonBodySlot', int]:
        """convert_to_vanilla(value)

        Convert a CommonBodySlot into the vanilla BodyType enum.

        :param value: An instance of a CommonBodySlot
        :type value: CommonBodySlot
        :return: The specified CommonBodySlot translated to a BodyType or the value itself if the CommonBodySlot could not be translated.
        :rtype: Union[BodyType, int]
        """
        if value is None or value == CommonBodySlot.NONE:
            return BodyType.NONE
        if isinstance(value, BodyType):
            return value
        mapping = dict()
        if hasattr(BodyType, 'ACNE'):
            mapping[CommonBodySlot.ACNE] = BodyType.ACNE
        if hasattr(BodyType, 'ATTACHMENT_BACK'):
            mapping[CommonBodySlot.ATTACHMENT_BACK] = BodyType.ATTACHMENT_BACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKARMS'):
            mapping[CommonBodySlot.BIRTHMARK_ARMS] = BodyType.BIRTHMARKARMS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKFACE'):
            mapping[CommonBodySlot.BIRTHMARK_FACE] = BodyType.BIRTHMARKFACE
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKLEGS'):
            mapping[CommonBodySlot.BIRTHMARK_LEGS] = BodyType.BIRTHMARKLEGS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKTORSOBACK'):
            mapping[CommonBodySlot.BIRTHMARK_TORSO_BACK] = BodyType.BIRTHMARKTORSOBACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKTORSOFRONT'):
            mapping[CommonBodySlot.BIRTHMARK_TORSO_FRONT] = BodyType.BIRTHMARKTORSOFRONT
        if hasattr(BodyType, 'BITE'):
            mapping[CommonBodySlot.BITE] = BodyType.BITE
        if hasattr(BodyType, 'BLANKET'):
            mapping[CommonBodySlot.BLANKET] = BodyType.BLANKET
        if hasattr(BodyType, 'BLUSH'):
            mapping[CommonBodySlot.BLUSH] = BodyType.BLUSH
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYFRECKLES'):
            mapping[CommonBodySlot.BODY_FRECKLES] = BodyType.BODYFRECKLES
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_ARM'):
            mapping[CommonBodySlot.BODY_HAIR_ARM] = BodyType.BODYHAIR_ARM
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_LEG'):
            mapping[CommonBodySlot.BODY_HAIR_LEG] = BodyType.BODYHAIR_LEG
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_TORSOBACK'):
            mapping[CommonBodySlot.BODY_HAIR_TORSO_BACK] = BodyType.BODYHAIR_TORSOBACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_TORSOFRONT'):
            mapping[CommonBodySlot.BODY_HAIR_TORSO_FRONT] = BodyType.BODYHAIR_TORSOFRONT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_ARMLEFT'):
            mapping[CommonBodySlot.BODY_SCAR_ARM_LEFT] = BodyType.BODYSCAR_ARMLEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_ARMRIGHT'):
            mapping[CommonBodySlot.BODY_SCAR_ARM_RIGHT] = BodyType.BODYSCAR_ARMRIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_LEGLEFT'):
            mapping[CommonBodySlot.BODY_SCAR_LEG_LEFT] = BodyType.BODYSCAR_LEGLEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_LEGRIGHT'):
            mapping[CommonBodySlot.BODY_SCAR_LEG_RIGHT] = BodyType.BODYSCAR_LEGRIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_TORSOBACK'):
            mapping[CommonBodySlot.BODY_SCAR_TORSO_BACK] = BodyType.BODYSCAR_TORSOBACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_TORSOFRONT'):
            mapping[CommonBodySlot.BODY_SCAR_TORSO_FRONT] = BodyType.BODYSCAR_TORSOFRONT
        if hasattr(BodyType, 'BRIDLE'):
            mapping[CommonBodySlot.BRIDLE] = BodyType.BRIDLE
        if hasattr(BodyType, 'BROW_RING_LEFT'):
            mapping[CommonBodySlot.BROW_RING_LEFT] = BodyType.BROW_RING_LEFT
        if hasattr(BodyType, 'BROW_RING_RIGHT'):
            mapping[CommonBodySlot.BROW_RING_RIGHT] = BodyType.BROW_RING_RIGHT
        if hasattr(BodyType, 'CUMMERBUND'):
            mapping[CommonBodySlot.CUMMERBUND] = BodyType.CUMMERBUND
        if hasattr(BodyType, 'EARRINGS'):
            mapping[CommonBodySlot.EARRINGS] = BodyType.EARRINGS
        if hasattr(BodyType, 'EARS'):
            mapping[CommonBodySlot.EARS] = BodyType.EARS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'EYECOLOR'):
            mapping[CommonBodySlot.EYE_COLOR] = BodyType.EYECOLOR
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'EYECOLOR_SECONDARY'):
            mapping[CommonBodySlot.EYE_COLOR_SECONDARY] = BodyType.EYECOLOR_SECONDARY
        if hasattr(BodyType, 'EYE_LINER'):
            mapping[CommonBodySlot.EYE_LINER] = BodyType.EYE_LINER
        if hasattr(BodyType, 'EYE_SHADOW'):
            mapping[CommonBodySlot.EYE_SHADOW] = BodyType.EYE_SHADOW
        if hasattr(BodyType, 'EYEBROWS'):
            mapping[CommonBodySlot.EYEBROWS] = BodyType.EYEBROWS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'FACEPAINT'):
            mapping[CommonBodySlot.FACE_PAINT] = BodyType.FACEPAINT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SCARFACE'):
            mapping[CommonBodySlot.FACE_SCAR] = BodyType.SCARFACE
        if hasattr(BodyType, 'FACIAL_HAIR'):
            mapping[CommonBodySlot.FACIAL_HAIR] = BodyType.FACIAL_HAIR
        if hasattr(BodyType, 'FINGERNAIL'):
            mapping[CommonBodySlot.FINGERNAIL] = BodyType.FINGERNAIL
        if hasattr(BodyType, 'FOREARM_SCAR'):
            mapping[CommonBodySlot.FOREARM_SCAR] = BodyType.FOREARM_SCAR
        if hasattr(BodyType, 'FULL_BODY'):
            mapping[CommonBodySlot.FULL_BODY] = BodyType.FULL_BODY
        if hasattr(BodyType, 'FUR_BODY'):
            mapping[CommonBodySlot.FUR_BODY] = BodyType.FUR_BODY
        if hasattr(BodyType, 'GLASSES'):
            mapping[CommonBodySlot.GLASSES] = BodyType.GLASSES
        if hasattr(BodyType, 'GLOVES'):
            mapping[CommonBodySlot.GLOVES] = BodyType.GLOVES
        if hasattr(BodyType, 'HAIR'):
            mapping[CommonBodySlot.HAIR] = BodyType.HAIR
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HAIRCOLOR_OVERRIDE'):
            mapping[CommonBodySlot.HAIR_COLOR_OVERRIDE] = BodyType.HAIRCOLOR_OVERRIDE
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HAIR_FEATHERS'):
            mapping[CommonBodySlot.HAIR_FEATHERS] = BodyType.HAIR_FEATHERS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HAIR_FORELOCK'):
            mapping[CommonBodySlot.HAIR_FORELOCK] = BodyType.HAIR_FORELOCK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HAIR_MANE'):
            mapping[CommonBodySlot.HAIR_MANE] = BodyType.HAIR_MANE
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HAIR_TAIL'):
            mapping[CommonBodySlot.HAIR_TAIL] = BodyType.HAIR_TAIL
        if hasattr(BodyType, 'HAT'):
            mapping[CommonBodySlot.HAT] = BodyType.HAT
        if hasattr(BodyType, 'HEAD'):
            mapping[CommonBodySlot.HEAD] = BodyType.HEAD
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HORN'):
            mapping[CommonBodySlot.HORN] = BodyType.HORN
        if hasattr(BodyType, 'INDEX_FINGER_LEFT'):
            mapping[CommonBodySlot.INDEX_FINGER_LEFT] = BodyType.INDEX_FINGER_LEFT
        if hasattr(BodyType, 'INDEX_FINGER_RIGHT'):
            mapping[CommonBodySlot.INDEX_FINGER_RIGHT] = BodyType.INDEX_FINGER_RIGHT
        if hasattr(BodyType, 'LIP_RING_LEFT'):
            mapping[CommonBodySlot.LIP_RING_LEFT] = BodyType.LIP_RING_LEFT
        if hasattr(BodyType, 'LIP_RING_RIGHT'):
            mapping[CommonBodySlot.LIP_RING_RIGHT] = BodyType.LIP_RING_RIGHT
        if hasattr(BodyType, 'LIPS_TICK'):
            mapping[CommonBodySlot.LIPSTICK] = BodyType.LIPS_TICK
        if hasattr(BodyType, 'LOWER_BODY'):
            mapping[CommonBodySlot.LOWER_BODY] = BodyType.LOWER_BODY
        if hasattr(BodyType, 'EYELASHES'):
            mapping[CommonBodySlot.EYELASHES] = BodyType.EYELASHES
        if hasattr(BodyType, 'MIDDLE_FINGER_LEFT'):
            mapping[CommonBodySlot.MIDDLE_FINGER_LEFT] = BodyType.MIDDLE_FINGER_LEFT
        if hasattr(BodyType, 'MIDDLE_FINGER_RIGHT'):
            mapping[CommonBodySlot.MIDDLE_FINGER_RIGHT] = BodyType.MIDDLE_FINGER_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'MOLEBACKUPPER'):
            mapping[CommonBodySlot.MOLE_BACK_UPPER] = BodyType.MOLEBACKUPPER
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'MOLECHESTUPPER'):
            mapping[CommonBodySlot.MOLE_CHEST_UPPER] = BodyType.MOLECHESTUPPER
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'MOLEFACE'):
            mapping[CommonBodySlot.MOLE_FACE] = BodyType.MOLEFACE
        if hasattr(BodyType, 'NECKLACE'):
            mapping[CommonBodySlot.NECKLACE] = BodyType.NECKLACE
        if hasattr(BodyType, 'NOSE_RING_LEFT'):
            mapping[CommonBodySlot.NOSE_RING_LEFT] = BodyType.NOSE_RING_LEFT
        if hasattr(BodyType, 'NOSE_RING_RIGHT'):
            mapping[CommonBodySlot.NOSE_RING_RIGHT] = BodyType.NOSE_RING_RIGHT
        if hasattr(BodyType, 'OCCULT_BROW'):
            mapping[CommonBodySlot.OCCULT_BROW] = BodyType.OCCULT_BROW
        if hasattr(BodyType, 'OCCULT_EYE_SOCKET'):
            mapping[CommonBodySlot.OCCULT_EYE_SOCKET] = BodyType.OCCULT_EYE_SOCKET
        if hasattr(BodyType, 'OCCULT_EYE_LID'):
            mapping[CommonBodySlot.OCCULT_EYELID] = BodyType.OCCULT_EYE_LID
        if hasattr(BodyType, 'OCCULT_LEFT_CHEEK'):
            mapping[CommonBodySlot.OCCULT_LEFT_CHEEK] = BodyType.OCCULT_LEFT_CHEEK
        if hasattr(BodyType, 'OCCULT_MOUTH'):
            mapping[CommonBodySlot.OCCULT_MOUTH] = BodyType.OCCULT_MOUTH
        if hasattr(BodyType, 'OCCULT_NECK_SCAR'):
            mapping[CommonBodySlot.OCCULT_NECK_SCAR] = BodyType.OCCULT_NECK_SCAR
        if hasattr(BodyType, 'OCCULT_RIGHT_CHEEK'):
            mapping[CommonBodySlot.OCCULT_RIGHT_CHEEK] = BodyType.OCCULT_RIGHT_CHEEK
        if hasattr(BodyType, 'REINS'):
            mapping[CommonBodySlot.REINS] = BodyType.REINS
        if hasattr(BodyType, 'RING_FINGER_LEFT'):
            mapping[CommonBodySlot.RING_FINGER_LEFT] = BodyType.RING_FINGER_LEFT
        if hasattr(BodyType, 'RING_FINGER_RIGHT'):
            mapping[CommonBodySlot.RING_FINGER_RIGHT] = BodyType.RING_FINGER_RIGHT
        if hasattr(BodyType, 'SADDLE'):
            mapping[CommonBodySlot.SADDLE] = BodyType.SADDLE
        if hasattr(BodyType, 'SHOES'):
            mapping[CommonBodySlot.SHOES] = BodyType.SHOES
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_ACNE_PUBERTY'):
            mapping[CommonBodySlot.SKIN_DETAIL_ACNE_PUBERTY] = BodyType.SKINDETAIL_ACNE_PUBERTY
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_CREASE_FOREHEAD'):
            mapping[CommonBodySlot.SKIN_DETAIL_CREASE_FOREHEAD] = BodyType.SKINDETAIL_CREASE_FOREHEAD
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_CREASE_MOUTH'):
            mapping[CommonBodySlot.SKIN_DETAIL_CREASE_MOUTH] = BodyType.SKINDETAIL_CREASE_MOUTH
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_DIMPLE_LEFT'):
            mapping[CommonBodySlot.SKIN_DETAIL_DIMPLE_LEFT] = BodyType.SKINDETAIL_DIMPLE_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_DIMPLE_RIGHT'):
            mapping[CommonBodySlot.SKIN_DETAIL_DIMPLE_RIGHT] = BodyType.SKINDETAIL_DIMPLE_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_FRECKLES'):
            mapping[CommonBodySlot.SKIN_DETAIL_FRECKLES] = BodyType.SKINDETAIL_FRECKLES
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_HOOF_COLOR'):
            mapping[CommonBodySlot.SKIN_DETAIL_HOOF_COLOR] = BodyType.SKINDETAIL_HOOF_COLOR
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_CHEEK_LEFT'):
            mapping[CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_LEFT] = BodyType.SKINDETAIL_MOLE_CHEEK_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_CHEEK_RIGHT'):
            mapping[CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_RIGHT] = BodyType.SKINDETAIL_MOLE_CHEEK_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_LIP_LEFT'):
            mapping[CommonBodySlot.SKIN_DETAIL_MOLE_LIP_LEFT] = BodyType.SKINDETAIL_MOLE_LIP_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_LIP_RIGHT'):
            mapping[CommonBodySlot.SKIN_DETAIL_MOLE_LIP_RIGHT] = BodyType.SKINDETAIL_MOLE_LIP_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_NOSE_COLOR'):
            mapping[CommonBodySlot.SKIN_DETAIL_NOSE_COLOR] = BodyType.SKINDETAIL_NOSE_COLOR
        if hasattr(BodyType, 'SKIN_OVERLAY'):
            mapping[CommonBodySlot.SKIN_OVERLAY] = BodyType.SKIN_OVERLAY
        if hasattr(BodyType, 'SOCKS'):
            mapping[CommonBodySlot.SOCKS] = BodyType.SOCKS
        if hasattr(BodyType, 'STRETCHMARKS_BACK'):
            mapping[CommonBodySlot.STRETCH_MARKS_BACK] = BodyType.STRETCHMARKS_BACK
        if hasattr(BodyType, 'STRETCHMARKS_FRONT'):
            mapping[CommonBodySlot.STRETCH_MARKS_FRONT] = BodyType.STRETCHMARKS_FRONT
        if hasattr(BodyType, 'TAIL'):
            mapping[CommonBodySlot.TAIL] = BodyType.TAIL
        if hasattr(BodyType, 'TAIL_BASE'):
            mapping[CommonBodySlot.TAIL_BASE] = BodyType.TAIL_BASE
        if hasattr(BodyType, 'TATTOO_ARM_LOWER_LEFT'):
            mapping[CommonBodySlot.TATTOO_ARM_LOWER_LEFT] = BodyType.TATTOO_ARM_LOWER_LEFT
        if hasattr(BodyType, 'TATTOO_ARM_LOWER_RIGHT'):
            mapping[CommonBodySlot.TATTOO_ARM_LOWER_RIGHT] = BodyType.TATTOO_ARM_LOWER_RIGHT
        if hasattr(BodyType, 'TATTOO_ARM_UPPER_LEFT'):
            mapping[CommonBodySlot.TATTOO_ARM_UPPER_LEFT] = BodyType.TATTOO_ARM_UPPER_LEFT
        if hasattr(BodyType, 'TATTOO_ARM_UPPER_RIGHT'):
            mapping[CommonBodySlot.TATTOO_ARM_UPPER_RIGHT] = BodyType.TATTOO_ARM_UPPER_RIGHT
        if hasattr(BodyType, 'TATTOO_LEG_LEFT'):
            mapping[CommonBodySlot.TATTOO_LEG_LEFT] = BodyType.TATTOO_LEG_LEFT
        if hasattr(BodyType, 'TATTOO_LEG_RIGHT'):
            mapping[CommonBodySlot.TATTOO_LEG_RIGHT] = BodyType.TATTOO_LEG_RIGHT
        if hasattr(BodyType, 'TATTOO_TORSO_BACK_LOWER'):
            mapping[CommonBodySlot.TATTOO_TORSO_BACK_LOWER] = BodyType.TATTOO_TORSO_BACK_LOWER
        if hasattr(BodyType, 'TATTOO_TORSO_BACK_UPPER'):
            mapping[CommonBodySlot.TATTOO_TORSO_BACK_UPPER] = BodyType.TATTOO_TORSO_BACK_UPPER
        if hasattr(BodyType, 'TATTOO_TORSO_FRONT_LOWER'):
            mapping[CommonBodySlot.TATTOO_TORSO_FRONT_LOWER] = BodyType.TATTOO_TORSO_FRONT_LOWER
        if hasattr(BodyType, 'TATTOO_TORSO_FRONT_UPPER'):
            mapping[CommonBodySlot.TATTOO_TORSO_FRONT_UPPER] = BodyType.TATTOO_TORSO_FRONT_UPPER
        if hasattr(BodyType, 'TEETH'):
            mapping[CommonBodySlot.TEETH] = BodyType.TEETH
        if hasattr(BodyType, 'TIGHTS'):
            mapping[CommonBodySlot.TIGHTS] = BodyType.TIGHTS
        if hasattr(BodyType, 'TOENAIL'):
            mapping[CommonBodySlot.TOENAIL] = BodyType.TOENAIL
        if hasattr(BodyType, 'UPPER_BODY'):
            mapping[CommonBodySlot.UPPER_BODY] = BodyType.UPPER_BODY
        if hasattr(BodyType, 'WRIST_LEFT'):
            mapping[CommonBodySlot.WRIST_LEFT] = BodyType.WRIST_LEFT
        if hasattr(BodyType, 'WRIST_RIGHT'):
            mapping[CommonBodySlot.WRIST_RIGHT] = BodyType.WRIST_RIGHT
        if hasattr(BodyType, 'WINGS'):
            mapping[CommonBodySlot.WINGS] = BodyType.WINGS
        if hasattr(BodyType, 'HEADDECO'):
            mapping[CommonBodySlot.HEAD_DECORATION] = BodyType.HEADDECO
        if hasattr(BodyType, 'SKINSPECULARITY'):
            mapping[CommonBodySlot.SKIN_SPECULARITY] = BodyType.SKINSPECULARITY
        return mapping.get(value, value)

    @staticmethod
    def convert_from_vanilla(value: Union['CommonBodySlot', BodyType, int]) -> Union['CommonBodySlot', BodyType, int]:
        """convert_from_vanilla(value)

        Convert a BodyType into a CommonBodySlot

        :param value: An instance of a BodyType
        :type value: Union[CommonBodySlot, BodyType, int]
        :return: The specified BodyType translated to a CommonBodySlot or the value itself if the BodyType could not be translated.
        :rtype: Union[CommonBodySlot, int]
        """
        if value is None or value == CommonBodySlot.NONE:
            return CommonBodySlot.NONE
        if isinstance(value, CommonBodySlot):
            return value
        mapping = dict()
        if hasattr(BodyType, 'ACNE'):
            mapping[BodyType.ACNE] = CommonBodySlot.ACNE
        if hasattr(BodyType, 'ATTACHMENT_BACK'):
            mapping[BodyType.ATTACHMENT_BACK] = CommonBodySlot.ATTACHMENT_BACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKARMS'):
            mapping[BodyType.BIRTHMARKARMS] = CommonBodySlot.BIRTHMARK_ARMS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKFACE'):
            mapping[BodyType.BIRTHMARKFACE] = CommonBodySlot.BIRTHMARK_FACE
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKLEGS'):
            mapping[BodyType.BIRTHMARKLEGS] = CommonBodySlot.BIRTHMARK_LEGS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKTORSOBACK'):
            mapping[BodyType.BIRTHMARKTORSOBACK] = CommonBodySlot.BIRTHMARK_TORSO_BACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BIRTHMARKTORSOFRONT'):
            mapping[BodyType.BIRTHMARKTORSOFRONT] = CommonBodySlot.BIRTHMARK_TORSO_FRONT
        if hasattr(BodyType, 'BITE'):
            mapping[BodyType.BITE] = CommonBodySlot.BITE
        if hasattr(BodyType, 'BLANKET'):
            mapping[BodyType.BLANKET] = CommonBodySlot.BLANKET
        if hasattr(BodyType, 'BLUSH'):
            mapping[BodyType.BLUSH] = CommonBodySlot.BLUSH
        if hasattr(BodyType, 'BRIDLE'):
            mapping[BodyType.BRIDLE] = CommonBodySlot.BRIDLE
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYFRECKLES'):
            mapping[BodyType.BODYFRECKLES] = CommonBodySlot.BODY_FRECKLES
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_ARM'):
            mapping[BodyType.BODYHAIR_ARM] = CommonBodySlot.BODY_HAIR_ARM
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_LEG'):
            mapping[BodyType.BODYHAIR_LEG] = CommonBodySlot.BODY_HAIR_LEG
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_TORSOBACK'):
            mapping[BodyType.BODYHAIR_TORSOBACK] = CommonBodySlot.BODY_HAIR_TORSO_BACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYHAIR_TORSOFRONT'):
            mapping[BodyType.BODYHAIR_TORSOFRONT] = CommonBodySlot.BODY_HAIR_TORSO_FRONT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_ARMLEFT'):
            mapping[BodyType.BODYSCAR_ARMLEFT] = CommonBodySlot.BODY_SCAR_ARM_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_ARMRIGHT'):
            mapping[BodyType.BODYSCAR_ARMRIGHT] = CommonBodySlot.BODY_SCAR_ARM_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_LEGLEFT'):
            mapping[BodyType.BODYSCAR_LEGLEFT] = CommonBodySlot.BODY_SCAR_LEG_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_LEGRIGHT'):
            mapping[BodyType.BODYSCAR_LEGRIGHT] = CommonBodySlot.BODY_SCAR_LEG_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_TORSOBACK'):
            mapping[BodyType.BODYSCAR_TORSOBACK] = CommonBodySlot.BODY_SCAR_TORSO_BACK
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'BODYSCAR_TORSOFRONT'):
            mapping[BodyType.BODYSCAR_TORSOFRONT] = CommonBodySlot.BODY_SCAR_TORSO_FRONT
        if hasattr(BodyType, 'BROW_RING_LEFT'):
            mapping[BodyType.BROW_RING_LEFT] = CommonBodySlot.BROW_RING_LEFT
        if hasattr(BodyType, 'BROW_RING_RIGHT'):
            mapping[BodyType.BROW_RING_RIGHT] = CommonBodySlot.BROW_RING_RIGHT
        if hasattr(BodyType, 'CUMMERBUND'):
            mapping[BodyType.CUMMERBUND] = CommonBodySlot.CUMMERBUND
        if hasattr(BodyType, 'EARRINGS'):
            mapping[BodyType.EARRINGS] = CommonBodySlot.EARRINGS
        if hasattr(BodyType, 'EARS'):
            mapping[BodyType.EARS] = CommonBodySlot.EARS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'EYECOLOR'):
            mapping[BodyType.EYECOLOR] = CommonBodySlot.EYE_COLOR
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'EYECOLOR_SECONDARY'):
            mapping[BodyType.EYECOLOR_SECONDARY] = CommonBodySlot.EYE_COLOR_SECONDARY
        if hasattr(BodyType, 'EYE_LINER'):
            mapping[BodyType.EYE_LINER] = CommonBodySlot.EYE_LINER
        if hasattr(BodyType, 'EYE_SHADOW'):
            mapping[BodyType.EYE_SHADOW] = CommonBodySlot.EYE_SHADOW
        if hasattr(BodyType, 'EYEBROWS'):
            mapping[BodyType.EYEBROWS] = CommonBodySlot.EYEBROWS
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'FACEPAINT'):
            mapping[BodyType.FACEPAINT] = CommonBodySlot.FACE_PAINT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SCARFACE'):
            mapping[BodyType.SCARFACE] = CommonBodySlot.FACE_SCAR
        if hasattr(BodyType, 'FACIAL_HAIR'):
            mapping[BodyType.FACIAL_HAIR] = CommonBodySlot.FACIAL_HAIR
        if hasattr(BodyType, 'FINGERNAIL'):
            mapping[BodyType.FINGERNAIL] = CommonBodySlot.FINGERNAIL
        if hasattr(BodyType, 'FOREARM_SCAR'):
            mapping[BodyType.FOREARM_SCAR] = CommonBodySlot.FOREARM_SCAR
        if hasattr(BodyType, 'FULL_BODY'):
            mapping[BodyType.FULL_BODY] = CommonBodySlot.FULL_BODY
        if hasattr(BodyType, 'FUR_BODY'):
            mapping[BodyType.FUR_BODY] = CommonBodySlot.FUR_BODY
        if hasattr(BodyType, 'GLASSES'):
            mapping[BodyType.GLASSES] = CommonBodySlot.GLASSES
        if hasattr(BodyType, 'GLOVES'):
            mapping[BodyType.GLOVES] = CommonBodySlot.GLOVES
        if hasattr(BodyType, 'HAIR'):
            mapping[BodyType.HAIR] = CommonBodySlot.HAIR
        if hasattr(BodyType, 'HAIR_FEATHERS'):
            mapping[BodyType.HAIR_FEATHERS] = CommonBodySlot.HAIR_FEATHERS
        if hasattr(BodyType, 'HAIR_FORELOCK'):
            mapping[BodyType.HAIR_FORELOCK] = CommonBodySlot.HAIR_FORELOCK
        if hasattr(BodyType, 'HAIR_MANE'):
            mapping[BodyType.HAIR_MANE] = CommonBodySlot.HAIR_MANE
        if hasattr(BodyType, 'HAIR_TAIL'):
            mapping[BodyType.HAIR_TAIL] = CommonBodySlot.HAIR_TAIL
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'HAIRCOLOR_OVERRIDE'):
            mapping[BodyType.HAIRCOLOR_OVERRIDE] = CommonBodySlot.HAIR_COLOR_OVERRIDE
        if hasattr(BodyType, 'HAT'):
            mapping[BodyType.HAT] = CommonBodySlot.HAT
        if hasattr(BodyType, 'HEAD'):
            mapping[BodyType.HEAD] = CommonBodySlot.HEAD
        if hasattr(BodyType, 'HORN'):
            mapping[BodyType.HORN] = CommonBodySlot.HORN
        if hasattr(BodyType, 'INDEX_FINGER_LEFT'):
            mapping[BodyType.INDEX_FINGER_LEFT] = CommonBodySlot.INDEX_FINGER_LEFT
        if hasattr(BodyType, 'INDEX_FINGER_RIGHT'):
            mapping[BodyType.INDEX_FINGER_RIGHT] = CommonBodySlot.INDEX_FINGER_RIGHT
        if hasattr(BodyType, 'LIP_RING_LEFT'):
            mapping[BodyType.LIP_RING_LEFT] = CommonBodySlot.LIP_RING_LEFT
        if hasattr(BodyType, 'LIP_RING_RIGHT'):
            mapping[BodyType.LIP_RING_RIGHT] = CommonBodySlot.LIP_RING_RIGHT
        if hasattr(BodyType, 'LIPS_TICK'):
            mapping[BodyType.LIPS_TICK] = CommonBodySlot.LIPSTICK
        if hasattr(BodyType, 'LOWER_BODY'):
            mapping[BodyType.LOWER_BODY] = CommonBodySlot.LOWER_BODY
        if hasattr(BodyType, 'EYELASHES'):
            mapping[BodyType.EYELASHES] = CommonBodySlot.EYELASHES
        if hasattr(BodyType, 'MIDDLE_FINGER_LEFT'):
            mapping[BodyType.MIDDLE_FINGER_LEFT] = CommonBodySlot.MIDDLE_FINGER_LEFT
        if hasattr(BodyType, 'MIDDLE_FINGER_RIGHT'):
            mapping[BodyType.MIDDLE_FINGER_RIGHT] = CommonBodySlot.MIDDLE_FINGER_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'MOLEBACKUPPER'):
            mapping[BodyType.MOLEBACKUPPER] = CommonBodySlot.MOLE_BACK_UPPER
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'MOLECHESTUPPER'):
            mapping[BodyType.MOLECHESTUPPER] = CommonBodySlot.MOLE_CHEST_UPPER
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'MOLEFACE'):
            mapping[BodyType.MOLEFACE] = CommonBodySlot.MOLE_FACE
        if hasattr(BodyType, 'NECKLACE'):
            mapping[BodyType.NECKLACE] = CommonBodySlot.NECKLACE
        if hasattr(BodyType, 'NOSE_RING_LEFT'):
            mapping[BodyType.NOSE_RING_LEFT] = CommonBodySlot.NOSE_RING_LEFT
        if hasattr(BodyType, 'NOSE_RING_RIGHT'):
            mapping[BodyType.NOSE_RING_RIGHT] = CommonBodySlot.NOSE_RING_RIGHT
        if hasattr(BodyType, 'OCCULT_BROW'):
            mapping[BodyType.OCCULT_BROW] = CommonBodySlot.OCCULT_BROW
        if hasattr(BodyType, 'OCCULT_EYE_SOCKET'):
            mapping[BodyType.OCCULT_EYE_SOCKET] = CommonBodySlot.OCCULT_EYE_SOCKET
        if hasattr(BodyType, 'OCCULT_EYE_LID'):
            mapping[BodyType.OCCULT_EYE_LID] = CommonBodySlot.OCCULT_EYELID
        if hasattr(BodyType, 'OCCULT_LEFT_CHEEK'):
            mapping[BodyType.OCCULT_LEFT_CHEEK] = CommonBodySlot.OCCULT_LEFT_CHEEK
        if hasattr(BodyType, 'OCCULT_MOUTH'):
            mapping[BodyType.OCCULT_MOUTH] = CommonBodySlot.OCCULT_MOUTH
        if hasattr(BodyType, 'OCCULT_NECK_SCAR'):
            mapping[BodyType.OCCULT_NECK_SCAR] = CommonBodySlot.OCCULT_NECK_SCAR
        if hasattr(BodyType, 'OCCULT_RIGHT_CHEEK'):
            mapping[BodyType.OCCULT_RIGHT_CHEEK] = CommonBodySlot.OCCULT_RIGHT_CHEEK
        if hasattr(BodyType, 'REINS'):
            mapping[BodyType.REINS] = CommonBodySlot.REINS
        if hasattr(BodyType, 'RING_FINGER_LEFT'):
            mapping[BodyType.RING_FINGER_LEFT] = CommonBodySlot.RING_FINGER_LEFT
        if hasattr(BodyType, 'RING_FINGER_RIGHT'):
            mapping[BodyType.RING_FINGER_RIGHT] = CommonBodySlot.RING_FINGER_RIGHT
        if hasattr(BodyType, 'SADDLE'):
            mapping[BodyType.SADDLE] = CommonBodySlot.SADDLE
        if hasattr(BodyType, 'SHOES'):
            mapping[BodyType.SHOES] = CommonBodySlot.SHOES
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_ACNE_PUBERTY'):
            mapping[BodyType.SKINDETAIL_ACNE_PUBERTY] = CommonBodySlot.SKIN_DETAIL_ACNE_PUBERTY
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_CREASE_FOREHEAD'):
            mapping[BodyType.SKINDETAIL_CREASE_FOREHEAD] = CommonBodySlot.SKIN_DETAIL_CREASE_FOREHEAD
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_CREASE_MOUTH'):
            mapping[BodyType.SKINDETAIL_CREASE_MOUTH] = CommonBodySlot.SKIN_DETAIL_CREASE_MOUTH
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_DIMPLE_LEFT'):
            mapping[BodyType.SKINDETAIL_DIMPLE_LEFT] = CommonBodySlot.SKIN_DETAIL_DIMPLE_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_DIMPLE_RIGHT'):
            mapping[BodyType.SKINDETAIL_DIMPLE_RIGHT] = CommonBodySlot.SKIN_DETAIL_DIMPLE_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_FRECKLES'):
            mapping[BodyType.SKINDETAIL_FRECKLES] = CommonBodySlot.SKIN_DETAIL_FRECKLES
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_HOOF_COLOR'):
            mapping[BodyType.SKINDETAIL_HOOF_COLOR] = CommonBodySlot.SKIN_DETAIL_HOOF_COLOR
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_CHEEK_LEFT'):
            mapping[BodyType.SKINDETAIL_MOLE_CHEEK_LEFT] = CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_CHEEK_RIGHT'):
            mapping[BodyType.SKINDETAIL_MOLE_CHEEK_RIGHT] = CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_LIP_LEFT'):
            mapping[BodyType.SKINDETAIL_MOLE_LIP_LEFT] = CommonBodySlot.SKIN_DETAIL_MOLE_LIP_LEFT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_MOLE_LIP_RIGHT'):
            mapping[BodyType.SKINDETAIL_MOLE_LIP_RIGHT] = CommonBodySlot.SKIN_DETAIL_MOLE_LIP_RIGHT
        # noinspection SpellCheckingInspection
        if hasattr(BodyType, 'SKINDETAIL_NOSE_COLOR'):
            mapping[BodyType.SKINDETAIL_NOSE_COLOR] = CommonBodySlot.SKIN_DETAIL_NOSE_COLOR
        if hasattr(BodyType, 'SKIN_OVERLAY'):
            mapping[BodyType.SKIN_OVERLAY] = CommonBodySlot.SKIN_OVERLAY
        if hasattr(BodyType, 'SOCKS'):
            mapping[BodyType.SOCKS] = CommonBodySlot.SOCKS
        if hasattr(BodyType, 'STRETCHMARKS_BACK'):
            mapping[BodyType.STRETCHMARKS_BACK] = CommonBodySlot.STRETCH_MARKS_BACK
        if hasattr(BodyType, 'STRETCHMARKS_FRONT'):
            mapping[BodyType.STRETCHMARKS_FRONT] = CommonBodySlot.STRETCH_MARKS_FRONT
        if hasattr(BodyType, 'TAIL'):
            mapping[BodyType.TAIL] = CommonBodySlot.TAIL
        if hasattr(BodyType, 'TAIL_BASE'):
            mapping[BodyType.TAIL_BASE] = CommonBodySlot.TAIL_BASE
        if hasattr(BodyType, 'TATTOO_ARM_LOWER_LEFT'):
            mapping[BodyType.TATTOO_ARM_LOWER_LEFT] = CommonBodySlot.TATTOO_ARM_LOWER_LEFT
        if hasattr(BodyType, 'TATTOO_ARM_LOWER_RIGHT'):
            mapping[BodyType.TATTOO_ARM_LOWER_RIGHT] = CommonBodySlot.TATTOO_ARM_LOWER_RIGHT
        if hasattr(BodyType, 'TATTOO_ARM_UPPER_LEFT'):
            mapping[BodyType.TATTOO_ARM_UPPER_LEFT] = CommonBodySlot.TATTOO_ARM_UPPER_LEFT
        if hasattr(BodyType, 'TATTOO_ARM_UPPER_RIGHT'):
            mapping[BodyType.TATTOO_ARM_UPPER_RIGHT] = CommonBodySlot.TATTOO_ARM_UPPER_RIGHT
        if hasattr(BodyType, 'TATTOO_LEG_LEFT'):
            mapping[BodyType.TATTOO_LEG_LEFT] = CommonBodySlot.TATTOO_LEG_LEFT
        if hasattr(BodyType, 'TATTOO_LEG_RIGHT'):
            mapping[BodyType.TATTOO_LEG_RIGHT] = CommonBodySlot.TATTOO_LEG_RIGHT
        if hasattr(BodyType, 'TATTOO_TORSO_BACK_LOWER'):
            mapping[BodyType.TATTOO_TORSO_BACK_LOWER] = CommonBodySlot.TATTOO_TORSO_BACK_LOWER
        if hasattr(BodyType, 'TATTOO_TORSO_BACK_UPPER'):
            mapping[BodyType.TATTOO_TORSO_BACK_UPPER] = CommonBodySlot.TATTOO_TORSO_BACK_UPPER
        if hasattr(BodyType, 'TATTOO_TORSO_FRONT_LOWER'):
            mapping[BodyType.TATTOO_TORSO_FRONT_LOWER] = CommonBodySlot.TATTOO_TORSO_FRONT_LOWER
        if hasattr(BodyType, 'TATTOO_TORSO_FRONT_UPPER'):
            mapping[BodyType.TATTOO_TORSO_FRONT_UPPER] = CommonBodySlot.TATTOO_TORSO_FRONT_UPPER
        if hasattr(BodyType, 'TEETH'):
            mapping[BodyType.TEETH] = CommonBodySlot.TEETH
        if hasattr(BodyType, 'TIGHTS'):
            mapping[BodyType.TIGHTS] = CommonBodySlot.TIGHTS
        if hasattr(BodyType, 'TOENAIL'):
            mapping[BodyType.TOENAIL] = CommonBodySlot.TOENAIL
        if hasattr(BodyType, 'UPPER_BODY'):
            mapping[BodyType.UPPER_BODY] = CommonBodySlot.UPPER_BODY
        if hasattr(BodyType, 'WRIST_LEFT'):
            mapping[BodyType.WRIST_LEFT] = CommonBodySlot.WRIST_LEFT
        if hasattr(BodyType, 'WRIST_RIGHT'):
            mapping[BodyType.WRIST_RIGHT] = CommonBodySlot.WRIST_RIGHT
        if hasattr(BodyType, 'WINGS'):
            mapping[BodyType.WINGS] = CommonBodySlot.WINGS
        if hasattr(BodyType, 'HEADDECO'):
            mapping[BodyType.HEADDECO] = CommonBodySlot.HEAD_DECORATION
        if hasattr(BodyType, 'SKINSPECULARITY'):
            mapping[BodyType.SKINSPECULARITY] = CommonBodySlot.SKIN_SPECULARITY
        return mapping.get(value, value)
