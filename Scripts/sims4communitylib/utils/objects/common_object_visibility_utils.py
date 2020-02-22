"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from objects.game_object import GameObject
from objects.persistence_groups import PersistenceGroups


class CommonObjectVisibilityUtils:
    """Utilities for manipulating the visibility and persistence of Objects.

    """

    @staticmethod
    def set_opacity(game_object: GameObject, opacity: int) -> bool:
        """set_opacity(game_object, opacity)

        Set the opacity of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param opacity: Determines how opaque the Object will be.
        :type opacity: int
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if game_object is None or opacity is None:
            return False
        game_object.opacity = opacity
        return True

    @staticmethod
    def get_opacity(game_object: GameObject) -> int:
        """get_opacity(game_object)

        Retrieve the opacity of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: How opaque the Object is.
        :rtype: int
        """
        if game_object is None:
            return 0
        # noinspection PyPropertyAccess
        return game_object.opacity

    @staticmethod
    def set_persistence_group(game_object: GameObject, persistence_group: PersistenceGroups) -> bool:
        """set_persistence_group(game_object, persistence_group)

        Set the persistence group of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param persistence_group: The PersistenceGroup of the Object.
        :type persistence_group: PersistenceGroups
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        if game_object is None or persistence_group is None:
            return False
        game_object.persistence_group = persistence_group
        return True

    @staticmethod
    def get_persistence_group(game_object: GameObject) -> PersistenceGroups:
        """get_persistence_group(game_object)

        Retrieve the persistence group of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The persistence group of the Object.
        :rtype: PersistenceGroups, optional
        """
        if game_object is None:
            return PersistenceGroups.NONE
        return game_object.persistence_group
