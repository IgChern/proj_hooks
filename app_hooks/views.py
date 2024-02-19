from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from .webhook import Service
# from .tasks import process_jira_callback_task
from .models import (Event, Filter, EndpointDirect,
                     EmbededFields, EmbededFooter, EndpointEmbeded, MiddlewaresBase)
from django.views.generic import ListView
from app_users.forms import (FilterForm, EndpointDirectForm,
                             EmbededFieldsForm, EmbededFooterForm,
                             EndpointEmbededForm, EventForm, MiddlewareForm)
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView, CreateView


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


class MakeDirectEndpoint(CreateView):
    model = EndpointDirect
    form_class = EndpointDirectForm
    middleware_form_class = MiddlewareForm
    template_name = 'app_hooks/makedirectevent.html'
    success_url = reverse_lazy('events:make_event')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['direct_form'] = context['form']
            context['middleware_form'] = self.middleware_form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f'Direct endpoint {self.object.name} добавлен')

        middleware_type = self.request.POST.get('type')

        # возвращает кортеж (middleware, true/false)
        middleware, created = MiddlewaresBase.objects.get_or_create(
            type=middleware_type)

        if created:
            messages.success(
                self.request, f'Новый middleware {middleware.type} создан')

        if middleware not in self.object.middleware.all():
            self.object.middleware.add(middleware)
            messages.success(
                self.request, f'Middleware {middleware.type} добавлен')

        return response


class MakeEmbededEndpoint(CreateView):
    model = EndpointEmbeded
    form_class = EndpointEmbededForm
    middleware_form_class = MiddlewareForm
    template_name = 'app_hooks/makeembededevent.html'
    success_url = reverse_lazy('events:make_event')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['embeded_form'] = context['form']
            context['middleware_form'] = self.middleware_form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f'Embed endpoint {self.object.name} добавлен')

        middleware_type = self.request.POST.get('type')

        # возвращает кортеж (middleware, true/false)
        middleware, created = MiddlewaresBase.objects.get_or_create(
            type=middleware_type)

        if created:
            messages.success(
                self.request, f'Новый middleware {middleware.type} создан')

        if middleware not in self.object.middleware.all():
            self.object.middleware.add(middleware)
            messages.success(
                self.request, f'Middleware {middleware.type} добавлен')

        return response


class MakeEvent(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'app_hooks/makeevent.html'
    success_url = reverse_lazy('events:events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['event_form'] = context['form']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Event {self.object.name} добавлен')
        return response


class MakeFilter(CreateView):
    model = Filter
    form_class = FilterForm
    template_name = 'app_hooks/makefilter.html'
    success_url = reverse_lazy('events:make_event')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter_form'] = context['form']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Filter {self.object.name} добавлен')
        return response


class MakeFields(CreateView):
    model = EmbededFields
    form_class = EmbededFieldsForm
    template_name = 'app_hooks/makefields.html'
    success_url = reverse_lazy('events:make_eventembed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['embededfields_form'] = context['form']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Field {self.object.name} добавлен')
        return response


class MakeFooter(CreateView):
    model = EmbededFooter
    form_class = EmbededFooterForm
    template_name = 'app_hooks/makefooter.html'
    success_url = reverse_lazy('events:make_eventembed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['footer_form'] = context['form']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Footer {self.object.text} добавлен')
        return response


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['event_form'] = context['form']
            context['event_id'] = self.object.id
        return context

    def post(self, request, pk):
        post = get_object_or_404(Event, pk=pk)
        form = EventForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if 'notpub_button' in request.POST:
                post.draft = False
            elif 'pub_button' in request.POST:
                post.draft = True
            post.save()
            form.save_m2m()
            messages.success(request, f"Event {post.name} обновлен")
            return redirect('events:upd_events', pk=post.pk)
        else:
            form = EventForm(instance=post)
        return render(request, "app_hooks/update.html", {"form": form, "event_id": pk})

    def get_success_url(self):
        return reverse_lazy('events:upd_events', kwargs={'pk': self.object.pk})
