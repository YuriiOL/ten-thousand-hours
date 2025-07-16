from rest_framework import serializers

from core.models import (Timer, TimerType)


class TimerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimerType
        fields = ['id', 'name']
        read_only_fields = ['id']


class TimerSerializer(serializers.ModelSerializer):
    timer_type = TimerTypeSerializer(many=True, required=False)

    class Meta:
        model = Timer
        fields = ['id', 'title', 'current_time', 'last_session', 'timer_type']
        read_only_fields = ['id']

    def _get_or_create_timer_type(self, timer_type, timer):
        auth_user = self.context['request'].user
        for type in timer_type:
            type_obj, created = TimerType.objects.get_or_create(
                user=auth_user,
                **type
            )
            timer.timer_type.add(type_obj)

    def create(self, validated_data):
        timer_type = validated_data.pop('timer_type', [])
        timer = Timer.objects.create(**validated_data)

        self._get_or_create_timer_type(timer_type, timer)

        return timer

    def update(self, instance, validated_data):
        timer_type = validated_data.pop('timer_type', None)
        if timer_type is not None:
            instance.timer_type.clear()
            self._get_or_create_timer_type(timer_type, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TimerDetailSerializer(TimerSerializer):

    class Meta(TimerSerializer.Meta):
        fields = TimerSerializer.Meta.fields + ['description', 'image']


class TimerTypeDetailsSerializer(TimerTypeSerializer):

    class Meta(TimerTypeSerializer.Meta):
        fields = TimerTypeSerializer.Meta.fields


class TimerImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timer
        fields = ['image']

    def update(self, instance, validation_data):
        instance.image = validation_data.get('image', instance.image)
        instance.save()
        return instance
