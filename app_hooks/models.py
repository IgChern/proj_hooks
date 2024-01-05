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


class EndpointInteface(models.Model):
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


class EndpointDirect(EndpointInteface):
    ENDPOINT_TYPE = 'discord_direct'

    template = models.TextField(_('Template'), blank=True)
    events = models.ManyToManyField(Event, related_name='direct_endpoints')

    class Meta:
        verbose_name = _('Direct Endpoint')
        verbose_name_plural = _('Direct Endpoints')


class EmbededFields(models.Model):

    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=False)
    inline = models.BooleanField(default=True)


class EndpointEmbeded(EndpointInteface):
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

    def parse_template_string(self, template: str, jira_data: Dict) -> str:
        pattern = r'{{\s*([^{}]+)\s*}}'

        def replace(match):
            keys = [key.strip() for key in match.group(1).split(',')]
            values = [self._get_nested_value(
                jira_data, key.split(',')) for key in keys]
            return ', '.join(str(value) for value in values)

        result = re.sub(pattern, replace, template)
        return result

    def _get_nested_value(self, dictionary: Dict, keys: list):
        try:
            for key in keys:
                dictionary = dictionary[key]
            return dictionary
        except (KeyError, TypeError):
            return None

    def get_discord_data(self, jira_data: dict) -> Any:
        parsed_title = self.parse_template_string(self.title, jira_data)
        parsed_description = self.parse_template_string(
            self.description, jira_data)
        parsed_url = self.parse_template_string(self.url, jira_data)
        parsed_color = self.parse_template_string(self.color, jira_data)
        parsed_thumbnail = self.parse_template_string(
            self.thumbnail, jira_data)
        parsed_author = self.parse_template_string(self.author, jira_data)
        parsed_footer = self.parse_template_string(self.footer, jira_data)
        parsed_fields = self.parse_template_string(self.fields, jira_data)

        if parsed_fields is not None:
            try:
                parsed_fields = json.loads(parsed_fields)
            except json.JSONDecodeError:
                parsed_fields = None

        fields_data = []
        if parsed_fields:
            for field in parsed_fields:
                name = self.parse_template_string(
                    field.get('name', ''), jira_data)
                value = self.parse_template_string(
                    field.get('value', ''), jira_data)
                inline = self.parse_template_string(field.get('inline', False))

                field_data = {
                    "name": name,
                    "value": value,
                    "inline": inline,
                }
                fields_data.append(field_data)

        data = {
            "embeds": [
                {
                    "title": parsed_title,
                    "description": parsed_description,
                    "url": parsed_url,
                    "color": parsed_color,
                    "thumbnail": {
                        "url": parsed_thumbnail,
                        "height": 1,
                        "width": 1
                    },
                    "author": {
                        "name": parsed_author,
                    },
                    "footer": {
                        "text": parsed_footer,
                        "icon_url": "https://appevent.ru/img/logo_clean@2x.png"
                    },
                    "fields": fields_data,
                }
            ]
        }

        return data
