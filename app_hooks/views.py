from django.shortcuts import render
from .serializers import FilterSerializer, EventSerializer
from .models import Filters, Event
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
class FilterViewSet(viewsets.ModelViewSet):
    queryset = Filters.objects.all()
    serializer_class = FilterSerializer

    def return_post(self, request, *args, **kwargs):
        serializer = FilterSerializer(data=request.data)
        if serializer:
            instance = serializer.save()
            response_data = instance.make_dict()
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
