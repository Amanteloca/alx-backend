#!/usr/bin/env python3
"""
LFU caching module
"""
from base_caching import BaseCaching
from typing import Any, Optional


class LFUCache(BaseCaching):
    """ LFU cache class
    """
    def __init__(self):
        """ Initializes new instance
        """
        super().__init__()
        self.counter = {}

    def put(self, key: Any, item: Any) -> None:
        """ Adds data to cache based on LRU policy
            - Args:
                - key: new entry's key
                - item: entry's value
        """
        if not key or not item:
            return
        counter = self.counter
        new_cache_data = {key: item}
        old_cache_data = self.cache_data.get(key)
        if len(self.cache_data) == self.MAX_ITEMS and not old_cache_data:
            key_to_remove = list(counter.keys())[0]
            self.cache_data.pop(key_to_remove)
            counter.pop(key_to_remove)
            print(f'DISCARD: {key_to_remove}')
        self.cache_data.update(new_cache_data)
        counter.update({key: counter.get(key, 0) + 1})
        counter = dict(sorted(counter.items(),
                              key=lambda x: (x[1], x[0])))

    def get(self, key: Any) -> Optional[Any]:
        """ Gets cache data associated with given key
            and updates dict in accordance to LFU policy
            - Args:
                - key to look for
            - Return:
                - value associated with the key
        """
        cache_item = self.cache_data.get(key)
        counter = self.counter
        if cache_item:
            counter.update({key: counter.get(key) + 1})
            counter = dict(sorted(counter.items(),
                                  key=lambda x: (x[1], x[0])))
        return cache_item
