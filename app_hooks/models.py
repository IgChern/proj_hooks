from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List, Any, Dict
import re
from .helpers import get_dict_path_or_none
import json


class Filter(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    data = JSONField(
        _('Filter Data'), default=list, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')


class Event(models.Model):
    name = models.CharField(_('Name'), max_length=255, blank=False)
    filters = models.ManyToManyField(Filter, related_name='events')
    endpoints = models.ManyToManyField(
        'EndpointEmbeded', blank=True, related_name='endpoints', null=True)

    def __str__(self):
        return self.name

    def get_filter_list(self) -> Dict[str, List[dict]]:
        data = {
            'id': self.id,
            'name': self.name,
            'filters': [],
            'endpoints': []
        }

        for endpoint in self.endpoints.all():
            filters_list = []
            for data_filter in self.filters.all():
                if isinstance(data_filter.data, list):
                    filters_list.extend(data_filter.data)
                else:
                    filters_list.append(data_filter.data)

            data['filters'].append({
                'filters': filters_list
            })

            data['endpoints'].append(endpoint.ENDPOINT_TYPE)

        return data

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class EndpointInterface(models.Model):
    ENDPOINT_TYPE = 'base'

    name = models.CharField(_('Name'), max_length=255, blank=False)
    callback = models.URLField(_('Callback'), blank=False)
    events = models.ManyToManyField(Event, related_name='endpoints')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _('Base Endpoint')
        verbose_name_plural = _('Base Endpoints')


class EndpointDirect(EndpointInterface):
    ENDPOINT_TYPE = 'discord_direct'

    template = models.TextField(_('Template'), blank=True)
    events = models.ManyToManyField(Event, related_name='direct_endpoints')

    def __str__(self):
        return self.template

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

    class Meta:
        verbose_name = _('Embeded Endpoint')
        verbose_name_plural = _('Embeded Endpoints')


class EndpointEmbeded(EndpointInterface):
    ENDPOINT_TYPE = 'discord_embeded'

    name = models.CharField(('Name'), max_length=255, blank=False)
    title = models.CharField(('Title'), max_length=255, blank=False)
    description = models.CharField(
        ('Description'), max_length=255, blank=False)
    url = models.URLField(_('Url'), blank=False)
    color = models.CharField(_('Color'), blank=False, max_length=15)
    thumbnail = models.TextField(
        _('Thumbnail'), null=True, blank=True)
    author = models.TextField(
        _('Author'), null=True, blank=True)
    footer = models.TextField(
        _('Footer'), null=True, blank=True)
    fields = models.ManyToManyField(EmbededFields, related_name='endpoint')
    events = models.ManyToManyField(
        Event, related_name='endpoints_embeded', related_query_name='endpoint_embeded')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Embeded Endpoint')
        verbose_name_plural = _('Embeded Endpoints')

    @staticmethod
    def extract_keys(template_string, jira_data):
        pattern = r'\{\{\s*([^{}]+)\s*\}\}'

        def replace_match(match):
            key_path = match.group(1).strip().split('.')
            value = get_dict_path_or_none(jira_data, *key_path)
            return str(value) if value is not None else match.group(0)

        result_string = re.sub(pattern, replace_match, template_string)
        return result_string

    def get_discord_data(self, jira_data: dict):

        data = {
            "embeds": [
                {
                    "title": self.extract_keys(self.title, jira_data),
                    "description": self.extract_keys(self.description, jira_data),
                    "url": self.extract_keys(self.url, jira_data),
                    "color": self.extract_keys(self.color, jira_data),
                    "thumbnail": self.extract_keys(self.thumbnail, jira_data),
                    "author": self.extract_keys(self.author, jira_data),
                    "footer": self.extract_keys(self.footer, jira_data),
                    "fields": [
                        {
                            "name": self.extract_keys(field.name, jira_data),
                            "value": self.extract_keys(field.value, jira_data),
                            "inline": self.extract_keys(field.inline, jira_data)
                        }
                        for field in self.fields.all()
                    ]
                }
            ]
        }
        return data
