import json
from django.http import JsonResponse
from .tasks import process_jira_callback_task


def jira_callback_view(request):
    data = json.loads(request.body)
    process_jira_callback_task.delay(data)
    return JsonResponse({'result': 'Task entered'})
