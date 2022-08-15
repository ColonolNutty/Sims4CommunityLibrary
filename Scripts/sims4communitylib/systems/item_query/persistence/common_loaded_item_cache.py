"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TypeVar, Generic

from sims4communitylib.systems.item_query.dtos.common_loaded_item import CommonLoadedItem
from sims4communitylib.systems.caching.common_serializable_object_cache import CommonSerializableObjectCache

CommonLoadedItemCacheType = TypeVar('CommonLoadedItemCacheType', bound=CommonLoadedItem)


class CommonLoadedItemCache(CommonSerializableObjectCache[CommonLoadedItemCacheType], Generic[CommonLoadedItemCacheType]):
    """A cache of Loaded Items."""
    pass
