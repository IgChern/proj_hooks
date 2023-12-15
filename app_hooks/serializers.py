from rest_framework import serializers
from .models import Filter, Event


class FilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Filter
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    filters = FilterSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        depth = 1
