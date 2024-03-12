"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union
from sims4.resources import Types
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.icons_enum import CommonIconId
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonIconUtils:
    """Utilities for loading icons.

    """
    @classmethod
    def load_arrow_right_icon(cls) -> Any:
        """load_arrow_right_icon()

        Get the Resource Key for the ARROW_RIGHT_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_ARROW_RIGHT_ICON)

    @classmethod
    def load_arrow_left_icon(cls) -> Any:
        """load_arrow_left_icon()

        Get the Resource Key for the ARROW_LEFT_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_ARROW_LEFT_ICON)

    @classmethod
    def load_arrow_navigate_into_icon(cls) -> Any:
        """load_arrow_navigate_into_icon()

        Get the Resource Key for the ARROW_NAVIGATE_INTO_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_ARROW_NAVIGATE_INTO_ICON)

    @classmethod
    def load_question_mark_icon(cls) -> Any:
        """load_question_mark_icon()

        Get the Resource Key for the QUESTION_MARK_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_QUESTION_MARK_ICON)

    @classmethod
    def load_checked_square_icon(cls) -> Any:
        """load_checked_square_icon()

        Get the Resource Key for the CHECKED_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_CHECKED_SQUARE_ICON)

    @classmethod
    def load_checked_circle_icon(cls) -> Any:
        """load_checked_circle_icon()

        Get the Resource Key for the CHECKED_CIRCLE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_CHECKED_CIRCLE_ICON)

    @classmethod
    def load_unchecked_square_icon(cls) -> Any:
        """load_unchecked_square_icon()

        Get the Resource Key for the UNCHECKED_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_UNCHECKED_SQUARE_ICON)

    @classmethod
    def load_x_icon(cls) -> Any:
        """load_x_icon()

        Get the Resource Key for the X_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_X_ICON)

    @classmethod
    def load_six_sided_dice_icon(cls) -> Any:
        """load_six_sided_dice_icon()

        Get the Resource Key for the SIX_SIDED_DICE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_SIX_SIDED_DICE_ICON)

    @classmethod
    def load_blank_square_icon(cls) -> Any:
        """load_blank_square_icon()

        Get the Resource Key for the BLANK_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_BLANK_SQUARE_ICON)

    @classmethod
    def load_text_prev_icon(cls) -> Any:
        """load_text_prev_icon()

        Get the Resource Key for the TEXT_PREV_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_TEXT_PREV_SQUARE_ICON)

    @classmethod
    def load_text_next_icon(cls) -> Any:
        """load_text_next_icon()

        Get the Resource Key for the TEXT_NEXT_SQUARE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_TEXT_NEXT_SQUARE_ICON)

    @classmethod
    def load_unfilled_circle_icon(cls) -> Any:
        """load_unfilled_circle_icon()

        Get the Resource Key for the UNFILLED_CIRCLE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_UNFILLED_CIRCLE_ICON)

    @classmethod
    def load_filled_circle_icon(cls) -> Any:
        """load_filled_circle_icon()

        Get the Resource Key for the FILLED_CIRCLE_ICON.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return cls.load_icon_by_id(CommonIconId.S4CLIB_FILLED_CIRCLE_ICON)

    @classmethod
    def load_icon_by_id(cls, icon: Union[int, CommonIconId, CommonInt]) -> Union[Any, None]:
        """load_icon_by_id(icon)

        Load an instance of an Icon by its identifier.

        :param icon: The identifier of an Icon.
        :type icon: Union[int, CommonIconId, CommonInt]
        :return: An instance of an Icon matching the decimal identifier or None if not found.
        :rtype: Union[Any, None]
        """
        return CommonResourceUtils.get_resource_key(Types.PNG, icon)
    
    @staticmethod
    def _load_icon(icon_id: Union[int, CommonIconId]) -> Any:
        """Obsolete, please use load_icon_by_id instead."""
        return CommonIconUtils.load_icon_by_id(icon_id)
