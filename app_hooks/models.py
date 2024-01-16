from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List, Any, Dict
from polymorphic.models import PolymorphicModel
import re
from .helpers import get_dict_path_or_none


class Filter(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    data = JSONField(
        _('Filter Data'), default=list, null=True, blank=True)

    def __str__(self):
        return self.name

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

    template = models.TextField(_('Template'), blank=True)

    def __str__(self):
        return self.name

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
        verbose_name = _('Embeded Field')
        verbose_name_plural = _('Embeded Fields')


class EndpointEmbeded(EndpointInterface):
    ENDPOINT_TYPE = 'discord_embeded'

    title = models.CharField(('Title'), max_length=255, blank=False)
    description = models.TextField(
        ('Description'), blank=False)
    url = models.URLField(_('Url'), blank=False)
    color = models.CharField(_('Color'), blank=False, max_length=15)
    thumbnail = models.URLField(
        _('Thumbnail'), null=True, blank=True)
    author = models.TextField(
        _('Author'), null=True, blank=True)
    footer = models.TextField(
        _('Footer'), null=True, blank=True)
    fields = models.ManyToManyField(EmbededFields, related_name='endpoint')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Embeded Endpoint')
        verbose_name_plural = _('Embeded Endpoints')

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
        # узнать за обязательные поля, добавить валидации, починить админку

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
                        "height": 0.5,
                        "width": 0.5
                        # узнать за размер иконки
                    },
                    "author": {
                        "name": self.extract_keys(self.author, jira_data),
                    },
                    "footer": {
                        "text": self.extract_keys(self.footer, jira_data),
                        "icon_url": "https://appevent.ru/img/logo_clean@2x.png"
                        # добавить урл в модели
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
