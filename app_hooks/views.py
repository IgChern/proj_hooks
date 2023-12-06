from .serializers import FilterSerializer, EventSerializer
from .models import Filter, Event
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
class FilterViewSet(viewsets.ModelViewSet):
    '''
    - serializer_class to transform Post model to JSON
    - function get_queryset for setting filter
    '''
    serializer_class = FilterSerializer

    def get_queryset(self):
        filter = Filter.objects.all()
        return filter


class EventViewSet(viewsets.ModelViewSet):
    '''
    - serializer_class to transform Post model to JSON
    - function get_queryset for setting events
    - function create to set filters in events
    '''
    serializer_class = EventSerializer

    def get_queryset(self):
        event = Event.objects.all()
        return event

    def create(self, request, *args, **kwargs):
        data = request.data

        event_obj = Event.objects.create(
            name=data['name'],
            endpoint=data['endpoint'],
            template=data['template'],
            callback=data['callback'])

        event_obj.save()

        for filter_data in data.get('filters', []):
            filter_obj, created = Filter.objects.get_or_create(**filter_data)
            event_obj.filters.add(filter_obj)

        serializer = EventSerializer(event_obj)
        return Response(serializer.data)
