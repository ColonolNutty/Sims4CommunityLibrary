"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Any, Dict, Union


class CommonCollectionUtils:
    """
        Utilities for collections.
    """
    @staticmethod
    def is_collection(obj: Any) -> bool:
        """
            Determine if an object is a collection or not.
        :param obj: An object.
        :return: True if the object is a collection, False if not.
        """
        if obj is None:
            return False
        return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, frozenset) or isinstance(obj, dict)

    @staticmethod
    def intersects(list_one: List[Any], *list_items: Any) -> bool:
        """
            Determine if a list contains any of the specified items.
        :param list_one: The list being checked.
        :param list_items: The items being searched for.
        :return: True if the list contains any of the specified items.
        """
        if list_one is None or list_items is None:
            return False
        for list_item in list_items:
            for item in list_item:
                if item in list_one:
                    return True
        return False

    @staticmethod
    def add_to_dict_if_not_exist(dictionary_one: Dict[Any, Any], dictionary_two: Dict[Any, Any]) -> Dict[Any, Any]:
        """
            Combine two dictionaries.
            If a key already exists in the first dictionary, the value from the second dictionary is ignored.
        :param dictionary_one: The first dictionary.
        :param dictionary_two: The second dictionary.
        :return: A new combined dictionary.
        """
        if dictionary_one is None or dictionary_two is None:
            return dict()
        has_new_keys = False
        new_dict = dict()
        for (to_add_key, to_add_value) in dictionary_two.items():
            if to_add_key in dictionary_one:
                continue
            has_new_keys = True
            new_dict[to_add_key] = to_add_value
        if not has_new_keys:
            return dictionary_one
        for (key, value) in dictionary_one.items():
            new_dict[key] = value
        return new_dict

    @staticmethod
    def flatten(to_flatten: Any) -> Union[Any, List[Any]]:
        """
            Flatten a collection of collections to a single list or itself if already flattened.
        :param to_flatten: The collection to flatten
        :return: A single flattened list or to_flatten if already flattened.
        """
        if not CommonCollectionUtils.is_collection(to_flatten):
            return to_flatten
        flat_list = list()
        for value in to_flatten:
            flat_list.append(CommonCollectionUtils.flatten(value))
        return flat_list
