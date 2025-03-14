"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, TypeVar, Iterator, Tuple, List
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

DialogOptionValueType = TypeVar('DialogOptionValueType')


class CommonDialogOptionContext:
    """CommonDialogOptionContext(\
        title_identifier,\
        description_identifier,\
        description_tokens=(),\
        tooltip_text_identifier=None,\
        tooltip_tokens=(),\
        icon=None,\
        is_enabled=True,\
        is_selected=False,\
        tag_list=()\
    )

    A context used by :class:`.CommonDialogOption` that provides customization of options.

    :param title_identifier: The title of the option.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description of the option.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: An iterator of Tokens that will be formatted into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterator of Tokens that will be formatted into the description.
    :type description_tokens: Iterator[Any], optional
    :param tooltip_text_identifier: Text that will be displayed upon hovering the option.
    :type tooltip_text_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param tooltip_tokens: An iterator of Tokens that will be formatted into the tooltip text.
    :type tooltip_tokens: Tuple[Any], optional
    :param icon: The icon to display for the option.
    :type icon: Any, optional
    :param is_enabled: If True, the dialog option will be selectable in the dialog. If False, the dialog option will be disabled in the dialog.
    :type is_enabled: bool, optional
    :param is_selected: If True, the dialog option will already be selected in the dialog. If False, the dialog option will not be selected in the dialog.
    :type is_selected: bool, optional
    :param tag_list: A list of tags that can be used when organizing the option. Default is no tags.
    :type tag_list: Iterator[str], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = (),
        tooltip_text_identifier: Union[int, str, LocalizedString, CommonStringId] = None,
        tooltip_tokens: Iterator[Any] = (),
        icon: Any = None,
        is_enabled: bool = True,
        is_selected: bool = False,
        tag_list: Iterator[str] = ()
    ):
        self._title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self._description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self._tooltip = CommonLocalizationUtils.create_localized_tooltip(tooltip_text_identifier, tooltip_tokens=tuple(tooltip_tokens))
        self._icon = icon
        self._is_enabled = is_enabled
        self._is_selected = is_selected
        self._tag_list = tuple(tag_list)

    @property
    def is_enabled(self) -> bool:
        """Determine if the dialog option is enabled.

        :return: True, if the dialog option is enabled. False, if not.
        :rtype: bool
        """
        return self._is_enabled

    @property
    def is_selected(self) -> bool:
        """Determine if the dialog option is selected.

        :return: True, if the dialog option is selected. False, if not.
        :rtype: bool
        """
        return self._is_selected

    @property
    def title(self) -> LocalizedString:
        """The title of the dialog option.

        :return: The title of the dialog option.
        :rtype: LocalizedString
        """
        return self._title

    @property
    def description(self) -> LocalizedString:
        """A description of what the dialog option does.

        :return: A description of what the dialog option does.
        :rtype: LocalizedString
        """
        return self._description

    @property
    def tooltip(self) -> Union[CommonLocalizationUtils.LocalizedTooltip, None]:
        """The tooltip displayed to the player on hover.

        :return: The tooltip displayed to the player on hover or None if no tooltip was specified.
        :rtype: Union[CommonLocalizationUtils.LocalizedTooltip, None]
        """
        return self._tooltip

    @property
    def tag_list(self) -> Tuple[str]:
        """A collection of tags used to filter the option.

        :return: A collection of tags used to filter the option.
        :rtype: Tuple[str]
        """
        return self._tag_list

    @property
    def hashed_tag_list(self) -> Tuple[int]:
        """Same as tag_list, but the values are hashed.

        :return: Same as :py:attr:`~tag_list`, but the values are hashed.
        :rtype: Tuple[str]
        """
        hashed_tag_list: List[int] = list()
        for tag in self.tag_list:
            hashed_tag_list.append((abs(hash(tag)) % (10 ** 8)))
        return tuple(hashed_tag_list)

    @property
    def icon(self) -> Any:
        """The icon displayed for this dialog option.

        :return: The icon displayed for this dialog option.
        :rtype: Any
        """
        return self._icon
