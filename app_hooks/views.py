from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FilterSerializer, EventSerializer
from .models import Filter, Event
from .tasks import process_jira_callback_task


class EventViewSet(APIView):
    def get(self, request, *args, **kwargs):
        filters = Filter.objects.all()
        events = Event.objects.all()

        filter_serializer = FilterSerializer(filters, many=True)
        event_serializer = EventSerializer(events, many=True)

        data = {
            'filters': filter_serializer.data,
            'events': event_serializer.data
        }

        return Response(data)

    def post(self, request, *args, **kwargs):
        data = request.data.get('data', {})

        event_obj = Event.objects.create(
            name=data.get('name', ''),
            endpoint=data.get('endpoint', ''),
            template=data.get('template', ''),
            callback=data.get('callback', '')
        )

        for filter_data in data.get('filters', []):
            filter_obj, created = Filter.objects.get_or_create(**filter_data)
            event_obj.filters.add(filter_obj)

        task_result = process_jira_callback_task.apply_async(
            data)

        filter_serializer = FilterSerializer(
            event_obj.filters.all(), many=True)
        event_serializer = EventSerializer(event_obj)

        response_data = {
            'filters': filter_serializer.data,
            'event': event_serializer.data,
            'task_id': task_result.id
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
