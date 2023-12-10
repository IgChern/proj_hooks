from typing import Dict
from app_hooks.parsers import CallbackParser
from app_hooks.storage import DjangoStorage


class Service:
    def __init__(self):
        self.parser = CallbackParser(data_storage=DjangoStorage())

    def process_jira_callback(self, data: Dict):
        return self.parser.parse_callback(data)
