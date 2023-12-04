from django.db import models


# Create your models here.
class Filters(models.Model):
    '''
    This model Filters makes fields for event name, project name,
    priority name and subtask as Bool.
    Method make_dict returns dictionary of fields.
    '''
    event_name = models.CharField(max_length=255)
    proj_name = models.CharField(max_length=255)
    priority_name = models.CharField(max_length=255)
    subtask = models.BooleanField()

    def __str__(self):
        return self.event_name

    def make_dict(self):
        return {
            'event_name': self.event_name,
            'proj_name': self.proj_name,
            'priority_name': self.priority_name,
            'subtask': self.subtask
        }


class Event(models.Model):
    '''
    This model Event makes fields for the name, endpoint,
    template and callback URL.
    '''
    name = models.CharField(max_length=255)
    endpoint = models.TextField()
    template = models.TextField()
    callback = models.URLField()
    filters = models.ManyToManyField(Filters)

    def __str__(self):
        return self.name
