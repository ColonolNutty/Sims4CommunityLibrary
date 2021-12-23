"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from functools import wraps
from typing import Any, Dict, Union, Iterator, Tuple

from sims4.commands import CommandType, CommandRestrictionFlags, Command, CheatOutput, Output
from sims4.common import Pack
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService


class CommonConsoleCommandArgument:
    """CommonConsoleCommandArgument(arg_name, arg_type_name, arg_description, is_optional=False, default_value=None)

    An object that describes details about an argument that is used in a command.

    :param arg_name: A name to display for the argument.
    :type arg_name: str
    :param arg_type_name: Text to display that represents the type of the argument.
    :type arg_type_name: str
    :param arg_description: Text that describes what the argument is for.
    :type arg_description: str
    :param is_optional: Whether or not the argument is optional or required to be specified in the command. Default is False.
    :type is_optional: bool, optional
    :param default_value: If the argument is optional, this is the default value that will be used for the argument. Default is None.
    :type default_value: Any, optional
    """
    def __init__(self, arg_name: str, arg_type_name: str, arg_description: str, is_optional: bool=False, default_value: Any=None):
        self.arg_name = arg_name
        self.arg_type_name = arg_type_name
        self.arg_description = arg_description or 'No Description Provided'
        self.is_optional = is_optional
        self.default_value = default_value

    def __repr__(self) -> str:
        name = self.arg_name
        if self.is_optional:
            default_value = self.default_value
            name = f'[{name}={default_value}]'
        else:
            name = f'{name}'
        return name

    def __str__(self) -> str:
        repr_result = self.__repr__()
        arg_type_name = self.arg_type_name
        description = self.arg_description
        return f'{repr_result} ({arg_type_name}) - {description}'


class CommonConsoleCommandOptionalArgument(CommonConsoleCommandArgument):
    """CommonConsoleCommandArgument(arg_name, arg_type_name, arg_description, default_value)

    An object that describes details about an Optional argument that is used in a command.

    :param arg_name: A name to display for the argument.
    :type arg_name: str
    :param arg_type_name: Text to display that represents the type of the argument.
    :type arg_type_name: str
    :param arg_description: Text that describes what the argument is for.
    :type arg_description: str
    :param default_value: This is the default value that will be used for the argument.
    :type default_value: Any
    """
    def __init__(self, arg_name: str, arg_type_name: str, arg_description: str, default_value: Any):
        super().__init__(arg_name, arg_type_name, arg_description, is_optional=True, default_value=default_value)


class CommonConsoleCommandRequiredArgument(CommonConsoleCommandArgument):
    """CommonConsoleCommandArgument(arg_name, arg_type_name, arg_description)

    An object that describes details about a Required argument that is used in a command.

    :param arg_name: A name to display for the argument.
    :type arg_name: str
    :param arg_type_name: Text to display that represents the type of the argument.
    :type arg_type_name: str
    :param arg_description: Text that describes what the argument is for.
    :type arg_description: str
    """
    def __init__(self, arg_name: str, arg_type_name: str, arg_description: str):
        super().__init__(arg_name, arg_type_name, arg_description, is_optional=False)


class _CommonConsoleCommandMetaclass(type):
    def __call__(
        cls,
        mod_identity: CommonModIdentity,
        command_name: str,
        command_description: str,
        command_aliases: Iterator[str]=(),
        command_arguments: Iterator[CommonConsoleCommandArgument]=(),
        command_type: CommandType=CommandType.Live,
        command_restriction_flags: CommandRestrictionFlags=CommandRestrictionFlags.UNRESTRICTED,
        required_pack_flags: Pack=None,
        console_type: CommandType=None
    ) -> Union['_CommonConsoleCommandMetaclass', None]:
        mod_name = mod_identity.name
        if mod_name is None:
            return None
        command = CommonConsoleCommandService().get_command_by_mod_and_name(mod_identity, command_name)
        if command is None:
            command = super(_CommonConsoleCommandMetaclass, cls).__call__(
                mod_identity,
                command_name,
                command_description,
                command_aliases=command_aliases,
                command_arguments=command_arguments,
                command_type=command_type,
                command_restriction_flags=command_restriction_flags,
                required_pack_flags=required_pack_flags,
                console_type=console_type
            )
            CommonConsoleCommandService()._add_command(command)
        return CommonConsoleCommandService().command(mod_identity, command_name, *command_aliases, command_type=command_type, command_restriction_flags=command_restriction_flags, required_pack_flags=required_pack_flags, console_type=console_type)


class CommonConsoleCommand(metaclass=_CommonConsoleCommandMetaclass):
    """CommonConsoleCommand(\
        mod_identity,\
        command_name,\
        command_description,\
        command_aliases=(),\
        command_arguments=(),\
        command_type=CommandType.Live,\
        command_restriction_flags=CommandRestrictionFlags.UNRESTRICTED,\
        required_pack_flags=None,\
        console_type=None\
    )

    Used to indicate a command that can be run in the CTRL+SHIFT+C console.

    .. note:: When a command is created, a Help command is also created for your Mod using the mod_identity.name (If it does not already exist) "<mod_name>.help". Use this command to display all commands that have been registered using CommonConsoleCommand.

    .. note:: To see an example command, run the command :class:`s4clib_testing.example_command` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python
        @CommonConsoleCommand(ModInfo.get_identity(), 's4clib_testing.example_command', 'Print an example message', command_aliases=('s4clib_testing.examplecommand',), command_arguments=(CommonConsoleCommandArgument('thing_to_print', 'Text or Num', 'If specified, this value will be printed to the console. Default is "24".'),))
        def _common_testing_do_example_command(output: Output, thing_to_print: str='24'):
            output(f'Here is what to print: {thing_to_print}')

    :param mod_identity: The identity of the mod that owns this command.
    :type mod_identity: CommonModIdentity
    :param command_name: The name of the command. This name can be used to run this command in the console.
    :type command_name: str
    :param command_description: Text that describes the purpose of this command and what it does.
    :type command_description: str
    :param command_aliases: Alternative names for the command that can be used to run this command in the console. Default is no aliases.
    :type command_aliases: Iterator[str], optional
    :param command_arguments: Command arguments that are used to describe details about the arguments of the command. Default is no arguments described.
    :type command_arguments: Iterator[CommonConsoleCommandArgument], optional
    :param command_type: The type of command, most of the time you will want it to be CommandType.Live. Default is CommandType.Live.
    :type command_type: CommandType, optional
    :param command_restriction_flags: Flags that indicate restrictions of the command. Default is CommandRestrictionFlags.UNRESTRICTED.
    :type command_restriction_flags: CommandRestrictionFlags, optional
    :param required_pack_flags: Flags to indicate what Game Packs are required in order for this command to be available. If set to None, no Game Packs will be required to run this command. Default is None.
    :type required_pack_flags: Pack, optional
    :param console_type: The type of console the command may be run in. If set to None, the default console will be used. Default is None.
    :type console_type: CommandType, optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        command_name: str,
        command_description: str,
        command_aliases: Iterator[str]=(),
        command_arguments: Iterator[CommonConsoleCommandArgument]=(),
        command_type: CommandType=CommandType.Live,
        command_restriction_flags: CommandRestrictionFlags=CommandRestrictionFlags.UNRESTRICTED,
        required_pack_flags: Pack=None,
        console_type: CommandType=None
    ) -> None:
        self.mod_identity = mod_identity
        self.command_name = command_name
        self.command_aliases = tuple(command_aliases)
        self.command_description = command_description
        self.command_type = command_type
        self.command_restriction_flags = command_restriction_flags
        self.required_pack_flags = required_pack_flags
        self.console_type = console_type
        self.command_arguments: Dict[str, CommonConsoleCommandArgument] = {
            arg.arg_name: arg
            for arg in command_arguments
            if arg.arg_name is not None
        }

    @property
    def arguments(self) -> Tuple[CommonConsoleCommandArgument]:
        """The arguments of the command."""
        return tuple(self.command_arguments.values())

    def __call__(self, *args, **kwargs) -> Any:
        # noinspection PyUnresolvedReferences
        return super().__call__(self, *args, **kwargs)

    def __repr__(self) -> str:
        arg_str = ' '.join([repr(command_argument) for command_argument in self.arguments])
        name = self.command_name
        description = self.command_description
        return f'{name} {arg_str} - {description}'

    def __str__(self) -> str:
        arg_str = '\n  '.join([str(command_argument) for command_argument in self.arguments])
        name = self.command_name
        description = self.command_description
        return f'{name} - {description}\n  {arg_str}'


class CommonConsoleCommandService(CommonService):
    """A service for creating and managing console commands."""

    def __init__(self) -> None:
        self._commands_by_mod_name: Dict[str, Dict[str, CommonConsoleCommand]] = dict()

    def _add_command(self, command: CommonConsoleCommand) -> None:
        """Add a command to the library of commands."""
        mod_identity = command.mod_identity
        mod_name = CommonModIdentity._get_mod_name(mod_identity.name).lower()
        if mod_name not in self._commands_by_mod_name:
            self._commands_by_mod_name[mod_name] = dict()
        self._commands_by_mod_name[mod_name][command.command_name] = command

        self._create_help_command(mod_identity)

    def _help_command_name(self, mod_identity: CommonModIdentity) -> str:
        mod_name = CommonModIdentity._get_mod_name(mod_identity.name).lower()
        return f'{mod_name}.help'

    def _create_help_command(self, mod_identity: CommonModIdentity) -> None:
        mod_name = CommonModIdentity._get_mod_name(mod_identity.name).lower()
        if mod_name not in self._commands_by_mod_name:
            self._commands_by_mod_name[mod_name] = dict()

        help_command_name = self._help_command_name(mod_identity)
        if help_command_name not in self._commands_by_mod_name[mod_name]:
            @CommonConsoleCommand(mod_identity, help_command_name, f'Show commands for the {mod_identity.name} mod.', command_arguments=(CommonConsoleCommandOptionalArgument('command_name', 'Text', f'If set, "{help_command_name}" will print the details of the <command_name> instead of all commands. Example: "{help_command_name} {help_command_name}"', default_value=None),))
            def _common_help_command(output: Output, command_name: str=None):
                output('--------------------')
                if command_name is not None:
                    _command = CommonConsoleCommandService().get_command_by_mod_and_name(mod_identity, command_name)
                    if _command is None:
                        output(f'No command found with name. {command_name}')
                    else:
                        output(str(_command))
                else:
                    output(f'{mod_identity.name} Commands:')
                    output('- Angle Brackets (<>) means the argument is Required and must be provided when running the command')
                    output('- Square Brackets ([]) means the argument is Optional and does not need to be provided when running the command.')
                    output('- The "=..." part of an argument indicates the default value of that argument IF NOT SPECIFIED when invoking the command.')
                    output(f'- For specific details about a command, run the command like so "{help_command_name} <command_name>"')
                    output('  ')
                    for (_command_name, _command) in CommonConsoleCommandService().get_commands_by_mod(mod_identity).items():
                        output(repr(_command))
                output('--------------------')

    def get_commands_by_mod(self, mod_identity: CommonModIdentity) -> Dict[str, CommonConsoleCommand]:
        """Retrieve the commands available for a mod."""
        mod_name = CommonModIdentity._get_mod_name(mod_identity.name).lower()
        if mod_name not in self._commands_by_mod_name:
            return dict()
        return self._commands_by_mod_name[mod_name]

    def get_command_by_mod_and_name(self, mod_identity: CommonModIdentity, command_name: str) -> Union[CommonConsoleCommand, None]:
        """Retrieve the commands available for a mod."""
        mod_name = CommonModIdentity._get_mod_name(mod_identity.name).lower()
        if mod_name not in self._commands_by_mod_name or command_name not in self._commands_by_mod_name[mod_name]:
            return None
        return self._commands_by_mod_name[mod_name][command_name]

    @staticmethod
    def command(mod_identity: CommonModIdentity, *command_aliases: str, command_type: CommandType=CommandType.Live, command_restriction_flags: CommandRestrictionFlags=CommandRestrictionFlags.UNRESTRICTED, required_pack_flags: Pack=None, console_type: CommandType=None) -> Any:
        """Create a command."""
        _command = Command(*command_aliases, command_type=command_type, command_restrictions=command_restriction_flags, pack=required_pack_flags, console_type=console_type)

        name = command_aliases[0]

        help_command_name = CommonConsoleCommandService()._help_command_name(mod_identity)

        def _wrapped_command(func) -> Any:
            arguments = inspect.signature(func).parameters
            num_of_arguments = len(arguments) - 1
            num_of_required_arguments = len([v for k, v in arguments.items() if v.default is inspect.Parameter.empty]) - 1

            @wraps(func)
            def _wrapped_func(*_, _connection: int=None, **__):
                output = CheatOutput(_connection)
                try:
                    if len(_) + len(__) > num_of_arguments:
                        output('Too many arguments were passed in.')
                        output(f'Use the help command "{help_command_name} {name}" to see what arguments are needed!')
                        return False
                    if len(_) < num_of_required_arguments:
                        output('Missing some arguments.')
                        output(f'Use the help command "{help_command_name} {name}" to see what arguments are required!')
                        return False
                    return func(output, *_, **__)
                except Exception as ex:
                    CommonExceptionHandler.log_exception(mod_identity, f'An exception occurred while running command. {func.__name__}', exception=ex)
                    output(f'An error occurred while running command. Exception: "{ex}"')

            return _command(_wrapped_func)
        return _wrapped_command


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_testing.example_command', 'Print an example message', command_aliases=('s4clib_testing.examplecommand',), command_arguments=(CommonConsoleCommandArgument('thing_to_print', 'Text or Num', 'If specified, this value will be printed to the console. Default is "24".'),))
def _common_testing_do_example_command(output: Output, thing_to_print: str='24'):
    output(f'Here is what to print: {thing_to_print}')
