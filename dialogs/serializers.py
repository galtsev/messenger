from rest_framework import serializers

from dialogs import models

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ("id", "participants", "created", "updated")

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ("id", "text", "sender", "thread", "created")