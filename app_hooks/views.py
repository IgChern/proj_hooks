from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from .webhook import Service
# from .tasks import process_jira_callback_task
from .models import Event, Filter, EndpointDirect, EmbededFields, EmbededFooter, EndpointEmbeded
from django.views.generic import ListView
from app_users.forms import FilterForm, EndpointDirectForm, EmbededFieldsForm, EmbededFooterForm, EndpointEmbededForm, EventForm
from django.shortcuts import redirect
from django.contrib import messages

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


class MakeDirectEndpoint(ListView):
    model = Event
    template_name = 'app_hooks/makedirectevent.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['direct_form'] = EndpointDirectForm()
        return context

    def post(self, request, *args, **kwargs):
        formdirect = EndpointDirectForm(request.POST)

        if formdirect.is_valid() and formdirect.cleaned_data:
            new_fields = EndpointDirect(
                name=formdirect.cleaned_data['name'],
                callback=formdirect.cleaned_data['callback'],
                template=formdirect.cleaned_data['template']
            )
            new_fields.save()
            messages.success(request, 'Direct endpoint добавлен')

        return redirect('make_events')


class MakeEmbededEndpoint(ListView):
    model = Event
    template_name = 'app_hooks/makeembededevent.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['embeded_form'] = EndpointEmbededForm()
        return context

    def post(self, request, *args, **kwargs):
        formembededendpoint = EndpointEmbededForm(request.POST)

        if formembededendpoint.is_valid() and formembededendpoint.cleaned_data:
            new_fields = EndpointEmbeded(
                name=formembededendpoint.cleaned_data['name'],
                callback=formembededendpoint.cleaned_data['callback'],
                title=formembededendpoint.cleaned_data['title'],
                description=formembededendpoint.cleaned_data['description'],
                url=formembededendpoint.cleaned_data['url'],
                color=formembededendpoint.cleaned_data['color'],
                thumbnail=formembededendpoint.cleaned_data['thumbnail'],
                author=formembededendpoint.cleaned_data['author']
            )
            new_fields.save()
            new_fields.footer.set(formembededendpoint.cleaned_data['footer'])
            new_fields.fields.set(formembededendpoint.cleaned_data['fields'])
            new_fields.save()
            messages.success(request, 'Endpoint embeded добавлен')

        return redirect('make_eventsembed')


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
        formevent = EventForm(request.POST)

        if formevent.is_valid() and formevent.cleaned_data:
            new_fields = Event(
                name=formevent.cleaned_data['name']
            )
            new_fields.save()
            new_fields.filters.set(formevent.cleaned_data['filters'])
            new_fields.endpoints.set(
                formevent.cleaned_data['endpoints'])
            new_fields.save()
            messages.success(request, 'Event добавлен')

        return redirect('make_events')


class MakeEmbededFields(ListView):
    model = Event
    template_name = 'app_hooks/makefields.html'
    context_object_name = 'makeevent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter_form'] = FilterForm()
            context['embededfields_form'] = EmbededFieldsForm()
            context['footer_form'] = EmbededFooterForm()
        return context

    def post(self, request, *args, **kwargs):
        formfilter = FilterForm(request.POST)
        formembededfields = EmbededFieldsForm(request.POST)
        formembededfooter = EmbededFooterForm(request.POST)

        if formembededfields.is_valid():
            new_fields = EmbededFields(
                name=formembededfields.cleaned_data['name'],
                value=formembededfields.cleaned_data['value'],
                inline=formembededfields.cleaned_data['inline']
            )
            new_fields.save()
            messages.success(request, 'Field добавлен')

        elif formembededfooter.is_valid():
            new_fields = EmbededFooter(
                text=formembededfooter.cleaned_data['text'],
                icon_url=formembededfooter.cleaned_data['icon_url']
            )
            new_fields.save()
            messages.success(request, 'Footer добавлен')

        elif formfilter.is_valid() and formfilter.cleaned_data['data'] is not None:
            new_fields = Filter(
                name=formfilter.cleaned_data['name'],
                data=formfilter.cleaned_data['data']
            )
            new_fields.save()
            messages.success(request, 'Filter добавлен')

        return redirect('make_embedfields')
