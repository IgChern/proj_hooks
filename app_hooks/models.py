from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List, Any, Dict
from polymorphic.models import PolymorphicModel
import re
from .helpers import get_dict_path_or_none
from django.core.exceptions import ValidationError


class MiddlewaresBase(models.Model):
    CHOICES = (
        ('task_stat', "Статистика задач"),
        ('release_stat', "Статистика релизов"),
    )

    CLASSES = {
        'task_stat': 'TaskStatMiddleware',
        'release_stat': 'ReleaseStatMiddleware',
    }
    name = models.CharField(_('Middleware name'), max_length=255, blank=True)
    class_type = models.CharField(
        _("Middleware Class Type"), max_length=255, choices=CHOICES)

    def __str__(self):
        return self.class_type

    def process_middleware(self, data):
        return self.CLASSES[self.class_type]().process(data)

    class Meta:
        verbose_name = _('Middleware')
        verbose_name_plural = _('Middlewares')


class ReleaseStatMiddleware(MiddlewaresBase):
    class_type = 'release_stat'
    project_id = models.CharField(_('Project'), max_length=255, blank=True)
    version = models.CharField(_('Version'), max_length=255, blank=True)

    def process(self, data):

        issues = jira.search_issues(
            f'fixVersion={self.version} AND project={self.project_id}')

        tasks = {}
        task_assignee = {
            x.key: x.fields.assignee.displayName for x in issues if x.fields.assignee}

        project = jira.project(self.project_id)

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
                     'version': self.version, 'tasks': tasks, 'class_type': self.class_type}

        middleware_config = MiddlewaresBase.objects.get(
            class_type=self.class_type)
        return middleware_config.process_middleware(jira_data)


class TaskStatMiddleware(MiddlewaresBase):
    class_type = 'task_stat'

    task_id = models.CharField(_('Task id'), max_length=255, blank=True)
    frontend_score = models.CharField(
        _('Front score'), max_length=255, blank=True)
    backend_score = models.CharField(
        _('Back score'), max_length=255, blank=True)

    def process(self, data):
        issue_obj = jira.issue(id=self.task_id, expand='changelog')
        estimates = {'frontend_score': self.frontend_score,
                     'backend_score': self.backend_score, 'estimates': []}

        if issue_obj.fields.subtasks:
            for subtask in issue_obj.fields.subtasks:
                estimates['estimates'].append(self.check_estimate(subtask))
        else:
            estimates['estimates'].append(self.check_estimate(issue_obj))

        data['estimates'] = estimates

        middleware_config = MiddlewaresBase.objects.get(class_type='task_stat')
        return middleware_config.process_middleware(data)


class Filter(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    data = JSONField(
        _('Filter Data'), default=list, null=True, blank=True, max_length=255,)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if not self.name:
            raise ValidationError({'filter': 'Filter is required'})

    class Meta:
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')


class EndpointInterface(PolymorphicModel):
    ENDPOINT_TYPE = 'base'

    name = models.CharField(_('Name'), max_length=255, blank=False)
    callback = models.URLField(_('Callback'), blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Endpoint')
        verbose_name_plural = _('All Endpoints')


class EndpointDirect(EndpointInterface):
    ENDPOINT_TYPE = 'discord_direct'

    template = models.TextField(_('Template'), blank=False)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if not self.template:
            raise ValidationError({'template': 'Template is required'})

        if not self.name:
            raise ValidationError({'name': 'Name is required'})

        if not self.callback:
            raise ValidationError({'callback': 'Callback is required'})

    class Meta:
        verbose_name = _('Direct Endpoint')
        verbose_name_plural = _('Direct Endpoints')


class EmbededFields(models.Model):

    name = models.CharField(max_length=255)
    value = models.CharField(
        max_length=255, blank=False, null=True)
    inline = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if not self.value:
            raise ValidationError({'value': 'Value is required'})

    class Meta:
        verbose_name = _('Embeded Field')
        verbose_name_plural = _('Embeded Fields')


class EmbededFooter(models.Model):

    text = models.CharField(
        max_length=255, null=True, blank=True)
    icon_url = models.URLField(
        _('Icon_URL'), null=True, blank=True)

    def __str__(self):
        return self.text or ''

    class Meta:
        verbose_name = _('Embeded Footer')
        verbose_name_plural = _('Embeded Footers')


class EndpointEmbeded(EndpointInterface):
    ENDPOINT_TYPE = 'discord_embeded'

    title = models.CharField(('Title'), max_length=255, blank=False)
    description = models.TextField(
        ('Description'), blank=False)
    url = models.URLField(_('Url'), blank=True)
    color = models.CharField(_('Color'), blank=False, max_length=15)
    thumbnail = models.URLField(
        _('Thumbnail'), null=True, blank=True)
    author = models.TextField(
        _('Author'), null=True, blank=False)
    footer = models.ManyToManyField(
        EmbededFooter, related_name='footers')
    fields = models.ManyToManyField(EmbededFields, related_name='endpoint')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Embeded Endpoint')
        verbose_name_plural = _('Embeded Endpoints')

    def clean(self):
        super().clean()

        if not self.title:
            raise ValidationError({'title': 'Title is required'})

        if not self.description:
            raise ValidationError({'description': 'Description is required'})

        if not self.color:
            raise ValidationError({'color': 'Color is required'})

        if not self.author:
            raise ValidationError({'author': 'Autor is required.'})

        if not self.name:
            raise ValidationError({'name': 'Name is required'})

        if not self.callback:
            raise ValidationError({'callback': 'Callback is required'})

    @staticmethod
    def extract_keys(template_string, jira_data):
        pattern = r'\{\{([^{}]+)\}\}'

        def replace_match(match):
            key_path = match.group(1).strip().split('.')
            value = get_dict_path_or_none(jira_data, *key_path)
            return str(value) if value is not None else match.group(0)

        result_string = re.sub(pattern, replace_match, template_string)
        return result_string

    def get_discord_data(self, jira_data: dict):

        priority_color = {
            "Hot": "10038562",
            "Highest": "15548997",
            "High": "15105570",
            "Medium": "15844367",
            "Low": "2123412",
            "Lowest": "3447003"
        }

        data = {
            "embeds": [
                {
                    "title": self.extract_keys(self.title, jira_data),
                    "description": self.extract_keys(self.description, jira_data),
                    "url": self.extract_keys(self.url, jira_data),
                    "color": int(self.extract_keys(self.color, jira_data)) if self.color in priority_color.values() else '0',
                    "thumbnail": {
                        "url": self.thumbnail,
                        "height": 1,
                        "width": 1
                    },
                    "author": {
                        "name": self.extract_keys(self.author, jira_data),
                    },
                    "footer":
                        {
                            "text": self.footer.get().text,
                            "icon_url": self.footer.get().icon_url
                    },
                    "fields": [
                        {
                            "name": self.extract_keys(field.name, jira_data),
                            "value": self.extract_keys(field.value, jira_data),
                            "inline": field.inline
                        }
                        for field in self.fields.all()
                    ]
                }
            ]
        }
        return data


class Event(models.Model):
    name = models.CharField(_('Name'), max_length=255, blank=False)
    filters = models.ManyToManyField(Filter, related_name='events')
    endpoints = models.ManyToManyField(
        EndpointInterface, blank=True, related_name='endpoints')
    draft = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        if not self.name:
            raise ValidationError({'name': 'Name is required'})

    def __str__(self):
        return self.name

    def get_filter_list(self) -> Dict[str, List[dict]]:

        filters_list = []

        for endpoint in self.endpoints.all():
            endpoint_filter_list = []

            for data_filter in self.filters.all():
                if isinstance(data_filter.data, list):
                    endpoint_filter_list.extend(data_filter.data)
                else:
                    endpoint_filter_list.append(data_filter.data)

            data = {
                'id': f'{self.id}-{endpoint.id}',
                'name': self.name,
                'filters': endpoint_filter_list,
                'endpoint': endpoint.ENDPOINT_TYPE,
                'endpoint_id': endpoint.id,
            }

            filters_list.append(data)

        return filters_list

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
