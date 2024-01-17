import json
from typing import Any, List, Optional

from .endpoints.discord import DiscordDirectEndpoint, DiscordEmbededEndpoint
from .helpers import get_dict_path_or_none
from .models import Filter
from .storage import StorageInterface


class CallbackParser(object):
    endpoints = {
        "discord_direct": DiscordDirectEndpoint,
        'discord_embeded': DiscordEmbededEndpoint,
    }

    def __init__(self, data_storage: StorageInterface):
        self._storage: StorageInterface = data_storage
        self._filters: List[dict] = self._storage.get_filters()

    def _check_list_key(self, dict_path: list, data_list: list) -> Optional[Any]:
        for data in data_list:
            result = get_dict_path_or_none(data, *dict_path)
            if result:
                return result
        return None

    def _parse_single_filter(self, data_filter: Filter, data: dict) -> bool:
        if isinstance(data_filter, dict):
            data_filter = [data_filter]
        if data_filter and data_filter[0].get('key'):
            value: Any = get_dict_path_or_none(data, *data_filter[0]['key'])
            if value and isinstance(value, list) and data_filter[0].get('list_key'):
                value = self._check_list_key(data_filter[0]['list_key'], value)

            if value is not None and any([(str(x) == str(value)) for x in data_filter[0]['value']]):
                return True

        return False

    def parse_callback(self, data: json) -> dict:
        matched_filters: dict = {}

        for data_filter in self._filters:
            filt = all([self._parse_single_filter(x['filters'], data)
                       for x in data_filter])
            if filt:
                matched_filters[data_filter[0]['id']] = {
                    'name': data_filter[0]['name'], 'endpoint': data_filter[0]['endpoint'],
                    'status': 0}

                result = False

                if data_filter[0]['endpoint'] in self.endpoints:
                    endpoint_instance = self.endpoints[data_filter[0]['endpoint']](
                        data_filter[0], data)
                    result = endpoint_instance.send_message()

                matched_filters[data_filter[0]['id']]['status'] = result

        return {'matched_filters': matched_filters}
