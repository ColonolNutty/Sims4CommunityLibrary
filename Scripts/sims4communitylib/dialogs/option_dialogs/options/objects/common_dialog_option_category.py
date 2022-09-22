"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CommonDialogObjectOptionCategory:
    """CommonDialogObjectOptionCategory(object_category, icon, category_name=None)

    An option category.

    :param object_category: The category of the option.
    :type object_category: str
    :param icon: The decimal identifier of the icon for the category.
    :type icon: int
    :param category_name: The name of the category. Default is the object_category value.
    :type category_name: LocalizedString
    """
    def __init__(self, object_category: str, icon: int, category_name: Union[int, str, LocalizedString, CommonStringId, None] = None):
        self.object_category = object_category
        self.icon = icon
        if category_name is None:
            category_name = object_category
        self.category_name = CommonLocalizationUtils.create_localized_string(category_name)
