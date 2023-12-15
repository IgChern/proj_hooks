from django.urls import path
from .views import EventViewSet

urlpatterns = [
    path('jira-callback/', EventViewSet.as_view(), name='jira-callback'),
]
