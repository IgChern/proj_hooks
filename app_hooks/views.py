from django.http import JsonResponse
from .tasks import process_jira_callback_task
import logging

logger = logging.getLogger(__name__)


def jira_callback_view(request):
    try:
        data = request.POST
        process_jira_callback_task.delay(data)
        return JsonResponse({'result': 'Task entered'})
    except Exception as e:
        logger.error(f"An error: {e}")
        return None
