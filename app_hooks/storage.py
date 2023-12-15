import json
import os
from abc import ABCMeta, abstractmethod
from typing import List

from .models import Filter, Event


class StorageInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_filters(self) -> List[Filter]:
        return []


class FileStorage(StorageInterface):

    def __init__(self):
        self._filters: List[Filter] = self.get_filters_from_file()

    def get_filters_from_file(self):
        file_path = './data_storage/filters.json'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

        return []

    def get_filters(self) -> List[Filter]:
        return self._filters


class DjangoStorage(StorageInterface):
    def get_filters(self) -> List[Filter]:
        return [event.get_filterlist() for event in Event.objects.all()]
