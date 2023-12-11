from typing import Dict
from .parsers import CallbackParser
from .storage import DjangoStorage


class Service:
    def __init__(self):
        self.parser = CallbackParser(data_storage=DjangoStorage())

    def process_jira_callback(self, data: Dict):
        return self.parser.parse_callback(data)
