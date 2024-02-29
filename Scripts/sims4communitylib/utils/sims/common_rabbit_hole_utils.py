"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

import services
from rabbit_hole.rabbit_hole import RabbitHole
from services.rabbit_hole_service import RabbitHoleService


class CommonRabbitHoleUtils:
    """Utilities for manipulating rabbit holes."""

    @classmethod
    def get_rabbit_hole_service(cls) -> RabbitHoleService:
        """get_rabbit_hole_service()

        Retrieve an instance of the Rabbit Hole Service.

        :return: The service that manages rabbit holes.
        :rtype: RabbitHoleService
        """
        return services.get_rabbit_hole_service()

    @classmethod
    def load_rabbit_hole_by_id(cls, rabbit_hole: Union[int, RabbitHole]) -> Union[RabbitHole, None]:
        """load_rabbit_hole_by_id(rabbit_hole)

        Load an instance of a Rabbit Hole by its identifier.

        :param rabbit_hole: The identifier of a Rabbit Hole.
        :type rabbit_hole: Union[int, RabbitHole]
        :return: An instance of a Rabbit Hole matching the decimal identifier or None if not found.
        :rtype: Union[RabbitHole, None]
        """
        if isinstance(rabbit_hole, RabbitHole):
            return rabbit_hole
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            rabbit_hole_instance = rabbit_hole()
            if isinstance(rabbit_hole_instance, RabbitHole):
                # noinspection PyTypeChecker
                return rabbit_hole
        except:
            pass
        # noinspection PyBroadException
        try:
            rabbit_hole: int = int(rabbit_hole)
        except:
            # noinspection PyTypeChecker
            rabbit_hole: RabbitHole = rabbit_hole
            return rabbit_hole

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.RABBIT_HOLE, rabbit_hole)
