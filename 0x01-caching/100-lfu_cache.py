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
        """ Adds data to cache based on LFU policy
            - Args:
                - key: new entry's key
                - item: entry's value
        """
        if not key or not item:
            return

        if key in self.cache_data:
            # Update existing item's frequency
            self.counter[key] += 1
        else:
            # If the cache is full, remove the LFU or LRU item
            if len(self.cache_data) >= self.MAX_ITEMS:
                lfu_key = min(self.counter, key=lambda k: (self.counter[k], self.timestamps[k]))
                self.cache_data.pop(lfu_key)
                self.counter.pop(lfu_key)
                self.timestamps.pop(lfu_key)

            # Add the new item
            self.counter[key] = 1
            self.timestamps[key] = self.timestamp
            self.timestamp += 1

        # Update the item in the cache
        self.cache_data[key] = item

    def get(self, key: Any) -> Optional[Any]:
        """ Gets cache data associated with given key
            and updates dict in accordance to LFU policy
            - Args:
                - key to look for
            - Return:
                - value associated with the key
        """
        cache_item = self.cache_data.get(key)
        if cache_item:
            # Update the item's frequency and timestamp
            self.counter[key] += 1
            self.timestamps[key] = self.timestamp
            self.timestamp += 1

        return cache_item
