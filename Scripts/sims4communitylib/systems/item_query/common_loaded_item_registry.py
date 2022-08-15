"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from threading import Thread
from typing import Iterator, Dict, List, Union, TypeVar, Generic, Tuple, Any

from sims4communitylib.systems.item_query.persistence.common_loaded_item_cache import CommonLoadedItemCache
from sims4communitylib.systems.item_query.persistence.common_loaded_item_cache_service import \
    CommonLoadedItemCacheService
from sims4communitylib.systems.item_query.item_loaders.common_base_item_loader import CommonBaseItemLoader
from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4.callback_utils import CallableList
from sims4communitylib.classes.time.common_stop_watch import CommonStopWatch
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService

CommonLoadedItemType = TypeVar('CommonLoadedItemType', bound=CommonLoadedItem)


class CommonLoadedItemRegistry(CommonService, HasLog, Generic[CommonLoadedItemType]):
    """ A registry that contains loaded items. """

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
        self._loaded = False
        self.item_loaders = list()
        self.loaded_items = None
        self._total = 0
        self._total_valid = 0
        self._total_invalid = 0
        self._total_time = 0.0
        self._duplicates = 0
        self._loading = False
        self._load_thread: Union[Thread, None] = None
        self._on_finished_loading_callback = CallableList()

    @property
    def loaded(self) -> bool:
        """True, if the registry has finished loading."""
        return self._loaded

    @property
    def loading(self) -> bool:
        """True, if the registry is currently loading."""
        return self._loading

    @property
    def total(self) -> int:
        """The total number of items that were found"""
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
    def item_loaders(self) -> List[CommonBaseItemLoader]:
        """Loaders that load items."""
        return self._item_loaders

    @property
    def duplicates(self) -> int:
        """The total number of duplicate items that were found."""
        return self._duplicates

    @property
    def total_time(self) -> float:
        """The total time the registry took to load in milliseconds."""
        return self._total_time

    @item_loaders.setter
    def item_loaders(self, value: List[CommonBaseItemLoader]):
        self._item_loaders = value

    def register_on_finished_loading_callback(self, callback) -> None:
        """Finished loading callback."""
        if callback not in self._on_finished_loading_callback:
            self._on_finished_loading_callback.append(callback)

    @property
    def loaded_items(self) -> Dict[str, CommonLoadedItemType]:
        """A library of items organized by their identifiers."""
        return self._loaded_items

    @loaded_items.setter
    def loaded_items(self, value: Dict[str, CommonLoadedItemType]):
        self._loaded_items = value

    def add_item_loader(self, item_loader: CommonBaseItemLoader) -> bool:
        """ Add a loader of items. """
        if item_loader in self.item_loaders:
            return False
        self.item_loaders.append(item_loader)
        return True

    def add_item(self, item: CommonLoadedItemType) -> bool:
        """add_item(item)

        Add an Item to the registry.

        :param item: An instance of an Item
        :type item: CommonLoadedItemType
        :return: True, if the item was successfully added. False, if not.
        :rtype: bool
        """
        if not self.loaded or self.loading:
            def _add_on_finished_loading() -> None:
                _unique_id = item.identifier
                if _unique_id in self.loaded_items:
                    return
                self.loaded_items[_unique_id] = item
                return

            self.register_on_finished_loading_callback(_add_on_finished_loading)
            self.load()
            return True
        unique_id = item.identifier
        if unique_id in self.loaded_items:
            return False
        self.loaded_items[unique_id] = item
        return True

    def load(self) -> None:
        """ Load data. """
        if self._loaded or self._loading:
            self.log.format_with_message('Not loading because already loaded.', loaded=self._loaded, loading=self._loading)
            return
        try:
            self._loading = True

            should_use_cache = self._should_use_cache()

            stop_watch = CommonStopWatch()
            stop_watch.start()
            self._total_time = 0.0
            self._total = 0
            self._total_valid = 0
            self._total_invalid = 0
            items_library: Dict[str, CommonLoadedItemType] = dict()
            if not should_use_cache or self._update_cache():
                self.log.debug(f'Clearing {self.__class__.__name__} cache.')
                self._clear_cache()

            loaded_items_cache = self._load_from_cache()
            if should_use_cache and loaded_items_cache is not None:
                items: Tuple[CommonLoadedItem, ...] = loaded_items_cache.cached_objects
                self._total = len(items)
                self._total_valid = self._total
                should_verify = True
            else:
                items: Tuple[CommonLoadedItem, ...] = tuple(self._load())
                cache_service = self._get_cache_service()
                if cache_service is not None:
                    self._save_to_cache(cache_service.create_cache(items, self._get_checksums()))
                should_verify = False

            self._duplicates = 0
            for item in items:
                if should_verify and not item.verify():
                    self._total_valid -= 1
                    self._total_invalid += 1
                    continue
                identifier = item.identifier
                if identifier in items_library:
                    self._duplicates += 1
                    self._total_valid -= 1
                    continue
                self._add_additional_item_data(item)
                items_library[identifier] = item

            self.loaded_items = items_library
            self._loaded = True
            self._load_thread = None
            self._loading = False
            self._total_time = stop_watch.stop_milliseconds()
            self._on_finished_loading_callback()
            self._on_finished_loading_callback.clear()
            self.log.debug('Finished loading items.')
        except Exception as ex:
            self.log.error('Error occurred while loading items.', exception=ex)

    def _should_use_cache(self) -> bool:
        return True

    def _save_to_cache(self, item_cache: CommonLoadedItemCache[CommonLoadedItemType]):
        cache_service = self._get_cache_service()
        if cache_service is None:
            return
        return cache_service.save_to_cache(item_cache)

    def _load_from_cache(self) -> Union[CommonLoadedItemCache[CommonLoadedItemType], None]:
        cache_service = self._get_cache_service()
        if cache_service is None:
            return
        return cache_service.load_from_cache()

    def _clear_cache(self) -> None:
        cache_service = self._get_cache_service()
        if cache_service is None:
            return
        return cache_service.clear_cache()

    def _get_cache_service(self) -> Union[CommonLoadedItemCacheService[CommonLoadedItemType], None]:
        return None

    def locate_by_identifier(self, identifier: str) -> Union[CommonLoadedItemType, None]:
        """Locate an item by an identifier."""
        if identifier is None:
            return None
        return self.loaded_items.get(identifier, None)

    def _get_checksums(self) -> Tuple[Any]:
        checksums: List[Any] = list()
        for item_loader in self.item_loaders:
            for new_checksum_data in item_loader.get_checksum_data_gen():
                checksums.append(new_checksum_data)
        return tuple(checksums)

    def _update_cache(self) -> bool:
        cache_service = self._get_cache_service()
        if cache_service is None:
            self.log.debug(f'No cache service found. {self.__class__.__name__}')
            return False
        for item_loader in self.item_loaders:
            for new_checksum_data in item_loader.get_checksum_data_gen():
                if cache_service.cache_needs_update(new_checksum_data):
                    self.log.debug(f'Found a checksum that was different. {self.__class__.__name__} {new_checksum_data}')
                    return True
        self.log.debug(f'Cache does not need update. {self.__class__.__name__}')
        return False

    def _load(self) -> Iterator[CommonLoadedItemType]:
        total_invalid = 0
        total_valid = 0
        for item_loader in self.item_loaders:
            for item in item_loader.load():
                if item is None:
                    total_valid -= 1
                    total_invalid += 1
                    continue
                yield item
            self.log.format_with_message('Done loading for loader.', loader=item_loader)
            self._total += item_loader.total
            self._total_valid += item_loader.total_valid + total_valid
            self._total_invalid += item_loader.total_invalid + total_invalid

    def _add_additional_item_data(self, item: CommonLoadedItemType) -> None:
        raise NotImplementedError()
