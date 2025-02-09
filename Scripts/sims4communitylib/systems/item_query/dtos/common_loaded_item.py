"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any, Set, Iterator, Dict, Type

from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_log_registry import CommonLog


class CommonLoadedItem(CommonSerializable, HasClassLog):
    """ Contains information about an item that was loaded from a Snippet. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        raise NotImplementedError()

    def __init__(
        self,
        tags: Set[Any],
        is_original: bool = False
    ):
        super().__init__()
        HasClassLog.__init__(self)
        self._tags = tuple(tags)
        if is_original:
            self._original = self
        else:
            self._original = self.clone()
        self.is_original = is_original
        # These are set to None initially to prevent the item from not being able to find them.
        self._identifier = None
        self._identifiers_backwards_compatible = None
        self._identifier = self._get_identifier().lower().strip()
        self._identifiers_backwards_compatible = tuple([identifier.lower().strip() for identifier in self._get_backwards_compatible_identifiers()])

    @property
    def original(self) -> 'CommonLoadedItem':
        """The original unmodified item."""
        return self._original

    @property
    def identifier(self) -> str:
        """ The identifier of the item. """
        return self._identifier

    @property
    def identifiers_backwards_compatible(self) -> Tuple[str]:
        """ The backwards compatible identifier of the item. """
        return self._identifiers_backwards_compatible

    def _get_backwards_compatible_identifiers(self) -> Tuple[str]:
        """Create a collection of old hashed identifiers for the item, in case the original identifier changes."""
        return tuple()

    def _get_identifier(self) -> str:
        """ Creates a hashed identifier for the item. """
        raise NotImplementedError()

    @property
    def short_name(self) -> str:
        """ A short name for the item. """
        return self.identifier

    @property
    def is_available(self) -> bool:
        """Determine if the item is available."""
        return True

    @property
    def tags(self) -> Tuple[Any]:
        """ A collection of tags that apply to the item. """
        return self._tags

    @tags.setter
    def tags(self, value: Iterator[Any]):
        self._tags = tuple(value)

    def has_tag(self, tag: Any) -> bool:
        """ Determine if the item has a tag. """
        return tag in self.tags

    def has_any_tags(self, tags: Iterator[Any]) -> CommonTestResult:
        """ Determine if the item has any of the specified tags. """
        for tag in tags:
            if self.has_tag(tag):
                return CommonTestResult(True, reason=f'Has tag {tag} {self.__class__.__name__}', hide_tooltip=True)
        tags_text = ', '.join([str(tag) for tag in tags])
        return CommonTestResult(False, reason=f'Missing tags {tags_text} {self.__class__.__name__}', hide_tooltip=True)

    def has_all_tags(self, tags: Iterator[Any]) -> CommonTestResult:
        """ Determine if the item has all the specified tags. """
        for tag in tags:
            if not self.has_tag(tag):
                return CommonTestResult(False, reason=f'Missing tag {tag} {self.__class__.__name__}', hide_tooltip=True)
        return CommonTestResult.TRUE

    def add_tag(self, tag: Any):
        """ Add a tag to the item. """
        new_tags = list(self._tags)
        if tag not in new_tags:
            new_tags.append(tag)
        self._tags = tuple(new_tags)

    def add_tags(self, tags: Iterator[Any]):
        """ Add tags to the item. """
        new_tags = list(self._tags)
        for tag in tags:
            if tag not in new_tags:
                new_tags.append(tag)
        self._tags = tuple(new_tags)

    def replace_tag(self, tag_to_remove: Any, tag_to_add: Any):
        """ Replace one tag with another on the item. """
        self.remove_tags((tag_to_remove,))
        self.add_tags((tag_to_add,))

    def remove_tag(self, tag: Any):
        """ Remove a tag from the item. """
        return self.remove_tags((tag, ))

    def remove_tags(self, tags: Iterator[Any]):
        """ Remove tags from the item. """
        new_tags = list(self._tags)
        for tag in tags:
            if tag in new_tags:
                new_tags.remove(tag)
        self._tags = tuple(new_tags)

    def verify(self) -> CommonTestResult:
        """Verify the item."""
        raise NotImplementedError()

    def clone(self) -> 'CommonLoadedItem':
        """Clone the item."""
        raise NotImplementedError()

    def __eq__(self, other: 'CommonLoadedItem') -> bool:
        if not isinstance(other, CommonLoadedItem):
            return False
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash((str(self.identifier),))

    def __repr__(self) -> str:
        tags_str = ', '.join((tag.name if hasattr(tag, 'name') else tag for tag in self.tags))
        return f'ID: {self.identifier}' \
               f'\nTags: ({tags_str})'

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def load_from_package(
        cls,
        package_item: Any,
        tuning_name: str,
        log: CommonLog
    ) -> Union['CommonLoadedItem', None]:
        """load_from_package(package_item, tuning_name, log)

        Load an item from a package.

        :param package_item: A package item.
        :type package_item: Any
        :param tuning_name: The name of the tuning being read from.
        :type tuning_name: str
        :param log: A log for warnings.
        :type log: CommonLog
        :return: An item or None if an error occurs.
        :rtype: Union[CommonLoadedItem, None]
        """
        raise NotImplementedError()

    def clear_cached_data(self) -> None:
        """Clear cached data."""
        pass

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self: 'CommonLoadedItem') -> Union[str, Dict[str, Any]]:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls: Type['CommonLoadedItem'], data: Union[str, Dict[str, Any]]) -> Union['CommonLoadedItem', None]:
        raise NotImplementedError()
