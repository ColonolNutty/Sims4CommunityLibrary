"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import itertools
from typing import List, Any, Dict, Union, Tuple, Set


class CommonCollectionUtils:
    """Utilities for collections.

    """
    @staticmethod
    def is_collection(obj: Any) -> bool:
        """is_collection(obj)

        Determine if an object is a collection or not.

        :param obj: An object.
        :type obj: Any
        :return: True, if the object is a collection, False, if not.
        :rtype: bool
        """
        if obj is None:
            return False
        return isinstance(obj, list)\
               or isinstance(obj, tuple)\
               or isinstance(obj, set)\
               or isinstance(obj, frozenset)\
               or isinstance(obj, dict)

    @staticmethod
    def intersects(list_one: List[Any], *list_items: Any) -> bool:
        """intersects(list_one, *list_items)

        Determine if a list contains any of the specified items.

        :param list_one: The list being checked.
        :type list_one: List[Any]
        :param list_items: An iterable of items being searched for.
        :type list_items: Any
        :return: True, if the list contains any of the specified items. False, if not.
        :rtype: bool
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
        """add_to_dict_if_not_exist(dictionary_one, dictionary_two)

        Combine two dictionaries.

        .. note:: If a key already exists in the first dictionary, the value from the second dictionary is ignored.

        :param dictionary_one: The first dictionary.
        :type dictionary_one: Dict[Any, Any]
        :param dictionary_two: The second dictionary.
        :type dictionary_two: Dict[Any, Any]
        :return: A new combined dictionary.
        :rtype: Dict[Any, Any]
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
        """flatten(to_flatten)

        Flatten a collection of collections to a single list or itself if already flattened.

        :param to_flatten: A collection of items.
        :type to_flatten: Any
        :return: A single flattened list or `to_flatten` if already flattened.
        :rtype: Union[Any, List[Any]]
        """
        if not CommonCollectionUtils.is_collection(to_flatten):
            return to_flatten
        flat_list = list()
        for value in to_flatten:
            flat_list.append(CommonCollectionUtils.flatten(value))
        return flat_list

    @staticmethod
    def create_possible_combinations(items: Union[List[Any], Tuple[Any]], items_per_combination: int) -> Set[Tuple[Any]]:
        """create_possible_combinations(items, items_per_combination)

        Create a collection of all possible combinations of the specified items.

        .. note:: Example: With items: [1, 2, 3] and combination_length: 2 the result will be: {(1, 2), (1, 3), (2, 3)}

        :param items: A collection of items to create combinations from.
        :type items: Union[List[Any], Tuple[Any]]
        :param items_per_combination: The number of items in each combination.
        :type items_per_combination: int
        :return: A collection of combinations
        :rtype: Set[Tuple[Any]]
        """
        possible_combinations = set()
        combinations = itertools.combinations(items, items_per_combination)
        for combination in combinations:
            (is_processed, new_combination_sets) = CommonCollectionUtils._process_item_sets(combination)
            if is_processed:
                for new_combination_set in new_combination_sets:
                    possible_combinations.add(tuple(sorted(new_combination_set)))
            else:
                possible_combinations.add(tuple(sorted(combination)))
        return possible_combinations

    @staticmethod
    def _process_item_sets(item_set: Union[Tuple[Any], List[Any], Set[Any]]) -> Tuple[bool, Union[Set[Any], List[Any]]]:
        item_sets = []
        # Item count 2
        # I1, T1
        # ((I1, I2), T1)
        # ((I1, I2), (T1, T2))
        # Item count 3
        # I1, T1, K1
        # ((I1, I2), T1, K1)
        # ((I1, I2), (T1, T2), K1)
        # ((I1, I2), (T1, T2), (K1, K2))
        has_unprocessed = False
        unprocessed_item_sets = []
        idx = 0
        for item in item_set:
            if isinstance(item, tuple) or isinstance(item, list) or isinstance(item, set):
                has_unprocessed = True
                elements_before = item_set[:idx]
                elements_after = item_set[idx + 1:]
                for items_in_set in item:
                    current_set = []
                    for element_before in elements_before:
                        current_set.append(element_before)
                    current_set.append(items_in_set)
                    for element_after in elements_after:
                        current_set.append(element_after)
                    unprocessed_item_sets.append(current_set)
                break
            idx += 1
        if len(unprocessed_item_sets) > 0:
            item_sets = []
            for unprocessed_item_set in unprocessed_item_sets:
                (is_processed, result) = CommonCollectionUtils._process_item_sets(unprocessed_item_set)
                if is_processed:
                    for new_item_set in result:
                        item_sets.append(new_item_set)
                else:
                    item_sets.append(unprocessed_item_set)
            return True, item_sets
        if not has_unprocessed:
            if isinstance(item_set, list) or isinstance(item_set, tuple):
                new_item_set = set()
                for item in item_set:
                    new_item_set.add(item)
                return False, new_item_set
            return False, item_set
        return True, item_sets
