from .base import EndpointInterface
from typing import Any
from ..templates import render_to_string
import requests
from jira import JIRA

# jira = JIRA('https://jira.appevent.ru', basic_auth=('<jira_username>', '<jira_password>'))


class DiscordEndpoint(EndpointInterface):
    """ Рендер из шаблона """

    def __init__(self, data_filter: dict, jira_data: dict):
        self.data_filter: dict = data_filter
        self.jira_data: dict = jira_data

    def get_discord_post_data(self) -> Any:
        return {'content': render_to_string(
            template=self.data_filter['template'], base_data=self.data_filter, jira_data=self.jira_data)}

    def send_message(self) -> bool:
        response = requests.post(
            self.data_filter['callback'],
            json=self.get_discord_post_data()
        )
        response.raise_for_status()
        if response.status_code == 204:
            return True
        return False
