from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from .webhook import Service
from .tasks import process_jira_callback_task

import logging

logger = logging.getLogger('app_hooks')


class EventViewSet(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = Service()

    def post(self, request):
        data = request.data
        process_jira_callback_task.apply_async(args=[data])
        return Response("New task", status=HTTP_200_OK)
