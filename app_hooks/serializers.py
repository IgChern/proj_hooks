from rest_framework import serializers
from .models import Filters, Event


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filters
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    filters = FilterSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
