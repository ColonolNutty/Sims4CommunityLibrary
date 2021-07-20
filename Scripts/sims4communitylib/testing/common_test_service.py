"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Dict, List, Union
from functools import wraps
from traceback import format_exc
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
# This try catch is here for when tests are being run via PyCharm rather than from in-game.
try:
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry

    community_test_log_log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'community_test_log')
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
        self._tests = dict()
        self._test_count = 0

    def add_test(self, test_name: str, test_function: Callable[..., Any], class_name: str=None):
        """add_test(test_name, test_function, class_name=None)
        Register a test with the specified name and class name.

        :param test_name: The name of the test.
        :param test_function: The test itself.
        :param class_name: The name of the class the test is contained within.
        """
        if class_name is None:
            class_name = 'generic'
        else:
            class_name = class_name.lower()
        class_tests = self._tests.get(class_name, list())
        class_tests.append((test_name, test_function))
        self._test_count += 1
        self._tests[class_name] = class_tests

    @property
    def total_test_count(self) -> int:
        """Get a count of the number of tests.

        :return: The number of registered tests.
        :rtype: int
        """
        return self._test_count

    @property
    def all_tests(self) -> Dict[str, Any]:
        """Get all registered tests.

        :return: A dictionary of tests.
        :rtype: Dict[str, Any]
        """
        return self._tests

    def get_tests_by_class_name(self, class_name: str) -> List[Any]:
        """get_tests_by_class_name(class_name)

        Retrieve tests by their class name.

        :param class_name: The name of the class to locate tests for.
        :type class_name: str
        :return: A list of tests matching the class name.
        :rtype: Any
        """
        return self._tests.get(class_name, list())

    @classmethod
    def _format_test_result(cls, test_result: str, test_name: str, stacktrace: str=None):
        return 'TEST {}: {} {}\n'.format(test_result, test_name, stacktrace or '')

    @staticmethod
    def test_class(mod_identifier: Union[str, CommonModIdentity]) -> Any:
        """test_class(mod_identifier)

        Decorate a class with this to register a class as containing tests.

        :param mod_identifier: The name or identity of the mod that owns the tests within the class.
        :param mod_identifier: Union[str, CommonModIdentity]
        :return: A class wrapped to run tests.
        :rtype: Any
        """
        @CommonExceptionHandler.catch_exceptions(mod_identifier)
        def _inner_test_class(cls) -> Any:
            name_of_class = cls.__name__
            if CommonLogRegistry is not None:
                cls.test_log_log = CommonLogRegistry().register_log(mod_identifier, name_of_class)
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
                    CommonTestService.get().add_test(test_name, _wrapper, class_name=class_name)
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

    def run_tests(self, *class_names: str, callback: Callable[..., Any]=print, **__):
        """run_tests(*class_names, callback=print, **__)

        Run all tests for the specified classes names.

        :param class_names: A collection of classes to run tests for.
        :type class_names: str
        :param callback: Any time a message needs to be printed or logged, it will be sent to this callback. Default is print.
        :type callback: Callable[str, Any]
        """
        total_run_test_count = 0
        total_failed_test_count = 0
        if len(class_names) > 0:
            class_tests = class_names
        else:
            class_tests = CommonTestService.get().all_tests.keys()
        callback('Running Tests')
        for class_name in class_tests:
            _community_test_log('Running tests for class \'{}\':\n'.format(class_name))
            callback('Running Tests for class \'{}\''.format(class_name))
            tests = CommonTestService.get().get_tests_by_class_name(class_name)
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
                callback('{} of {} {} {}'.format(current_test_count, total_test_count, result, test_name))
            total_passed = total_test_count-failed_test_count
            _community_test_log('{} of {} tests Succeeded for class \'{}\'\n'.format(total_passed, total_test_count, class_name))
            callback('{} of {} tests Succeeded for class \'{}\'\n'.format(total_passed, total_test_count, class_name))
        total_run_passed = total_run_test_count-total_failed_test_count
        _community_test_log('{} of {} total tests Succeeded'.format(total_run_passed, total_run_test_count))
        callback('{} of {} total tests Succeeded'.format(total_run_passed, total_run_test_count))


try:
    import sims4.commands

    @sims4.commands.Command('s4clib.run_tests', command_type=sims4.commands.CommandType.Live)
    def _common_run_tests(*_, _connection: int=None, **__):
        output = sims4.commands.CheatOutput(_connection)
        CommonTestService.get().run_tests(*_, callback=output, **__)
except ModuleNotFoundError:
    pass
