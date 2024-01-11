from django.contrib import admin
from .models import Event, Filter, EndpointEmbeded, EmbededFields


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', )


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('events', )
    list_display = ('name', 'data')


@admin.register(EndpointEmbeded)
class EndpointEmbededAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(EmbededFields)
class EmbededFieldsAdmin(admin.ModelAdmin):
    list_display = ('name', )
