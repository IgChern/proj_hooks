from .base import EndpointInterface
from typing import Any
from ..templates import render_to_string
from ..helpers import get_dict_path_or_none
import requests
from jira import JIRA

# jira = JIRA('https://jira.appevent.ru', basic_auth=('<jira_username>', '<jira_password>'))


class DiscordDirectEndpoint(EndpointInterface):
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


class DiscordEmbededEndpoint(DiscordDirectEndpoint):
    """ Рендер встроенного шаблона """

    def get_discord_post_data(self, jira_data: dict) -> Any:

        name = jira_data['user']['displayName']
        task_type = jira_data['issue']['fields']['issuetype']['name']
        priority = jira_data['issue']['fields']['priority']['name']
        project = jira_data['issue']['fields']['project']['name']
        key = jira_data['issue']['key']
        summary = jira_data['issue']['fields']['summary']
        status = jira_data['issue']['fields']['status']['name']
        assignee = jira_data['issue']['fields']['assignee']['displayName']
        from_status = jira_data['changelog']['items'][0]['fromString']
        to_status = jira_data['changelog']['items'][0]['toString']
        comment = jira_data['comment']['body']
        qa_specialist = jira_data['issue']['fields']['customfield_10500']['displayName']

        frontend_score = jira_data['issue']['fields']['customfield_10601']
        backend_score = jira_data['issue']['fields']['customfield_10600']

        description = ''
        icon_url = 'https://cdn-icons-png.flaticon.com/32/148/148781.png'

        priority_color = {
            "Hot": "10038562",
            "Highest": "15548997",
            "High": "15105570",
            "Medium": "15844367",
            "Low": "2123412",
            "Lowest": "3447003"
        }

        if self.data_filter['template'] == 'created_default':
            description = f"Создана **{task_type}** с приоритетом **{priority}**"
            icon_url = 'https://cdn-icons-png.flaticon.com/32/148/148781.png'
        elif self.data_filter['template'] == 'status_updated_default':
            description = f"**{task_type}** перенесена из `{from_status}` в `{to_status}`"
            icon_url = 'https://cdn-icons-png.flaticon.com/32/9203/9203782.png'
        elif self.data_filter['template'] == 'comment_created_default':
            description = f"Создан комментарий в **{task_type}**\n\n" + comment
            icon_url = 'https://cdn-icons-png.flaticon.com/32/9969/9969794.png'
        elif self.data_filter['template'] == 'comment_updated_default':
            description = f"Изменен комментарий в **{task_type}**\n\n" + comment
            icon_url = 'https://cdn-icons-png.flaticon.com/32/9969/9969794.png'

        data = {
            "embeds": [
                {
                    "title": f"{key}: {summary}",
                    "description": description,
                    "url": f"https://jira.appevent.ru/browse/{key}",
                    "color": priority_color.get(priority, "0"),
                    "thumbnail": {
                        "url": icon_url,
                        "height": 1,
                        "width": 1
                    },
                    "author": {
                        "name": name,
                    },
                    "footer": {
                        "text": project,
                        "icon_url": "https://appevent.ru/img/logo_clean@2x.png"
                    },
                    "fields": [
                        {
                            "name": "Статус",
                            "value": status,
                            "inline": True
                        },
                        {
                            "name": 'Исполнитель',
                            "value": assignee if assignee else 'Не назначен',
                            "inline": True
                        },
                        {
                            "name": 'Приоритет',
                            "value": priority,
                            "inline": True
                        },
                        {
                            "name": "QA Инженер",
                            "value": qa_specialist if qa_specialist else 'Не назначен',
                            "inline": True
                        },
                        {
                            "name": "Оценка",
                            "value": f"FrontEnd: {frontend_score}, BackEnd: {backend_score}",
                            "inline": True
                        },
                    ]
                }]
        }

        return data
