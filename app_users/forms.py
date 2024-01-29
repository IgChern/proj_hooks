from django import forms
from app_hooks.models import Filter, EmbededFooter, EmbededFields, EndpointDirect, EndpointEmbeded, Event

from django.forms import inlineformset_factory


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['name', 'data']
        labels = {
            'name': 'Название фильтра',
            'data': 'Данные фильтра',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }


class EndpointDirectForm(forms.ModelForm):
    class Meta:
        model = EndpointDirect
        fields = ['name', 'callback', 'template']
        labels = {
            'name': 'Название endpoint',
            'callback': 'Данные callback(url)',
            'template': 'Данные template'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'callback': forms.TextInput(attrs={'class': 'form-control'}),
            'template': forms.Textarea(attrs={'class': 'form-control'})
        }


class EmbededFieldsForm(forms.ModelForm):
    class Meta:
        model = EmbededFields
        fields = ['name', 'value', 'inline']
        labels = {
            'name': 'Название field',
            'value': 'Данные value',
            'inline': 'Inline(T/F)'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmbededFooterForm(forms.ModelForm):
    class Meta:
        model = EmbededFooter
        fields = ['text', 'icon_url']
        labels = {
            'text': 'Текст footer',
            'icon_url': 'Ссылка на image'
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'icon_url': forms.TextInput(attrs={'class': 'form-control'})
        }


class EndpointEmbededForm(forms.ModelForm):

    class Meta:
        model = EndpointEmbeded
        fields = ['name', 'callback', 'title', 'description',
                  'url', 'color', 'thumbnail', 'author', 'fields', 'footer']
        labels = {
            'name': 'Название endpoint',
            'callback': 'Данные callback(url)',
            'title': 'Данные title',
            'description': 'Данные description',
            'url': 'Данные URL',
            'color': 'Данные color',
            'thumbnail': 'Данные thumbnail(url)',
            'author': 'Данные author',
            'fields': 'Выберите fields или добавьте новый',
            'footer': 'Выберите footer или добавьте новый'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'callback': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'fields': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'footer': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'filters', 'endpoints']
        labels = {
            'name': 'Введите название Ивента',
            'filters': 'Выберите filter из списка или добавьте новый',
            'endpoints': 'Выберите endpoint из списка или добавьте новый'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'filters': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'endpoints': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
