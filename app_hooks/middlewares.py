from .helpers import get_dict_path_or_none
from jira import JIRA
from abc import ABCMeta, abstractmethod
import datetime


class MiddlewareInterface(metaclass=ABCMeta):

    @abstractmethod
    def process(self, jira_data):
        return {}


class TaskStatMiddleware(MiddlewareInterface):
    def process(self, jira_data):
        jira = JIRA('https://jira.appevent.ru',
                    basic_auth=('<jira_username>', '<jira_password>'))

        issue_obj = jira.issue(
            id=jira_data['issue']['id'], expand='changelog')

        assignee = issue_obj.fields.assignee.displayName if issue_obj.fields.assignee else "Не назначен"
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
                        elif temp_date.date().weekday() not in [5, 6]:
                            time_spended += 1
                        temp_date += datetime.timedelta(days=1)
            elif history['items'][0]['field'] == 'status' and history['items'][0]['toString'] == 'Reopened':
                reopen_count += 1

        m_data = {'assignee': assignee, 'reopen_count': reopen_count,
                  'time_spended': round(time_spended, 2)}
        return {'task_stat': m_data}


class ReleaseStatMiddleware(MiddlewareInterface):

    def process(self, jira_data):

        project_id = get_dict_path_or_none(
            jira_data, 'version', 'projectId')
        version = get_dict_path_or_none(jira_data, 'version', 'name')

        jira = JIRA('https://jira.appevent.ru',
                    basic_auth=('<jira_username>', '<jira_password>'))

        issues = jira.search_issues(
            f'fixVersion={version} AND project={project_id}')

        task_assignee = {
            x.key: x.fields.assignee.displayName for x in issues if x.fields.assignee}

        project = jira.project(project_id)

        tasks = {}
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

        m_data = {'project': project.name,
                  'version': version, 'tasks': tasks}

        return {'release_stat': m_data}
