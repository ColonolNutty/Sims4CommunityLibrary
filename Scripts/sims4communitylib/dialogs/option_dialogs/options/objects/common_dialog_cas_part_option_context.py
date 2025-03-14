"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Union, Any

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.enums.common_gender import CommonGender
from sims4communitylib.enums.strings_enum import CommonStringId


class CommonDialogCASPartOptionContext(CommonDialogOptionContext):
    """CommonDialogCASPartOptionContext(\
        use_catalog_product_thumbnails=False,\
        use_cas_catalog_product_thumbnails=True,\
        displayed_gender=None,\
        is_new=False,\
        tooltip_text_identifier=None,\
        tooltip_tokens=(),\
        is_selected=False,\
        tag_list=()\
    )

    A context used by CommonDialogCASPartOption that contains customization of the option.

    :param use_catalog_product_thumbnails: If True, the image of the CAS Part will be the catalog product thumbnail. If False, it will not be. Default is False.
    :type use_catalog_product_thumbnails: bool, optional
    :param use_cas_catalog_product_thumbnails: If True, the image of the CAS Part will be the CAS catalog product thumbnail. If False, it will not be. Default is True.
    :type use_cas_catalog_product_thumbnails: bool, optional
    :param displayed_gender: The CAS Part thumbnail will display the CAS Part using this gender. Default is the gender of the Sim in the option.
    :type displayed_gender: CommonGender, optional
    :param is_new: If True, this CAS Part will be considered as New. If False, the CAS Part will not be considered as New. Default is False.
    :type is_new: bool, optional
    :param tooltip_text_identifier: Text that will be displayed upon hovering the option.
    :type tooltip_text_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param tooltip_tokens: An iterator of Tokens that will be formatted into the tooltip text.
    :type tooltip_tokens: Tuple[Any], optional
    :param is_selected: If True, the CAS Part will already be selected in the dialog. If False, the CAS Part will not be selected in the dialog.
    :type is_selected: bool, optional
    :param tag_list: A list of tags that can be used when organizing the CAS Part. Default is no tags.
    :type tag_list: Iterator[str], optional
    """
    def __init__(
        self,
        use_catalog_product_thumbnails: bool = False,
        use_cas_catalog_product_thumbnails: bool = True,
        displayed_gender: CommonGender = None,
        is_new: bool = False,
        tooltip_text_identifier: Union[int, str, LocalizedString, CommonStringId] = None,
        tooltip_tokens: Iterator[Any] = (),
        is_selected: bool = False,
        tag_list: Iterator[str] = ()
    ):
        super().__init__(
            0,
            0,
            tooltip_text_identifier=tooltip_text_identifier,
            tooltip_tokens=tooltip_tokens,
            is_selected=is_selected,
            tag_list=tag_list
        )
        self._use_catalog_product_thumbnails = use_catalog_product_thumbnails
        self._use_cas_catalog_product_thumbnails = use_cas_catalog_product_thumbnails
        self._displayed_gender = displayed_gender
        self._is_new = is_new

    @property
    def displayed_gender(self) -> CommonGender:
        """The gender displayed in the CAS Part dialog for the Sim wearing the part."""
        return self._displayed_gender

    @property
    def use_catalog_product_thumbnails(self) -> bool:
        """If True, the image of the CAS Part will be the catalog product thumbnail. If False, it will not be."""
        return self._use_catalog_product_thumbnails

    @property
    def use_cas_catalog_product_thumbnails(self) -> bool:
        """If True, the image of the CAS Part will be the CAS catalog product thumbnail. If False, it will not be."""
        return self._use_cas_catalog_product_thumbnails

    @property
    def is_new(self) -> bool:
        """If True, this CAS Part will be considered as New. If False, the CAS Part will not be considered as New."""
        return self._is_new
