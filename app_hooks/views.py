import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .webhook import Service


@require_POST
def jira_callback_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    service = Service()
    result = service.process_jira_callback(data)

    return JsonResponse(result)
