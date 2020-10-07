"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from typing import Any


class CommonSaveUtils:
    """ Utilities for managing save files. """
    @staticmethod
    def get_save_slot_guid() -> int:
        """get_save_slot_guid()

        Retrieve the guid identifier for the current save slot.

        :return: The GUID identifier for the current save slot.
        :return: int
        """
        return services.get_persistence_service().get_save_slot_proto_guid()

    @staticmethod
    def get_save_slot() -> Any:
        """get_save_slot()

        Retrieve the current save slot.

        :return: The current save slot.
        :return: Any
        """
        return services.get_persistence_service().get_save_slot_proto_buff()

    @staticmethod
    def get_save_slot_id() -> int:
        """get_save_slot_id()

        Retrieve the identifier for the current save slot.

        :return: The identifier for the current save slot.
        :return: int
        """
        return CommonSaveUtils.get_save_slot().slot_id

    @staticmethod
    def get_save_account() -> Any:
        """get_save_account()

        Retrieve the current save account.

        :return: The current save account.
        :return: Any
        """
        return services.get_persistence_service().get_account_proto_buff()
