"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from objects.game_object import GameObject
from server_commands.argument_helpers import OptionalTargetParam, RequiredTargetParam
from sims.sim_info import SimInfo
from sims4.commands import CheatOutput


class CommonConsoleCommandOutput(CheatOutput):
    """An output object used when writing text to the console."""
    @property
    def connection(self) -> int:
        """The connection id to the console."""
        return self._context

    def get_sim(self, target: Union[OptionalTargetParam, RequiredTargetParam]) -> Union[SimInfo, None]:
        """get_sim(target)

        Retrieve an instance of a Sim referenced by an OptionalTargetParam or RequiredTargetParam.

        :param target: A target param.
        :type target: Union[OptionalTargetParam, RequiredTargetParam]
        :return: An instance of the Sim that matches the target or None if not found.
        :rtype: Union[Sim, None]
        """
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        from server_commands.argument_helpers import get_optional_target
        sim = get_optional_target(target, self.connection)
        sim_info = CommonSimUtils.get_sim_info(sim)
        if sim_info is None:
            self(f'Failed, Sim {target} did not exist.')
            return
        return sim_info

    def get_object(self, target: Union[OptionalTargetParam, RequiredTargetParam]) -> Union[GameObject, None]:
        """get_object(target)

        Retrieve an instance of a Game Object referenced by an OptionalTargetParam or RequiredTargetParam.

        :param target: A target param.
        :type target: Union[OptionalTargetParam, RequiredTargetParam]
        :return: An instance of the Sim that matches the target or None if not found.
        :rtype: Union[Sim, None]
        """
        if isinstance(target, OptionalTargetParam):
            from server_commands.argument_helpers import get_optional_target
            game_object = get_optional_target(target, self.connection)
        else:
            game_object: GameObject = target
        if game_object is None:
            self(f'Failed, Game Object {target} did not exist.')
            return
        return game_object
