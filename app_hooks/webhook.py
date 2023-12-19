from .parsers import CallbackParser
from .storage import DjangoStorage


class Service:
    def __init__(self):
        self.parser = CallbackParser(data_storage=DjangoStorage())

    def process_jira_callback(self, data: dict) -> dict:
        """
        Process Jira callback.

        param data: Dictionary from Jira callback data.
        return: Return result as a dictionary.
        """
        return self.parser.parse_callback(data)
