from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response


from dialogs.serializers import ThreadSerializer, MessageSerializer
from dialogs import models


# class ThreadViewSet(viewsets.ModelViewSet):
#     queryset = models.Thread.objects.all()
#     serializer_class = serializers.ThreadSerializer


class ThreadList(APIView):
    def get(self, request):
        threads = models.Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThreadDetail(APIView):
    def get_thread(self, pk):
        try:
            return models.Thread.objects.get(pk=pk)
        except models.Thread.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        thread = self.get_thread(pk)
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request, pk):
        thread = self.get_thread(pk)
        serializer = ThreadSerializer(thread, data.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        thread = self.get_thread(pk)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = MessageSerializer
