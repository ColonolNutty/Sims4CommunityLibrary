"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.utils.objects.common_object_tag_utils import CommonObjectTagUtils


class CommonObjectTypeUtils:
    """ Utilities for determining the type of an object. """
    @staticmethod
    def is_window(game_object: GameObject) -> bool:
        """is_window(game_object)

        Determine if an Object is a window.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Window. False, if not.
        :rtype: bool
        """
        from sims4communitylib.enums.tags_enum import CommonGameTag
        from sims4communitylib.utils.objects.common_object_tag_utils import CommonObjectTagUtils
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.BUILD_WINDOW, ))

    @staticmethod
    def is_toilet(game_object: GameObject) -> bool:
        """is_toilet(game_object)

        Determine if an Object is a Toilet.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Toilet. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_TOILET,
            CommonGameTag.FUNC_PUBLIC_BATHROOM,
            CommonGameTag.FUNC_TOILET_TALKING
        ))

    @staticmethod
    def is_loveseat(game_object: GameObject) -> bool:
        """is_loveseat(game_object)

        Determine if an Object is a Loveseat.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Loveseat. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.BUY_CAT_SS_LOVE_SEAT, ))

    @staticmethod
    def is_bed(game_object: GameObject) -> bool:
        """is_bed(game_object)

        Determine if an Object is a Bed.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Bed. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED,
            CommonGameTag.FUNC_DOUBLE_BED,
            CommonGameTag.FUNC_SINGLE_BED,
            CommonGameTag.FUNC_TODDLER_BED,
            CommonGameTag.FUNC_BED_KID,
            CommonGameTag.FUNC_PET_BED,
            CommonGameTag.BUY_CAT_SS_BED,
            CommonGameTag.BUY_CAT_SS_BED_SINGLE,
            CommonGameTag.BUY_CAT_SS_BED_DOUBLE,
            CommonGameTag.BUY_CAT_SS_PET_BED,
            CommonGameTag.FUNC_DOCTOR_OBJECT_EXAM_BED,
            CommonGameTag.FUNC_ACTOR_CAREER_HOSPITAL_EXAM_BED
        ))

    @staticmethod
    def is_human_sim_bed(game_object: GameObject) -> bool:
        """is_human_sim_bed(game_object)

        Determine if an Object is a Bed for Human Sims.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Bed for Human Sims. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED,
            CommonGameTag.FUNC_DOUBLE_BED,
            CommonGameTag.FUNC_SINGLE_BED,
            CommonGameTag.FUNC_TODDLER_BED,
            CommonGameTag.FUNC_BED_KID
        ))

    @staticmethod
    def is_adult_bed(game_object: GameObject) -> bool:
        """is_adult_bed(game_object)

        Determine if an Object is a Bed for Adult Sims.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Bed for Adult Sims. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED,
            CommonGameTag.FUNC_DOUBLE_BED,
            CommonGameTag.FUNC_SINGLE_BED
        ))

    @staticmethod
    def is_child_bed(game_object: GameObject) -> bool:
        """is_adult_bed(game_object)

        Determine if an Object is a Bed for Child Sims.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Bed for Child Sims. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED_KID,
        ))

    @staticmethod
    def is_toddler_bed(game_object: GameObject) -> bool:
        """is_toddler_bed(game_object)

        Determine if an Object is a Bed for Toddler Sims.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Bed for Toddler Sims. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_TODDLER_BED,
        ))

    @staticmethod
    def is_single_bed(game_object: GameObject) -> bool:
        """is_single_bed(game_object)

        Determine if an Object is a Single Bed.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Single Bed. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_SINGLE_BED,
            CommonGameTag.BUY_CAT_SS_BED_SINGLE
        ))

    @staticmethod
    def is_double_bed(game_object: GameObject) -> bool:
        """is_double_bed(game_object)

        Determine if an Object is a Double Bed.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Double Bed. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_DOUBLE_BED,
            CommonGameTag.BUY_CAT_SS_BED_DOUBLE
        ))

    @staticmethod
    def is_light(game_object: GameObject) -> bool:
        """is_light(game_object)

        Determine if an Object is a Light.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Light. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.BUY_CAT_LD_WALL_LIGHT,
            CommonGameTag.BUY_CAT_LD_OUTDOOR_LIGHT,
            CommonGameTag.BUY_CAT_LD_CEILING_LIGHT,
            CommonGameTag.BUY_CAT_LD_NIGHT_LIGHT,
            CommonGameTag.BUY_CAT_LD_MISC_LIGHT,
            CommonGameTag.FUNC_LIGHT_NON_ELECTRIC,
            CommonGameTag.FUNC_POOL_LIGHT,
            CommonGameTag.FUNC_BUSINESS_LIGHT,
            CommonGameTag.FUNC_LASER_LIGHT,
            CommonGameTag.FUNC_RETAIL_NEON_LIGHT,
            CommonGameTag.STYLE_FESTIVAL_LIGHT,
            CommonGameTag.FUNC_HOLIDAY_FESTIVE_LIGHTING
        ))

    @staticmethod
    def is_stair(game_object: GameObject) -> bool:
        """is_stair(game_object)

        Determine if an Object is a Stair.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Stair. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.BUILD_STAIR,
        ))

    @staticmethod
    def is_door(game_object: GameObject) -> bool:
        """is_door(game_object)

        Determine if an Object is a Door.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Door. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.common_type_utils import CommonTypeUtils
        return CommonTypeUtils.is_door(game_object) or CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.BUILD_DOOR,
            CommonGameTag.BUILD_DOOR_SINGLE,
            CommonGameTag.BUILD_DOOR_DOUBLE,
            CommonGameTag.FUNC_GATE,
            CommonGameTag.BUILD_GATE,
            CommonGameTag.BUILD_GATE_SINGLE,
            CommonGameTag.BUILD_GATE_DOUBLE,
            CommonGameTag.FUNC_TEMPLE_GATE,
            CommonGameTag.FUNC_ACTOR_CAREER_CELL_DOOR,
            CommonGameTag.FUNC_LAB_DOOR,
            CommonGameTag.FUNC_VAULT_DOOR,
            CommonGameTag.FUNC_ACTOR_CAREER_STUDIO_DOOR_PRIVATE,
            CommonGameTag.FUNC_INVESTIGATION_SEALED_DOOR_HALLWAY,
            CommonGameTag.FUNC_INVESTIGATION_SEALED_DOOR_MOTHER_PLANT
        ))
