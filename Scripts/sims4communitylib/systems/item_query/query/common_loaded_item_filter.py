"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, TypeVar, Generic

from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.systems.item_query.query.common_loaded_item_key import CommonLoadedItemKey
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

ItemKeyType = TypeVar('ItemKeyType', int, CommonInt, CommonIntFlags)


class CommonLoadedItemFilter(HasLog, Generic[ItemKeyType]):
    """ A filter for use when querying loaded items. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    def __init__(
        self,
        match_all: bool,
        match_at_least_one: bool = False,
        exclude: bool = False,
        key_type: ItemKeyType = None
    ):
        super().__init__()
        self._match_all = match_all
        self._match_at_least_one = match_at_least_one
        self._exclude = exclude
        self._key_type = key_type

    @property
    def _match_text(self) -> str:
        match_text = ''
        if self.match_all and not self.exclude:
            match_text = 'has all'
        if self.match_at_least_one and not self.exclude:
            match_text = 'has any'
        if self.exclude:
            match_text = 'has none'
        return match_text

    @property
    def key_type(self) -> Union[ItemKeyType, None]:
        """ The type of keys produced by this filter. """
        return self._key_type

    @property
    def match_all(self) -> bool:
        """
            Determine if we should match all (True) the keys or any (False) of them.
        """
        return self._match_all

    @property
    def exclude(self) -> bool:
        """
            Determine if we should not have any of the keys.
        """
        return self._exclude

    @property
    def match_at_least_one(self) -> bool:
        """
            Determine if we should match at least one key.
        """
        return self._match_at_least_one

    def get_keys(self) -> Tuple[CommonLoadedItemKey]:
        """ Retrieve the keys of this filter. """
        return tuple()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        match_text = self._match_text
        if self._key_type is None:
            return f'{self.__class__.__name__}, {match_text}'
        return f'{self._key_type.name}, {match_text}'
