from rest_framework import viewsets

from dialogs import models, serializers


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = models.Thread.objects.all()
    serializer_class = serializers.ThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
