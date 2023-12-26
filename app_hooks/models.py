from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from typing import List


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
    endpoint = models.CharField(_('Endpoint'), max_length=255, blank=False)
    template = models.TextField(_('Template'), blank=True)
    callback = models.URLField(_('Callback'), blank=False)
    filters = models.ManyToManyField(Filter, related_name='events')

    def __str__(self):
        return self.name

    def get_filter_list(self) -> List[dict]:
        filters_list = []
        for filter_item in self.filters.all():
            if isinstance(filter_item.data, list):
                filters_list.extend(filter_item.data)
            else:
                filters_list.append(filter_item.data)

        data = {
            'id': self.id,
            'name': self.name,
            'endpoint': self.endpoint,
            'template': self.template,
            'callback': self.callback,
            'filters': filters_list
        }
        return data

    def get_endpoint_list(self) -> List[dict]:
        endpoint_list = []
        for event in Event.objects.filter(endpoint=self.endpoint):
            event_data = {
                'id': event.id,
                'name': event.name,
                'endpoint': event.endpoint,
                'template': event.template,
                'callback': event.callback,
                'filters': event.get_filter_list()
            }
            endpoint_list.append(event_data)
        return endpoint_list

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class EndpointInteface(models.Model):
    ENDPOINTTYPE = 'base'

    name = models.CharField(('Name'), max_length=255, blank=False)
    callback = models.URLField(('Callback'), blank=False)
    events = models.ManyToManyField(Event, related_name='endpoints')

    def str(self):
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
    value_string = models.CharField(max_length=255, blank=True)
    value_list = models.JSONField(blank=True, null=True)
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
