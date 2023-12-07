# services.py
import json
from typing import Dict

from .parsers import CallbackParser
from .storage import FileStorage


class Service:
    def __init__(self):
        self.parser = CallbackParser(data_storage=FileStorage())

    def process_jira_callback(self, data: Dict):
        return self.parser.parse_callback(data)
