"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Tuple, Iterator
from distributor.shared_messages import IconInfoData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogResponse
from ui.ui_dialog_notification import UiDialogNotification


class CommonBasicNotification:
    """CommonBasicNotification(\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        urgency=UiDialogNotification.UiDialogNotificationUrgency.DEFAULT,\
        information_level=UiDialogNotification.UiDialogNotificationLevel.SIM,\
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.USER_SETTING,\
        visual_type=UiDialogNotification.UiDialogNotificationVisualType.INFORMATION,\
        ui_responses=()\
    )

    A basic notification.

    .. note:: Notifications are the messages that appear at the top right in-game.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_basic_notification` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        # Will display a test dialog.
        def _common_testing_show_basic_notification():
            # LocalizedStrings within other LocalizedStrings
            title_tokens = (
                CommonLocalizationUtils.create_localized_string(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    text_color=CommonLocalizedStringColor.BLUE
                ),
            )
            description_tokens = (
                CommonLocalizationUtils.create_localized_string(
                    CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME,
                    tokens=(CommonSimUtils.get_active_sim_info(),),
                    text_color=CommonLocalizedStringColor.BLUE
                ),
            )
            dialog = CommonBasicNotification(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
            )
            dialog.show()

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param urgency: The urgency to which the notification will appear. (URGENT makes it orange) Default is Default (Blue).
    :type urgency: UiDialogNotification.UiDialogNotificationUrgency, optional
    :param information_level: The information level of the notification. Default is Sim.
    :type information_level: UiDialogNotification.UiDialogNotificationLevel, optional
    :param expand_behavior: Specify how the notification will expand. Default is User Setting.
    :type expand_behavior: UiDialogNotification.UiDialogNotificationExpandBehavior, optional
    :param visual_type: How the notification should appear. Default is Information
    :type visual_type: UiDialogNotification.UiDialogNotificationVisualType, optional
    :param ui_responses: A collection of UI Responses that may be performed within the notification.
    :type ui_responses: Tuple[UiDialogResponse], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = (),
        urgency: UiDialogNotification.UiDialogNotificationUrgency = UiDialogNotification.UiDialogNotificationUrgency.DEFAULT,
        information_level: UiDialogNotification.UiDialogNotificationLevel = UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior: UiDialogNotification.UiDialogNotificationExpandBehavior = UiDialogNotification.UiDialogNotificationExpandBehavior.USER_SETTING,
        visual_type: UiDialogNotification.UiDialogNotificationVisualType = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION,
        ui_responses: Tuple[UiDialogResponse] = ()
    ):
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self.visual_type = visual_type
        self.urgency = urgency
        self.information_level = information_level
        self.expand_behavior = expand_behavior
        self.ui_responses = ui_responses

    def show(self, icon: IconInfoData = None, secondary_icon: IconInfoData = None):
        """show(icon=None, secondary_icon=None)

        Show the notification to the player.

        :param icon: The first icon that will display in the notification.
        :type icon: IconInfoData, optional
        :param secondary_icon: The second icon that will display in the notification.
        :type secondary_icon: IconInfoData, optional
        """
        _notification = self._create_dialog()
        if _notification is None:
            return

        _notification.show_dialog(
            icon_override=icon,
            secondary_icon_override=secondary_icon
        )

    def _create_dialog(self) -> Union[UiDialogNotification, None]:
        """_create_dialog()

        Create a dialog for use in :func:``show`.

        .. note:: Override this method with any arguments you want to.
        """
        return UiDialogNotification.TunableFactory().default(
            None,
            title=lambda *args, **kwargs: self.title,
            text=lambda *args, **kwargs: self.description,
            visual_type=self.visual_type,
            urgency=self.urgency,
            information_level=self.information_level,
            ui_responses=self.ui_responses,
            expand_behavior=self.expand_behavior
        )


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_basic_notification',
    'Show an example of CommonBasicNotification.'
)
def _common_testing_show_basic_notification(output: CommonConsoleCommandOutput):
    output('Showing test basic notification.')

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (
        CommonLocalizationUtils.create_localized_string(
            CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
            text_color=CommonLocalizedStringColor.BLUE
        ),
    )
    description_tokens = (
        CommonLocalizationUtils.create_localized_string(
            CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME,
            tokens=(CommonSimUtils.get_active_sim_info(),),
            text_color=CommonLocalizedStringColor.BLUE
        ),
    )
    dialog = CommonBasicNotification(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
    )
    dialog.show()
