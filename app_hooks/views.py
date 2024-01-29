from typing import Any
from django.core.paginator import Paginator
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from .webhook import Service
# from .tasks import process_jira_callback_task
from .models import Event, Filter, EndpointDirect, EmbededFields, EmbededFooter, EndpointEmbeded
from django.views.generic import ListView
from app_users.forms import FilterForm, EndpointDirectForm, EmbededFieldsForm, EmbededFooterForm, EndpointEmbededForm, EventForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
import logging

logger = logging.getLogger('app_hooks')


class EventViewSet(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = Service()

    def post(self, request):
        data = request.data
        result = self.service.process_jira_callback(data)
        return Response(result, status=HTTP_200_OK)
        # process_jira_callback_task.apply_async(args=[data])
        # return Response("New task", status=HTTP_200_OK)


class EventListView(ListView):
    model = Event
    template_name = 'app_hooks/events.html'
    context_object_name = 'events'
    paginate_by = 5

    def get_queryset(self):
        return Event.objects.all().order_by('name')


class MakeDirectEndpoint(ListView):
    model = EndpointDirect
    template_name = 'app_hooks/makedirectevent.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['direct_form'] = EndpointDirectForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EndpointDirectForm(request.POST)

        if form.is_valid() and form.cleaned_data:
            new_fields = EndpointDirect(
                name=form.cleaned_data['name'],
                callback=form.cleaned_data['callback'],
                template=form.cleaned_data['template']
            )
            new_fields.save()
            messages.success(
                request, f'Direct endpoint {new_fields.name} добавлен')
            return redirect('events:make_event')
        else:
            form = EndpointDirectForm()
        return redirect(request, "make_directevent.html", {"form": form})


class MakeEmbededEndpoint(ListView):
    model = EndpointEmbeded
    template_name = 'app_hooks/makeembededevent.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['embeded_form'] = EndpointEmbededForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EndpointEmbededForm(request.POST)

        if form.is_valid() and form.cleaned_data:
            new_fields = EndpointEmbeded(
                name=form.cleaned_data['name'],
                callback=form.cleaned_data['callback'],
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                url=form.cleaned_data['url'],
                color=form.cleaned_data['color'],
                thumbnail=form.cleaned_data['thumbnail'],
                author=form.cleaned_data['author']
            )
            new_fields.save()
            new_fields.footer.set(form.cleaned_data['footer'])
            new_fields.fields.set(form.cleaned_data['fields'])
            new_fields.save()
            messages.success(
                request, f'Endpoint embeded {new_fields.name} добавлен')
            return redirect('events:make_event')
        else:
            form = EndpointEmbededForm()
        return redirect(request, "makeembededevent.html", {"form": form})


class MakeEvent(ListView):
    model = Event
    template_name = 'app_hooks/makeevent.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['event_form'] = EventForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)

        if form.is_valid() and form.cleaned_data:
            new_fields = Event(
                name=form.cleaned_data['name']
            )
            new_fields.save()
            new_fields.filters.set(form.cleaned_data['filters'])
            new_fields.endpoints.set(
                form.cleaned_data['endpoints'])
            new_fields.save()
            messages.success(request, f"Event {new_fields.name} добавлен")
            return redirect('events:events')
        else:
            form = EventForm()
        return redirect(request, "makeevent.html", {"form": form})


class MakeFilter(ListView):
    model = Filter
    template_name = 'app_hooks/makefilter.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter_form'] = FilterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = FilterForm(request.POST)

        if form.is_valid():
            new_fields = Filter(
                name=form.cleaned_data['name'],
                data=form.cleaned_data['data']
            )
            new_fields.save()
            messages.success(request, f'Filter {new_fields.name} добавлен')
            return redirect('events:make_event')
        else:
            form = FilterForm()

        return redirect(request, "makefilter.html", {"form": form})


class MakeFields(ListView):
    model = EmbededFields
    template_name = 'app_hooks/makefields.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['embededfields_form'] = EmbededFieldsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EmbededFieldsForm(request.POST)

        if form.is_valid():
            new_fields = EmbededFields(
                name=form.cleaned_data['name'],
                value=form.cleaned_data['value'],
                inline=form.cleaned_data['inline']
            )
            new_fields.save()
            messages.success(request, f'Field {new_fields.name} добавлен')
            return redirect('events:make_eventembed')
        else:
            form = EmbededFieldsForm()

        return redirect(request, "makefields.html", {"form": form})


class MakeFooter(ListView):
    model = EmbededFooter
    template_name = 'app_hooks/makefooter.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['footer_form'] = EmbededFooterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EmbededFooterForm(request.POST)

        if form.is_valid():
            new_fields = EmbededFooter(
                text=form.cleaned_data['text'],
                icon_url=form.cleaned_data['icon_url']
            )
            new_fields.save()
            messages.success(request, f'Footer {new_fields.text} добавлен')
            return redirect('events:make_eventembed')

        else:
            form = EmbededFooterForm()
        return redirect(request, "makefooter.html", {"form": form})


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('events:events')

    def get_success_url(self):
        messages.success(self.request, f'Event {self.object.name} удален')
        return super().get_success_url()


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'app_hooks/update.html'
    success_url = reverse_lazy('events:upd_events')

    def get_success_url(self):
        messages.success(self.request, f'Event изменен')
        return reverse_lazy('events:upd_events', kwargs={'pk': self.object.pk})
