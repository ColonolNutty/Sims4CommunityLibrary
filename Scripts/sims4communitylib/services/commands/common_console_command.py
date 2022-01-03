"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from functools import wraps
from typing import Any, Dict, Union, Iterator, Tuple, Type

from sims4.commands import CommandType, CommandRestrictionFlags, CheatOutput, Output, CustomParam
from sims4.common import Pack
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from singletons import UNSET


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
        console_type: CommandType=None,
        show_with_help_command: bool=True
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
                console_type=console_type,
                show_with_help_command=show_with_help_command
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
        console_type=None,\
        show_with_help_command=True\
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
    :param show_with_help_command: If True, this command will appear when a player does "<mod_name>.help". If False, it will not appear when a player does "<mod_name>.help" but will still appear when they do "<mod_name>.help <command>". Default is True.
    :type show_with_help_command: bool, optional
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
        console_type: CommandType=None,
        show_with_help_command: bool=True
    ) -> None:
        self.mod_identity = mod_identity
        self.command_name = command_name
        self.command_aliases = tuple(command_aliases)
        self.command_description = command_description
        self.command_type = command_type
        self.command_restriction_flags = command_restriction_flags
        self.required_pack_flags = required_pack_flags
        self.console_type = console_type
        self.show_with_help_command = show_with_help_command
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
                        _command: CommonConsoleCommand = _command
                        if not _command.show_with_help_command:
                            continue
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

    @classmethod
    def command(cls, mod_identity: CommonModIdentity, *command_aliases: str, command_type: CommandType=CommandType.Live, command_restriction_flags: CommandRestrictionFlags=CommandRestrictionFlags.UNRESTRICTED, required_pack_flags: Pack=None, console_type: CommandType=None) -> Any:
        """Create a command."""
        log = CommonLogRegistry().register_log(mod_identity, f'{mod_identity.name}_command_log')
        _command = cls._command(log, *command_aliases, command_type=command_type, command_restrictions=command_restriction_flags, pack=required_pack_flags, console_type=console_type)

        name = command_aliases[0]

        help_command_name = CommonConsoleCommandService()._help_command_name(mod_identity)

        def _wrapped_command(func) -> Any:
            arguments = inspect.signature(func).parameters
            num_of_arguments = len(arguments) - 1
            num_of_required_arguments = len([v for k, v in arguments.items() if v.default is inspect.Parameter.empty]) - 1
            full_arg_spec = inspect.getfullargspec(func)

            @wraps(func)
            def _wrapped_func(*_, _connection: int=None, _account: int=None, **__):
                output = CheatOutput(_connection)
                try:
                    if '_account' in full_arg_spec.args or '_account' in full_arg_spec.kwonlyargs:
                        __['_account'] = _account
                    if '_connection' in full_arg_spec.args or '_connection' in full_arg_spec.kwonlyargs:
                        __['_connection'] = _connection
                    output('Doing command')
                    if len(_) + len(__) > num_of_arguments:
                        output('Too many arguments were passed in.')
                        output(f'Use the help command "{help_command_name} {name}" to see what arguments are needed!')
                        return False
                    if len(_) < num_of_required_arguments:
                        output('Missing some arguments.')
                        output(f'Use the help command "{help_command_name} {name}" to see what arguments are required!')
                        return False
                    command_result = func(output, *_, **__)
                    output('Done')
                    return command_result
                except Exception as ex:
                    log.error(f'An exception occurred while running command. {func.__name__}', exception=ex)
                    output(f'Error: "{ex}"')

            result = _command(_wrapped_func, func)
            return result

        return _wrapped_command

    # noinspection PyMissingTypeHints
    @classmethod
    def _command(cls, log: CommonLog, *aliases, command_type=CommandType.DebugOnly, command_restrictions=CommandRestrictionFlags.UNRESTRICTED, pack=None, console_type=None):
        import sims4.common
        import paths
        import sims4.telemetry
        from sims4.commands import CommandType, \
            is_command_available, cheats_writer, TELEMETRY_FIELD_NAME, TELEMETRY_FIELD_ARGS, TELEMETRY_HOOK_COMMAND, CustomParam, \
            prettify_usage, register
        if console_type is not None and not paths.IS_DESKTOP:
            relevant_type = console_type
        else:
            relevant_type = command_type
        if console_type is not None:
            most_limited_type = min(command_type, console_type)
        else:
            most_limited_type = command_type

        def _is_valid_command() -> bool:
            if relevant_type == CommandType.DebugOnly:
                return False
            elif pack and not sims4.common.are_packs_available(pack):
                return False
            return True

        def _named_command(wrapped_func, original_func) -> Any:
            if not _is_valid_command():
                return
            name = aliases[0]
            full_arg_spec = inspect.getfullargspec(original_func)

            def _invoke_command(*args, _session_id: int=0, **kw):
                kw['_account'] = _session_id
                kw['_connection'] = _session_id
                output = CheatOutput(_session_id)
                try:
                    args = cls._parse_arguments(full_arg_spec, args, output)
                    if not is_command_available(relevant_type):
                        return
                    if relevant_type == CommandType.Cheat:
                        with sims4.telemetry.begin_hook(cheats_writer, TELEMETRY_HOOK_COMMAND) as hook:
                            hook.write_string(TELEMETRY_FIELD_NAME, name)
                            hook.write_string(TELEMETRY_FIELD_ARGS, str(args))
                    return wrapped_func(*args, **kw)
                except BaseException as e:
                    output(f'Error: {e}')
                    log.warn('Error executing command')
                    if (full_arg_spec.varargs is None or full_arg_spec.varkw is None) and any(isinstance(arg_type, type) and issubclass(arg_type, CustomParam) for arg_type in full_arg_spec.annotations.values()):
                        log.warn('Command has CustomParams, consider adding *args and **kwargs to your command params')
                    raise e

            _invoke_command.__name__ = 'invoke_command ({})'.format(name)
            # noinspection PyDeprecation
            usage = prettify_usage(str.format(inspect.formatargspec(*full_arg_spec)))
            description = ''
            for alias in aliases:
                register(alias, command_restrictions, _invoke_command, description, usage, most_limited_type)
            return wrapped_func

        return _named_command

    @classmethod
    def _parse_arguments(cls, spec, args, output: Output):
        args = list(args)
        index = 0
        # We slice off the front so that output is not considered.
        spec_args = [_arg for _arg in spec.args if _arg != 'output']
        for (name, index) in zip(spec_args, range(len(spec.args))):
            if index >= len(args):
                break
            arg_type = spec.annotations.get(name)
            if isinstance(arg_type, type) and issubclass(arg_type, CustomParam):
                (arg_count, arg_value) = arg_type.get_arg_count_and_value(*args[index:])
                if arg_value is UNSET:
                    arg_values = args[index:index + arg_count]
                    args[index] = arg_type(*arg_values)
                else:
                    args[index] = arg_value

                if arg_count > 1:
                    del args[index + 1:index + arg_count]
                    index += arg_count - 1
                    if arg_type is not None:
                        arg_value = args[index]
                        cls._parse_arg(args, arg_type, arg_value, name, index, output)

            elif arg_type is not None:
                arg_value = args[index]
                cls._parse_arg(args, arg_type, arg_value, name, index, output)
        if spec.varargs is not None:
            arg_type = spec.annotations.get(spec.varargs)
            if arg_type is not None:
                index += 1
                vararg_list = args[index:]
                name = spec.varargs
                for arg_value in vararg_list:
                    cls._parse_arg(args, arg_type, arg_value, name, index, output)
                    index += 1
        return args

    @classmethod
    def _parse_arg(cls, args, arg_type: Type, arg_value: Any, name: str, index: int, output: Output):
        from sims4.commands import CustomParam, \
            BOOL_TRUE, BOOL_FALSE
        if isinstance(arg_value, str):
            if arg_type is bool:
                lower_arg_value = arg_value.lower()
                if lower_arg_value in BOOL_TRUE:
                    args[index] = True
                elif lower_arg_value in BOOL_FALSE:
                    args[index] = False
                else:
                    output('Invalid entry specified for bool {}: {} (Expected one of {} for True, or one of {} for False.)'.format(name, arg_value, BOOL_TRUE, BOOL_FALSE))
                    raise ValueError('invalid literal for boolean parameter')
            else:
                if arg_type is int:
                    args[index] = int(arg_value, base=0)
                elif isinstance(arg_type, type) and issubclass(arg_type, CustomParam):
                    pass
                else:
                    args[index] = arg_type(arg_value)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_testing.example_command', 'Print an example message', command_aliases=('s4clib_testing.examplecommand',), command_arguments=(CommonConsoleCommandArgument('thing_to_print', 'Text or Num', 'If specified, this value will be printed to the console. Default is "24".'),))
def _common_testing_do_example_command(output: Output, thing_to_print: str='24'):
    output(f'Here is what to print: {thing_to_print}')
