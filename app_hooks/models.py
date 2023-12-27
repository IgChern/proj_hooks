from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List, Any
from app_hooks.endpoints.discord import DiscordEmbededEndpoint


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
    # поменять на мени2мени для EndpointDirect?
    endpoint = models.CharField(_('Endpoint'), max_length=255, blank=False)
    filters = models.ManyToManyField(Filter, related_name='events')

    def __str__(self):
        return self.name

    # функция с ендпоинтами, переписать эту или сделать новую, которая будет возвращать список ендпоинтов?
    # не пойму как она должна выглядеть в принципе
    # + как потом сделать сумму списков, это сумма функции ниже + функция с ендпоинтами? + вопрос по админ панели
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
            'endpoint': self.endpoint,
            'filters': filters_list
        }
        return data

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class EndpointInteface(models.Model):
    ENDPOINTTYPE = 'base'

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
    ENDPOINTTYPE = 'direct'

    template = models.TextField(_('Template'), blank=True)
    events = models.ManyToManyField(Event, related_name='direct_endpoints')

    class Meta:
        verbose_name = _('Direct Endpoint')
        verbose_name_plural = _('Direct Endpoints')


class EmbededFields(models.Model):

    name = models.CharField(max_length=255)
    value_string = models.CharField(max_length=255, blank=True, null=True)
    value_frontend = JSONField(blank=True, null=True)
    value_backend = JSONField(blank=True, null=True)
    inline = models.BooleanField(default=True)


class EndpointEmbeded(EndpointInteface):
    ENDPOINT_TYPE = 'embeded'
    title = models.CharField(('Title'), max_length=255, blank=False)
    description = models.CharField(('Title'), max_length=255, blank=False)
    url = models.URLField(_('Callback'), blank=False)
    color = models.IntegerField(_('Color'), blank=False)
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

    def get_discord_data(self) -> Any:

        data = DiscordEmbededEndpoint.get_discord_post_data()

        data['embeds'][0]['title'] = self.title  # Как получить key и summary?
        data['embeds'][0]['description'] = self.description
        data['embeds'][0]['url'] = self.url
        data['embeds'][0]['color'] = self.color
        data['embeds'][0]['thumbnail'] = {
            'url': self.thumbnail['url'],
            'height': self.thumbnail['height'],
            'width': self.thumbnail['width']
        }
        data['embeds'][0]['author'] = {'name': self.author['name']}
        data['embeds'][0]['footer'] = {
            'text': self.footer['text'],
            'icon_url': self.footer['icon_url']
        }

        fields = []
        for field in self.fields.all():
            field_data = {
                'name': field.name,
                'inline': field.inline
            }

            if field.value_string:
                field_data['value'] = field.value_string
            elif field.value_frontend:
                # Как получить фронт енд скор?
                field_data['value'] = f'FrontEnd: {field.value_frontend}'
            elif field.value_backend:
                # Как получить бэкенд скор?
                field_data['value'] = f'BackEnd: {field.value_backend}'

            fields.append(field_data)

        data['embeds'][0]['fields'] = fields

        return data
