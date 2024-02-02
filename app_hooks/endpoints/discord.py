from .base import EndpointInterfaceABC
from typing import Any
from ..templates import render_to_string
import requests
from ..helpers import get_dict_path_or_none
from jira import JIRA
from ..models import EndpointDirect
import datetime

# jira = JIRA('https://jira.appevent.ru', basic_auth=('<jira_username>', '<jira_password>'))


class DiscordDirectEndpoint(EndpointInterfaceABC):
    """ Рендер из шаблона """

    def get_discord_post_data(self, endpoint) -> Any:

        if isinstance(endpoint, EndpointDirect):
            template = endpoint.template

        return {'content': render_to_string(
            template=template, base_data=self.data_filter, jira_data=self.jira_data)}

    def send_message(self, endpoint) -> bool:
        response = requests.post(
            self.endpoint.callback,
            json=self.get_discord_post_data(self.endpoint)
        )
        response.raise_for_status()
        if response.status_code == 204:
            return True
        return False


class DiscordEmbededEndpoint(DiscordDirectEndpoint):
    """ Рендер встроенного шаблона """

    def get_discord_post_data(self, endpoint) -> Any:
        post = self.endpoint.get_discord_data(jira_data=self.jira_data)
        return post

    def send_message(self, endpoint) -> bool:
        response = requests.post(
            self.endpoint.callback,
            json=self.get_discord_post_data(self.endpoint)
        )
        response.raise_for_status()
        if response.status_code == 204:
            return True
        return False
