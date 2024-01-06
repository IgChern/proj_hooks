from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List, Any, Dict
import re
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

    def __str__(self):
        return self.name

    def get_filter_list(self) -> List[dict]:
        filters_list = []
        for filter in self.filters.all():
            if isinstance(filter.data, list):
                filters_list.extend(filter.data)
            else:
                filters_list.append(filter.data)

        data = {
            'id': self.id,
            'name': self.name,
            'filters': filters_list
        }
        return data

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class EndpointInterface(models.Model):
    ENDPOINT_TYPE = 'base'

    name = models.CharField(('Name'), max_length=255, blank=False)
    callback = models.URLField(('Callback'), blank=False)
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

    class Meta:
        verbose_name = _('Direct Endpoint')
        verbose_name_plural = _('Direct Endpoints')


class EmbededFields(models.Model):

    name = models.CharField(max_length=255)
    value = models.CharField(
        max_length=255, blank=False, default=list, null=True)
    inline = models.BooleanField(default=True)


class EndpointEmbeded(EndpointInterface):
    ENDPOINT_TYPE = 'discord_embeded'

    name = models.CharField(('Name'), max_length=255, blank=False)
    title = models.CharField(('Title'), max_length=255, blank=False)
    description = models.CharField(
        ('Description'), max_length=255, blank=False)
    url = models.URLField(_('Url'), blank=False)
    color = models.CharField(_('Color'), blank=False)
    thumbnail = models.JSONField(
        _('Thumbnail'), default=list, null=True, blank=True)
    author = models.JSONField(
        _('Author'), default=list, null=True, blank=True)
    footer = models.JSONField(
        _('Footer'), default=list, null=True, blank=True)
    fields = models.ManyToManyField(EmbededFields, related_name='endpoint')
    events = models.ManyToManyField(Event, related_name='embeded_endpoints')

    class Meta:
        verbose_name = _('Embeded Endpoint')
        verbose_name_plural = _('Embeded Endpoints')

    @staticmethod
    def extract_keys(template_string):
        pattern = r'\{\{\s*([^{}]+)\s*\}\}'
        matches = re.findall(pattern, template_string)
        return [key.strip() for key in matches if key.strip()]

    def get_discord_data(self, jira_data: dict):

        data = {
            "embeds": [
                {
                    "title": self.title,
                    "description": self.description,
                    "url": self.url,
                    "color": self.color,
                    "thumbnail": {
                        "url": self.thumbnail['url'],
                        "height": self.thumbnail['height'],
                        "width": self.thumbnail['width']
                    },
                    "author": {'name': self.author['name']},
                    "footer": {
                        'text': self.footer['text'],
                        'icon_url': self.footer['icon_url']
                    },
                    "fields": [
                        {
                            "name": field.name,
                            "value": field.value,
                            "inline": field.inline
                        }
                        for field in self.fields.all()
                    ]
                }
            ]
        }
        return data

    def find_value(self, data, path) -> Any:
        keys = path.split(',')
        value = data
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return None
        return value
