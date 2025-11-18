"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from tag import TagCategory


class CommonGameTagCategory(CommonInt):
    """Variants of Game Tag Categories."""
    INVALID: 'CommonGameTagCategory' = ...
    ACCESSORIES: 'CommonGameTagCategory' = ...
    ACNE_LEVEL: 'CommonGameTagCategory' = ...
    AGE_APPROPRIATE: 'CommonGameTagCategory' = ...
    APPEARANCE_MODIFIER: 'CommonGameTagCategory' = ...
    ARCHETYPE: 'CommonGameTagCategory' = ...
    ATTRACTOR_POINT_TRAIN_SPOT: 'CommonGameTagCategory' = 137
    BOTTOM: 'CommonGameTagCategory' = ...
    BOTTOM_ACCESSORY: 'CommonGameTagCategory' = ...
    BREED: 'CommonGameTagCategory' = ...
    BREED_GROUP: 'CommonGameTagCategory' = ...
    BUILD: 'CommonGameTagCategory' = ...
    BUY_CAT_EE: 'CommonGameTagCategory' = ...
    BUY_CAT_LD: 'CommonGameTagCategory' = ...
    BUY_CAT_MAG: 'CommonGameTagCategory' = ...
    BUY_CAT_PA: 'CommonGameTagCategory' = ...
    BUY_CAT_SS: 'CommonGameTagCategory' = ...
    BUY_CAT_VO: 'CommonGameTagCategory' = ...
    CAS_CATEGORY: 'CommonGameTagCategory' = ...
    COAT_PATTERN: 'CommonGameTagCategory' = ...
    COLOR: 'CommonGameTagCategory' = ...
    COLOR_PALETTE: 'CommonGameTagCategory' = ...
    DOG_SIZE: 'CommonGameTagCategory' = ...
    EARS: 'CommonGameTagCategory' = ...
    ENSEMBLE: 'CommonGameTagCategory' = ...
    EYE_BROW_SHAPE: 'CommonGameTagCategory' = ...
    EYE_BROW_THICKNESS: 'CommonGameTagCategory' = ...
    EYE_COLOR: 'CommonGameTagCategory' = ...
    FABRIC: 'CommonGameTagCategory' = ...
    FACE_DETAIL: 'CommonGameTagCategory' = ...
    FACE_MAKE_UP: 'CommonGameTagCategory' = ...
    FACIAL_HAIR: 'CommonGameTagCategory' = ...
    FASHION: 'CommonGameTagCategory' = ...
    FLOOR_PATTERN: 'CommonGameTagCategory' = ...
    FULL_BODY: 'CommonGameTagCategory' = ...
    FUR: 'CommonGameTagCategory' = ...
    FUR_LENGTH: 'CommonGameTagCategory' = ...
    GENDER_APPROPRIATE: 'CommonGameTagCategory' = ...
    GROWTH_LEVEL: 'CommonGameTagCategory' = ...
    GROWTH_TYPE: 'CommonGameTagCategory' = ...
    HAIR: 'CommonGameTagCategory' = ...
    HAIR_COLOR: 'CommonGameTagCategory' = ...
    HAIR_LENGTH: 'CommonGameTagCategory' = ...
    HAIR_TEXTURE: 'CommonGameTagCategory' = ...
    HAT: 'CommonGameTagCategory' = ...
    HOOF_COLOR: 'CommonGameTagCategory' = ...
    HORN_COLOR: 'CommonGameTagCategory' = ...
    LESSON: 'CommonGameTagCategory' = ...
    MOOD: 'CommonGameTagCategory' = ...
    NOSE_COLOR: 'CommonGameTagCategory' = ...
    NUDE_PART: 'CommonGameTagCategory' = ...
    OCCULT: 'CommonGameTagCategory' = ...
    OUTFIT_CATEGORY: 'CommonGameTagCategory' = ...
    PATTERN: 'CommonGameTagCategory' = ...
    PERSONA: 'CommonGameTagCategory' = ...
    REWARD: 'CommonGameTagCategory' = ...
    SHOES: 'CommonGameTagCategory' = ...
    SKILL: 'CommonGameTagCategory' = ...
    SKIN_HUE: 'CommonGameTagCategory' = ...
    SKIN_TONE_BLEND: 'CommonGameTagCategory' = ...
    SKIN_TONE_TYPE: 'CommonGameTagCategory' = ...
    SKIN_VALUE: 'CommonGameTagCategory' = ...
    SPECIAL: 'CommonGameTagCategory' = ...
    SPECIAL_CONTENT: 'CommonGameTagCategory' = ...
    STYLE: 'CommonGameTagCategory' = ...
    TAIL: 'CommonGameTagCategory' = ...
    TERRAIN_PAINT: 'CommonGameTagCategory' = ...
    TOP: 'CommonGameTagCategory' = ...
    TRAIT_GROUP: 'CommonGameTagCategory' = ...
    UNIFORM: 'CommonGameTagCategory' = ...
    VAMPIRE_ARCHETYPE: 'CommonGameTagCategory' = ...
    WALL_PATTERN: 'CommonGameTagCategory' = ...
    WING_TYPE: 'CommonGameTagCategory' = ...
    WORLD_LOG: 'CommonGameTagCategory' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonGameTagCategory'] = None) -> Tuple['CommonGameTagCategory']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGameTagCategory], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonGameTagCategory]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonGameTagCategory, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonGameTagCategory'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGameTagCategory], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonGameTagCategory'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGameTagCategory], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonGameTagCategory') -> Union[TagCategory, None]:
        """convert_to_vanilla(value)

        Convert a value into the vanilla TagCategory enum.

        :param value: An instance of CommonGameTagCategory
        :type value: CommonGameTagCategory
        :return: The specified value translated to TagCategory or INVALID if the value could not be translated.
        :rtype: Union[TagCategory, None]
        """
        if value is None or value == CommonGameTagCategory.INVALID:
            return TagCategory.INVALID
        if isinstance(value, TagCategory):
            return value
        mapping = dict()
        if hasattr(TagCategory, 'Mood'):
            mapping[CommonGameTagCategory.MOOD] = TagCategory.Mood
        if hasattr(TagCategory, 'Color'):
            mapping[CommonGameTagCategory.COLOR] = TagCategory.Color
        if hasattr(TagCategory, 'Style'):
            mapping[CommonGameTagCategory.STYLE] = TagCategory.Style
        if hasattr(TagCategory, 'AgeAppropriate'):
            mapping[CommonGameTagCategory.AGE_APPROPRIATE] = TagCategory.AgeAppropriate
        if hasattr(TagCategory, 'Archetype'):
            mapping[CommonGameTagCategory.ARCHETYPE] = TagCategory.Archetype
        if hasattr(TagCategory, 'AtPo_TrainSpot'):
            mapping[CommonGameTagCategory.ATTRACTOR_POINT_TRAIN_SPOT] = TagCategory.AtPo_TrainSpot
        if hasattr(TagCategory, 'CASCategory'):
            mapping[CommonGameTagCategory.CAS_CATEGORY] = TagCategory.CASCategory
        if hasattr(TagCategory, 'HoofColor'):
            mapping[CommonGameTagCategory.HOOF_COLOR] = TagCategory.HoofColor
        if hasattr(TagCategory, 'HornColor'):
            mapping[CommonGameTagCategory.HORN_COLOR] = TagCategory.HornColor
        if hasattr(TagCategory, 'Lesson'):
            mapping[CommonGameTagCategory.LESSON] = TagCategory.Lesson
        if hasattr(TagCategory, 'OutfitCategory'):
            mapping[CommonGameTagCategory.OUTFIT_CATEGORY] = TagCategory.OutfitCategory
        if hasattr(TagCategory, 'Skill'):
            mapping[CommonGameTagCategory.SKILL] = TagCategory.Skill
        if hasattr(TagCategory, 'EyeColor'):
            mapping[CommonGameTagCategory.EYE_COLOR] = TagCategory.EyeColor
        if hasattr(TagCategory, 'Persona'):
            mapping[CommonGameTagCategory.PERSONA] = TagCategory.Persona
        if hasattr(TagCategory, 'Special'):
            mapping[CommonGameTagCategory.SPECIAL] = TagCategory.Special
        if hasattr(TagCategory, 'HairColor'):
            mapping[CommonGameTagCategory.HAIR_COLOR] = TagCategory.HairColor
        if hasattr(TagCategory, 'ColorPalette'):
            mapping[CommonGameTagCategory.COLOR_PALETTE] = TagCategory.ColorPalette
        if hasattr(TagCategory, 'Hair'):
            mapping[CommonGameTagCategory.HAIR] = TagCategory.Hair
        if hasattr(TagCategory, 'FacialHair'):
            mapping[CommonGameTagCategory.FACIAL_HAIR] = TagCategory.FacialHair
        if hasattr(TagCategory, 'Hat'):
            mapping[CommonGameTagCategory.HAT] = TagCategory.Hat
        if hasattr(TagCategory, 'FaceMakeup'):
            mapping[CommonGameTagCategory.FACE_MAKE_UP] = TagCategory.FaceMakeup
        if hasattr(TagCategory, 'Top'):
            mapping[CommonGameTagCategory.TOP] = TagCategory.Top
        if hasattr(TagCategory, 'Bottom'):
            mapping[CommonGameTagCategory.BOTTOM] = TagCategory.Bottom
        if hasattr(TagCategory, 'FullBody'):
            mapping[CommonGameTagCategory.FULL_BODY] = TagCategory.FullBody
        if hasattr(TagCategory, 'Shoes'):
            mapping[CommonGameTagCategory.SHOES] = TagCategory.Shoes
        if hasattr(TagCategory, 'BottomAccessory'):
            mapping[CommonGameTagCategory.BOTTOM_ACCESSORY] = TagCategory.BottomAccessory
        if hasattr(TagCategory, 'BuyCatEE'):
            mapping[CommonGameTagCategory.BUY_CAT_EE] = TagCategory.BuyCatEE
        if hasattr(TagCategory, 'BuyCatPA'):
            mapping[CommonGameTagCategory.BUY_CAT_PA] = TagCategory.BuyCatPA
        if hasattr(TagCategory, 'BuyCatLD'):
            mapping[CommonGameTagCategory.BUY_CAT_LD] = TagCategory.BuyCatLD
        if hasattr(TagCategory, 'BuyCatSS'):
            mapping[CommonGameTagCategory.BUY_CAT_SS] = TagCategory.BuyCatSS
        if hasattr(TagCategory, 'BuyCatVO'):
            mapping[CommonGameTagCategory.BUY_CAT_VO] = TagCategory.BuyCatVO
        if hasattr(TagCategory, 'Uniform'):
            mapping[CommonGameTagCategory.UNIFORM] = TagCategory.Uniform
        if hasattr(TagCategory, 'Accessories'):
            mapping[CommonGameTagCategory.ACCESSORIES] = TagCategory.Accessories
        if hasattr(TagCategory, 'BuyCatMAG'):
            mapping[CommonGameTagCategory.BUY_CAT_MAG] = TagCategory.BuyCatMAG
        if hasattr(TagCategory, 'FloorPattern'):
            mapping[CommonGameTagCategory.FLOOR_PATTERN] = TagCategory.FloorPattern
        if hasattr(TagCategory, 'WallPattern'):
            mapping[CommonGameTagCategory.WALL_PATTERN] = TagCategory.WallPattern
        if hasattr(TagCategory, 'Fabric'):
            mapping[CommonGameTagCategory.FABRIC] = TagCategory.Fabric
        if hasattr(TagCategory, 'Build'):
            mapping[CommonGameTagCategory.BUILD] = TagCategory.Build
        if hasattr(TagCategory, 'Pattern'):
            mapping[CommonGameTagCategory.PATTERN] = TagCategory.Pattern
        if hasattr(TagCategory, 'HairLength'):
            mapping[CommonGameTagCategory.HAIR_LENGTH] = TagCategory.HairLength
        if hasattr(TagCategory, 'HairTexture'):
            mapping[CommonGameTagCategory.HAIR_TEXTURE] = TagCategory.HairTexture
        if hasattr(TagCategory, 'TraitGroup'):
            mapping[CommonGameTagCategory.TRAIT_GROUP] = TagCategory.TraitGroup
        if hasattr(TagCategory, 'SkinHue'):
            mapping[CommonGameTagCategory.SKIN_HUE] = TagCategory.SkinHue
        if hasattr(TagCategory, 'Reward'):
            mapping[CommonGameTagCategory.REWARD] = TagCategory.Reward
        if hasattr(TagCategory, 'TerrainPaint'):
            mapping[CommonGameTagCategory.TERRAIN_PAINT] = TagCategory.TerrainPaint
        if hasattr(TagCategory, 'EyebrowThickness'):
            mapping[CommonGameTagCategory.EYE_BROW_THICKNESS] = TagCategory.EyebrowThickness
        if hasattr(TagCategory, 'EyebrowShape'):
            mapping[CommonGameTagCategory.EYE_BROW_SHAPE] = TagCategory.EyebrowShape
        if hasattr(TagCategory, 'Ensemble'):
            mapping[CommonGameTagCategory.ENSEMBLE] = TagCategory.Ensemble
        if hasattr(TagCategory, 'SkintoneType'):
            mapping[CommonGameTagCategory.SKIN_TONE_TYPE] = TagCategory.SkintoneType
        if hasattr(TagCategory, 'Occult'):
            mapping[CommonGameTagCategory.OCCULT] = TagCategory.Occult
        if hasattr(TagCategory, 'SkintoneBlend'):
            mapping[CommonGameTagCategory.SKIN_TONE_BLEND] = TagCategory.SkintoneBlend
        if hasattr(TagCategory, 'GenderAppropriate'):
            mapping[CommonGameTagCategory.GENDER_APPROPRIATE] = TagCategory.GenderAppropriate
        if hasattr(TagCategory, 'NudePart'):
            mapping[CommonGameTagCategory.NUDE_PART] = TagCategory.NudePart
        if hasattr(TagCategory, 'FaceDetail'):
            mapping[CommonGameTagCategory.FACE_DETAIL] = TagCategory.FaceDetail
        if hasattr(TagCategory, 'VampireArchetype'):
            mapping[CommonGameTagCategory.VAMPIRE_ARCHETYPE] = TagCategory.VampireArchetype
        if hasattr(TagCategory, 'Ears'):
            mapping[CommonGameTagCategory.EARS] = TagCategory.Ears
        if hasattr(TagCategory, 'Breed'):
            mapping[CommonGameTagCategory.BREED] = TagCategory.Breed
        if hasattr(TagCategory, 'Tail'):
            mapping[CommonGameTagCategory.TAIL] = TagCategory.Tail
        if hasattr(TagCategory, 'Fur'):
            mapping[CommonGameTagCategory.FUR] = TagCategory.Fur
        if hasattr(TagCategory, 'DogSize'):
            mapping[CommonGameTagCategory.DOG_SIZE] = TagCategory.DogSize
        if hasattr(TagCategory, 'BreedGroup'):
            mapping[CommonGameTagCategory.BREED_GROUP] = TagCategory.BreedGroup
        if hasattr(TagCategory, 'NoseColor'):
            mapping[CommonGameTagCategory.NOSE_COLOR] = TagCategory.NoseColor
        if hasattr(TagCategory, 'WorldLog'):
            mapping[CommonGameTagCategory.WORLD_LOG] = TagCategory.WorldLog
        if hasattr(TagCategory, 'CoatPattern'):
            mapping[CommonGameTagCategory.COAT_PATTERN] = TagCategory.CoatPattern
        if hasattr(TagCategory, 'FurLength'):
            mapping[CommonGameTagCategory.FUR_LENGTH] = TagCategory.FurLength
        if hasattr(TagCategory, 'AppearanceModifier'):
            mapping[CommonGameTagCategory.APPEARANCE_MODIFIER] = TagCategory.AppearanceModifier
        if hasattr(TagCategory, 'SpecialContent'):
            mapping[CommonGameTagCategory.SPECIAL_CONTENT] = TagCategory.SpecialContent
        if hasattr(TagCategory, 'Fashion'):
            mapping[CommonGameTagCategory.FASHION] = TagCategory.Fashion
        if hasattr(TagCategory, 'GrowthLevel'):
            mapping[CommonGameTagCategory.GROWTH_LEVEL] = TagCategory.GrowthLevel
        if hasattr(TagCategory, 'GrowthType'):
            mapping[CommonGameTagCategory.GROWTH_TYPE] = TagCategory.GrowthType
        if hasattr(TagCategory, 'SkinValue'):
            mapping[CommonGameTagCategory.SKIN_VALUE] = TagCategory.SkinValue
        if hasattr(TagCategory, 'AcneLevel'):
            mapping[CommonGameTagCategory.ACNE_LEVEL] = TagCategory.AcneLevel
        if hasattr(TagCategory, 'WingType'):
            mapping[CommonGameTagCategory.WING_TYPE] = TagCategory.WingType
        return mapping.get(value, TagCategory.INVALID)

    @staticmethod
    def convert_from_vanilla(value: Union[int, TagCategory]) -> 'CommonGameTagCategory':
        """convert_from_vanilla(value)

        Convert a value into a CommonGameTagCategory enum.

        :param value: An instance of TagCategory
        :type value: TagCategory
        :return: The specified value translated to CommonGameTagCategory or INVALID if the value could not be translated.
        :rtype: CommonGameTagCategory
        """
        if value is None or value == TagCategory.INVALID:
            return CommonGameTagCategory.INVALID
        if isinstance(value, CommonGameTagCategory):
            return value
        mapping = dict()
        if hasattr(TagCategory, 'Mood'):
            mapping[TagCategory.Mood] = CommonGameTagCategory.MOOD
        if hasattr(TagCategory, 'Color'):
            mapping[TagCategory.Color] = CommonGameTagCategory.COLOR
        if hasattr(TagCategory, 'Style'):
            mapping[TagCategory.Style] = CommonGameTagCategory.STYLE
        if hasattr(TagCategory, 'AgeAppropriate'):
            mapping[TagCategory.AgeAppropriate] = CommonGameTagCategory.AGE_APPROPRIATE
        if hasattr(TagCategory, 'Archetype'):
            mapping[TagCategory.Archetype] = CommonGameTagCategory.ARCHETYPE
        if hasattr(TagCategory, 'AtPo_TrainSpot'):
            mapping[TagCategory.AtPo_TrainSpot] = CommonGameTagCategory.ATTRACTOR_POINT_TRAIN_SPOT
        if hasattr(TagCategory, 'HoofColor'):
            mapping[TagCategory.HoofColor] = CommonGameTagCategory.HOOF_COLOR
        if hasattr(TagCategory, 'HornColor'):
            mapping[TagCategory.HornColor] = CommonGameTagCategory.HORN_COLOR
        if hasattr(TagCategory, 'Lesson'):
            mapping[TagCategory.Lesson] = CommonGameTagCategory.LESSON
        if hasattr(TagCategory, 'CASCategory'):
            mapping[TagCategory.CASCategory] = CommonGameTagCategory.CAS_CATEGORY
        if hasattr(TagCategory, 'OutfitCategory'):
            mapping[TagCategory.OutfitCategory] = CommonGameTagCategory.OUTFIT_CATEGORY
        if hasattr(TagCategory, 'Skill'):
            mapping[TagCategory.Skill] = CommonGameTagCategory.SKILL
        if hasattr(TagCategory, 'EyeColor'):
            mapping[TagCategory.EyeColor] = CommonGameTagCategory.EYE_COLOR
        if hasattr(TagCategory, 'Persona'):
            mapping[TagCategory.Persona] = CommonGameTagCategory.PERSONA
        if hasattr(TagCategory, 'Special'):
            mapping[TagCategory.Special] = CommonGameTagCategory.SPECIAL
        if hasattr(TagCategory, 'HairColor'):
            mapping[TagCategory.HairColor] = CommonGameTagCategory.HAIR_COLOR
        if hasattr(TagCategory, 'ColorPalette'):
            mapping[TagCategory.ColorPalette] = CommonGameTagCategory.COLOR_PALETTE
        if hasattr(TagCategory, 'Hair'):
            mapping[TagCategory.Hair] = CommonGameTagCategory.HAIR
        if hasattr(TagCategory, 'FacialHair'):
            mapping[TagCategory.FacialHair] = CommonGameTagCategory.FACIAL_HAIR
        if hasattr(TagCategory, 'Hat'):
            mapping[TagCategory.Hat] = CommonGameTagCategory.HAT
        if hasattr(TagCategory, 'FaceMakeup'):
            mapping[TagCategory.FaceMakeup] = CommonGameTagCategory.FACE_MAKE_UP
        if hasattr(TagCategory, 'Top'):
            mapping[TagCategory.Top] = CommonGameTagCategory.TOP
        if hasattr(TagCategory, 'Bottom'):
            mapping[TagCategory.Bottom] = CommonGameTagCategory.BOTTOM
        if hasattr(TagCategory, 'FullBody'):
            mapping[TagCategory.FullBody] = CommonGameTagCategory.FULL_BODY
        if hasattr(TagCategory, 'Shoes'):
            mapping[TagCategory.Shoes] = CommonGameTagCategory.SHOES
        if hasattr(TagCategory, 'BottomAccessory'):
            mapping[TagCategory.BottomAccessory] = CommonGameTagCategory.BOTTOM_ACCESSORY
        if hasattr(TagCategory, 'BuyCatEE'):
            mapping[TagCategory.BuyCatEE] = CommonGameTagCategory.BUY_CAT_EE
        if hasattr(TagCategory, 'BuyCatPA'):
            mapping[TagCategory.BuyCatPA] = CommonGameTagCategory.BUY_CAT_PA
        if hasattr(TagCategory, 'BuyCatLD'):
            mapping[TagCategory.BuyCatLD] = CommonGameTagCategory.BUY_CAT_LD
        if hasattr(TagCategory, 'BuyCatSS'):
            mapping[TagCategory.BuyCatSS] = CommonGameTagCategory.BUY_CAT_SS
        if hasattr(TagCategory, 'BuyCatVO'):
            mapping[TagCategory.BuyCatVO] = CommonGameTagCategory.BUY_CAT_VO
        if hasattr(TagCategory, 'Uniform'):
            mapping[TagCategory.Uniform] = CommonGameTagCategory.UNIFORM
        if hasattr(TagCategory, 'Accessories'):
            mapping[TagCategory.Accessories] = CommonGameTagCategory.ACCESSORIES
        if hasattr(TagCategory, 'BuyCatMAG'):
            mapping[TagCategory.BuyCatMAG] = CommonGameTagCategory.BUY_CAT_MAG
        if hasattr(TagCategory, 'FloorPattern'):
            mapping[TagCategory.FloorPattern] = CommonGameTagCategory.FLOOR_PATTERN
        if hasattr(TagCategory, 'WallPattern'):
            mapping[TagCategory.WallPattern] = CommonGameTagCategory.WALL_PATTERN
        if hasattr(TagCategory, 'Fabric'):
            mapping[TagCategory.Fabric] = CommonGameTagCategory.FABRIC
        if hasattr(TagCategory, 'Build'):
            mapping[TagCategory.Build] = CommonGameTagCategory.BUILD
        if hasattr(TagCategory, 'Pattern'):
            mapping[TagCategory.Pattern] = CommonGameTagCategory.PATTERN
        if hasattr(TagCategory, 'HairLength'):
            mapping[TagCategory.HairLength] = CommonGameTagCategory.HAIR_LENGTH
        if hasattr(TagCategory, 'HairTexture'):
            mapping[TagCategory.HairTexture] = CommonGameTagCategory.HAIR_TEXTURE
        if hasattr(TagCategory, 'TraitGroup'):
            mapping[TagCategory.TraitGroup] = CommonGameTagCategory.TRAIT_GROUP
        if hasattr(TagCategory, 'SkinHue'):
            mapping[TagCategory.SkinHue] = CommonGameTagCategory.SKIN_HUE
        if hasattr(TagCategory, 'Reward'):
            mapping[TagCategory.Reward] = CommonGameTagCategory.REWARD
        if hasattr(TagCategory, 'TerrainPaint'):
            mapping[TagCategory.TerrainPaint] = CommonGameTagCategory.TERRAIN_PAINT
        if hasattr(TagCategory, 'EyebrowThickness'):
            mapping[TagCategory.EyebrowThickness] = CommonGameTagCategory.EYE_BROW_THICKNESS
        if hasattr(TagCategory, 'EyebrowShape'):
            mapping[TagCategory.EyebrowShape] = CommonGameTagCategory.EYE_BROW_SHAPE
        if hasattr(TagCategory, 'Ensemble'):
            mapping[TagCategory.Ensemble] = CommonGameTagCategory.ENSEMBLE
        if hasattr(TagCategory, 'SkintoneType'):
            mapping[TagCategory.SkintoneType] = CommonGameTagCategory.SKIN_TONE_TYPE
        if hasattr(TagCategory, 'Occult'):
            mapping[TagCategory.Occult] = CommonGameTagCategory.OCCULT
        if hasattr(TagCategory, 'SkintoneBlend'):
            mapping[TagCategory.SkintoneBlend] = CommonGameTagCategory.SKIN_TONE_BLEND
        if hasattr(TagCategory, 'GenderAppropriate'):
            mapping[TagCategory.GenderAppropriate] = CommonGameTagCategory.GENDER_APPROPRIATE
        if hasattr(TagCategory, 'NudePart'):
            mapping[TagCategory.NudePart] = CommonGameTagCategory.NUDE_PART
        if hasattr(TagCategory, 'FaceDetail'):
            mapping[TagCategory.FaceDetail] = CommonGameTagCategory.FACE_DETAIL
        if hasattr(TagCategory, 'VampireArchetype'):
            mapping[TagCategory.VampireArchetype] = CommonGameTagCategory.VAMPIRE_ARCHETYPE
        if hasattr(TagCategory, 'Ears'):
            mapping[TagCategory.Ears] = CommonGameTagCategory.EARS
        if hasattr(TagCategory, 'Breed'):
            mapping[TagCategory.Breed] = CommonGameTagCategory.BREED
        if hasattr(TagCategory, 'Tail'):
            mapping[TagCategory.Tail] = CommonGameTagCategory.TAIL
        if hasattr(TagCategory, 'Fur'):
            mapping[TagCategory.Fur] = CommonGameTagCategory.FUR
        if hasattr(TagCategory, 'DogSize'):
            mapping[TagCategory.DogSize] = CommonGameTagCategory.DOG_SIZE
        if hasattr(TagCategory, 'BreedGroup'):
            mapping[TagCategory.BreedGroup] = CommonGameTagCategory.BREED_GROUP
        if hasattr(TagCategory, 'NoseColor'):
            mapping[TagCategory.NoseColor] = CommonGameTagCategory.NOSE_COLOR
        if hasattr(TagCategory, 'WorldLog'):
            mapping[TagCategory.WorldLog] = CommonGameTagCategory.WORLD_LOG
        if hasattr(TagCategory, 'CoatPattern'):
            mapping[TagCategory.CoatPattern] = CommonGameTagCategory.COAT_PATTERN
        if hasattr(TagCategory, 'FurLength'):
            mapping[TagCategory.FurLength] = CommonGameTagCategory.FUR_LENGTH
        if hasattr(TagCategory, 'AppearanceModifier'):
            mapping[TagCategory.AppearanceModifier] = CommonGameTagCategory.APPEARANCE_MODIFIER
        if hasattr(TagCategory, 'SpecialContent'):
            mapping[TagCategory.SpecialContent] = CommonGameTagCategory.SPECIAL_CONTENT
        if hasattr(TagCategory, 'Fashion'):
            mapping[TagCategory.Fashion] = CommonGameTagCategory.FASHION
        if hasattr(TagCategory, 'GrowthLevel'):
            mapping[TagCategory.GrowthLevel] = CommonGameTagCategory.GROWTH_LEVEL
        if hasattr(TagCategory, 'GrowthType'):
            mapping[TagCategory.GrowthType] = CommonGameTagCategory.GROWTH_TYPE
        if hasattr(TagCategory, 'SkinValue'):
            mapping[TagCategory.SkinValue] = CommonGameTagCategory.SKIN_VALUE
        if hasattr(TagCategory, 'AcneLevel'):
            mapping[TagCategory.AcneLevel] = CommonGameTagCategory.ACNE_LEVEL
        if hasattr(TagCategory, 'WingType'):
            mapping[TagCategory.WingType] = CommonGameTagCategory.WING_TYPE
        return mapping.get(value, CommonGameTagCategory.INVALID)
