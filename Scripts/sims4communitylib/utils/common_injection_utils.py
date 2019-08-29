"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import inspect
from functools import wraps
from typing import Any, Callable


class CommonInjectionUtils:
    """ Utilities to inject custom functionality into other functions. """
    @staticmethod
    def inject_into(target_object: Any, target_function_name: str) -> Callable:
        """
            A decorator used to inject code into another function

            Example 'cls' Usage:
            @CommonInjectionUtils.inject_into(SimSpawner, SimSpawner.spawn_sim._name__)
            def do_custom_spawn_sim(original, cls, *args, **kwargs):
                return original(*args, **kwargs)

            Example 'self' Usage:
            @CommonInjectionUtils.inject_into(SimInfo, SimInfo.load_sim_info.__name__)
            def do_custom_load_sim_info(original, self, *args, **kwargs):
                return original(self, *args, **kwargs)

            Note:
             Injection WILL work on:
               - Functions decorated with 'classmethod'
               - Functions with 'cls' or 'self' as the first argument.
             Injection WILL NOT work on:
               - Functions decorated with 'staticmethod'
               - Global functions, i.e. Functions not contained within a class.
        :param target_object: The class that contains the target function.
        :param target_function_name: The name of the function being injected to.
        :return: A wrapped function.
        """

        def _wrapper(wrap_function):
            orig_function = getattr(target_object, target_function_name)

            @wraps(orig_function)
            def _wrapped_function(*args, **kwargs):
                return wrap_function(orig_function, *args, **kwargs)

            if inspect.ismethod(orig_function):
                override_function = classmethod(_wrapped_function)
            else:
                override_function = _wrapped_function

            setattr(target_object, target_function_name, override_function)
            return wrap_function

        return _wrapper
