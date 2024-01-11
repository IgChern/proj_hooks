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


class EmbededFieldsInline(admin.TabularInline):
    model = EmbededFields
    extra = 1


class EndpointDirectAdmin(PolymorphicChildModelAdmin):
    base_model = EndpointDirect
    inlines = [EmbededFieldsInline]


class EndpointEmbededAdmin(PolymorphicChildModelAdmin):
    base_model = EndpointEmbeded
    inlines = [EmbededFieldsInline]


class EndpointInterfaceAdmin(PolymorphicParentModelAdmin):
    base_model = EndpointDirect
    child_models = [EndpointDirect, EndpointEmbeded]
    inlines = [EmbededFieldsInline]
