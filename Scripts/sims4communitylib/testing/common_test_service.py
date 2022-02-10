"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Dict, List, Union, Tuple
from functools import wraps
from traceback import format_exc
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
# This try catch is here for when tests are being run via PyCharm rather than from in-game.
try:
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry

    community_test_log_log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'community_test_log')
    community_test_log_log.enable()

    def _community_test_log(val: str):
        community_test_log_log.debug(val)
except ModuleNotFoundError:
    # noinspection PyMissingOrEmptyDocstring
    class CommonLogRegistry:

        @classmethod
        def get(cls, *_, **__) -> 'CommonLogRegistry':
            pass

        def register_log(self) -> None:
            pass

    def _community_test_log(_: str):
        pass


class CommonTestResultType:
    """Use to identify the results of running a test.

    """
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'


class CommonTestService(CommonService):
    """Use to register and run python tests.

    :Example Test Registration:

    .. highlight:: python
    .. code-block:: python

        @CommonTestService.test_class('mod_name')
        class TestClass:
            # Important that it is a static method, you won't get a cls or self value passed in, so don't expect one!
            @staticmethod
            @CommonTestService.test(1, 1, expected_value=2)
            @CommonTestService.test(2, 1, expected_value=3)
            def example_add_test(one: int, two: int, expected_value: int=24):
                result = one + two
                CommonAssertionUtils.are_equal(result, expected_value, message='{} plus {} did not equal {}!'.format(one, two, expected_value))

    """
    def __init__(self) -> None:
        self._tests_by_mod_identity = dict()
        self._test_count = 0

    def add_test(self, mod_identity: CommonModIdentity, test_name: str, test_function: Callable[..., Any], class_name: str=None):
        """add_test(mod_identity, test_name, test_function, class_name=None)

        Register a test with the specified name and class name.

        :param mod_identity: The identity of the mod the test is for.
        :type mod_identity: CommonModIdentity
        :param test_name: The name of the test.
        :type test_name: str
        :param test_function: The test itself.
        :type test_function: Callable[..., Any]
        :param class_name: The name of the class the test is contained within.
        :type class_name: str
        """
        if class_name is None:
            class_name = 'generic'
        else:
            class_name = class_name.lower()
        class_tests_by_name = self.get_test_library_by_mod(mod_identity)
        class_tests = class_tests_by_name.get(class_name, list())
        class_tests.append((test_name, test_function))
        self._test_count += 1
        class_tests_by_name[class_name] = class_tests
        self._tests_by_mod_identity[mod_identity] = class_tests_by_name

    @property
    def total_test_count(self) -> int:
        """Get a count of the number of tests.

        :return: The number of registered tests.
        :rtype: int
        """
        return self._test_count

    @property
    def all_tests(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tests.

        :return: A dictionary of tests by mod name.
        :rtype: Dict[str, Dict[str, Any]]
        """
        return self._tests_by_mod_identity

    def get_tests_by_class_name(self, class_name: str) -> List[Any]:
        """get_tests_by_class_name(class_name)

        Retrieve tests by their class name.

        :param class_name: The name of the class to locate tests for.
        :type class_name: str
        :return: A list of tests matching the class name.
        :rtype: List[Any]
        """
        class_tests = list()
        for (_, class_tests_by_class_name) in self._tests_by_mod_identity.items():
            class_tests.extend(class_tests_by_class_name.get(class_name, list()))
        return class_tests

    def get_test_library_by_mod(self, mod_identifier: Union[str, CommonModIdentity]) -> Dict[str, Any]:
        """get_test_library_by_mod(mod_identifier)

        Retrieve a library of tests for a Mod organized by class name.

        :param mod_identifier: The name or identity of the mod to search tests for.
        :param mod_identifier: Union[str, CommonModIdentity]
        :return: A library of tests for the specified Mod organized by class name.
        :rtype: Dict[str, Any]
        """
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier, include_version=False).lower()
        for (mod_identity, tests_by_class_name) in self._tests_by_mod_identity.items():
            lower_mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identity, include_version=False).lower()
            if lower_mod_name == mod_name:
                return tests_by_class_name
        return dict()

    def get_tests_by_mod_name(self, mod_identifier: Union[str, CommonModIdentity]) -> Tuple[Any]:
        """get_tests_by_mod_name(mod_name)

        Retrieve tests by a mod name.

        :param mod_identifier: The name or identity of the mod that owns the tests within the class.
        :param mod_identifier: Union[str, CommonModIdentity]
        :return: A collection of tests for the specified Mod.
        :rtype: Tuple[Any]
        """
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier, include_version=False).lower()
        class_tests_by_class_name = self._tests_by_mod_identity.get(mod_name, dict())
        all_tests: List[Any] = list()
        for (_, tests) in class_tests_by_class_name.items():
            all_tests.extend(tests)
        return tuple(all_tests)

    @classmethod
    def _format_test_result(cls, test_result: str, test_name: str, stacktrace: str=None):
        return 'TEST {}: {} {}\n'.format(test_result, test_name, stacktrace or '')

    @staticmethod
    def test_class(mod_identity: CommonModIdentity) -> Any:
        """test_class(mod_identity)

        Decorate a class with this to register a class as containing tests.

        :param mod_identity: The identity of the mod that owns the tests within the class.
        :param mod_identity: CommonModIdentity
        :return: A class wrapped to run tests.
        :rtype: Any
        """
        @CommonExceptionHandler.catch_exceptions(mod_identity)
        def _inner_test_class(cls) -> Any:
            name_of_class = cls.__name__
            if CommonLogRegistry is not None:
                cls.test_log_log = CommonLogRegistry().register_log(mod_identity, name_of_class)
                cls.test_log_log.enable()
                cls.test_log = lambda val: cls.test_log_log.debug(val)
            else:
                cls.test_log = lambda val: print(val)
            for method_name in dir(cls):
                method = getattr(cls, method_name)
                if not hasattr(method, 'is_test'):
                    continue

                def _test_function(class_name, test_name, test_method, *_, **__) -> None:
                    @wraps(test_method)
                    def _wrapper(*args, **kwargs) -> str:
                        arguments = (_ + args)
                        new_test_name = '{} (Arguments: {}, Keyword Arguments: {})'.format(test_name, arguments, (kwargs, __))
                        # noinspection PyBroadException
                        try:
                            test_method(*(_ + args), **kwargs, **__)
                            cls.test_log(CommonTestService._format_test_result(CommonTestResultType.SUCCESS, new_test_name))
                        except AssertionError:
                            cls.test_log(CommonTestService._format_test_result(CommonTestResultType.FAILED, new_test_name, stacktrace=format_exc()))
                            return CommonTestResultType.FAILED
                        except Exception:
                            cls.test_log(CommonTestService._format_test_result(CommonTestResultType.FAILED, new_test_name, stacktrace=format_exc()))
                            return CommonTestResultType.FAILED
                        return CommonTestResultType.SUCCESS
                    CommonTestService.get().add_test(mod_identity, test_name, _wrapper, class_name=class_name)
                if hasattr(method, 'test_parameters') and len(method.test_parameters) > 0:
                    idx = 1
                    for test_args, test_kwargs in method.test_parameters:
                        _test_function(name_of_class, '{} {}'.format(method_name, str(idx)), method, *test_args, **test_kwargs)
                        idx += 1
                else:
                    _test_function(name_of_class, method_name, method)
            return cls
        return _inner_test_class

    @staticmethod
    def test(*args, **kwargs) -> Callable[..., Any]:
        """test(args, kwargs)

        Decorate a function with this to register that function as a test.
        When the test is run, it will be sent the specified arguments and keyword arguments.

        .. warning:: The function being registered MUST be a staticmethod.

        :param args: The arguments that will be sent to the function upon run.
        :type args: Any
        :param kwargs: The keyword arguments that will be sent to the function upon run.
        :type kwargs: Any
        :return: A function wrapped to run a test upon invocation.
        :rtype: Callable[..., Any]
        """
        def _test_func(test_function) -> Any:
            test_function.is_test = True
            if not hasattr(test_function, 'test_parameters'):
                test_function.test_parameters = list()
            test_function.test_parameters.append((args, kwargs))
            return test_function
        return _test_func

    def run_tests(self, class_names: Tuple[str]=tuple(), callback: Callable[..., Any]=print):
        """run_tests(class_names=tuple(), callback=print)

        Run all tests for the specified classes names.

        :param class_names: A collection of classes to run tests for.
        :type class_names: Tuple[str]
        :param callback: Any time a message needs to be printed or logged, it will be sent to this callback. Default is print.
        :type callback: Callable[str, Any]
        """
        return self._run_tests(mod_identifier=None, class_names=class_names, callback=callback)

    def run_tests_by_mod_name(self, mod_identifier: Union[str, CommonModIdentity], class_names: Tuple[str]=tuple(), callback: Callable[..., Any]=print):
        """run_tests_by_mod_name(mod_identifier, class_names=tuple(), callback=print)

        Run all tests for the specified classes names for a specific Mod.

        :param mod_identifier: The name or identity of the mod to run tests for.
        :param mod_identifier: Union[str, CommonModIdentity]
        :param class_names: A collection of classes to run tests for. Default is all tests.
        :type class_names: Tuple[str], optional
        :param callback: Any time a message needs to be printed or logged, it will be sent to this callback. Default is print.
        :type callback: Callable[str, Any]
        """
        return self._run_tests(mod_identifier=mod_identifier, class_names=class_names, callback=callback)

    def _run_tests(self, mod_identifier: Union[str, CommonModIdentity]=None, class_names: Tuple[str]=tuple(), callback: Callable[..., Any]=print):
        total_run_test_count = 0
        total_failed_test_count = 0
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        if mod_identifier:
            to_run_mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier, include_version=False).lower()
        else:
            to_run_mod_name = None
        for (mod_identity, class_tests_by_class_name) in self.all_tests.items():
            mod_name = mod_identity.name
            if to_run_mod_name:
                from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
                cleaned_mod_name = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identity, include_version=False).lower()
                if cleaned_mod_name != to_run_mod_name:
                    continue
            mod_log = CommonLogRegistry().register_log(mod_identity, 'test_log')
            try:
                mod_log.enable()
                callback(f'Running Tests for mod \'{mod_name}\'')
                mod_log.debug(f'Running Tests for mod \'{mod_name}\'')
                for (class_name, tests) in class_tests_by_class_name.items():
                    if class_names and class_name not in class_names:
                        continue
                    class_log = CommonLogRegistry().register_log(mod_identity, class_name)
                    try:
                        class_log.enable()
                        callback(f'Running Tests for class \'{class_name}\'')
                        class_log.debug(f'Running Tests for class \'{class_name}\'')
                        total_test_count = len(tests)
                        failed_test_count = 0
                        current_test_count = 0
                        for test_name, test in tests:
                            total_run_test_count += 1
                            current_test_count += 1
                            result = test()
                            if result == CommonTestResultType.FAILED:
                                failed_test_count += 1
                                total_failed_test_count += 1
                            callback(f'{current_test_count} of {total_test_count} {result} {test_name}')
                            class_log.debug(f'{current_test_count} of {total_test_count} {result} {test_name}')
                        total_passed = total_test_count-failed_test_count
                        callback(f'{total_passed} of {total_test_count} tests Succeeded for class \'{class_name}\'\n')
                        class_log.debug(f'{total_passed} of {total_test_count} tests Succeeded for class \'{class_name}\'\n')
                    finally:
                        class_log.disable()
                total_run_passed = total_run_test_count-total_failed_test_count
                callback(f'{total_run_passed} of {total_run_test_count} total tests Succeeded')
                mod_log.debug(f'{total_run_passed} of {total_run_test_count} total tests Succeeded')
            finally:
                mod_log.disable()


try:
    from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
        CommonConsoleCommandArgument
    from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput

    @CommonConsoleCommand(
        ModInfo.get_identity(),
        's4clib.run_tests',
        'Run any tests that are registered with S4CL (Only useful to mod authors)',
        command_arguments=(
            CommonConsoleCommandArgument('class_name', 'Text', 'If specified, only the tests located within the class matching this name will be run. If not specified, all registered tests will run.', is_optional=True, default_value='All Tests'),
            CommonConsoleCommandArgument('mod_name', 'Text', 'If specified, only the tests registered by the mod with this name will be run. If not specified, all registered tests by all mods will run.', is_optional=True, default_value='All Mods'),
        )
    )
    def _common_run_tests(output: CommonConsoleCommandOutput, class_name: str=None, mod_name: str=None):
        class_names = tuple()
        if class_name is not None:
            class_names = (class_name,)
        if mod_name is not None:
            CommonTestService().run_tests_by_mod_name(mod_name, class_names, callback=output)
        else:
            CommonTestService.get().run_tests(class_names, callback=output)
except ModuleNotFoundError:
    pass
