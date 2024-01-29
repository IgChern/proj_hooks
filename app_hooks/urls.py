from django.urls import path
from .views import (EventViewSet, EventListView, MakeDirectEndpoint,
                    MakeEmbededEndpoint, MakeEvent, MakeFields, MakeFilter, MakeFooter,
                    EventDeleteView, EventUpdateView)
from django.contrib.auth.decorators import login_required

app_name = 'events'

urlpatterns = [
    path('jira-callback/', EventViewSet.as_view(), name='jira-callback'),
    path('events/', login_required(EventListView.as_view()), name='events'),
    path('make_eventdirect/',
         login_required(MakeDirectEndpoint.as_view()), name='make_eventdirect'),
    path('make_eventembed/', login_required(MakeEmbededEndpoint.as_view()),
         name='make_eventembed'),
    path('make_event/', login_required(MakeEvent.as_view()),
         name='make_event'),
    path('make_fields/', login_required(MakeFields.as_view()),
         name='make_fields'),
    path('make_filter/', login_required(MakeFilter.as_view()),
         name='make_filter'),
    path('make_footer/', login_required(MakeFooter.as_view()),
         name='make_footer'),
    path('events/<int:pk>/delete', login_required(EventDeleteView.as_view()),
         name='del_events'),
    path('events/<int:pk>/update', login_required(EventUpdateView.as_view()),
         name='upd_events'),

]
