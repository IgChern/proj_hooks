from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List, Any, Dict
from polymorphic.models import PolymorphicModel
import re
from .helpers import get_dict_path_or_none
from django.core.exceptions import ValidationError


class Filter(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    data = JSONField(
        _('Filter Data'), default=dict, null=True, blank=True, max_length=255,)

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
