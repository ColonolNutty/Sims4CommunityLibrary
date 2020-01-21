"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Any, Union, Iterator
from distributor.shared_messages import IconInfoData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_notification import UiDialogNotification
log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'common_basic_notification')


class CommonBasicNotification:
    """Use to create a basic notification.

    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        urgency: UiDialogNotification.UiDialogNotificationUrgency=UiDialogNotification.UiDialogNotificationUrgency.DEFAULT,
        information_level: UiDialogNotification.UiDialogNotificationLevel=UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior: UiDialogNotification.UiDialogNotificationExpandBehavior=UiDialogNotification.UiDialogNotificationExpandBehavior.USER_SETTING
    ):
        """Create a notification.

        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        :param urgency: The urgency to which the notification will appear. (URGENT makes it orange)
        :param information_level: The information level of the notification.
        :param expand_behavior: Specify how the notification will expand.
        """
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self.visual_type = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        self.urgency = urgency
        self.information_level = information_level
        self.expand_behavior = expand_behavior
        self.ui_responses = ()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def show(self, icon: IconInfoData=None, secondary_icon: IconInfoData=None):
        """Show the notification to the player.

        """
        _notification = self._create_dialog()
        if _notification is None:
            return

        _notification.show_dialog(icon_override=icon, secondary_icon_override=secondary_icon)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _create_dialog(self) -> Union[UiDialogNotification, None]:
        return UiDialogNotification.TunableFactory().default(None,
                                                             title=lambda *args, **kwargs: self.title,
                                                             text=lambda *args, **kwargs: self.description,
                                                             visual_type=self.visual_type,
                                                             urgency=self.urgency,
                                                             information_level=self.information_level,
                                                             ui_responses=self.ui_responses,
                                                             expand_behavior=self.expand_behavior)


@sims4.commands.Command('s4clib_testing.show_basic_notification', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_basic_notification(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test basic notification.')

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.BLUE),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        dialog = CommonBasicNotification(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                         CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                         title_tokens=title_tokens,
                                         description_tokens=description_tokens,
                                         urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT)
        dialog.show()
    except Exception as ex:
        log.format_error_with_message('Failed to show a basic notification', exception=ex)
        output('Failed to show a basic notification, please locate your exception log file.')
    output('Done showing.')
