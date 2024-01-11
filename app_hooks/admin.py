from django.contrib import admin
from .models import Event, Filter, EndpointEmbeded, EmbededFields, EndpointDirect
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', )


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('events', )
    list_display = ('name', 'data')
