from django import forms
from app_hooks.models import Filter, EmbededFooter, EmbededFields, EndpointDirect, EndpointEmbeded, Event
from django.forms.widgets import Textarea


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['name', 'data']


class EndpointDirectForm(forms.ModelForm):
    class Meta:
        model = EndpointDirect
        fields = ['name', 'callback', 'template']


class EmbededFieldsForm(forms.ModelForm):
    class Meta:
        model = EmbededFields
        fields = ['name', 'value', 'inline']


class EmbededFooterForm(forms.ModelForm):
    class Meta:
        model = EmbededFooter
        fields = ['text', 'icon_url']


class EndpointEmbededForm(forms.ModelForm):

    class Meta:
        model = EndpointEmbeded
        fields = ['name', 'callback', 'title', 'description',
                  'url', 'color', 'thumbnail', 'author', 'fields', 'footer']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'filters', 'endpoints']
