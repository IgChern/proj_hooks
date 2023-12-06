from rest_framework import serializers
from .models import Filter, Event


class FilterSerializer(serializers.ModelSerializer):
    '''
    Serializer for filters
    '''
    class Meta:
        model = Filter
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    '''
    Serializer for events
    '''
    filters = FilterSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1
