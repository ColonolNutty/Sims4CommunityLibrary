"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from collections import namedtuple

from typing import Tuple, Any, Callable, Union, Iterator, List

from pprint import pformat

from interactions.base.picker_interaction import PurchasePickerData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_option_category import \
    CommonDialogObjectOptionCategory
from sims4communitylib.enums.common_object_delivery_method import CommonObjectDeliveryMethod
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_inventory_utils import CommonSimInventoryUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiObjectPicker, UiPurchasePicker, PurchasePickerRow, UiDialogObjectPicker


class CommonPurchaseObjectsDialog(CommonChooseDialog):
    """CommonPurchaseObjectsDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        purchasable_object_rows,\
        title_tokens=(),\
        description_tokens=(),\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    Create a dialog that allows the player to purchase some objects.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_purchase_objects_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_purchase_objects_dialog():
            def _on_chosen(choices: Any, outcome: CommonChoiceOutcome):
                output('Chose {} with result: {}.'.format(pformat(choices), pformat(outcome)))

        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        show_discount = True
        from sims4communitylib.utils.common_icon_utils import CommonIconUtils
        active_sim_info = CommonSimUtils.get_active_sim_info()
        obj_id = 20359
        obj_definition = CommonObjectUtils.get_object_definition(obj_id)
        tags = obj_definition.build_buy_tags
        options = [
            PurchasePickerRow(
                def_id=obj_definition.id,
                num_owned=CommonSimInventoryUtils.get_count_of_object_in_inventory(active_sim_info, obj_id),
                tags=obj_definition.build_buy_tags,
                num_available=2000,
                custom_price=50,
                objects=tuple(),
                show_discount=show_discount,
                icon_info_data_override=None,  # Should be an instance of IconInfoData
                is_enable=True,
                row_tooltip=None,
                row_description=None
            ),
        ]
        categories = list()
        for tag in tags:
            tag_name = CommonGameTag.value_to_name.get(tag, None)
            if tag_name is None:
                continue
            categories.append(CommonDialogObjectOptionCategory(tag, obj_definition.icon, category_name=tag_name))
        dialog = CommonPurchaseObjectsDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            tuple(options),
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )
        dialog.show(on_chosen=_on_chosen, categories=categories)

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param purchasable_objects: The objects that may be purchased
    :type purchasable_objects: Iterator[PurchasePickerRow]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        purchasable_objects: Iterator[PurchasePickerRow],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = (),
        required_tooltip: Union[int, str, LocalizedString, CommonStringId] = None,
        required_tooltip_tokens: Iterator[Any] = ()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            purchasable_objects,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity,
            required_tooltip=required_tooltip,
            required_tooltip_tokens=required_tooltip_tokens
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def rows(self) -> Tuple[PurchasePickerRow]:
        # noinspection PyTypeChecker
        result: Tuple[PurchasePickerRow] = super().rows
        return result

    # noinspection PyMissingOrEmptyDocstring
    def add_row(self, choice: PurchasePickerRow, *_, **__):
        """add_row(row, *_, **__)

        Add a row to the dialog.

        :param choice: The row to add.
        :type choice: PurchasePickerRow
        """
        super().add_row(choice, *_, **__)

    def show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], Any] = CommonFunctionUtils.noop,
        target_sim_info_to_receive_objects: SimInfo = None,
        categories: Iterator[CommonDialogObjectOptionCategory] = (),
        object_delivery_method: CommonObjectDeliveryMethod = CommonObjectDeliveryMethod.INVENTORY
    ):
        """show(\
            on_chosen=CommonFunctionUtils.noop,\
            target_sim_info_to_receive_objects=None,\
            categories=(),\
            object_delivery_method=CommonObjectDeliveryMethod.INVENTORY,\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], optional
        :param target_sim_info_to_receive_objects: The Sim that will appear in the dialog image. They will also be the receiver of purchased objects if object_delivery_method is set to INVENTORY. The default Sim is the Active Sim. Default is None.
        :type target_sim_info_to_receive_objects: SimInfo, optional
        :param categories: A collection of categories to display in the dialog. They will appear in a drop down above the rows. Default is an empty collection.
        :type categories: Iterator[CommonDialogObjectOptionCategory], optional
        :param object_delivery_method: The method of delivery for purchased objects. If set to INVENTORY, objects that are purchased will be immediately available within the inventory of the specified Sim or the Active Sim if no Sim is specified.\
        If set to MAIL, objects that are purchased will be delivered via the Mail Man. They may also appear within the Household Inventory upon the mail being delivered. Default is INVENTORY.
        :type object_delivery_method: CommonObjectDeliveryMethod, optional
        """
        try:
            if object_delivery_method is CommonObjectDeliveryMethod.NONE:
                raise AssertionError('object_delivery_method was set to NONE.')
            return self._show(
                on_chosen=on_chosen,
                target_sim_info_to_receive_objects=target_sim_info_to_receive_objects,
                categories=categories,
                object_delivery_method=object_delivery_method
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(CommonPurchaseObjectsDialog.show.__name__), exception=ex)

    def _show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], bool] = CommonFunctionUtils.noop,
        target_sim_info_to_receive_objects: SimInfo = None,
        categories: Iterator[CommonDialogObjectOptionCategory] = (),
        object_delivery_method: CommonObjectDeliveryMethod = CommonObjectDeliveryMethod.INVENTORY
    ):
        def _on_chosen(choice: Any, outcome: CommonChoiceOutcome) -> bool:
            try:
                self.log.debug('Choice made.')
                self.log.format_with_message('Choose Object Choice made.', choice=choice)
                result = on_chosen(choice, outcome)
                self.log.format_with_message('Finished handling choose object _show.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        _dialog = self.build_dialog(
            on_chosen=_on_chosen,
            target_sim_info_to_receive_objects=target_sim_info_to_receive_objects,
            categories=categories,
            object_delivery_method=object_delivery_method
        )
        if not _dialog:
            raise AssertionError('Failed to create the purchase objects dialog.')
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], bool] = CommonFunctionUtils.noop,
        target_sim_info_to_receive_objects: SimInfo = None,
        categories: Iterator[CommonDialogObjectOptionCategory] = (),
        object_delivery_method: CommonObjectDeliveryMethod = CommonObjectDeliveryMethod.INVENTORY
    ) -> Union[UiPurchasePicker, None]:
        self.log.format_with_message('Attempting to build dialog.', categories=categories)

        _dialog = self._create_dialog(
            categories=categories,
            target_sim_info_to_receive_objects=target_sim_info_to_receive_objects,
            object_delivery_method=object_delivery_method
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self.rows) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        def _on_chosen(dialog: UiPurchasePicker) -> bool:
            try:
                self.log.format_with_message('Choice made.', picked_results=dialog.picked_results)
                if not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    return on_chosen(None, CommonChoiceOutcome.CANCEL)
                self.log.debug('Dialog accepted, checking if choices were made.')
                choices = dialog.get_result_definitions_and_counts()
                zipped_choices = zip(choices[0], choices[1])
                self.log.format_with_message('Purchase Objects choice made.', choice=zipped_choices)
                outcome = CommonChoiceOutcome.CHOICE_MADE
                if not choices:
                    outcome = CommonChoiceOutcome.CANCEL
                result = on_chosen(zipped_choices, outcome)
                self.log.format_with_message('Finished handling purchase objects _on_chosen.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        self._setup_dialog_rows(
            _dialog
        )

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog

    def _setup_dialog_rows(
        self,
        _dialog: UiPurchasePicker
    ):
        self.log.debug('Adding rows.')
        for row in self.rows:
            _dialog.add_row(row)

    def _create_dialog(
        self,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType = UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        target_sim_info_to_receive_objects: SimInfo = None,
        categories: Iterator[CommonDialogObjectOptionCategory] = (),
        object_delivery_method: CommonObjectDeliveryMethod = CommonObjectDeliveryMethod.INVENTORY
    ) -> Union[UiPurchasePicker, None]:
        try:
            category_type = namedtuple('category_type', ('tag', 'icon', 'tooltip'))
            dialog_categories = list()
            for category in tuple(categories):
                dialog_categories.append(
                    category_type(
                        category.object_category,
                        CommonIconUtils._load_icon(category.icon),
                        CommonLocalizationUtils.create_localized_string(category.category_name)
                    )
                )

            target_to_receive_sim_info = target_sim_info_to_receive_objects or CommonSimUtils.get_active_sim_info()
            inventory_target_id = CommonSimUtils.get_sim_id(target_to_receive_sim_info)
            purchase_objects: List[int] = list()
            dialog = UiPurchasePicker.TunableFactory().default(
                target_to_receive_sim_info,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
                categories=dialog_categories,
                max_selectable=UiDialogObjectPicker._MaxSelectableUnlimited()
            )
            purchase_picker_data = PurchasePickerData()
            if object_delivery_method == CommonObjectDeliveryMethod.INVENTORY:
                purchase_picker_data.inventory_owner_id_to_purchase_to = inventory_target_id
            if object_delivery_method == CommonObjectDeliveryMethod.MAIL:
                purchase_picker_data.delivery_method = CommonObjectDeliveryMethod.convert_to_vanilla(object_delivery_method)
            if object_delivery_method == CommonObjectDeliveryMethod.DELIVERY_SERVICE:
                purchase_picker_data.delivery_method = CommonObjectDeliveryMethod.convert_to_vanilla(object_delivery_method)
            for purchase_object in purchase_objects:
                purchase_picker_data.add_definition_to_purchase(purchase_object)
            dialog.set_target_sim(CommonSimUtils.get_sim_instance(target_to_receive_sim_info))
            dialog.object_id = purchase_picker_data.inventory_owner_id_to_purchase_to
            dialog.inventory_object_id = purchase_picker_data.inventory_owner_id_to_purchase_from
            dialog.purchase_by_object_ids = purchase_picker_data.use_obj_ids_in_response
            dialog.delivery_method = purchase_picker_data.delivery_method
            dialog.show_description = 1
            dialog.show_description_tooltip = 1
            dialog.use_dialog_pick_response = True
            dialog.max_selectable_num = len(self.rows)
            dialog.use_dropdown_filter = len(dialog_categories) > 0
            right_custom_text = None
            if right_custom_text is not None:
                dialog.right_custom_text = right_custom_text
            return dialog
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_purchase_objects_dialog',
    'Show an example of CommonPurchaseObjectsDialog.'
)
def _common_testing_show_purchase_objects_dialog(output: CommonConsoleCommandOutput):
    output('Showing test purchase object dialog.')

    def _on_chosen(choices: str, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choices), pformat(outcome)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    show_discount = True
    active_sim_info = CommonSimUtils.get_active_sim_info()
    obj_id = 20359
    obj_definition = CommonObjectUtils.get_object_definition(obj_id)
    tags = obj_definition.build_buy_tags
    options = [
        PurchasePickerRow(
            def_id=obj_definition.id,
            num_owned=CommonSimInventoryUtils.get_count_of_object_in_inventory(active_sim_info, obj_id),
            tags=obj_definition.build_buy_tags,
            num_available=2000,
            custom_price=50,
            objects=tuple(),
            show_discount=show_discount,
            icon_info_data_override=None,  # Should be an instance of IconInfoData
            is_enable=True,
            row_tooltip=None,
            row_description=None
        ),
    ]
    categories = list()
    for tag in tags:
        tag_name = CommonGameTag.value_to_name.get(tag, None)
        if tag_name is None:
            continue
        categories.append(CommonDialogObjectOptionCategory(tag, obj_definition.icon, category_name=tag_name))
    dialog = CommonPurchaseObjectsDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        tuple(options),
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )
    dialog.log.enable()
    dialog.show(on_chosen=_on_chosen, categories=categories)
    output('Done showing.')
