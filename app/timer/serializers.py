from rest_framework import serializers

from core.models import Timer


class TimerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timer
        fields = ['id', 'title', 'current_time', 'last_session']
        read_only_fields = ['id']


class TimerDetailSerializer(TimerSerializer):
    """
    Serializer for the timer detail view
    """
    class Meta(TimerSerializer.Meta):
        fields = TimerSerializer.Meta.fields + ['description']
