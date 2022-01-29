"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

import services
from server.client import Client
from server.clientmanager import ClientManager
from sims.household import Household


class CommonGameClientUtils:
    """ Utilities for getting information about the game client. """

    @staticmethod
    def get_first_game_client() -> Union[Client, None]:
        """get_first_game_client()

        Retrieve an instance of the first available Game Client.

        :return: An instance of the first available Game Client or None if not found.
        :rtype: Union[Client, None]
        """
        client_manager = CommonGameClientUtils.get_game_client_manager()
        if client_manager is None:
            return None
        return client_manager.get_first_client()

    @staticmethod
    def get_first_game_client_id() -> Union[int, None]:
        """get_first_game_client_id()

        Retrieve the id of the first available Game Client.

        :return: The id of the first available Game Client or None if not found.
        :rtype: Union[int, None]
        """
        client_manager = CommonGameClientUtils.get_game_client_manager()
        if client_manager is None:
            return None
        return client_manager.get_first_client_id()

    @staticmethod
    def get_game_client_by_household(household: Household) -> Union[Client, None]:
        """get_game_client_by_household(household)

        Locate a Game Client by a Household.

        :return: The Game Client that matches the specified Household or None if not found.
        :rtype: Union[Client, None]
        """
        if household is None:
            return None
        client_manager = CommonGameClientUtils.get_game_client_manager()
        if client_manager is None:
            return None
        return client_manager.get_client_by_household(household)

    @staticmethod
    def get_game_client_by_household_id(household_id: int) -> Union[Client, None]:
        """get_game_client_by_household_id(household_id)

        Locate a Game Client by a Household Id.

        :return: The Game Client that matches the specified Household Id or None if not found.
        :rtype: Union[Client, None]
        """
        if household_id is None:
            return None
        client_manager = CommonGameClientUtils.get_game_client_manager()
        if client_manager is None:
            return None
        return client_manager.get_client_by_household_id(household_id)

    @staticmethod
    def get_game_client_by_account_id(account_id: int) -> Union[Client, None]:
        """get_game_client_by_account_id(account_id)

        Locate a Game Client by an Account Id.

        :return: The Game Client that matches the specified Account Id or None if not found.
        :rtype: Union[Client, None]
        """
        if account_id is None:
            return None
        client_manager = CommonGameClientUtils.get_game_client_manager()
        if client_manager is None:
            return None
        return client_manager.get_client_by_account(account_id)

    @staticmethod
    def get_game_client_manager() -> ClientManager:
        """get_game_client_manager()

        Retrieve the manager that manages the Game Clients for the game.

        :return: The manager that manages the Game Clients for the game.
        :rtype: ClientManager
        """
        return services.client_manager()
