"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from functools import wraps
from typing import Any, Callable
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonInjectionUtils:
    """Utilities to inject custom functionality into functions.

    """
    @staticmethod
    def inject_into(target_object: Any, target_function_name: str) -> Callable:
        """inject_into(target_object, target_function_name)

        .. warning:: This function is DEPRECATED.\
            Use :func:`~inject_safely_into` instead.

        """
        return CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), target_object, target_function_name)

    @staticmethod
    def inject_safely_into(mod_identity: CommonModIdentity, target_object: Any, target_function_name: str) -> Callable:
        """inject_safely_into(mod_identity, target_object, target_function_name)

        A decorator used to inject code into a function.
        It will catch and log exceptions, as well as run the original function should any problems occur.

        :Example of cls usage:

        .. highlight:: python
        .. code-block:: python

            # cls usage
            @CommonInjectionUtils.inject_safely_into(SimSpawner, SimSpawner.spawn_sim._name__)
            def do_custom_spawn_sim(original, cls, *args, **kwargs):
                return original(*args, **kwargs)

        :Example of self usage:

        .. highlight:: python
        .. code-block:: python

            # Self usage
            @CommonInjectionUtils.inject_safely_into(SimInfo, SimInfo.load_sim_info.__name__)
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

        :param mod_identity: The identity of the Mod that is injecting custom code.
        :type mod_identity: CommonModIdentity
        :param target_object: The class that contains the target function.
        :type target_object: Any
        :param target_function_name: The name of the function being injected to.
        :type target_function_name: str
        :return: A wrapped function.
        :rtype: Callable
        """

        def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
            # noinspection PyBroadException
            try:
                @wraps(original_function)
                def _wrapped_function(*args, **kwargs) -> Any:
                    try:
                        if type(original_function) is property:
                            return new_function(original_function.fget, *args, **kwargs)
                        return new_function(original_function, *args, **kwargs)
                    except Exception as ex:
                        # noinspection PyBroadException
                        try:
                            from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
                            CommonExceptionHandler.log_exception(mod_identity, 'Error occurred while injecting into function \'{}\' of class \'{}\''.format(new_function.__name__, target_object.__name__), exception=ex)
                        except Exception:
                            pass
                        return original_function(*args, **kwargs)
                if inspect.ismethod(original_function):
                    return classmethod(_wrapped_function)
                if type(original_function) is property:
                    return property(_wrapped_function)
                return _wrapped_function
            except:
                def _func(*_, **__) -> Any:
                    pass
                return _func

        def _injected(wrap_function) -> Any:
            original_function = getattr(target_object, str(target_function_name))
            setattr(target_object, str(target_function_name), _function_wrapper(original_function, wrap_function))
            return wrap_function
        return _injected
