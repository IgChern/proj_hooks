from .serializers import FilterSerializer, EventSerializer
from .models import Filters, Event
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
class FilterViewSet(viewsets.ModelViewSet):
    serializer_class = FilterSerializer

    def get_queryset(self):
        filter = Filters.objects.all()
        return filter


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        event = Event.objects.all()
        return event

    def create(self, request, *args, **kwargs):
        data = request.data

        newevent = Event.objects.create(
            name=data['name'],
            endpoint=data['endpoint'],
            template=data['template'],
            callback=data['callback'])
        newevent.save()

        for filter in data['filters']:
            filter_obj = Filters.objects.get(filter_name=filter['filter_name'])
            newevent.filters.add(filter_obj)

        serializer = EventSerializer(newevent)

        return Response(serializer.data)
