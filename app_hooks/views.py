from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from .models import Event
from .serializers import EventSerializer
from .webhook import Service
from .tasks import process_jira_callback_task

import logging

logger = logging.getLogger(__name__)


class EventViewSet(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = Service()

    def get(self):
        events = Event.objects.all()
        serialized_events = EventSerializer(events, many=True).data
        return Response(serialized_events, status=HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            process_jira_callback_task.delay(data)
            return Response("New task", status=HTTP_200_OK)
        except Exception as e:
            logger.error(
                f"An error occurred while processing the Jira callback task: {e}")
            return Response("Internal Server Error", status=500)
