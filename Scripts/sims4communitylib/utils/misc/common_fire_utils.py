"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple

from objects.fire.fire import Fire
from objects.game_object import GameObject
from services.fire_service import FireService
from sims4communitylib.classes.math.common_location import CommonLocation


class CommonFireUtils:
    """Utilities for manipulating fires."""

    @classmethod
    def has_active_fires(cls) -> bool:
        """has_active_fires()

        Determine if Fires are currently blazing.

        :return: True, if fires are currently blazing somewhere. False, if not.
        :rtype: bool
        """
        fire_service = cls.get_fire_service()
        if fire_service is None:
            return False
        return fire_service.fire_is_active

    @classmethod
    def get_all_active_fires(cls) -> Tuple[Fire]:
        """get_all_active_fires()

        Retrieve an instance of all active Fires.

        :return: A collection of fires currently active.
        :rtype: Tuple[Fire]
        """
        fire_service = cls.get_fire_service()
        if fire_service is None:
            return tuple()
        return fire_service.fire_is_active

    @classmethod
    def spawn_scorch_marks_at_location(cls, location: CommonLocation) -> bool:
        """spawn_scorch_marks_at_location(location)

        Spawn scorch marks at a location.

        :param location: The location to spawn the scorch marks at.
        :type location: CommonLocation
        :return: True, if scorch marks were spawned successfully. False, if not.
        :rtype: bool
        """
        fire_service = cls.get_fire_service()
        if fire_service is None:
            return False
        position = location.transform.translation
        surface_id = location.routing_surface.secondary_id
        return fire_service.add_scorch_mark(position, surface_id)

    @classmethod
    def despawn_scorch_marks_at_location(cls, location: CommonLocation) -> bool:
        """despawn_scorch_marks_at_location(location)

        Despawn scorch marks at a location.

        :param location: The location to despawn the scorch marks at.
        :type location: CommonLocation
        :return: True, if scorch marks were despawned successfully. False, if not.
        :rtype: bool
        """
        fire_service = cls.get_fire_service()
        if fire_service is None:
            return False
        position = location.transform.translation
        surface_id = location.routing_surface.secondary_id
        return fire_service.remove_scorch_mark(position, surface_id)

    @classmethod
    def is_fire_allowed_at_location(cls, location: CommonLocation, run_placement_tests: bool = True) -> bool:
        """is_fire_allowed_at_location(location, run_placement_tests=True)

        Determine if Fires are allowed to be placed at a Location.

        :param location: The location to check.
        :type location: CommonLocation
        :param run_placement_tests: Set True to run placement tests for the fire. Set False to exclude running placement tests for the fire. Default is True.
        :type run_placement_tests: bool, optional
        :return: True, if fire can be spawned as the specified location. False, if not.
        :rtype: bool
        """
        transform = location.transform
        routing_surface = location.routing_surface
        fire_service = cls.get_fire_service()
        if fire_service is None:
            return False
        return fire_service.is_fire_allowed(transform, routing_surface, run_placement_tests=run_placement_tests)

    @classmethod
    def spawn_fires_on_object(cls, game_object: GameObject, number_of_fires: int = 1) -> bool:
        """spawn_fires_on_object(game_object, number_of_fires=1)

        Spawn a number of fires on an object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param number_of_fires: The number of fires to spawn on the Object. Must be above zero. Default is 1.
        :type number_of_fires: int, optional
        :return: True, if fires have been spawned successfully. False, if not.
        :rtype: bool
        """
        if number_of_fires <= 0:
            raise AssertionError('The number of fires to spawn must be above zero.')
        fire_service = cls.get_fire_service()
        if fire_service is None:
            return False
        fire_service.spawn_fire_at_object(game_object)
        return True

    @classmethod
    def get_fire_service(cls) -> Union[FireService, None]:
        """get_fire_service()

        Retrieve the service that manages Fires.

        :return: A service that manages fires or None if not found.
        :rtype: Union[FireService, None]
        """
        import services
        return services.get_fire_service()
