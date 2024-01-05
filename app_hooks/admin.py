from django.contrib import admin
from .models import Event, Filter, EndpointEmbeded


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ('name', 'endpoint')
    list_filter = ('endpoint', )
    list_display = ('name', 'endpoint')


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('events', )
    list_display = ('name', 'data')


@admin.register(EndpointEmbeded)
class EndponitAdmin(admin.ModelAdmin):
    list_display = ('data_filter', 'jira_data')
