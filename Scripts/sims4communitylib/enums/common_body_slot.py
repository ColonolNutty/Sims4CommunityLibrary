"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.outfits.outfit_enums import BodyType
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonBodySlot(CommonIntFlags):
    """Slots on the body of Sims that CAS Parts can be attached to."""
    NONE: 'CommonBodySlot' = 0
    ACNE: 'CommonBodySlot' = 72
    BITE: 'CommonBodySlot' = 76
    BLUSH: 'CommonBodySlot' = 32
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
    FACIAL_HAIR: 'CommonBodySlot' = 28
    FINGERNAIL: 'CommonBodySlot' = 73
    FOREARM_SCAR: 'CommonBodySlot' = 71
    FULL_BODY: 'CommonBodySlot' = 5
    FUR_BODY: 'CommonBodySlot' = 59
    GLASSES: 'CommonBodySlot' = 11
    GLOVES: 'CommonBodySlot' = 13
    HAIR: 'CommonBodySlot' = 2
    HAIR_COLOR_OVERRIDE: 'CommonBodySlot' = 75
    HAT: 'CommonBodySlot' = 1
    HEAD: 'CommonBodySlot' = 3
    INDEX_FINGER_LEFT: 'CommonBodySlot' = 22
    INDEX_FINGER_RIGHT: 'CommonBodySlot' = 23
    LIP_RING_LEFT: 'CommonBodySlot' = 16
    LIP_RING_RIGHT: 'CommonBodySlot' = 17
    LIPSTICK: 'CommonBodySlot' = 29
    LOWER_BODY: 'CommonBodySlot' = 7
    MASCARA: 'CommonBodySlot' = 37
    MIDDLE_FINGER_LEFT: 'CommonBodySlot' = 26
    MIDDLE_FINGER_RIGHT: 'CommonBodySlot' = 27
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
    RING_FINGER_LEFT: 'CommonBodySlot' = 24
    RING_FINGER_RIGHT: 'CommonBodySlot' = 25
    SHOES: 'CommonBodySlot' = 8
    SKIN_DETAIL_ACNE_PUBERTY: 'CommonBodySlot' = 89
    SKIN_DETAIL_CREASE_FOREHEAD: 'CommonBodySlot' = 38
    SKIN_DETAIL_CREASE_MOUTH: 'CommonBodySlot' = 57
    SKIN_DETAIL_DIMPLE_LEFT: 'CommonBodySlot' = 40
    SKIN_DETAIL_DIMPLE_RIGHT: 'CommonBodySlot' = 41
    SKIN_DETAIL_FRECKLES: 'CommonBodySlot' = 39
    SKIN_DETAIL_MOLE_CHEEK_LEFT: 'CommonBodySlot' = 55
    SKIN_DETAIL_MOLE_CHEEK_RIGHT: 'CommonBodySlot' = 56
    SKIN_DETAIL_MOLE_LIP_LEFT: 'CommonBodySlot' = 43
    SKIN_DETAIL_MOLE_LIP_RIGHT: 'CommonBodySlot' = 44
    SKIN_DETAIL_NOSE_COLOR: 'CommonBodySlot' = 62
    SKIN_OVERLAY: 'CommonBodySlot' = 58
    SOCKS: 'CommonBodySlot' = 36
    TAIL: 'CommonBodySlot' = 61
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
    UNUSED_1: 'CommonBodySlot' = 77
    UPPER_BODY: 'CommonBodySlot' = 6
    WRIST_LEFT: 'CommonBodySlot' = 14
    WRIST_RIGHT: 'CommonBodySlot' = 15

    @staticmethod
    def convert_to_vanilla(value: 'CommonBodySlot') -> Union[BodyType, int]:
        """convert_to_vanilla(value)

        Convert a CommonBodySlot into the vanilla BodyType enum.

        :param value: An instance of a CommonBodySlot
        :type value: CommonBodySlot
        :return: The specified CommonBodySlot translated to a BodyType or NONE if the CommonBodySlot could not be translated.
        :rtype: Union[BodyType, int]
        """
        if value is None or value == CommonBodySlot.NONE:
            return BodyType.NONE
        if isinstance(value, BodyType):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), BodyType, default_value=int(value))

    @staticmethod
    def convert_from_vanilla(value: Union['CommonBodySlot', BodyType, int]) -> Union['CommonBodySlot', int]:
        """convert_from_vanilla(value)

        Convert a BodyType into a CommonBodySlot

        :param value: An instance of a BodyType
        :type value: Union[CommonBodySlot, BodyType, int]
        :return: The specified BodyType translated to a CommonBodySlot or NONE if the BodyType could not be translated.
        :rtype: Union[CommonBodySlot, int]
        """
        if value is None or value == CommonBodySlot.NONE:
            return CommonBodySlot.NONE
        if isinstance(value, CommonBodySlot):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonBodySlot, default_value=int(value))
