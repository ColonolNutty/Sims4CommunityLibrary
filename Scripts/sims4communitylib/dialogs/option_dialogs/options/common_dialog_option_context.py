"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any, TypeVar, Iterator
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

DialogOptionValueType = TypeVar('DialogOptionValueType')


class CommonDialogOptionContext:
    """A context used by CommonDialogOption that contains options for customization of the option.

    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString],
        description_identifier: Union[int, str, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        tooltip_text_identifier: Union[int, str, LocalizedString]=None,
        tooltip_tokens: Tuple[Any]=(),
        icon: Any=None,
        is_enabled: bool=True,
        is_selected: bool=False
    ):
        self._title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self._description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self._tooltip = CommonLocalizationUtils.create_localized_tooltip(tooltip_text_identifier, tooltip_tokens=tooltip_tokens)
        self._icon = icon
        self._is_enabled = is_enabled
        self._is_selected = is_selected

    @property
    def is_enabled(self) -> bool:
        """Determine if the dialog option is enabled.

        """
        return self._is_enabled

    @property
    def is_selected(self) -> bool:
        """Determine if the dialog option is selected.

        """
        return self._is_selected

    @property
    def title(self) -> LocalizedString:
        """The title of the dialog option.

        """
        return self._title

    @property
    def description(self) -> LocalizedString:
        """A description of what the dialog option does.

        """
        return self._description

    @property
    def tooltip(self) -> Union[CommonLocalizationUtils.LocalizedTooltip, None]:
        """The tooltip displayed to the player on hover.

        """
        return self._tooltip

    @property
    def icon(self) -> Any:
        """The icon displayed for this dialog option.

        """
        return self._icon
