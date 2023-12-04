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
