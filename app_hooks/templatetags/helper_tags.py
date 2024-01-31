from django import template

register = template.Library()


@register.simple_tag
def init_form(form, instance):
    return form.__class__(instance=instance)
