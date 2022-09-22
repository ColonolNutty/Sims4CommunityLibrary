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
    NONE: 'CommonBodySlot' = ...
    ACNE: 'CommonBodySlot' = ...
    BITE: 'CommonBodySlot' = ...
    BLUSH: 'CommonBodySlot' = ...
    BODY_HAIR_ARM: 'CommonBodySlot' = ...
    BODY_HAIR_LEG: 'CommonBodySlot' = ...
    BODY_HAIR_TORSO_BACK: 'CommonBodySlot' = ...
    BODY_HAIR_TORSO_FRONT: 'CommonBodySlot' = ...
    BODY_SCAR_ARM_LEFT: 'CommonBodySlot' = ...
    BODY_SCAR_ARM_RIGHT: 'CommonBodySlot' = ...
    BODY_SCAR_LEG_LEFT: 'CommonBodySlot' = ...
    BODY_SCAR_LEG_RIGHT: 'CommonBodySlot' = ...
    BODY_SCAR_TORSO_BACK: 'CommonBodySlot' = ...
    BODY_SCAR_TORSO_FRONT: 'CommonBodySlot' = ...
    BROW_RING_LEFT: 'CommonBodySlot' = ...
    BROW_RING_RIGHT: 'CommonBodySlot' = ...
    CUMMERBUND: 'CommonBodySlot' = ...
    EARRINGS: 'CommonBodySlot' = ...
    EARS: 'CommonBodySlot' = ...
    EYE_COLOR: 'CommonBodySlot' = ...
    EYE_COLOR_SECONDARY: 'CommonBodySlot' = ...
    EYE_LINER: 'CommonBodySlot' = ...
    EYE_SHADOW: 'CommonBodySlot' = ...
    EYEBROWS: 'CommonBodySlot' = ...
    FACE_PAINT: 'CommonBodySlot' = ...
    FACIAL_HAIR: 'CommonBodySlot' = ...
    FINGERNAIL: 'CommonBodySlot' = ...
    FOREARM_SCAR: 'CommonBodySlot' = ...
    FULL_BODY: 'CommonBodySlot' = ...
    FUR_BODY: 'CommonBodySlot' = ...
    GLASSES: 'CommonBodySlot' = ...
    GLOVES: 'CommonBodySlot' = ...
    HAIR: 'CommonBodySlot' = ...
    HAIR_COLOR_OVERRIDE: 'CommonBodySlot' = ...
    HAT: 'CommonBodySlot' = ...
    HEAD: 'CommonBodySlot' = ...
    INDEX_FINGER_LEFT: 'CommonBodySlot' = ...
    INDEX_FINGER_RIGHT: 'CommonBodySlot' = ...
    LIP_RING_LEFT: 'CommonBodySlot' = ...
    LIP_RING_RIGHT: 'CommonBodySlot' = ...
    LIPSTICK: 'CommonBodySlot' = ...
    LOWER_BODY: 'CommonBodySlot' = ...
    MASCARA: 'CommonBodySlot' = ...
    MIDDLE_FINGER_LEFT: 'CommonBodySlot' = ...
    MIDDLE_FINGER_RIGHT: 'CommonBodySlot' = ...
    NECKLACE: 'CommonBodySlot' = ...
    NOSE_RING_LEFT: 'CommonBodySlot' = ...
    NOSE_RING_RIGHT: 'CommonBodySlot' = ...
    OCCULT_BROW: 'CommonBodySlot' = ...
    OCCULT_EYE_SOCKET: 'CommonBodySlot' = ...
    OCCULT_EYELID: 'CommonBodySlot' = ...
    OCCULT_LEFT_CHEEK: 'CommonBodySlot' = ...
    OCCULT_MOUTH: 'CommonBodySlot' = ...
    OCCULT_NECK_SCAR: 'CommonBodySlot' = ...
    OCCULT_RIGHT_CHEEK: 'CommonBodySlot' = ...
    RING_FINGER_LEFT: 'CommonBodySlot' = ...
    RING_FINGER_RIGHT: 'CommonBodySlot' = ...
    SHOES: 'CommonBodySlot' = ...
    SKIN_DETAIL_ACNE_PUBERTY: 'CommonBodySlot' = ...
    SKIN_DETAIL_CREASE_FOREHEAD: 'CommonBodySlot' = ...
    SKIN_DETAIL_CREASE_MOUTH: 'CommonBodySlot' = ...
    SKIN_DETAIL_DIMPLE_LEFT: 'CommonBodySlot' = ...
    SKIN_DETAIL_DIMPLE_RIGHT: 'CommonBodySlot' = ...
    SKIN_DETAIL_FRECKLES: 'CommonBodySlot' = ...
    SKIN_DETAIL_MOLE_CHEEK_LEFT: 'CommonBodySlot' = ...
    SKIN_DETAIL_MOLE_CHEEK_RIGHT: 'CommonBodySlot' = ...
    SKIN_DETAIL_MOLE_LIP_LEFT: 'CommonBodySlot' = ...
    SKIN_DETAIL_MOLE_LIP_RIGHT: 'CommonBodySlot' = ...
    SKIN_DETAIL_NOSE_COLOR: 'CommonBodySlot' = ...
    SKIN_OVERLAY: 'CommonBodySlot' = ...
    SOCKS: 'CommonBodySlot' = ...
    TAIL: 'CommonBodySlot' = ...
    TATTOO_ARM_LOWER_LEFT: 'CommonBodySlot' = ...
    TATTOO_ARM_LOWER_RIGHT: 'CommonBodySlot' = ...
    TATTOO_ARM_UPPER_LEFT: 'CommonBodySlot' = ...
    TATTOO_ARM_UPPER_RIGHT: 'CommonBodySlot' = ...
    TATTOO_LEG_LEFT: 'CommonBodySlot' = ...
    TATTOO_LEG_RIGHT: 'CommonBodySlot' = ...
    TATTOO_TORSO_BACK_LOWER: 'CommonBodySlot' = ...
    TATTOO_TORSO_BACK_UPPER: 'CommonBodySlot' = ...
    TATTOO_TORSO_FRONT_LOWER: 'CommonBodySlot' = ...
    TATTOO_TORSO_FRONT_UPPER: 'CommonBodySlot' = ...
    TEETH: 'CommonBodySlot' = ...
    TIGHTS: 'CommonBodySlot' = ...
    TOENAIL: 'CommonBodySlot' = ...
    UNUSED_1: 'CommonBodySlot' = ...
    UPPER_BODY: 'CommonBodySlot' = ...
    WRIST_LEFT: 'CommonBodySlot' = ...
    WRIST_RIGHT: 'CommonBodySlot' = ...

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
        :return: The specified CommonBodySlot translated to a BodyType or NONE if the CommonBodySlot could not be translated.
        :rtype: Union[BodyType, int]
        """
        if value is None or value == CommonBodySlot.NONE:
            return BodyType.NONE
        if isinstance(value, BodyType):
            return value
        mapping = {
            CommonBodySlot.ACNE: BodyType.ACNE,
            CommonBodySlot.BITE: BodyType.BITE,
            CommonBodySlot.BLUSH: BodyType.BLUSH,
            CommonBodySlot.BODY_HAIR_ARM: BodyType.BODYHAIR_ARM,
            CommonBodySlot.BODY_HAIR_LEG: BodyType.BODYHAIR_LEG,
            CommonBodySlot.BODY_HAIR_TORSO_BACK: BodyType.BODYHAIR_TORSOBACK,
            CommonBodySlot.BODY_HAIR_TORSO_FRONT: BodyType.BODYHAIR_TORSOFRONT,
            CommonBodySlot.BODY_SCAR_ARM_LEFT: BodyType.BODYSCAR_ARMLEFT,
            CommonBodySlot.BODY_SCAR_ARM_RIGHT: BodyType.BODYSCAR_ARMRIGHT,
            CommonBodySlot.BODY_SCAR_LEG_LEFT: BodyType.BODYSCAR_LEGLEFT,
            CommonBodySlot.BODY_SCAR_LEG_RIGHT: BodyType.BODYSCAR_LEGRIGHT,
            CommonBodySlot.BODY_SCAR_TORSO_BACK: BodyType.BODYSCAR_TORSOBACK,
            CommonBodySlot.BODY_SCAR_TORSO_FRONT: BodyType.BODYSCAR_TORSOFRONT,
            CommonBodySlot.BROW_RING_LEFT: BodyType.BROW_RING_LEFT,
            CommonBodySlot.BROW_RING_RIGHT: BodyType.BROW_RING_RIGHT,
            CommonBodySlot.CUMMERBUND: BodyType.CUMMERBUND,
            CommonBodySlot.EARRINGS: BodyType.EARRINGS,
            CommonBodySlot.EARS: BodyType.EARS,
            CommonBodySlot.EYE_COLOR: BodyType.EYECOLOR,
            CommonBodySlot.EYE_COLOR_SECONDARY: BodyType.EYECOLOR_SECONDARY,
            CommonBodySlot.EYE_LINER: BodyType.EYE_LINER,
            CommonBodySlot.EYE_SHADOW: BodyType.EYE_SHADOW,
            CommonBodySlot.EYEBROWS: BodyType.EYEBROWS,
            CommonBodySlot.FACE_PAINT: BodyType.FACEPAINT,
            CommonBodySlot.FACIAL_HAIR: BodyType.FACIAL_HAIR,
            CommonBodySlot.FINGERNAIL: BodyType.FINGERNAIL,
            CommonBodySlot.FOREARM_SCAR: BodyType.FOREARM_SCAR,
            CommonBodySlot.FULL_BODY: BodyType.FULL_BODY,
            CommonBodySlot.FUR_BODY: BodyType.FUR_BODY,
            CommonBodySlot.GLASSES: BodyType.GLASSES,
            CommonBodySlot.GLOVES: BodyType.GLOVES,
            CommonBodySlot.HAIR: BodyType.HAIR,
            CommonBodySlot.HAIR_COLOR_OVERRIDE: BodyType.HAIRCOLOR_OVERRIDE,
            CommonBodySlot.HAT: BodyType.HAT,
            CommonBodySlot.HEAD: BodyType.HEAD,
            CommonBodySlot.INDEX_FINGER_LEFT: BodyType.INDEX_FINGER_LEFT,
            CommonBodySlot.INDEX_FINGER_RIGHT: BodyType.INDEX_FINGER_RIGHT,
            CommonBodySlot.LIP_RING_LEFT: BodyType.LIP_RING_LEFT,
            CommonBodySlot.LIP_RING_RIGHT: BodyType.LIP_RING_RIGHT,
            CommonBodySlot.LIPSTICK: BodyType.LIPS_TICK,
            CommonBodySlot.LOWER_BODY: BodyType.LOWER_BODY,
            CommonBodySlot.MASCARA: BodyType.MASCARA,
            CommonBodySlot.MIDDLE_FINGER_LEFT: BodyType.MIDDLE_FINGER_LEFT,
            CommonBodySlot.MIDDLE_FINGER_RIGHT: BodyType.MIDDLE_FINGER_RIGHT,
            CommonBodySlot.NECKLACE: BodyType.NECKLACE,
            CommonBodySlot.NOSE_RING_LEFT: BodyType.NOSE_RING_LEFT,
            CommonBodySlot.NOSE_RING_RIGHT: BodyType.NOSE_RING_RIGHT,
            CommonBodySlot.OCCULT_BROW: BodyType.OCCULT_BROW,
            CommonBodySlot.OCCULT_EYE_SOCKET: BodyType.OCCULT_EYE_SOCKET,
            CommonBodySlot.OCCULT_EYELID: BodyType.OCCULT_EYE_LID,
            CommonBodySlot.OCCULT_LEFT_CHEEK: BodyType.OCCULT_LEFT_CHEEK,
            CommonBodySlot.OCCULT_MOUTH: BodyType.OCCULT_MOUTH,
            CommonBodySlot.OCCULT_NECK_SCAR: BodyType.OCCULT_NECK_SCAR,
            CommonBodySlot.OCCULT_RIGHT_CHEEK: BodyType.OCCULT_RIGHT_CHEEK,
            CommonBodySlot.RING_FINGER_LEFT: BodyType.RING_FINGER_LEFT,
            CommonBodySlot.RING_FINGER_RIGHT: BodyType.RING_FINGER_RIGHT,
            CommonBodySlot.SHOES: BodyType.SHOES,
            CommonBodySlot.SKIN_DETAIL_ACNE_PUBERTY: BodyType.SKINDETAIL_ACNE_PUBERTY,
            CommonBodySlot.SKIN_DETAIL_CREASE_FOREHEAD: BodyType.SKINDETAIL_CREASE_FOREHEAD,
            CommonBodySlot.SKIN_DETAIL_CREASE_MOUTH: BodyType.SKINDETAIL_CREASE_MOUTH,
            CommonBodySlot.SKIN_DETAIL_DIMPLE_LEFT: BodyType.SKINDETAIL_DIMPLE_LEFT,
            CommonBodySlot.SKIN_DETAIL_DIMPLE_RIGHT: BodyType.SKINDETAIL_DIMPLE_RIGHT,
            CommonBodySlot.SKIN_DETAIL_FRECKLES: BodyType.SKINDETAIL_FRECKLES,
            CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_LEFT: BodyType.SKINDETAIL_MOLE_CHEEK_LEFT,
            CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_RIGHT: BodyType.SKINDETAIL_MOLE_CHEEK_RIGHT,
            CommonBodySlot.SKIN_DETAIL_MOLE_LIP_LEFT: BodyType.SKINDETAIL_MOLE_LIP_LEFT,
            CommonBodySlot.SKIN_DETAIL_MOLE_LIP_RIGHT: BodyType.SKINDETAIL_MOLE_LIP_RIGHT,
            CommonBodySlot.SKIN_DETAIL_NOSE_COLOR: BodyType.SKINDETAIL_NOSE_COLOR,
            CommonBodySlot.SKIN_OVERLAY: BodyType.SKIN_OVERLAY,
            CommonBodySlot.SOCKS: BodyType.SOCKS,
            CommonBodySlot.TAIL: BodyType.TAIL,
            CommonBodySlot.TATTOO_ARM_LOWER_LEFT: BodyType.TATTOO_ARM_LOWER_LEFT,
            CommonBodySlot.TATTOO_ARM_LOWER_RIGHT: BodyType.TATTOO_ARM_LOWER_RIGHT,
            CommonBodySlot.TATTOO_ARM_UPPER_LEFT: BodyType.TATTOO_ARM_UPPER_LEFT,
            CommonBodySlot.TATTOO_ARM_UPPER_RIGHT: BodyType.TATTOO_ARM_UPPER_RIGHT,
            CommonBodySlot.TATTOO_LEG_LEFT: BodyType.TATTOO_LEG_LEFT,
            CommonBodySlot.TATTOO_LEG_RIGHT: BodyType.TATTOO_LEG_RIGHT,
            CommonBodySlot.TATTOO_TORSO_BACK_LOWER: BodyType.TATTOO_TORSO_BACK_LOWER,
            CommonBodySlot.TATTOO_TORSO_BACK_UPPER: BodyType.TATTOO_TORSO_BACK_UPPER,
            CommonBodySlot.TATTOO_TORSO_FRONT_LOWER: BodyType.TATTOO_TORSO_FRONT_LOWER,
            CommonBodySlot.TATTOO_TORSO_FRONT_UPPER: BodyType.TATTOO_TORSO_FRONT_UPPER,
            CommonBodySlot.TEETH: BodyType.TEETH,
            CommonBodySlot.TIGHTS: BodyType.TIGHTS,
            CommonBodySlot.TOENAIL: BodyType.TOENAIL,
            CommonBodySlot.UNUSED_1: BodyType.UNUSED1,
            CommonBodySlot.UPPER_BODY: BodyType.UPPER_BODY,
            CommonBodySlot.WRIST_LEFT: BodyType.WRIST_LEFT,
            CommonBodySlot.WRIST_RIGHT: BodyType.WRIST_RIGHT,
        }
        return mapping.get(value, value)

    @staticmethod
    def convert_from_vanilla(value: Union['CommonBodySlot', BodyType, int]) -> Union['CommonBodySlot', BodyType, int]:
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
        mapping = {
            BodyType.ACNE: CommonBodySlot.ACNE,
            BodyType.BITE: CommonBodySlot.BITE,
            BodyType.BLUSH: CommonBodySlot.BLUSH,
            BodyType.BODYHAIR_ARM: CommonBodySlot.BODY_HAIR_ARM,
            BodyType.BODYHAIR_LEG: CommonBodySlot.BODY_HAIR_LEG,
            BodyType.BODYHAIR_TORSOBACK: CommonBodySlot.BODY_HAIR_TORSO_BACK,
            BodyType.BODYHAIR_TORSOFRONT: CommonBodySlot.BODY_HAIR_TORSO_FRONT,
            BodyType.BODYSCAR_ARMLEFT: CommonBodySlot.BODY_SCAR_ARM_LEFT,
            BodyType.BODYSCAR_ARMRIGHT: CommonBodySlot.BODY_SCAR_ARM_RIGHT,
            BodyType.BODYSCAR_LEGLEFT: CommonBodySlot.BODY_SCAR_LEG_LEFT,
            BodyType.BODYSCAR_LEGRIGHT: CommonBodySlot.BODY_SCAR_LEG_RIGHT,
            BodyType.BODYSCAR_TORSOBACK: CommonBodySlot.BODY_SCAR_TORSO_BACK,
            BodyType.BODYSCAR_TORSOFRONT: CommonBodySlot.BODY_SCAR_TORSO_FRONT,
            BodyType.BROW_RING_LEFT: CommonBodySlot.BROW_RING_LEFT,
            BodyType.BROW_RING_RIGHT: CommonBodySlot.BROW_RING_RIGHT,
            BodyType.CUMMERBUND: CommonBodySlot.CUMMERBUND,
            BodyType.EARRINGS: CommonBodySlot.EARRINGS,
            BodyType.EARS: CommonBodySlot.EARS,
            BodyType.EYECOLOR: CommonBodySlot.EYE_COLOR,
            BodyType.EYECOLOR_SECONDARY: CommonBodySlot.EYE_COLOR_SECONDARY,
            BodyType.EYE_LINER: CommonBodySlot.EYE_LINER,
            BodyType.EYE_SHADOW: CommonBodySlot.EYE_SHADOW,
            BodyType.EYEBROWS: CommonBodySlot.EYEBROWS,
            BodyType.FACEPAINT: CommonBodySlot.FACE_PAINT,
            BodyType.FACIAL_HAIR: CommonBodySlot.FACIAL_HAIR,
            BodyType.FINGERNAIL: CommonBodySlot.FINGERNAIL,
            BodyType.FOREARM_SCAR: CommonBodySlot.FOREARM_SCAR,
            BodyType.FULL_BODY: CommonBodySlot.FULL_BODY,
            BodyType.FUR_BODY: CommonBodySlot.FUR_BODY,
            BodyType.GLASSES: CommonBodySlot.GLASSES,
            BodyType.GLOVES: CommonBodySlot.GLOVES,
            BodyType.HAIR: CommonBodySlot.HAIR,
            BodyType.HAIRCOLOR_OVERRIDE: CommonBodySlot.HAIR_COLOR_OVERRIDE,
            BodyType.HAT: CommonBodySlot.HAT,
            BodyType.HEAD: CommonBodySlot.HEAD,
            BodyType.INDEX_FINGER_LEFT: CommonBodySlot.INDEX_FINGER_LEFT,
            BodyType.INDEX_FINGER_RIGHT: CommonBodySlot.INDEX_FINGER_RIGHT,
            BodyType.LIP_RING_LEFT: CommonBodySlot.LIP_RING_LEFT,
            BodyType.LIP_RING_RIGHT: CommonBodySlot.LIP_RING_RIGHT,
            BodyType.LIPS_TICK: CommonBodySlot.LIPSTICK,
            BodyType.LOWER_BODY: CommonBodySlot.LOWER_BODY,
            BodyType.MASCARA: CommonBodySlot.MASCARA,
            BodyType.MIDDLE_FINGER_LEFT: CommonBodySlot.MIDDLE_FINGER_LEFT,
            BodyType.MIDDLE_FINGER_RIGHT: CommonBodySlot.MIDDLE_FINGER_RIGHT,
            BodyType.NECKLACE: CommonBodySlot.NECKLACE,
            BodyType.NOSE_RING_LEFT: CommonBodySlot.NOSE_RING_LEFT,
            BodyType.NOSE_RING_RIGHT: CommonBodySlot.NOSE_RING_RIGHT,
            BodyType.OCCULT_BROW: CommonBodySlot.OCCULT_BROW,
            BodyType.OCCULT_EYE_SOCKET: CommonBodySlot.OCCULT_EYE_SOCKET,
            BodyType.OCCULT_EYE_LID: CommonBodySlot.OCCULT_EYELID,
            BodyType.OCCULT_LEFT_CHEEK: CommonBodySlot.OCCULT_LEFT_CHEEK,
            BodyType.OCCULT_MOUTH: CommonBodySlot.OCCULT_MOUTH,
            BodyType.OCCULT_NECK_SCAR: CommonBodySlot.OCCULT_NECK_SCAR,
            BodyType.OCCULT_RIGHT_CHEEK: CommonBodySlot.OCCULT_RIGHT_CHEEK,
            BodyType.RING_FINGER_LEFT: CommonBodySlot.RING_FINGER_LEFT,
            BodyType.RING_FINGER_RIGHT: CommonBodySlot.RING_FINGER_RIGHT,
            BodyType.SHOES: CommonBodySlot.SHOES,
            BodyType.SKINDETAIL_ACNE_PUBERTY: CommonBodySlot.SKIN_DETAIL_ACNE_PUBERTY,
            BodyType.SKINDETAIL_CREASE_FOREHEAD: CommonBodySlot.SKIN_DETAIL_CREASE_FOREHEAD,
            BodyType.SKINDETAIL_CREASE_MOUTH: CommonBodySlot.SKIN_DETAIL_CREASE_MOUTH,
            BodyType.SKINDETAIL_DIMPLE_LEFT: CommonBodySlot.SKIN_DETAIL_DIMPLE_LEFT,
            BodyType.SKINDETAIL_DIMPLE_RIGHT: CommonBodySlot.SKIN_DETAIL_DIMPLE_RIGHT,
            BodyType.SKINDETAIL_FRECKLES: CommonBodySlot.SKIN_DETAIL_FRECKLES,
            BodyType.SKINDETAIL_MOLE_CHEEK_LEFT: CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_LEFT,
            BodyType.SKINDETAIL_MOLE_CHEEK_RIGHT: CommonBodySlot.SKIN_DETAIL_MOLE_CHEEK_RIGHT,
            BodyType.SKINDETAIL_MOLE_LIP_LEFT: CommonBodySlot.SKIN_DETAIL_MOLE_LIP_LEFT,
            BodyType.SKINDETAIL_MOLE_LIP_RIGHT: CommonBodySlot.SKIN_DETAIL_MOLE_LIP_RIGHT,
            BodyType.SKINDETAIL_NOSE_COLOR: CommonBodySlot.SKIN_DETAIL_NOSE_COLOR,
            BodyType.SKIN_OVERLAY: CommonBodySlot.SKIN_OVERLAY,
            BodyType.SOCKS: CommonBodySlot.SOCKS,
            BodyType.TAIL: CommonBodySlot.TAIL,
            BodyType.TATTOO_ARM_LOWER_LEFT: CommonBodySlot.TATTOO_ARM_LOWER_LEFT,
            BodyType.TATTOO_ARM_LOWER_RIGHT: CommonBodySlot.TATTOO_ARM_LOWER_RIGHT,
            BodyType.TATTOO_ARM_UPPER_LEFT: CommonBodySlot.TATTOO_ARM_UPPER_LEFT,
            BodyType.TATTOO_ARM_UPPER_RIGHT: CommonBodySlot.TATTOO_ARM_UPPER_RIGHT,
            BodyType.TATTOO_LEG_LEFT: CommonBodySlot.TATTOO_LEG_LEFT,
            BodyType.TATTOO_LEG_RIGHT: CommonBodySlot.TATTOO_LEG_RIGHT,
            BodyType.TATTOO_TORSO_BACK_LOWER: CommonBodySlot.TATTOO_TORSO_BACK_LOWER,
            BodyType.TATTOO_TORSO_BACK_UPPER: CommonBodySlot.TATTOO_TORSO_BACK_UPPER,
            BodyType.TATTOO_TORSO_FRONT_LOWER: CommonBodySlot.TATTOO_TORSO_FRONT_LOWER,
            BodyType.TATTOO_TORSO_FRONT_UPPER: CommonBodySlot.TATTOO_TORSO_FRONT_UPPER,
            BodyType.TEETH: CommonBodySlot.TEETH,
            BodyType.TIGHTS: CommonBodySlot.TIGHTS,
            BodyType.TOENAIL: CommonBodySlot.TOENAIL,
            BodyType.UNUSED1: CommonBodySlot.UNUSED_1,
            BodyType.UPPER_BODY: CommonBodySlot.UPPER_BODY,
            BodyType.WRIST_LEFT: CommonBodySlot.WRIST_LEFT,
            BodyType.WRIST_RIGHT: CommonBodySlot.WRIST_RIGHT,
        }
        return mapping.get(value, value)
