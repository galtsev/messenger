from rest_framework import serializers

from dialogs import models

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ["id", "participants", "created", "updated"]
        read_only_fields = ["participants"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["id", "text", "sender", "thread", "created"]


class UserIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
