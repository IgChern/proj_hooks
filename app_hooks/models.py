from django.db import models
from django.core.serializers import serialize
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class Filter(models.Model):

    name = models.CharField(_('Name'), max_length=255, blank=False)
    data = ArrayField(models.JSONField(_('Filter Data'), default=list))

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
        data = {
            'id': self.id,
            'name': self.name,
            'endpoint': self.endpoint,
            'template': self.template,
            'callback': self.callback,
            'filters': serialize('json', self.filters.all())
        }
        return data

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


events = Event.objects.prefetch_related('filters').all()
