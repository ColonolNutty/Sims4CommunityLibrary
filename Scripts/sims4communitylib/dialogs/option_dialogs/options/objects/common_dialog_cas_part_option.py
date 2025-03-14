"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_cas_part_option_context import \
    CommonDialogCASPartOptionContext
from sims4communitylib.dtos.common_cas_part import CommonCASPart
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import ObjectPickerRow
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption


class CommonDialogCASPartOption(CommonDialogOption):
    """CommonDialogCASPartOption(\
        cas_part,\
        owning_sim_info,\
        context,\
        displayed_sim_info=None,\
        on_chosen=CommonFunctionUtils.noop,\
    )

    An option the player can choose within a CAS Part dialog.

    :param cas_part: The decimal identifier of the CAS Part this option displays.
    :type cas_part: int
    :param owning_sim_info: The info of the Sim the CAS Part is owned by.
    :type owning_sim_info: SimInfo
    :param context: A context to customize the dialog option.
    :type context: CommonDialogCASPartOptionContext
    :param displayed_sim_info: The info of the Sim the CAS Part will be displayed on. If not specified, owning_sim_info will be used.
    :type displayed_sim_info: SimInfo, optional
    :param on_chosen: A callback invoked when the dialog option is chosen. The values are as follows: (option_identifier, value)
    :type on_chosen: Callable[[CommonCASPart], None], optional
    """
    def __init__(
        self,
        cas_part: CommonCASPart,
        owning_sim_info: SimInfo,
        context: CommonDialogCASPartOptionContext,
        displayed_sim_info: SimInfo = None,
        on_chosen: Callable[[CommonCASPart], None] = CommonFunctionUtils.noop,
    ):
        self._owning_sim_info = owning_sim_info
        self._displayed_sim_info = displayed_sim_info or owning_sim_info

        super().__init__(cas_part, context, on_chosen=on_chosen)

    @property
    def value(self) -> CommonCASPart:
        """The value of the option.

        :return: The value of the option.
        :rtype: CommonCASPart
        """
        return self._value

    @property
    def owning_sim_info(self) -> SimInfo:
        """The info of the Sim owning the option.

        :return: The info of the Sim owning the option.
        :rtype: SimInfo
        """
        return self._owning_sim_info

    @property
    def displayed_sim_info(self) -> SimInfo:
        """The info of the Sim the option is displayed for.

        :return: The info of the Sim the option is displayed for.
        :rtype: SimInfo
        """
        return self._displayed_sim_info

    @property
    def context(self) -> CommonDialogCASPartOptionContext:
        """The context of the option.

        :return: The context of the option.
        :rtype: CommonDialogCASPartOptionContext
        """
        # noinspection PyTypeChecker
        return self._option_context

    def as_row(self, option_id: int) -> ObjectPickerRow:
        """as_row(option_id)

        Convert the option into a picker row.

        :param option_id: The index of the option.
        :type option_id: int
        :return: The option as a Picker Row
        :rtype: ObjectPickerRow
        """
        return ObjectPickerRow(
            option_id=option_id,
            def_id=self.value.cas_part_id,
            tag=self,
            tag_list=list(self.tag_list),
            use_catalog_product_thumbnails=self.context.use_catalog_product_thumbnails,
            use_cas_catalog_product_thumbnails=self.context.use_cas_catalog_product_thumbnails,
            cas_catalog_gender=CommonGender.convert_to_vanilla(self.context.displayed_gender or CommonGender.get_gender(self.displayed_sim_info)),
            owner_sim_id=CommonSimUtils.get_sim_id(self.owning_sim_info),
            is_new=self.context.is_new,
            target_sim_id=CommonSimUtils.get_sim_id(self.displayed_sim_info),
            is_selected=self.context.is_selected,
            row_tooltip=self.tooltip
        )
