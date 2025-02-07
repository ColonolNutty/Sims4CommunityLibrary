"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from functools import wraps
from typing import Any, Dict, Union, Iterator, Tuple, Type, List, TYPE_CHECKING

from objects.game_object import GameObject
from sims.sim_info import SimInfo
from sims4.commands import CommandType, CommandRestrictionFlags, Output, CustomParam
from sims4.common import Pack
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService
from singletons import UNSET

if TYPE_CHECKING:
    from sims4communitylib.utils.common_log_registry import CommonLog


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
        self.is_optional = is_optional or (default_value is not None)
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
    .. note:: If the command_name contains underscores, a variant of the command_name without underscores will be added to command_aliases. i.e. 's4cl.do_thing' will be added as 's4cl.dothing' to command_aliases.
    .. note:: If any command_aliases contain underscores, variants of those command_aliases without underscores will be added to command_aliases. i.e. 's4cl.do_the_thing' will be added as 's4cl.dothething' to command_aliases.

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
        command_aliases: Iterator[str] = (),
        command_arguments: Iterator[CommonConsoleCommandArgument] = (),
        command_type: CommandType = CommandType.Live,
        command_restriction_flags: CommandRestrictionFlags = CommandRestrictionFlags.UNRESTRICTED,
        required_pack_flags: Pack = None,
        console_type: CommandType = None,
        show_with_help_command: bool = True
    ) -> None:
        self.mod_identity = mod_identity
        self.command_name = command_name
        command_without_underscores = command_name.replace('_', '')
        new_command_aliases = list(command_aliases)
        if command_without_underscores != command_name and command_without_underscores not in new_command_aliases:
            new_command_aliases.append(command_without_underscores)
        for command_alias in command_aliases:
            command_alias_without_underscores = command_alias.replace('_', '')
            if command_alias_without_underscores != command_alias and command_alias_without_underscores not in new_command_aliases:
                new_command_aliases.append(command_alias_without_underscores)
        self.command_aliases = tuple(new_command_aliases)
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


class CommonConsoleCommandService(CommonService, HasClassLog):
    """A service for creating and managing console commands."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_console_command_service'

    def __init__(self) -> None:
        super().__init__()
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
        from sims4communitylib.utils.common_log_registry import CommonLogRegistry
        help_log = CommonLogRegistry().register_log(mod_identity, f'{mod_identity.name}_help')
        mod_name = CommonModIdentity._get_mod_name(mod_identity.name).lower()
        if mod_name not in self._commands_by_mod_name:
            self._commands_by_mod_name[mod_name] = dict()

        help_command_name = self._help_command_name(mod_identity)
        if help_command_name not in self._commands_by_mod_name[mod_name]:
            @CommonConsoleCommand(
                mod_identity,
                help_command_name,
                f'Show commands for the {mod_identity.name} mod.',
                command_arguments=(
                    CommonConsoleCommandOptionalArgument('command_name', 'Text', f'If set, "{help_command_name}" will print the details of the <command_name> instead of all commands. Example: "{help_command_name} {help_command_name}"', default_value=None),
                ))
            def _common_help_command(output: CommonConsoleCommandOutput, command_name: str=None):
                try:
                    help_log.enable()
                    output('--------------------')
                    help_log.debug('--------------------')
                    output(f'NOTE: The following details have also been logged to "The Sims 4/mod_logs/<mod_name>_Messages.txt", in case not all data is shown.')
                    if command_name:
                        _command = CommonConsoleCommandService().get_command_by_mod_and_name(mod_identity, command_name)
                        if _command is None:
                            output(f'No command found with name. {command_name}')
                            help_log.debug(f'No command found with name. {command_name}')
                        else:
                            command_str = str(_command)
                            output(command_str)
                            help_log.debug(command_str)
                    else:
                        output(f'{mod_identity.name} Commands:')
                        output('- Angle Brackets (<>) means the argument is Required and must be provided when running the command')
                        output('- Square Brackets ([]) means the argument is Optional and does not need to be provided when running the command.')
                        output('- The "=..." part of an argument indicates the default value of that argument IF NOT SPECIFIED when invoking the command.')
                        output(f'- For specific details about a command, run the command like so "{help_command_name} <command_name>"')
                        output('  ')
                        help_log.debug(f'{mod_identity.name} Commands:')
                        help_log.debug('- Angle Brackets (<>) means the argument is Required and must be provided when running the command')
                        help_log.debug('- Square Brackets ([]) means the argument is Optional and does not need to be provided when running the command.')
                        help_log.debug('- The "=..." part of an argument indicates the default value of that argument IF NOT SPECIFIED when invoking the command.')
                        help_log.debug(f'- For specific details about a command, run the command like so "{help_command_name} <command_name>"')
                        help_log.debug('  ')
                        for (_command_name, _command) in sorted(list(CommonConsoleCommandService().get_commands_by_mod(mod_identity).items()), key=lambda x: x[0]):
                            _command: CommonConsoleCommand = _command
                            if not _command.show_with_help_command:
                                continue
                            command_repr = repr(_command)
                            output(command_repr)
                            help_log.debug(command_repr)
                    output('--------------------')
                    help_log.debug('--------------------')
                    output(f'NOTE: The above details have also been logged to "The Sims 4/mod_logs/<mod_name>_Messages.txt", in case not all data is shown.')
                finally:
                    help_log.disable()

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
        from sims4communitylib.utils.common_log_registry import CommonLogRegistry
        log = CommonLogRegistry().register_log(mod_identity, f'{mod_identity.name}_command_log')
        _command = cls._command(log, *command_aliases, command_type=command_type, command_restrictions=command_restriction_flags, pack=required_pack_flags, console_type=console_type)

        help_command_name = CommonConsoleCommandService()._help_command_name(mod_identity)

        def _wrapped_command(func) -> Any:
            # command_name = command_aliases[0]
            full_arg_spec = inspect.getfullargspec(func)

            @wraps(func)
            def _wrapped_func(output: CommonConsoleCommandOutput, *_, _connection: int=None, _account: int=None, **__):
                try:
                    if '_account' in full_arg_spec.args or '_account' in full_arg_spec.kwonlyargs:
                        __['_account'] = _account
                    if '_connection' in full_arg_spec.args or '_connection' in full_arg_spec.kwonlyargs:
                        __['_connection'] = _connection
                    # output(f'Running command "{command_name}"')
                    command_result = func(output, *_, **__)
                    # output(f'Command "{command_name}" finished running.')
                    return command_result
                except Exception as ex:
                    log.error(f'An exception occurred while running command. {func.__name__}', exception=ex)
                    output(f'Error: "{ex}"')

            result = _command(_wrapped_func, func, help_command_name)
            return result

        return _wrapped_command

    # noinspection PyMissingTypeHints
    @classmethod
    def _command(cls, log: 'CommonLog', *aliases: str, command_type: CommandType=CommandType.DebugOnly, command_restrictions: CommandRestrictionFlags=CommandRestrictionFlags.UNRESTRICTED, pack: Pack=None, console_type: CommandType=None):
        # noinspection PyBroadException
        try:
            import sims4.common
            import paths
            import sims4.telemetry
        except:
            # noinspection PyUnusedLocal
            def _named_command(wrapped_func, original_func, help_command_name) -> Any:
                return
            return _named_command

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

        def _named_command(wrapped_func, original_func, help_command_name) -> Any:
            if not _is_valid_command():
                return
            name = aliases[0]
            arguments = inspect.signature(original_func).parameters
            num_of_arguments = len(arguments) - 1
            num_of_required_arguments = len([v for k, v in arguments.items() if v.default is inspect.Parameter.empty]) - 1
            full_arg_spec = inspect.getfullargspec(original_func)
            spec_args = [_arg for _arg in full_arg_spec.args]
            arg_names: Tuple[str, ...] = tuple([arg_name for (arg_name, (k, v)) in zip(spec_args, arguments.items()) if arg_name != 'output' and v.default is inspect.Parameter.empty])
            kwarg_parameters_by_name = {arg_name: v.default for (arg_name, (k, v)) in zip(spec_args, arguments.items()) if arg_name != 'output' and v.default is not inspect.Parameter.empty}

            def _invoke_command(*args: str, _session_id: int=0, **kwargs):
                output = CommonConsoleCommandOutput(_session_id)
                try:
                    if not is_command_available(relevant_type):
                        return False
                    args = cls._parse_arguments(full_arg_spec, tuple(args), arg_names, kwarg_parameters_by_name, kwargs, output)
                    if args is None:
                        output('No args specified.')
                        return False
                    if len(args) + len(kwargs) > num_of_arguments:
                        output('Too many arguments were passed in.')
                        output(f'Use the help command "{help_command_name} {name}" to see what arguments are needed!')
                        return False
                    if len(args) < num_of_required_arguments:
                        num_of_args = len(args)
                        output(f'Missing some arguments. Specified Args: {num_of_args}, Required Args: {num_of_required_arguments}')
                        output(f'Use the help command "{help_command_name} {name}" to see what arguments are required!')
                        return False
                    kwargs['_account'] = _session_id
                    kwargs['_connection'] = _session_id
                    if relevant_type == CommandType.Cheat:
                        with sims4.telemetry.begin_hook(cheats_writer, TELEMETRY_HOOK_COMMAND) as hook:
                            hook.write_string(TELEMETRY_FIELD_NAME, name)
                            hook.write_string(TELEMETRY_FIELD_ARGS, str(args))
                    cls.get_log().format_with_message('Invoking the command now.', command_name=name, with_args=args, with_kwargs=kwargs)
                    return wrapped_func(output, *args, **kwargs)
                except Exception as ex:
                    output(f'ERROR: {ex}')
                    if (full_arg_spec.varargs is None or full_arg_spec.varkw is None) and any(inspect.isclass(arg_type) and isinstance(arg_type, type) and issubclass(arg_type, CustomParam) for arg_type in full_arg_spec.annotations.values()):
                        log.format_error_with_message(f'Command "{name}" has CustomParams, consider adding *args and **kwargs to your command params', exception=ex)
                    else:
                        log.error(f'Error executing command {name}', exception=ex)
                    raise ex

            _invoke_command.__name__ = 'invoke_command ({})'.format(name)
            # noinspection PyDeprecation
            usage = prettify_usage(str.format(inspect.formatargspec(*full_arg_spec)))
            description = ''
            for alias in aliases:
                register(alias, command_restrictions, _invoke_command, description, usage, most_limited_type)
            return wrapped_func

        return _named_command

    @classmethod
    def _clean_arguments(cls, args: Tuple[str]) -> Tuple[Tuple[str], Dict[str, str]]:
        cleaned_args: List[str] = list()
        cleaned_kwargs: Dict[str, Any] = dict()

        def _add_cleaned_arg_value(_cleaned_arg) -> None:
            if '=' in _cleaned_arg:
                split_val = _cleaned_arg.split('=')
                cleaned_kwargs[split_val[0]] = split_val[1]
            else:
                cleaned_args.append(_cleaned_arg)

        cls.get_log().format_with_message('Cleaning args.', args=args)

        waiting_for_match_arg: Union[str, None] = None
        for arg_val in args:
            if waiting_for_match_arg is not None:
                if '=' in arg_val:
                    # The start of a new argument, thus ending the previous one.
                    _add_cleaned_arg_value(waiting_for_match_arg)
                    waiting_for_match_arg = arg_val
                elif '"' in arg_val:
                    # The end value that results in the complete argument.
                    waiting_for_match_arg += arg_val.replace('"', '')
                    _add_cleaned_arg_value(waiting_for_match_arg)
                    waiting_for_match_arg = None
                    continue
                else:
                    # A continuation of the argument we are waiting for.
                    waiting_for_match_arg += arg_val
                    continue

            if '"' in arg_val:
                # The start of an argument that has multiple values.
                waiting_for_match_arg = arg_val.replace('"', '')
                continue

            _add_cleaned_arg_value(arg_val)

        if waiting_for_match_arg is not None:
            # If we are still waiting for an argument, we'll just put it at the end.
            _add_cleaned_arg_value(waiting_for_match_arg)
        cls.get_log().format_with_message('Cleaned up args.', args=args, cleaned_args=cleaned_args, cleaned_kwargs=cleaned_kwargs)
        return tuple(cleaned_args), cleaned_kwargs

    @classmethod
    def _parse_arguments(cls, full_arg_spec: inspect.FullArgSpec, args: Tuple[str], arg_names: Tuple[str], kwargs_by_name, kwargs: Dict[str, Any], output: Union[CommonConsoleCommandOutput, Output]):
        (cleaned_args, cleaned_kwargs) = cls._clean_arguments(args)

        from sims4communitylib.services.commands.common_console_command_parameters import CommonConsoleCommandParameter,\
            CommonOptionalSimInfoConsoleCommandParameter, CommonRequiredGameObjectConsoleCommandParameter, \
            CommonRequiredSimInfoConsoleCommandParameter
        arg_length = len(cleaned_args)
        new_args = list()
        unassigned_cleaned_args = list(cleaned_args)
        if len(cleaned_args) > len(arg_names):
            # If there are more specified arguments than there are actual arguments, we chop off the extra specified arguments to be used as kwargs instead.
            unassigned_cleaned_args = list(cleaned_args[len(arg_names):])
            cleaned_args = list(cleaned_args[:len(arg_names)])
        elif len(cleaned_args) <= len(arg_names):
            arg_names = arg_names[:len(cleaned_args)]
            unassigned_cleaned_args = list()
        for (name, cleaned_arg_value, index) in zip(arg_names, cleaned_args, range(len(arg_names))):
            if index >= arg_length:
                continue
            arg_type = full_arg_spec.annotations.get(name)
            arg_values = cleaned_arg_value.split(' ')
            if inspect.isclass(arg_type) and ((isinstance(arg_type, type) and issubclass(arg_type, CustomParam)) or arg_type is SimInfo or issubclass(arg_type, SimInfo) or arg_type is GameObject or issubclass(arg_type, GameObject)):
                if arg_type is SimInfo or issubclass(arg_type, SimInfo):
                    arg_value = CommonRequiredSimInfoConsoleCommandParameter.get_value(output, *arg_values)
                elif arg_type is GameObject or issubclass(arg_type, GameObject):
                    arg_value = CommonRequiredGameObjectConsoleCommandParameter.get_value(output, *arg_values)
                elif arg_type is CommonConsoleCommandParameter or issubclass(arg_type, CommonConsoleCommandParameter):
                    arg_value = arg_type.get_value(output, *arg_values)
                else:
                    arg_value = arg_type.get_arg_count_and_value(*arg_values)[1]

                if arg_value is UNSET:
                    new_args.append(arg_type(*arg_values))
                else:
                    new_args.append(arg_value)

            elif arg_type is not None:
                new_args.append(cls._parse_arg(arg_type, cleaned_arg_value, name, None, output))

        if full_arg_spec.varargs is not None:
            arg_type = full_arg_spec.annotations.get(full_arg_spec.varargs)
            if arg_type is not None:
                name = full_arg_spec.varargs
                for arg_value in unassigned_cleaned_args:
                    new_args.append(cls._parse_arg(arg_type, arg_value, name, None, output))

        cls.get_log().format_with_message('Finished parsing arg values', unassigned_cleaned_args=unassigned_cleaned_args, kwargs_by_name=kwargs_by_name)

        for (kwarg_name, kwarg_default_val) in kwargs_by_name.items():
            if kwarg_name not in cleaned_kwargs or cleaned_kwargs[kwarg_name] is None:
                if not unassigned_cleaned_args:
                    if kwarg_default_val is not None:
                        kwargs[kwarg_name] = kwarg_default_val
                        continue
                    kwarg_values = ()
                else:
                    kwarg_values = unassigned_cleaned_args.pop(0).split(' ')
            else:
                kwarg_values = cleaned_kwargs[kwarg_name].split(' ')

            kwarg_type = full_arg_spec.annotations.get(kwarg_name)
            if inspect.isclass(kwarg_type) and ((isinstance(kwarg_type, type) and issubclass(kwarg_type, CustomParam)) or kwarg_type is SimInfo or issubclass(kwarg_type, SimInfo) or kwarg_type is GameObject or issubclass(kwarg_type, GameObject)):
                if kwarg_type is SimInfo or issubclass(kwarg_type, SimInfo):
                    kwarg_value = CommonOptionalSimInfoConsoleCommandParameter.get_value(output, *kwarg_values)
                elif kwarg_type is GameObject or issubclass(kwarg_type, GameObject):
                    kwarg_value = CommonRequiredGameObjectConsoleCommandParameter.get_value(output, *kwarg_values)
                elif kwarg_type is CommonConsoleCommandParameter or issubclass(kwarg_type, CommonConsoleCommandParameter):
                    kwarg_value = kwarg_type.get_value(output, *kwarg_values)
                else:
                    (_, kwarg_value) = kwarg_type.get_arg_count_and_value(*kwarg_values)

                if kwarg_value is UNSET:
                    kwargs[kwarg_name] = kwarg_type(*kwarg_values)
                else:
                    kwargs[kwarg_name] = kwarg_value

            elif kwarg_type is not None:
                kwargs[kwarg_name] = cls._parse_arg(kwarg_type, ' '.join(kwarg_values), kwarg_name, kwarg_default_val, output)
        cls.get_log().format_with_message('Finished parsing arguments.', args=new_args, kwargs=kwargs)
        return new_args

    @classmethod
    def _parse_arg(cls, arg_type: Type, arg_value: Any, name: str, default_value: Any, output: Output) -> Any:
        from sims4.commands import CustomParam, BOOL_TRUE, BOOL_FALSE
        arg_type_name = arg_type.__name__ if hasattr(arg_type, '__name__') else name
        if isinstance(arg_value, str):
            if arg_type is bool:
                lower_arg_value = arg_value.lower()
                if lower_arg_value in BOOL_TRUE:
                    return True
                elif lower_arg_value in BOOL_FALSE:
                    return False
                else:
                    output(f'ERROR: Invalid entry specified for bool {name}: {arg_value} (Expected one of {BOOL_TRUE} for True, or one of {BOOL_FALSE} for False.)')
                    raise ValueError('invalid literal for boolean parameter')
            else:
                from sims4communitylib.enums.enumtypes.common_int import CommonInt
                from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
                if inspect.isclass(arg_type) and (arg_type is CommonInt or arg_type is CommonIntFlags or issubclass(arg_type, CommonInt) or issubclass(arg_type, CommonIntFlags)):
                    if arg_value is not None:
                        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
                        result = CommonResourceUtils.get_enum_by_name(arg_value.upper(), arg_type, default_value=default_value)
                        if result is None:
                            # noinspection PyUnresolvedReferences,PyTypeChecker
                            valid_values = ', '.join([val.name for val in arg_type.values])
                            output(f'ERROR: {arg_value} is not a valid {arg_type_name}. Valid {arg_type_name}: {valid_values}')
                            return None
                        return result
                elif arg_type is float:
                    # noinspection PyBroadException
                    try:
                        return float(arg_value)
                    except:
                        output(f'ERROR: Failed to parse float value {arg_value} as {arg_type_name}. Value is not a {arg_type_name}.')
                        return default_value
                elif arg_type is int or arg_value.isnumeric():
                    # noinspection PyBroadException
                    try:
                        return int(arg_value, base=0)
                    except:
                        output(f'ERROR: Failed to parse int value {arg_value} as {arg_type_name}. Value is not an {arg_type_name}.')
                        return default_value
                elif arg_type is str and not arg_value:
                    return default_value
                elif inspect.isclass(arg_type) and ((isinstance(arg_type, type) and issubclass(arg_type, CustomParam)) or arg_type is SimInfo or issubclass(arg_type, SimInfo) or arg_type is GameObject or issubclass(arg_type, GameObject)):
                    pass
                else:
                    try:
                        return arg_type(arg_value)
                    except ValueError as ex:
                        output(f'ERROR: Failed to parse value {arg_value} as {arg_type_name}: {ex}')
                        return default_value
                    except Exception as ex:
                        output(f'ERROR: Failed to parse custom value {arg_value} as {arg_type_name}: {ex}')
                        raise ex
        return arg_value


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.example_command',
    'Print an example message',
    command_aliases=('s4clib_testing.alternativeexamplecommand',),
    command_arguments=(
        CommonConsoleCommandArgument('thing_to_print', 'Text or Num', 'If specified, this value will be printed to the console.', is_optional=True, default_value='example message'),
    )
)
def _common_testing_do_example_command(output: CommonConsoleCommandOutput, thing_to_print: str = 'example message'):
    output(f'Here is what to print: {thing_to_print}')
