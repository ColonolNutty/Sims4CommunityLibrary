"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4.resources import Types
from sims4communitylib.enums.icons_enum import CommonIconId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonIconUtils:
    """Utilities for loading icons.

    """
    @staticmethod
    def load_arrow_right_icon() -> Any:
        """load_arrow_right_icon()

        Get the Resource Key for the ARROW_RIGHT_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_ARROW_RIGHT_ICON)

    @staticmethod
    def load_arrow_left_icon() -> Any:
        """load_arrow_left_icon()

        Get the Resource Key for the ARROW_LEFT_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_ARROW_LEFT_ICON)

    @staticmethod
    def load_arrow_navigate_into_icon() -> Any:
        """load_arrow_navigate_into_icon()

        Get the Resource Key for the ARROW_NAVIGATE_INTO_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_ARROW_NAVIGATE_INTO_ICON)

    @staticmethod
    def load_question_mark_icon() -> Any:
        """load_question_mark_icon()

        Get the Resource Key for the QUESTION_MARK_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_QUESTION_MARK_ICON)

    @staticmethod
    def load_checked_square_icon() -> Any:
        """load_checked_square_icon()

        Get the Resource Key for the CHECKED_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_CHECKED_SQUARE_ICON)

    @staticmethod
    def load_checked_circle_icon() -> Any:
        """load_checked_circle_icon()

        Get the Resource Key for the CHECKED_CIRCLE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_CHECKED_CIRCLE_ICON)

    @staticmethod
    def load_unchecked_square_icon() -> Any:
        """load_unchecked_square_icon()

        Get the Resource Key for the UNCHECKED_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_UNCHECKED_SQUARE_ICON)

    @staticmethod
    def load_x_icon() -> Any:
        """load_x_icon()

        Get the Resource Key for the X_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_X_ICON)

    @staticmethod
    def load_six_sided_dice_icon() -> Any:
        """load_six_sided_dice_icon()

        Get the Resource Key for the SIX_SIDED_DICE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_SIX_SIDED_DICE_ICON)

    @staticmethod
    def load_blank_square_icon() -> Any:
        """load_blank_square_icon()

        Get the Resource Key for the BLANK_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_BLANK_SQUARE_ICON)

    @staticmethod
    def load_text_prev_icon() -> Any:
        """load_text_prev_icon()

        Get the Resource Key for the TEXT_PREV_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_TEXT_PREV_SQUARE_ICON)

    @staticmethod
    def load_text_next_icon() -> Any:
        """load_text_next_icon()

        Get the Resource Key for the TEXT_NEXT_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_TEXT_NEXT_SQUARE_ICON)

    @staticmethod
    def load_unfilled_circle_icon() -> Any:
        """load_unfilled_circle_icon()

        Get the Resource Key for the UNFILLED_CIRCLE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_UNFILLED_CIRCLE_ICON)

    @staticmethod
    def load_filled_circle_icon() -> Any:
        """load_filled_circle_icon()

        Get the Resource Key for the FILLED_CIRCLE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, CommonIconId.S4CLIB_FILLED_CIRCLE_ICON)
    
    @staticmethod
    def _load_icon(icon_id: int) -> Any:
        return CommonResourceUtils.get_resource_key(Types.PNG, icon_id)
