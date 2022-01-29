"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any

from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.commands import CustomParam
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class CommonConsoleCommandParameter(CustomParam):
    """A custom console command parameter."""
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_value(cls, output: CommonConsoleCommandOutput, *args: str) -> Any:
        return cls.get_arg_count_and_value(output, *args)[1]

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_arg_count_and_value(cls, output: CommonConsoleCommandOutput, *args: str) -> Tuple[int, Any]:
        return super().get_arg_count_and_value(*args)


class CommonRequiredSimInfoConsoleCommandParameter(CommonConsoleCommandParameter):
    """A param that requires a Sim ID, a Sims First Name, or a Sims First and Last Name of a Sim to be specified."""

    @classmethod
    def _get_target_id(cls, arg) -> Union[int, None]:
        try:
            int_val = int(arg, 0)
        except ValueError:
            int_val = None
        return int_val

    @classmethod
    def get_value(cls, output: CommonConsoleCommandOutput, *args: str) -> SimInfo:
        """Retrieve the number of arguments taken and the value returned."""
        from singletons import UNSET
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        if len(args) == 0:
            return UNSET
        sim_id = cls._get_target_id(args[0])
        if sim_id:
            sim_info_from_id = CommonSimUtils.get_sim_info(sim_id)
            if sim_info_from_id is not None:
                return sim_info_from_id
            else:
                output(f'ERROR: Failed to locate Sim with id {args[0]}')

        if len(args) >= 2 and isinstance(args[1], str):
            first_name = args[0].lower()
            last_name = args[1].lower()
            for _sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
                if CommonSimNameUtils.get_first_name(_sim_info).lower() != first_name:
                    continue
                lower_last_name = CommonSimNameUtils.get_last_name(_sim_info).lower()
                if lower_last_name == last_name:
                    return _sim_info
                if lower_last_name == '':
                    return _sim_info

        if len(args) >= 1 and isinstance(args[0], str):
            first_name = args[0].lower()
            for _sim_info in CommonSimUtils.get_sim_info_for_all_sims_with_first_name_generator(first_name):
                return _sim_info
            output(f'ERROR: Failed to locate Sim with first name {args[0]}')
        return super().get_value(output, *args)

    def __new__(cls, output: CommonConsoleCommandOutput, *args: str) -> Union[SimInfo, None]:
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        if len(args) == 0:
            return None
        int_val = cls._get_target_id(args[0])
        if int_val is not None:
            sim_info = CommonSimUtils.get_sim_info(int_val)
            if sim_info is not None:
                return sim_info

        first_name = args[0]
        last_name = '' if len(args) == 1 else args[1]
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_with_first_name_generator(first_name):
            if last_name == '':
                return sim_info
            lower_last_name = CommonSimNameUtils.get_last_name(sim_info).lower()
            if lower_last_name == last_name:
                return sim_info
        return None


class CommonOptionalSimInfoConsoleCommandParameter(CommonRequiredSimInfoConsoleCommandParameter):
    """A param that optionally requires a Sim ID, a Sims First Name, or a Sims First and Last Name of a Sim to be specified. If not provided, the active SimInfo will be supplied instead."""

    @classmethod
    def get_value(cls, output: CommonConsoleCommandOutput, *args: str) -> SimInfo:
        """Retrieve the number of arguments taken and the value returned."""
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        sim_info = super().get_value(output, *args)
        from singletons import UNSET
        if sim_info is UNSET:
            return CommonSimUtils.get_active_sim_info()
        return sim_info

    def __new__(cls, output: CommonConsoleCommandOutput, *args: str) -> Union[SimInfo, None]:
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        return super().__new__(cls, output, *args) or CommonSimUtils.get_active_sim_info()


class CommonRequiredGameObjectConsoleCommandParameter(CommonConsoleCommandParameter):
    """A param that requires the ID of a Game Object to specified."""

    @classmethod
    def _get_target_id(cls, arg: str) -> Union[int, None]:
        try:
            int_val = int(arg, 0)
        except ValueError:
            int_val = None
        return int_val

    @classmethod
    def get_value(cls, output: CommonConsoleCommandOutput, *args: str) -> GameObject:
        """Retrieve the number of arguments taken and the value returned."""
        from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
        from singletons import UNSET
        if len(args) == 0:
            return UNSET
        obj_id = cls._get_target_id(args[0])
        if obj_id:
            game_object = CommonObjectUtils.get_game_object(obj_id)
            if game_object is not None:
                return game_object
            output(f'Failed to locate Object with id {args[0]}')
        return super().get_value(output, *args)

    def __new__(cls, output: CommonConsoleCommandOutput, *args: str) -> Union[GameObject, None]:
        from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
        from singletons import UNSET
        if len(args) == 0:
            return UNSET
        int_val = cls._get_target_id(args[0])
        if int_val is not None:
            game_object = CommonObjectUtils.get_game_object(int_val)
            if game_object is not None:
                return game_object
        return None
