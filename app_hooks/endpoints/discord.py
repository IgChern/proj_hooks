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


class DiscordTaskStatEndpoint(DiscordDirectEndpoint):

    def check_estimate(self, obj):

        issue_obj = jira.issue(id=obj.id, expand='changelog')

        try:
            assignee = issue_obj.fields.assignee.displayName
        except Exception:
            assignee = "Не назначен"

        date_start = None
        date_end = None
        time_spended = 0
        reopen_count = 0
        for history in issue_obj.raw['changelog']['histories']:
            if history['items'][0]['field'] == 'status' and history['items'][0]['toString'] == 'In Progress':
                date_start = datetime.datetime.fromisoformat(
                    history['created'][:-5])
            elif history['items'][0]['field'] == 'status' and history['items'][0]['fromString'] == 'In Progress':
                date_end = datetime.datetime.fromisoformat(
                    history['created'][:-5])
                if date_start.date() == date_end.date():
                    time_spended += ((date_end -
                                     date_start).total_seconds() / 3600) / 8

                else:
                    temp_date = date_start
                    while temp_date.date() <= date_end.date():
                        if temp_date.date() == date_start.date():
                            temp_date2 = temp_date.replace(hour=19, minute=00)
                            time_spended += ((temp_date2 -
                                             temp_date).total_seconds() / 3600) / 8
                        elif temp_date.date() == date_end.date():
                            temp_date2 = temp_date.replace(hour=8, minute=00)
                            time_spended += ((temp_date -
                                             temp_date2).total_seconds() / 3600) / 8
                        elif temp_date.date().weekday() in [5, 6]:
                            pass
                        else:
                            time_spended += 1

                        temp_date += datetime.timedelta(days=1)

            elif history['items'][0]['field'] == 'status' and history['items'][0]['toString'] == 'Reopened':
                reopen_count += 1

        return {'assignee': assignee, 'reopen_count': reopen_count, 'time_spended': round(time_spended, 2)}

    def get_discord_post_data(self) -> Any:
        task_id = get_dict_path_or_none(self.jira_data, 'issue', 'id')
        issue_obj = jira.issue(id=task_id, expand='changelog')
        frontend_score = get_dict_path_or_none(
            self.jira_data, 'issue', 'fields', 'customfield_10601')
        backend_score = get_dict_path_or_none(
            self.jira_data, 'issue', 'fields', 'customfield_10600')
        estimates = {'frontend_score': frontend_score,
                     'backend_score': backend_score, 'estimates': []}

        if issue_obj.fields.subtasks:
            for subtask in issue_obj.fields.subtasks:
                estimates['estimates'].append(self.check_estimate(subtask))
        else:
            estimates['estimates'].append(self.check_estimate(issue_obj))

        self.jira_data['estimates'] = estimates

        self.process_middleware()

        return {'content': render_to_string(
            template=self.endpoint.template, base_data=self.data_filter, jira_data=self.jira_data)}


class DiscordReleaseNotesEndpoint(DiscordDirectEndpoint):

    def get_discord_post_data(self):
        project_id = get_dict_path_or_none(
            self.jira_data, 'version', 'projectId')
        version = get_dict_path_or_none(self.jira_data, 'version', 'name')

        issues = jira.search_issues(
            f'fixVersion={version} AND project={project_id}')

        tasks = {}
        task_assignee = {
            x.key: x.fields.assignee.displayName for x in issues if x.fields.assignee}

        project = jira.project(project_id)

        for task in issues:
            if task.fields.issuetype.subtask:
                continue

            if task.fields.issuetype.name not in tasks:
                tasks[task.fields.issuetype.name] = []

            assignee = []
            if task.fields.subtasks:
                assignee = [task_assignee.get(
                    x.key) for x in task.fields.subtasks if task_assignee.get(x.key)]
            elif task.fields.assignee:
                assignee.append(task.fields.assignee.displayName)

            qa = task.fields.customfield_10500.displayName if task.fields.customfield_10500 else None

            tasks[task.fields.issuetype.name].append(
                {"key": task.key, 'name': task.fields.summary, 'assignee': assignee, 'qa': qa})

        jira_data = {'project': project.name,
                     'version': version, 'tasks': tasks}

        self.process_middleware()

        return {'content': render_to_string(
            template=self.endpoint.template, base_data=self.data_filter, jira_data=jira_data)}
