from django.contrib import admin
from .models import Event, Filter, EndpointEmbeded, EmbededFields, EndpointDirect, EndpointInterface
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


@admin.register(EmbededFields)
class EmbededAdmin(admin.ModelAdmin):
    search_fields = ('name', 'value')
    list_display = ('name', 'value', 'inline')


class EmbededFieldsInline(admin.TabularInline):
    model = EmbededFields
    extra = 1


@admin.register(EndpointDirect)
class EndpointDirectAdmin(PolymorphicChildModelAdmin):
    base_model = EndpointDirect


@admin.register(EndpointEmbeded)
class EndpointEmbededAdmin(PolymorphicChildModelAdmin):
    base_model = EndpointEmbeded
    # inlines = [EmbededFieldsInline]


@admin.register(EndpointInterface)
class EndpointInterfaceAdmin(PolymorphicParentModelAdmin):
    base_model = EndpointInterface
    child_models = [EndpointDirect, EndpointEmbeded]
