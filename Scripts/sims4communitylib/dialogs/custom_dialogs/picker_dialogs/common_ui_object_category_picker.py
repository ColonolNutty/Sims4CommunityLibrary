"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from distributor.rollback import ProtocolBufferRollback
from interactions.utils.tunable_icon import TunableIconFactory
from sims4.localization import TunableLocalizedString
from sims4.tuning.tunable import TunableTuple, TunableList, Tunable
from ui.ui_dialog_picker import UiObjectPicker
from distributor.shared_messages import build_icon_info_msg
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class CommonUiObjectCategoryPicker(UiObjectPicker):
    """An ObjectPicker with categories listed in a drop down.

    """
    FACTORY_TUNABLES = {
        'object_categories': TunableList(
            description='\n            The categories to display in the drop down for this picker.\n            ',
            tunable=TunableTuple(
                object_category=Tunable(
                    tunable_type=str,
                    default='ALL'
                ),
                icon=TunableIconFactory(),
                category_name=TunableLocalizedString()
            )
        )
    }

    def _build_customize_picker(self, picker_data) -> None:
        for category in self.object_categories:
            with ProtocolBufferRollback(picker_data.filter_data) as category_data:
                category_data.tag_type = abs(hash(category.object_category)) % (10 ** 8)
                build_icon_info_msg(category.icon(None), None, category_data.icon_info)
                category_data.description = category.category_name
        super()._build_customize_picker(picker_data)
