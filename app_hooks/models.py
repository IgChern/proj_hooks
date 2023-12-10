from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


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
    endpoint = models.TextField(_('Endpoint'), blank=False)
    template = models.TextField(_('Template'), blank=True)
    callback = models.URLField(_('Callback'), blank=False)
    filters = models.ManyToManyField(Filter, related_name='events')

    def __str__(self):
        return self.name

    def get_filterlist(self):

        filters_list = list()
        for i in self.filters.all():
            if isinstance(i, list):
                filters_list.extend(i)
            else:
                filters_list.append(i)

        data = {
            'id': self.id,
            'name': self.name,
            'endpoint': self.endpoint,
            'template': self.template,
            'callback': self.callback,
            'filters': filters_list
        }
        return data

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
