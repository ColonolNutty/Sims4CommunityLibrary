"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils


class CommonPhoneUtils:
    """ Utilities for manipulating the Phone. """
    @staticmethod
    def silence_phone() -> None:
        """silence_phone()

        Silence the phone.
        """
        CommonPhoneUtils._set_phone_is_silenced(True)

    @staticmethod
    def unsilence_phone() -> None:
        """unsilence_phone()

        Unsilence the phone.
        """
        CommonPhoneUtils._set_phone_is_silenced(False)

    @staticmethod
    def phone_is_silenced() -> bool:
        """phone_is_silenced()

        Determine if the phone is silenced.

        :return: True, if the Phone is silenced. False, if not.
        :rtype: bool
        """
        # noinspection PyUnresolvedReferences
        return CommonLocationUtils.get_current_zone().ui_dialog_service.is_phone_silenced

    @staticmethod
    def _set_phone_is_silenced(is_silenced: bool):
        # noinspection PyUnresolvedReferences
        CommonLocationUtils.get_current_zone().ui_dialog_service._set_is_phone_silenced(is_silenced)


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.silence_phone',
    'Turn on the silent mode for the phone.',
    command_aliases=(
        's4clib.silencephone',
    )
)
def _common_silence_phone(output: CommonConsoleCommandOutput):
    output('Silencing Phone')
    CommonPhoneUtils.silence_phone()
    output('Done')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.unsilence_phone',
    'Turn off the silent mode for the phone.',
    command_aliases=(
        's4clib.unsilencephone',
    )
)
def _common_unsilence_phone(output: CommonConsoleCommandOutput):
    output('Unsilencing Phone')
    CommonPhoneUtils.unsilence_phone()
    output('Done')
