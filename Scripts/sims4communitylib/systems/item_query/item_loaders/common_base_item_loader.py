"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Any, Union, TypeVar, Generic

from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4.resources import Types
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

CommonLoadedItemType = TypeVar('CommonLoadedItemType', bound=CommonLoadedItem)


class CommonBaseItemLoader(CommonService, HasLog, Generic[CommonLoadedItemType]):
    """ Loads items. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    @property
    def snippet_names(self) -> Tuple[str]:
        """ The names of snippets containing items. """
        raise NotImplementedError()

    def __init__(self) -> None:
        super().__init__()
        self._total = 0
        self._total_valid = 0
        self._total_invalid = 0

    @property
    def total(self) -> int:
        """The total number of items that were looked at"""
        return self._total

    @property
    def total_valid(self) -> int:
        """The total number of items that were valid."""
        return self._total_valid

    @property
    def total_invalid(self) -> int:
        """The total number of items that were invalid."""
        return self._total_invalid

    def get_checksum_data_gen(self) -> Iterator[Tuple[str, int, int]]:
        """Generate checksums."""
        raise NotImplementedError()

    def load(self) -> Iterator[CommonLoadedItemType]:
        """load()

        Loads all items.

        :return: An iterator of the valid items.
        :rtype: Iterator[Any]
        """
        self._total = 0
        self._total_valid = 0
        self._total_invalid = 0
        snippet_names: Tuple[str] = self.snippet_names
        for item_package in CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, snippet_names):
            tuning_name = item_package.__name__
            try:
                items = tuple(self._load(item_package, tuning_name))

                total = 0
                total_valid = 0
                total_invalid = 0

                for item in items:
                    total += 1

                    if item is None:
                        total_invalid += 1
                        continue
                    verify_result = item.verify()
                    if verify_result:
                        total_valid += 1
                        yield item
                    else:
                        self.log.warn(f'{item.short_name} was not valid. Reason: {verify_result}')
                        total_invalid += 1

                self._total += total
                self._total_valid += total_valid
                self._total_invalid += total_invalid
                self.log.warn(f'Loaded {tuning_name}, Valid: {total_valid}, Total Invalid: {total_invalid}, Total: {total}')
            except Exception as ex:
                self.log.error(f'An error occurred while parsing items from snippet \'{tuning_name}\'', exception=ex)

    def _load(self, package_item: Any, tuning_name: str) -> Tuple[Union[CommonLoadedItemType, None]]:
        raise NotImplementedError()
