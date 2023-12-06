from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _


class Filter(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    data = models.JSONField(_('Filter Data'), default=dict)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')


class Event(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    endpoint = models.TextField(_('Endpoint'), blank=False)
    template = models.TextField(_('Template'), blank=True)
    callback = models.URLField(_('Callback'), blank=False)
    filters = models.ManyToManyField(Filter, related_name='events')

    def __str__(self):
        return self.name

    def get_event(self):
        item = model_to_dict(self, fields=['id', 'name', 'endpoint', 'template', 'callback'])
        item['filters'] = [x.data for x in self.filters.all()]
        return item

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
