#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import Dict, List, Optional


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """ Returns page data plus info to next and prev pages
            - Args:
                - page: page to look for information
                - page_size: size of each page
            - Return:
                - dictionary of:
                    - index: index of first item in the current pages
                    - next_index: index of next piece of data
                    - data: actual page of the dataset
                    - page_size: current page size
        """
        indexed_data = self.indexed_dataset()
        indexed_data_length = len(indexed_data)
        assert index is not None and index < indexed_data_length and index >= 0
        truncated_data: List[List] = []
        next_index = index
        while len(truncated_data) < page_size and \
                next_index < indexed_data_length:
            data = indexed_data.get(next_index)
            if data:
                truncated_data.append(data)
            next_index += 1

        page_size = len(truncated_data)
        response_data = {'index': index,
                         'next_index': next_index,
                         'page_size': page_size,
                         'data': truncated_data}
        return response_data
