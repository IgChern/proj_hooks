from .views import jira_callback_view
from django.urls import path


urlpatterns = [
    path('jira-callback/', jira_callback_view, name='jira_callback'),
]
