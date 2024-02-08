from django import forms
from app_hooks.models import Filter, EmbededFooter, EmbededFields, EndpointDirect, EndpointEmbeded, Event
from django.contrib.auth.forms import AuthenticationForm

from django.forms import inlineformset_factory


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['name', 'data']
        labels = {
            'name': 'Введите название фильтра',
            'data': 'Введите данные фильтра',
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
            'name': 'Введите название эндпоинта',
            'callback': 'Введите данные callback(url)',
            'template': 'Введите данные template'
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
            'name': 'Введите название доп. поля',
            'value': 'Введите данные доп. поля',
            'inline': 'Выберите Inline'
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
            'text': 'Введите текст футера',
            'icon_url': 'Введите ссылку на изображение футера'
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
            'name': 'Введите название эндпоинта',
            'callback': 'Введите данные callback(url)',
            'title': 'Введите данные title',
            'description': 'Введите данные description',
            'url': 'Введите URL',
            'color': 'Введите цвет в формате цифр',
            'thumbnail': 'Введите данные thumbnail(url)',
            'author': 'Введите автора',
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
            'filters': 'Выберите фильтр из списка или добавьте новый',
            'endpoints': 'Выберите эндпоинт из списка или добавьте новый'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'filters': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'endpoints': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
