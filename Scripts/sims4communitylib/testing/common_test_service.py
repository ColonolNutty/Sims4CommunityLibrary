"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Dict, List
from functools import wraps
from traceback import format_exc
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
try:
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry

    community_test_log_log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'community_test_log')
    community_test_log_log.enable()

    def _community_test_log(val: str):
        community_test_log_log.debug(val)
except ModuleNotFoundError:
    CommonLogRegistry = None

    def _community_test_log(_: str):
        pass


class CommonTestResultType:
    """Use to identify the results of running a test.

    """
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'


class CommonTestService(CommonService):
    """Use to register and run python tests.

    Test Registration Example:

    @CommonTestService.test_class('mod_name')
    class TestClass:
        # Important that it is a static method, you won't get a cls or self value passed in, so don't expect one!
        @staticmethod
        @CommonTestService.test(1, 1, 2)
        @CommonTestService.test(2, 1, 3)
        def example_add_test(one: int, two: int, expected_value: int):
            result = one + two
            CommonAssertionUtils.are_equal(result, expected_value, message='{} plus {} did not equal {}!'.format(one, two, expected_value))
    """
    def __init__(self):
        self._tests = dict()
        self._test_count = 0

    def add_test(self, test_name: str, test_function: Callable[..., Any], class_name: str=None):
        """Adds a test with a test name and class name.

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
        """Get total test count.

        :return: A count of how many tests there are.
        """
        return self._test_count

    @property
    def all_tests(self) -> Dict[str, Any]:
        """Get all tests.

        :return: A dictionary of tests.
        """
        return self._tests

    def get_tests_by_class_name(self, class_name: str) -> List[Any]:
        """Retrieve tests by their class name.

        :param class_name: The name of the class to locate tests for.
        :return: A list of tests matching the class name.
        """
        return self._tests.get(class_name, list())

    @classmethod
    def _format_test_result(cls, test_result: str, test_name: str, stacktrace: str=None):
        return 'TEST {}: {} {}'.format(test_result, test_name, stacktrace or '')

    @staticmethod
    def test_class(mod_name: str):
        """Decorator to indicate a test class.

        :param mod_name: The name of the mod this test class is contained within.
        :return: A wrapped function.
        """
        @CommonExceptionHandler.catch_exceptions(mod_name)
        def _inner_test_class(cls):
            name_of_class = cls.__name__
            if CommonLogRegistry is not None:
                cls.test_log_log = CommonLogRegistry.get().register_log(mod_name, name_of_class)
                cls.test_log_log.enable()
                cls.test_log = lambda val: cls.test_log_log.debug(val)
            else:
                cls.test_log = lambda val: print(val)
            for method_name in dir(cls):
                method = getattr(cls, method_name)
                if not hasattr(method, 'is_test'):
                    continue

                def _test_function(class_name, test_name, test_method, *_, **__):
                    @wraps(test_method)
                    def _wrapper(*args, **kwargs):
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
    def test(*args, **kwargs):
        """Decorator to indicate a test.
        When the test is run, it will be sent the specified arguments and keyword arguments.

        :return: A wrapped function.
        """
        def _test_func(test_function):
            test_function.is_test = True
            if not hasattr(test_function, 'test_parameters'):
                test_function.test_parameters = list()
            test_function.test_parameters.append((args, kwargs))
            return test_function
        return _test_func

    def run_tests(self, *class_names: str, callback: Callable[..., Any]=print, **__):
        """Runs the tests of the specified classes.

        :param class_names: A collection of classes to run tests for.
        :param callback: The callback to send string results to.
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
