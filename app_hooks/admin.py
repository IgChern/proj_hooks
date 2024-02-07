from django.contrib import admin
from .models import (Event, Filter, EndpointEmbeded,
                     EmbededFields, EndpointDirect,
                     EndpointInterface, EmbededFooter,
                     MiddlewaresBase)
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin


@admin.register(MiddlewaresBase)
class MiddlewareAdmin(admin.ModelAdmin):
    search_fields = ('type', )
    list_display = ('type', )


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


@admin.register(EmbededFooter)
class EmbededAdmin(admin.ModelAdmin):
    search_fields = ('text', 'icon_url')
    list_display = ('text', 'icon_url')


class EmbededFieldsInline(admin.TabularInline):
    model = EmbededFields
    extra = 1


class EmbededFooterInline(admin.TabularInline):
    model = EmbededFooter
    extra = 1


@admin.register(EndpointDirect)
class EndpointDirectAdmin(PolymorphicChildModelAdmin):
    base_model = EndpointDirect


@admin.register(EndpointEmbeded)
class EndpointEmbededAdmin(PolymorphicChildModelAdmin):
    base_model = EndpointEmbeded
    # inlines = [EmbededFieldsInline, EmbededFooterInline]


@admin.register(EndpointInterface)
class EndpointInterfaceAdmin(PolymorphicParentModelAdmin):
    base_model = EndpointInterface
    child_models = [EndpointDirect, EndpointEmbeded]
