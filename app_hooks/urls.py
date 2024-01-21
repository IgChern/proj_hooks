from django.urls import path
from .views import EventViewSet, EventListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('jira-callback/', EventViewSet.as_view(), name='jira-callback'),
    path('events/', login_required(EventListView.as_view()), name='events'),
]
