import json
from typing import Any, List, Optional

from .endpoints.discord import DiscordEndpoint
from .helpers import get_dict_path_or_none
from .models import Filter, Event
from .storage import StorageInterface
from django.db.models import QuerySet


class CallbackParser(object):
    endpoints = {
        "discord_direct": DiscordEndpoint,
    }

    def __init__(self, data_storage: StorageInterface):
        self._storage: StorageInterface = data_storage
        self._filters: List[Event] = self._storage.get_filters()

    def _check_list_key(self, dict_path: list, data_list: list) -> Optional[Any]:
        for data in data_list:
            result = get_dict_path_or_none(data, *dict_path)
            if result:
                return result
        return None

    def _parse_single_filter(self, data_filter: Filter, data: dict) -> bool:
        value: Any = get_dict_path_or_none(data, *data_filter['key'])
        if value and isinstance(value, list) and data_filter['list_key']:
            value = self._check_list_key(data_filter['list_key'], value)

        if value is not None and any([(str(x) == str(value)) for x in data_filter['value']]):
            return True

        return False

    def parse_callback(self, data: json) -> dict:
        matched_filters: dict = {}

        for data_filter in self._filters:
            if all([self._parse_single_filter(x, data) for x in data_filter['filters']]):
                matched_filters[data_filter['id']] = {
                    'name': data_filter['name'], 'endpoint': data_filter['endpoint'], 'template': data_filter['template'],
                    'callback': data_filter['callback'], 'status': 0}

                result = False

                if data_filter.get('endpoint') in self.endpoints:
                    endpoint_instance = self.endpoints[data_filter['endpoint']](
                        data_filter, data)
                    result = endpoint_instance.send_message()

                matched_filters[data_filter['id']]['status'] = result

        return {'matched_filters': matched_filters}
