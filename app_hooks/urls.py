from django.urls import path
from .views import EventViewSet
from django.views.generic import TemplateView

urlpatterns = [
    path('jira-callback/', EventViewSet.as_view(), name='jira-callback'),
    path('events/', TemplateView.as_view(template_name="events.html")),
]
