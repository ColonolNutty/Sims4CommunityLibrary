"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from functools import wraps
from typing import Any, Callable, TYPE_CHECKING

from sims4communitylib.mod_support.mod_identity import CommonModIdentity

if TYPE_CHECKING:
    from sims4communitylib.utils.common_log_registry import CommonLog
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'


class _TypeChecking:
    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    @classmethod
    def class_method(cls):
        pass

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    def self_method(self):
        pass

    # noinspection PyPropertyDefinition,PyMissingTypeHints,PyMissingOrEmptyDocstring
    @property
    def property_type(self):
        pass

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    @staticmethod
    def static_method():
        pass


ClassMethodType = type(_TypeChecking.class_method)
SelfMethodType = type(_TypeChecking.self_method)
StaticMethodType = type(_TypeChecking.static_method)
PropertyType = type(_TypeChecking.property_type)


class CommonInjectionUtils:
    """Utilities to inject custom functionality into functions.

    """
    @staticmethod
    def inject_into(target_object: Any, target_function_name: str) -> Callable:
        """inject_into(target_object, target_function_name)

        .. warning:: This function is DEPRECATED.\
            Use :func:`~inject_safely_into` instead.

        """
        # noinspection PyTypeChecker
        return CommonInjectionUtils.inject_safely_into(None, target_object, target_function_name)

    @staticmethod
    def inject_safely_into(mod_identity: CommonModIdentity, target_object: Any, target_function_name: str, handle_exceptions: bool = True) -> Callable:
        """inject_safely_into(mod_identity, target_object, target_function_name, handle_exceptions=True)

        A decorator used to inject code into a function.
        It will run the original function should any problems occur.
        If handle_exceptions is True, it will catch and log exceptions.

        :Example of cls usage:

        .. highlight:: python
        .. code-block:: python

            # cls usage
            @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimSpawner, SimSpawner.spawn_sim._name__)
            def do_custom_spawn_sim(original, cls, *args, **kwargs):
                return original(*args, **kwargs)

        :Example of self usage:

        .. highlight:: python
        .. code-block:: python

            # Self usage
            @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.load_sim_info.__name__)
            def do_custom_load_sim_info(original, self, *args, **kwargs):
                return original(self, *args, **kwargs)

        .. note::

           Injection WILL work on

           - Functions decorated with 'property'
           - Functions decorated with 'classmethod'
           - Functions decorated with 'staticmethod'
           - Functions with 'cls' or 'self' as the first argument.

        .. note::

           Injection WILL NOT work on

           - Global functions, i.e. Functions not contained within a class.
           - Global variables, i.e. Variables not contained within a class or function.

        :param mod_identity: The identity of the Mod that is injecting custom code.
        :type mod_identity: CommonModIdentity
        :param target_object: The class that contains the target function.
        :type target_object: Any
        :param target_function_name: The name of the function being injected to.
        :type target_function_name: str
        :param handle_exceptions: If set to True, any exceptions thrown by the wrapped function will be handled. If set to False, any exceptions thrown by the wrapped function will not be caught. Default is True.
        :type handle_exceptions: bool, optional
        :return: A wrapped function.
        :rtype: Callable
        """
        if ON_RTD:
            def _injected(wrap_function) -> Any:
                return wrap_function
            return _injected

        if handle_exceptions:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                # noinspection PyBroadException
                try:
                    if isinstance(original_function, ClassMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_class_function(cls, *args, **kwargs) -> Any:
                            try:
                                # noinspection PyMissingTypeHints
                                def _do_original(*_, **__):
                                    return original_function_func(cls, *_, **__)

                                return new_function(_do_original, cls, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from sims4communitylib.exceptions.common_exceptions_handler import \
                                        CommonExceptionHandler
                                    CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while injecting into function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function_func(cls, *args, **kwargs)
                        return classmethod(_wrapped_class_function)

                    if isinstance(original_function, SelfMethodType):
                        @wraps(original_function)
                        def _wrapped_self_function(self, *args, **kwargs) -> Any:
                            try:
                                return new_function(original_function, self, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                                    CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while injecting into function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function(self, *args, **kwargs)

                        return _wrapped_self_function

                    if isinstance(original_function, PropertyType):
                        # noinspection PyTypeChecker
                        @wraps(original_function)
                        def _wrapped_property_function(self, *args, **kwargs) -> Any:
                            try:
                                return new_function(original_function.fget, self, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                                    CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while injecting into function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function(self, *args, **kwargs)

                        return property(_wrapped_property_function)

                    if isinstance(original_function, StaticMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_static_function(*args, **kwargs) -> Any:
                            try:
                                # noinspection PyMissingTypeHints
                                def _do_original(*_, **__):
                                    return original_function_func(*_, **__)

                                return new_function(_do_original, *args, **kwargs)
                            except Exception as ex:
                                # noinspection PyBroadException
                                try:
                                    from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                                    CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while injecting into function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                                except Exception:
                                    pass
                                return original_function_func(*args, **kwargs)

                        return staticmethod(_wrapped_static_function)

                    @wraps(original_function)
                    def _wrapped_other_function(*args, **kwargs) -> Any:
                        try:
                            return new_function(original_function, *args, **kwargs)
                        except Exception as ex:
                            # noinspection PyBroadException
                            try:
                                from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                                CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while injecting into function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                            except Exception:
                                pass
                            return original_function(*args, **kwargs)

                    return _wrapped_other_function
                except:
                    def _func(*_, **__) -> Any:
                        pass
                    return _func
        else:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                # noinspection PyBroadException
                try:
                    if isinstance(original_function, ClassMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_class_function(cls, *args, **kwargs) -> Any:
                            # noinspection PyMissingTypeHints
                            def _do_original(*_, **__):
                                return original_function_func(cls, *_, **__)

                            return new_function(_do_original, cls, *args, **kwargs)
                        return classmethod(_wrapped_class_function)

                    if isinstance(original_function, SelfMethodType):
                        @wraps(original_function)
                        def _wrapped_self_function(self, *args, **kwargs) -> Any:
                            return new_function(original_function, self, *args, **kwargs)

                        return _wrapped_self_function

                    if isinstance(original_function, PropertyType):
                        # noinspection PyTypeChecker
                        @wraps(original_function)
                        def _wrapped_property_function(self, *args, **kwargs) -> Any:
                            return new_function(original_function.fget, self, *args, **kwargs)

                        return property(_wrapped_property_function)

                    if isinstance(original_function, StaticMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_static_function(*args, **kwargs) -> Any:
                            # noinspection PyMissingTypeHints
                            def _do_original(*_, **__):
                                return original_function_func(*_, **__)

                            return new_function(_do_original, *args, **kwargs)

                        return staticmethod(_wrapped_static_function)

                    @wraps(original_function)
                    def _wrapped_other_function(*args, **kwargs) -> Any:
                        return new_function(original_function, *args, **kwargs)

                    return _wrapped_other_function
                except:
                    def _func(*_, **__) -> Any:
                        pass
                    return _func

        def _injected(wrap_function) -> Any:
            original_function = getattr(target_object, str(target_function_name))
            setattr(target_object, str(target_function_name), _function_wrapper(original_function, wrap_function))
            return wrap_function
        return _injected

    @staticmethod
    def inject_safely_into_function(mod_identity: CommonModIdentity, target_object: Any, target_function_name: str, callback: Callable[..., Any], replace_return: bool = False, handle_exceptions: bool = True) -> Callable:
        """inject_safely_into_function(mod_identity, target_object, target_function_name, callback, replace_return=False, handle_exceptions=True)

        A decorator used to inject code into a function.
        It will run the original function should any problems occur.
        If handle_exceptions is True, it will catch and log exceptions.

        :Example of cls usage:

        .. highlight:: python
        .. code-block:: python

            # cls usage
            @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimSpawner, SimSpawner.spawn_sim._name__)
            def do_custom_spawn_sim(original, cls, *args, **kwargs):
                return original(*args, **kwargs)

        :Example of self usage:

        .. highlight:: python
        .. code-block:: python

            # Self usage
            @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.load_sim_info.__name__)
            def do_custom_load_sim_info(original, self, *args, **kwargs):
                return original(self, *args, **kwargs)

        .. note::

           Injection WILL work on

           - Functions decorated with 'property'
           - Functions decorated with 'classmethod'
           - Functions decorated with 'staticmethod'
           - Functions with 'cls' or 'self' as the first argument.

        .. note::

           Injection WILL NOT work on

           - Global functions, i.e. Functions not contained within a class.
           - Global variables, i.e. Variables not contained within a class or function.

        :param mod_identity: The identity of the Mod that is injecting custom code.
        :type mod_identity: CommonModIdentity
        :param target_object: The class that contains the target function.
        :type target_object: Any
        :param target_function_name: The name of the function being injected to.
        :type target_function_name: str
        :param callback: When the injected function is invoked, this callback will be invoked.
        :type callback: Callable[..., Any]
        :param replace_return: If True, the returned result of the callback argument will replace the returned result of the original function. If False, the callback will be invoked, but the result of invoking the original function will be returned. Default is False.
        :type replace_return: bool, optional
        :param handle_exceptions: If set to True, any exceptions thrown by the wrapped function will be handled. If set to False, any exceptions thrown by the wrapped function will not be caught. Default is True.
        :type handle_exceptions: bool, optional
        :return: A wrapped function.
        :rtype: Callable
        """

        @CommonInjectionUtils.inject_safely_into(mod_identity, target_object, target_function_name, handle_exceptions=handle_exceptions)
        def _inject_and_invoke_callback(original, *args, **kwargs) -> Any:
            callback_result = callback(*args, **kwargs)
            if replace_return:
                return callback_result
            return original(*args, **kwargs)

        return _inject_and_invoke_callback

    @staticmethod
    def inject_and_print_arguments(mod_identity: CommonModIdentity, target_object: Any, target_function_name: str, log: 'CommonLog', log_stack_trace: bool = False, handle_exceptions: bool = True) -> Callable:
        """inject_and_print_arguments(mod_identity, target_object, target_function_name, log, log_stack_trace=False, handle_exceptions=True)

        A decorator used to inject code into a function and print any arguments or keyword arguments passed to it.

        .. note:: See documentation of :func:`~inject_safely_into` for more details about the arguments and keyword arguments.

        :Example of cls usage:

        .. highlight:: python
        .. code-block:: python

            # cls usage
            @CommonInjectionUtils.inject_and_print_arguments(ModInfo.get_identity(), SimSpawner, SimSpawner.spawn_sim._name__)

        :Example of self usage:

        .. highlight:: python
        .. code-block:: python

            # Self usage
            @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SimInfo, SimInfo.load_sim_info.__name__)
            def do_custom_load_sim_info(original, self, *args, **kwargs):
                return original(self, *args, **kwargs)

        .. note::

           Injection WILL work on

           - Functions decorated with 'property'
           - Functions decorated with 'classmethod'
           - Functions decorated with 'staticmethod'
           - Functions with 'cls' or 'self' as the first argument.

        .. note::

           Injection WILL NOT work on

           - Global functions, i.e. Functions not contained within a class.
           - Global variables, i.e. Variables not contained within a class or function.

        :param mod_identity: The identity of the Mod that is injecting custom code.
        :type mod_identity: CommonModIdentity
        :param target_object: The class that contains the target function.
        :type target_object: Any
        :param target_function_name: The name of the function being injected to.
        :type target_function_name: str
        :param log: The log being printed to when the injected function is invoked. The arguments and keyword arguments sent to the function will be printed.
        :type log: CommonLog
        :param log_stack_trace: If True, the stack trace will be logged in addition to the arguments and keyword arguments. If False, the stack trace will not be logged. Default is False.
        :type log_stack_trace: bool, optional
        :param handle_exceptions: If set to True, any exceptions thrown by the wrapped function will be handled. If set to False, any exceptions thrown by the wrapped function will not be caught. Default is True.
        :type handle_exceptions: bool, optional
        :return: A wrapped function.
        :rtype: Callable
        """
        @CommonInjectionUtils.inject_safely_into(mod_identity, target_object, target_function_name, handle_exceptions=handle_exceptions)
        def _inject_and_print(original, *args, **kwargs) -> Any:
            log.format_with_message('{}.{}'.format(target_object, target_function_name), argles=args, kwargles=kwargs)
            if log_stack_trace:
                log.log_stack()
            return original(*args, **kwargs)

        return _inject_and_print
