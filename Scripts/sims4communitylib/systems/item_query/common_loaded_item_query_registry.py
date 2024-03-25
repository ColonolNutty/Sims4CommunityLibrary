"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import collections
from typing import List, Dict, Any, Tuple, Set, Callable, Union, Iterator, TypeVar, Generic

from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.systems.item_query.item_tests.common_loaded_item_test import CommonLoadedItemTest
from sims4communitylib.systems.item_query.query.common_loaded_item_filter_request import CommonLoadedItemFilterRequest
from sims4communitylib.systems.item_query.query.common_loaded_item_organizer import CommonLoadedItemOrganizer
from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4communitylib.systems.item_query.common_loaded_item_registry import CommonLoadedItemRegistry
from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.systems.item_query.enums.common_query_method_type import CommonQueryMethodType
from sims4communitylib.utils.misc.common_text_utils import CommonTextUtils

CommonLoadedItemType = TypeVar('CommonLoadedItemType', bound=CommonLoadedItem)


class CommonLoadedItemQueryRegistry(CommonService, HasLog, Generic[CommonLoadedItemType]):
    """ Registry handling item queries. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    def __init__(self) -> None:
        super().__init__()
        self._collecting = False
        self.item_library = collections.defaultdict(set)
        self.__item_organizers: List[CommonLoadedItemOrganizer] = list()
        self._all: List[CommonLoadedItemType] = list()
        self._total = 0
        self._total_valid = 0
        self._total_invalid = 0
        self._duplicates = 0

    @property
    def _registry(self) -> CommonLoadedItemRegistry:
        raise NotImplementedError()

    @property
    def _item_organizers(self) -> List[CommonLoadedItemOrganizer]:
        return self.__item_organizers

    @property
    def _item_name(self) -> str:
        return 'item'

    @property
    def collecting(self) -> bool:
        """Determine if items are being collected."""
        return self._collecting

    @property
    def item_library(self) -> Dict[Tuple[Any, Any], Set[str]]:
        """ A library of items organized by filter keys. """
        return self._item_library

    @item_library.setter
    def item_library(self, value: Dict[Tuple[Any, Any], Set[str]]):
        self._item_library = value

    @property
    def total(self) -> int:
        """The total number of items that were looked at"""
        return self._total

    @property
    def total_invalid(self) -> int:
        """The total number of items that were invalid."""
        return self._total_invalid

    @property
    def total_valid(self) -> int:
        """The total number of items that were valid."""
        return self._total_valid

    @property
    def duplicates(self) -> int:
        """The total number of items that were valid."""
        return self._duplicates

    def add_item_organizer(
        self,
        item_organizer_init: Callable[[Any], CommonLoadedItemOrganizer],
        key_type: Any
    ):
        """ Add an item organizer. """
        self._item_organizers.append(item_organizer_init(key_type))

    def has_items(self, requests: Tuple[CommonLoadedItemFilterRequest]) -> bool:
        """ Determine if items exist for queries. """
        if self.log.enabled:
            self.log.format_with_message(f'Checking if has {self._item_name}s', queries=requests)
        for _ in self.get_items_gen(requests):
            return True
        return False

    def get_items_gen(self, requests: Tuple[CommonLoadedItemFilterRequest]) -> Iterator[CommonLoadedItemType]:
        """ Retrieve items matching the requests. """
        if self.log.enabled:
            self.log.format_with_message(f'Getting {self._item_name}s', requests=requests)
        if self._collecting:
            return tuple()
        for request in requests:
            yield from self._query_items(request, request.item_tests)
        if self.verbose_log.enabled:
            self.verbose_log.debug(f'Finished locating {self._item_name}s')

    def _run_tests(self, item: CommonLoadedItemType, item_tests: Iterator[CommonLoadedItemTest]) -> CommonTestResult:
        for _item_test in item_tests:
            _result = _item_test.test_item(item)
            if not _result:
                return _result
        return CommonTestResult.TRUE

    def _query_items(self, request: CommonLoadedItemFilterRequest, item_tests: Iterator[CommonLoadedItemTest]) -> Iterator[CommonLoadedItemType]:
        if self.log.enabled:
            self.log.format_with_message(f'Querying for {self._item_name}s using query', query=request, item_tests=item_tests)
        item_tests = tuple(item_tests)
        all_keys = request.include_all_keys
        any_keys = request.include_any_keys
        exclude_keys = request.exclude_keys
        match_at_least_one_key_sets = request.must_match_at_least_one_key_sets
        found_item_identifiers = None

        def _convert_found_items(_found_identifiers: Set[str]) -> Iterator[CommonLoadedItemType]:
            count = 0
            for _item_identifier in _found_identifiers:
                _item = self._registry.locate_by_identifier(_item_identifier)
                if _item is None:
                    continue
                _passes_tests = self._run_tests(_item, item_tests)
                if not _passes_tests:
                    if self.log.is_enabled:
                        self.log.format_with_message(f'{self._item_name} failed item test', item=_item.short_name, reason=_passes_tests.reason)
                    continue
                count += 1
                yield _item

            if self.log.enabled:
                self.log.debug(f'After item tests keys {count}')

        if self.log.enabled:
            self.log.format_with_message('Using match_at_least_one_sets', match_at_least_one_sets=match_at_least_one_key_sets)
        if match_at_least_one_key_sets:
            self.verbose_log.format_with_message('Has match at least one sets.', match_at_least_one_sets=match_at_least_one_key_sets)
            found_all_matching = False
            for match_at_least_one_key_set in match_at_least_one_key_sets:
                if self.log.enabled:
                    self.log.format_with_message('Attempting to locate a match for set.', match_at_least_one_set=match_at_least_one_key_set)
                found_matching = False
                total_matching_items = None
                for match_at_least_one_key in match_at_least_one_key_set:
                    if match_at_least_one_key is None:
                        continue
                    if match_at_least_one_key.key not in self.item_library:
                        # One of the Match At Least One keys is not within the Item library! This means no Items pass the Match At Least One keys.
                        if self.log.enabled:
                            self.log.format_with_message(f'Match At Least One Key not found within the {self._item_name} library, meaning there are no {self._item_name}s available for it! Skipping this key.', key=match_at_least_one_key.key)
                        continue
                    new_found_items = self.item_library[match_at_least_one_key.key]
                    if total_matching_items is not None:
                        if self.log.enabled:
                            self.log.debug(f'Looking for key {match_at_least_one_key}')
                            before_intersect_match_at_least_one_count = len(total_matching_items)
                            self.log.format_with_message(f'Before intersect for match_at_least_one_keys {before_intersect_match_at_least_one_count}', match=match_at_least_one_key)
                        if len(new_found_items) != 0:
                            found_matching = True
                        new_found_items = total_matching_items | new_found_items
                        if self.log.enabled:
                            after_intersect_match_at_least_one_count = len(new_found_items)
                            self.log.format_with_message(f'After intersect for match_at_least_one_keys {after_intersect_match_at_least_one_count}', match=match_at_least_one_key)
                        total_matching_items = new_found_items
                    else:
                        if self.log.enabled:
                            new_found_match_at_least_one_count = len(new_found_items)
                            self.log.format_with_message(f'Found with match_at_least_one_keys {new_found_match_at_least_one_count}', match=match_at_least_one_key)
                        if new_found_items is not None and len(new_found_items) != 0:
                            found_matching = True
                        total_matching_items = new_found_items

                if not found_matching or not total_matching_items:
                    if self.log.enabled:
                        self.log.format_with_message(f'No {self._item_name}s found for match_at_least_one_set.', match_at_least_one_set=match_at_least_one_key_set)
                    return tuple()
                self.verbose_log.format_with_message('Located a match for set, combining it with what currently exists.', match_at_least_one_set=match_at_least_one_key_set)
                if found_item_identifiers is not None:
                    if self.log.enabled:
                        self.log.debug(f'Connecting set {match_at_least_one_key_set}')
                        total_count_before = len(total_matching_items)
                        self.log.debug(f'Before intersect for match_at_least_one_set {total_count_before}')
                    if len(total_matching_items) != 0:
                        found_all_matching = True
                    total_matching_items = found_item_identifiers & total_matching_items
                    if self.log.enabled:
                        total_count_after = len(total_matching_items)
                        self.log.debug(f'After intersect for match_at_least_one_set {total_count_after}')
                    found_item_identifiers = total_matching_items
                else:
                    if self.log.enabled:
                        total_count_after = len(total_matching_items)
                        self.log.debug(f'Found with match_at_least_ones {total_count_after}')
                    if total_matching_items is not None and len(total_matching_items) != 0:
                        found_all_matching = True
                    found_item_identifiers = total_matching_items
            if not found_all_matching:
                if self.log.enabled:
                    self.log.format_with_message(f'No {self._item_name}s found for match_at_least_one_set', match_at_least_one_sets=match_at_least_one_key_sets)
                return tuple()

        self.log.format_with_message('Using all_keys', all_keys=all_keys)
        for include_all_key in all_keys:
            if include_all_key is None:
                continue
            if include_all_key.key not in self.item_library:
                # One of All keys is not within the item library! This means no items match ALL keys.
                if self.log.enabled:
                    self.log.format_with_message(f'All Key not found within the {self._item_name} library, meaning there are no {self._item_name}s available for it! Skipping this key.', key=include_all_key.key)
                return tuple()
            new_found_items = self.item_library[include_all_key.key]
            if found_item_identifiers is not None:
                if self.log.enabled:
                    before_intersect_all_count = len(found_item_identifiers)
                    self.log.format_with_message(f'Before intersect for all_keys {before_intersect_all_count}', include_all_key=include_all_key)
                new_found_items = found_item_identifiers & new_found_items
                if self.log.enabled:
                    after_intersect_all_count = len(new_found_items)
                    self.log.format_with_message(f'After intersect for all_keys {after_intersect_all_count}', include_all_key=include_all_key)
            else:
                if self.log.enabled:
                    new_match_all_count = len(new_found_items)
                    self.log.format_with_message(f'Found with all_keys {new_match_all_count}', include_all_key=include_all_key)

            found_item_identifiers = new_found_items

        if found_item_identifiers is None and all_keys:
            if self.log.enabled:
                self.log.format_with_message(f'No {self._item_name}s found for all_keys.', all_keys=all_keys)
            return tuple()

        if self.log.enabled:
            after_all_keys = len(found_item_identifiers) if found_item_identifiers is not None else 0
            self.log.debug(f'After all_keys {after_all_keys}')
        if self.verbose_log.enabled:
            if found_item_identifiers is not None:
                found_all_items: List[str] = list()
                for anim_identifier in found_item_identifiers:
                    item = self._registry.locate_by_identifier(anim_identifier)
                    if item is None:
                        continue
                    found_all_items.append(item.short_name)
                self.verbose_log.format_with_message(f'Found {self._item_name}s via all keys', items=found_all_items)

        self.log.format_with_message('Using any_keys', any_keys=any_keys)
        found_items_via_any_keys = set()
        for include_any_key in any_keys:
            if include_any_key is None:
                continue
            if include_any_key.key not in self.item_library:
                if self.log.enabled:
                    self.log.format_with_message(f'Any Key not found within the {self._item_name} library, meaning there are no {self._item_name}s available for it! Skipping this key.', key=include_any_key.key)
                continue
            found_items_via_any_keys = found_items_via_any_keys | self.item_library[include_any_key.key]

        if self.log.enabled:
            found_any_keys_count = len(found_items_via_any_keys) if found_items_via_any_keys is not None else 0
            self.log.debug(f'Found {self._item_name}s via any {found_any_keys_count}')

        if self.verbose_log.enabled:
            found_any_items: List[str] = list()
            for anim_identifier in found_items_via_any_keys:
                item = self._registry.locate_by_identifier(anim_identifier)
                if item is None:
                    continue
                found_any_items.append(item.short_name)
            self.verbose_log.format_with_message(f'Found {self._item_name}s via any keys', items=found_any_items)

        if found_item_identifiers is None:
            if self.log.enabled:
                self.log.debug(f'No {self._item_name}s found for all_keys.')
            if not all_keys:
                self.log.debug('Returning any keys.')
                yield from _convert_found_items(found_items_via_any_keys)
                return tuple()
        else:
            query_type = request.query_type
            if not any_keys and (query_type == CommonQueryMethodType.ALL_INTERSECT_ANY or query_type == CommonQueryMethodType.ALL_INTERSECT_ANY_MUST_HAVE_ONE):
                query_type = CommonQueryMethodType.ALL_PLUS_ANY
            if query_type == CommonQueryMethodType.ALL_PLUS_ANY:
                found_item_identifiers = found_item_identifiers | found_items_via_any_keys
            elif query_type == CommonQueryMethodType.ALL_INTERSECT_ANY:
                found_item_identifiers = found_item_identifiers & found_items_via_any_keys

            if query_type == CommonQueryMethodType.ALL_PLUS_ANY_MUST_HAVE_ONE:
                if not found_items_via_any_keys:
                    return tuple()
                found_item_identifiers = found_item_identifiers | found_items_via_any_keys
            elif query_type == CommonQueryMethodType.ALL_INTERSECT_ANY_MUST_HAVE_ONE:
                if not found_items_via_any_keys:
                    return tuple()
                found_item_identifiers = found_item_identifiers & found_items_via_any_keys

        if found_item_identifiers is None or not found_item_identifiers:
            if self.log.enabled:
                self.log.debug(f'No found {self._item_name}s after combining any keys. All Keys: {all_keys} Any Keys: {any_keys}')
            return tuple()

        if self.log.enabled:
            after_any_keys_count = len(found_item_identifiers)
            self.log.debug(f'After any keys {after_any_keys_count}')

        self.log.format_with_message('Using exclude', exclude_keys=exclude_keys)
        for exclude_key in exclude_keys:
            if exclude_key is None:
                continue
            exclude_key = exclude_key.key
            if exclude_key not in self.item_library:
                continue
            to_exclude_items = self.item_library[exclude_key]
            if self.log.enabled:
                before_found_item_count = len(found_item_identifiers)
                before_to_exclude_item_count = len(to_exclude_items)
                self.log.debug(f'Before exclude key {exclude_key} {before_found_item_count} to exclude {before_to_exclude_item_count}')
            found_item_identifiers = found_item_identifiers - to_exclude_items
            if self.log.enabled:
                after_found_item_count = len(found_item_identifiers)
                after_to_exclude_item_count = len(to_exclude_items)
                self.log.debug(f'After exclude key {exclude_key} {after_found_item_count} to exclude {after_to_exclude_item_count}')

        if self.log.enabled:
            after_exclude_item_count = len(found_item_identifiers)
            self.log.debug(f'After exclude {after_exclude_item_count}')
        stop_watch = CommonStopWatch()
        stop_watch.start()
        yield from _convert_found_items(found_item_identifiers)

        if self.log.enabled:
            time_taken = CommonTextUtils.to_truncated_decimal(stop_watch.stop_milliseconds())
            self.log.format_with_message(f'Finished running loaded item tests in {time_taken}ms')
        else:
            stop_watch.stop()

    def get_all(self) -> Tuple[CommonLoadedItemType]:
        """ Get all items. """
        if self._collecting:
            return tuple()
        return tuple(self._all)

    def _organize(self, items: Tuple[CommonLoadedItemType]):
        if self.log.enabled:
            self.log.debug(f'Collecting {self._item_name}s Query Data...')
        self.item_library.clear()
        new_item_library = dict()
        item_organizers = tuple(self._item_organizers)
        for item in items:
            item.clear_cached_data()
            if self.log.enabled:
                self.log.format_with_message(f'Handling keys for {self._item_name}', item=item.short_name)
            item_identifier = item.identifier
            item_keys = list()
            for item_organizer in item_organizers:
                if not item_organizer.applies(item):
                    continue
                item_key_type = item_organizer.key_type
                for item_key_value in item_organizer.get_key_values(item):
                    item_key = (item_key_type, item_key_value)
                    item_keys.append(item_key)
                    if item_key not in new_item_library:
                        new_item_library[item_key] = set()
                    if item_identifier in new_item_library[item_key]:
                        continue
                    new_item_library[item_key].add(item_identifier)
            if self.log.enabled:
                self.log.format_with_message(f'Applied keys to {self._item_name}.', name=item.short_name, keys=item_keys)

        if self.log.enabled:
            self.log.format_with_message(f'Completed collecting {self._item_name} Query Data.', item_library=new_item_library)
        self.item_library = new_item_library

    def trigger_collection(self, show_loading_notification: bool = True) -> None:
        """trigger_collection(show_loading_notification=True)

        Trigger the action code to collect all items and organize them by a number of keys.

        :param show_loading_notification: If set to True, the Loading Item's notification will be shown. If set to False, the Loading Item's notification will not be shown. Default is True.
        :type show_loading_notification: bool, optional
        """
        def _recollect_data() -> None:
            try:
                if not self._registry.loaded or self._registry.loading:
                    def _on_finished_loading() -> None:
                        self.trigger_collection(show_loading_notification=False)

                    if show_loading_notification:
                        CommonBasicNotification(
                            self._loading_items_title(),
                            self._loading_items_description()
                        ).show()
                    self._registry.register_on_finished_loading_callback(_on_finished_loading)
                    self._registry.load()
                    return

                number_of_items = self._collect()
                if number_of_items == -1:
                    return
                CommonBasicNotification(
                    self._finished_loading_title(),
                    self._finished_loading_description(),
                    description_tokens=(str(self.total_valid), str(self.total), str(self.duplicates), str(self.total_invalid))
                ).show()
            except Exception as ex:
                self.log.error(f'Error occurred while collecting {self._item_name}s.', exception=ex)
            finally:
                self._collecting = False

        _recollect_data()

    def _collect(self) -> int:
        if self._collecting:
            return -1
        self._collecting = True
        try:
            # noinspection PyTypeChecker
            self._all: Tuple[CommonLoadedItemType] = tuple(self._registry.loaded_items.values())
            self._total = self._registry.total
            self._total_valid = self._registry.total_valid
            self._total_invalid = self._registry.total_invalid
            self._duplicates = self._registry.duplicates
            self.log.format_with_message(
                f'Loaded {self._item_name}s',
                all_list=self._all
            )
            enabled = self.log.enabled
            self.log.enable()
            after_load_time = CommonTextUtils.to_truncated_decimal(self._registry.total_time)
            loaded_items_count = len(self._all)
            self.log.debug(f'Took {after_load_time}ms to collect {loaded_items_count} {self._item_name}s.')
            if not enabled:
                self.log.disable()
            stop_watch = CommonStopWatch()
            stop_watch.start()
            self._organize(self._all)
            self._collecting = False
            self.log.enable()
            time_taken = CommonTextUtils.to_truncated_decimal(stop_watch.stop_milliseconds())
            after_organize_time = time_taken
            found_count = len(self._all)
            self.log.debug(f'Took {after_organize_time}ms to organize {found_count} {self._item_name}s')
            if not enabled:
                self.log.disable()
            if self.log.enabled:
                found_all_count = len(self._all)
                self.log.debug(f'Loaded {found_all_count} {self._item_name}s.')
            return len(self._all)
        except Exception as ex:
            self.log.error(f'Error occurred while collecting {self._item_name}s.', exception=ex)
            return -1
        finally:
            self._collecting = False

    @classmethod
    def register_item_organizer(cls, key_type: Any) -> Callable[[Any], Any]:
        """ Register an item organizer. """
        return cls()._register_item_organizer(key_type)

    def _register_item_organizer(self, key_type: Any) -> Callable[[Any], Any]:
        def _method_wrapper(item_filter: Callable[[int], CommonLoadedItemOrganizer]):
            self.add_item_organizer(item_filter, key_type)
            return item_filter
        return _method_wrapper

    @classmethod
    def _should_show_finished_loading_notification(cls) -> bool:
        return True

    @classmethod
    def _finished_loading_title(cls) -> Union[int, str]:
        raise NotImplementedError()

    @classmethod
    def _finished_loading_description(cls) -> Union[int, str]:
        raise NotImplementedError()

    @classmethod
    def _loading_items_title(cls) -> Union[int, str]:
        raise NotImplementedError()

    @classmethod
    def _loading_items_description(cls) -> Union[int, str]:
        raise NotImplementedError()

    @classmethod
    def _load_items_on_zone_early_load(cls, event_data: S4CLZoneEarlyLoadEvent, show_loading_notification: bool = False):
        if event_data.game_loaded:
            # If the game is already loaded, we've already loaded the data once.
            return False
        cls().trigger_collection(show_loading_notification=show_loading_notification)
        return True

    @classmethod
    def _load_items_on_zone_late_load(cls, event_data: S4CLZoneLateLoadEvent, show_loading_notification: bool = True):
        if event_data.game_loaded:
            # If the game is already loaded, we've already loaded the data once.
            return False
        cls().trigger_collection(show_loading_notification=show_loading_notification)
        return True

    @classmethod
    def _notify_items_loaded_on_zone_late_load(cls, event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            # If the game is already loaded, we've already notified about the data once.
            return False
        if not cls().collecting and cls._should_show_finished_loading_notification():
            CommonBasicNotification(
                cls._finished_loading_title(),
                cls._finished_loading_description(),
                description_tokens=(str(cls().total_valid), str(cls().total), str(cls().duplicates), str(cls().total_invalid))
            ).show()
        return True

    @classmethod
    def _show_item_loading_notification_on_first_update(cls) -> None:
        if cls().collecting:
            CommonBasicNotification(
                cls._loading_items_title(),
                cls._loading_items_description()
            ).show()
