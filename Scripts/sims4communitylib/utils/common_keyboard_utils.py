"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from sims4communitylib.enums.common_key_code import CommonKeyCode
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo

# noinspection PyBroadException
try:
    if os.name == 'nt':
        import ctypes_module
        user32 = ctypes_module.WinDLL('user32', use_last_error=True)

        def _can_detect_key_state_for_current_os() -> bool:
            return user32 is not None

        def _is_key_currently_pressed(key: CommonKeyCode) -> bool:
            key_code = _translate_to_key_code(key)
            if key_code == -1:
                return False
            return user32.GetKeyState(key_code) > 1

        def _is_key_toggled_on(key: CommonKeyCode):
            key_code = _translate_to_key_code(key)
            if key_code == -1:
                return False
            return user32.GetKeyState(key_code) == 1

        def _translate_to_key_code(key: CommonKeyCode) -> int:
            if isinstance(key, int):
                return key
            if key is None:
                return -1
            try:
                if isinstance(key, CommonKeyCode):
                    letter_key = key.name.replace('KEY_', '')
                    if len(letter_key) == 1:
                        virtual_key = user32.VkKeyScanW(ord(letter_key))
                        if virtual_key != -1:
                            mapped_virtual_key = user32.MapVirtualKeyW(virtual_key & 255, 0)
                            mapped_scan_key = user32.MapVirtualKeyW(mapped_virtual_key & 255, 1)
                            if mapped_scan_key != 0:
                                return mapped_scan_key
            except Exception as ex:
                CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'An error occurred while translating key to key code. {}'.format(key.name), exception=ex)
            return int(key)
    else:
        # noinspection PyUnresolvedReferences, PyPackageRequirements
        import Quartz

        def _can_detect_key_state_for_current_os() -> bool:
            return Quartz.CGEventSourceKeyState is not None

        def _is_key_currently_pressed(key: CommonKeyCode) -> bool:
            key_code = _translate_to_key_code(key)
            if key_code == -1:
                return False
            return bool(Quartz.CGEventSourceKeyState(Quartz.kCGEventSourceStateHIDSystemState, key_code))

        def _is_key_toggled_on(key: CommonKeyCode):
            return _is_key_currently_pressed(key)

        def _translate_to_key_code(key: CommonKeyCode) -> int:
            if key is None:
                return -1
            return int(key)
except:
    def _can_detect_key_state_for_current_os() -> bool:
        return False

    def _is_key_currently_pressed(_: CommonKeyCode) -> bool:
        return False

    def _is_key_toggled_on(_: CommonKeyCode) -> bool:
        return False

    def _translate_to_key_code(_: CommonKeyCode) -> int:
        return int(_)


class CommonKeyboardUtils:
    """Utilities for manipulating the keyboard."""
    @staticmethod
    def can_detect_key_state_for_current_os() -> bool:
        """can_detect_key_state_for_current_os()

        Determine if CommonKeyboardUtils can detect key state for the current Operating System.

        :return: True, if CommonKeyboardUtils may correctly detect key states. False, if not.
        :rtype: bool
        """
        return _can_detect_key_state_for_current_os()

    @staticmethod
    def is_key_currently_pressed(key: CommonKeyCode) -> bool:
        """is_key_currently_pressed(key)

        Determine if a key is currently being pressed down.

        :param key: The Key to check.
        :type key: CommonKeyCode
        :return: True, if the specified key is currently being pressed down. False, if not.
        :rtype: bool
        """
        return _is_key_currently_pressed(key)

    @staticmethod
    def is_key_toggle_on(key: CommonKeyCode) -> bool:
        """is_key_toggle_on(key)

        Determine if a key is currently toggled to its on state, such as the CAPS LOCK key.

        :param key: The Key to check.
        :type key: CommonKeyCode
        :return: True, if the specified key is currently toggled on. False, if not.
        :rtype: bool
        """
        return _is_key_toggled_on(key)

    @staticmethod
    def translate_to_key_code(key: CommonKeyCode) -> int:
        """translate_to_key_code(key)

        Translate a Key to its Key Code counterpart.

        :param key: The Key to convert.
        :type key: CommonKeyCode
        :return: The integer representation of the key.
        :rtype: int
        """
        return _translate_to_key_code(key)
