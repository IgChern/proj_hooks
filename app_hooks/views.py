from django.http import JsonResponse
from .tasks import process_jira_callback_task, new_task
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def jira_callback_view(request):
    try:
        data = request.POST
        return JsonResponse({'result': 'Task entered'})
    except Exception as e:
        logger.error(f"An error: {e}")
        return JsonResponse({'error': f'{e}'})


def my_view():
    new_task.apply_async()
    print('Success')
