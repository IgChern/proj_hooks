from typing import Any
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from .webhook import Service
# from .tasks import process_jira_callback_task
from .models import Event, Filter, EndpointDirect, EmbededFields, EmbededFooter, EndpointEmbeded
from django.views.generic import ListView
from app_users.forms import FilterForm, EndpointDirectForm, EmbededFieldsForm, EmbededFooterForm, EndpointEmbededForm, EventForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    def get_queryset(self):
        return Event.objects.all().order_by('name')

    def get(self, request):
        eventsobj = Event.objects.all().order_by('name')
        page = request.GET.get('page', 1)
        paginator = Paginator(eventsobj, 5)
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'events': events})


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
            messages.success(request, 'Direct endpoint добавлен')
            return redirect('make_eventdirect')
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
            messages.success(request, 'Endpoint embeded добавлен')
            return redirect('make_eventembed')
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
            messages.success(request, 'Event добавлен')
            return redirect('make_event')
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
            messages.success(request, 'Filter добавлен')
            return redirect('make_filter')
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
            messages.success(request, 'Field добавлен')
            return redirect('make_fields')
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
            messages.success(request, 'Footer добавлен')
            return redirect('make_footer')

        else:
            form = EmbededFooterForm()
        return redirect(request, "makefooter.html", {"form": form})
