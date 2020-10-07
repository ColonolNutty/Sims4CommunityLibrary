"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
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
