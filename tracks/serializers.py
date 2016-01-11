from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    time = serializers.DurationField()
    distance = serializers.FloatField()

    def create(self, validated_data):
        return Track.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
