"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from objects.pools.pool import SwimmingPool
from objects.pools.pool_seat import PoolSeat
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED,
            CommonGameTag.FUNC_DOUBLE_BED,
            CommonGameTag.FUNC_SINGLE_BED,
            CommonGameTag.FUNC_TODDLER_BED,
            CommonGameTag.FUNC_BED_KID
        ))

    @staticmethod
    def is_pet_sim_bed(game_object: GameObject) -> bool:
        """is_pet_sim_bed(game_object)

        Determine if an Object is a Bed for Pet Sims.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Bed for Pet Sims. False, if not.
        :rtype: bool
        """
        if not isinstance(game_object, GameObject):
            return False
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED,
            CommonGameTag.FUNC_PET_BED,
            CommonGameTag.BUY_CAT_SS_BED_SINGLE,
            CommonGameTag.BUY_CAT_SS_BED_DOUBLE,
            CommonGameTag.BUY_CAT_SS_PET_BED,
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_BED,
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
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
        if not isinstance(game_object, GameObject):
            return False
        from objects.doors.door import Door
        return isinstance(game_object, Door) or CommonObjectTagUtils.has_game_tags(game_object, (
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

    @staticmethod
    def is_fence(game_object: GameObject) -> bool:
        """is_fence(game_object)

        Determine if an Object is a Fence.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Door. False, if not.
        :rtype: bool
        """
        if not isinstance(game_object, GameObject):
            return False
        return CommonObjectTypeUtils.is_door(game_object) and CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.BUILD_FENCE,
        ))

    @staticmethod
    def is_swimming_pool(game_object: GameObject) -> bool:
        """is_swimming_pool(game_object)

        Determine if an Object is a Swimming Pool.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Swimming Pool. False, if not.
        :rtype: bool
        """
        if not isinstance(game_object, GameObject):
            return False
        return isinstance(game_object, SwimmingPool)

    @staticmethod
    def is_swimming_pool_seat(game_object: GameObject) -> bool:
        """is_swimming_pool_seat(game_object)

        Determine if an Object is a Swimming Pool Seat.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Swimming Pool Seat. False, if not.
        :rtype: bool
        """
        if not isinstance(game_object, GameObject):
            return False
        return isinstance(game_object, PoolSeat)

    @staticmethod
    def is_cow(game_object: GameObject) -> bool:
        """is_cow(game_object)

        Determine if an Object is a Cow.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Cow. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_COW, CommonGameTag.FUNC_ANIMAL_OBJECT_LIVESTOCK_COW))

    @staticmethod
    def is_dolphin(game_object: GameObject) -> bool:
        """is_dolphin(game_object)

        Determine if an Object is a Dolphin.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Dolphin. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_DOLPHIN_ALBINO,
            CommonGameTag.FUNC_DOLPHIN_MERFOLK,
            CommonGameTag.FUNC_DOLPHIN_SPAWNER,
            CommonGameTag.FUNC_DOLPHIN_STANDARD
        ))

    @staticmethod
    def is_llama(game_object: GameObject) -> bool:
        """is_llama(game_object)

        Determine if an Object is a Llama.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Llama. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_LLAMA, CommonGameTag.FUNC_ANIMAL_OBJECT_LIVESTOCK_LLAMA))

    @staticmethod
    def is_livestock(game_object: GameObject) -> bool:
        """is_livestock(game_object)

        Determine if an Object is considered to be Livestock.

        .. note:: Objects considered to be Livestock are Llamas and Cows.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is Livestock. False, if not.
        :rtype: bool
        """
        return CommonObjectTypeUtils.is_cow(game_object) or CommonObjectTypeUtils.is_llama(game_object) or CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_ANIMAL_OBJECT_LIVESTOCK,))

    @staticmethod
    def is_hen(game_object: GameObject) -> bool:
        """is_hen(game_object)

        Determine if an Object is a Hen.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Hen. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_HEN, CommonGameTag.FUNC_ANIMAL_OBJECT_LIVESTOCK_CHICKEN_HEN))

    @staticmethod
    def is_rooster(game_object: GameObject) -> bool:
        """is_rooster(game_object)

        Determine if an Object is a Rooster.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Rooster. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_ROOSTER, CommonGameTag.FUNC_ANIMAL_OBJECT_LIVESTOCK_CHICKEN_ROOSTER))

    @staticmethod
    def is_chicken(game_object: GameObject) -> bool:
        """is_chicken(game_object)

        Determine if an Object is a Chicken.

        .. note:: A Chicken is either a Hen or Rooster.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Chicken. False, if not.
        :rtype: bool
        """
        return CommonObjectTypeUtils.is_hen(game_object) or CommonObjectTypeUtils.is_rooster(game_object) or CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_ANIMAL_OBJECT_LIVESTOCK_CHICKEN, ))

    @staticmethod
    def is_rabbit(game_object: GameObject) -> bool:
        """is_rabbit(game_object)

        Determine if an Object is a Rabbit.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Rabbit. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (CommonGameTag.FUNC_ANIMAL_OBJECT_WILD_RABBIT,))

    @staticmethod
    def is_vacuum_cleaner(game_object: GameObject) -> bool:
        """is_vacuum_cleaner(game_object)

        Determine if an Object is a Vacuum Cleaner.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the Object is a Vacuum Cleaner. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (
            CommonGameTag.FUNC_VACUUM_CLEANER,
            CommonGameTag.FUNC_VACUUM_CLEANER_HANDHELD,
            CommonGameTag.FUNC_VACUUM_CLEANER_HIGH,
            CommonGameTag.FUNC_VACUUM_CLEANER_LOW,
            CommonGameTag.FUNC_VACUUM_CLEANER_MED,
            CommonGameTag.FUNC_VACUUM_CLEANER_UPRIGHT
        ))
