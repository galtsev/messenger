from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response


from dialogs.serializers import ThreadSerializer, MessageSerializer
from accounts.models import CustomUser
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
        if not request.user.is_admin():
            raise exceptions.PermissionDenied(detail="Only admin can create threads")
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            thread = models.Thread.objects.get(pk=serializer.data['id'])
            thread.participants.add(request.user)
            serializer = ThreadSerializer(thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_thread(pk):
    try:
        return models.Thread.objects.get(pk=pk)
    except models.Thread.DoesNotExist:
        raise Http404


class ThreadDetail(APIView):

    def get(self, request, pk):
        thread = get_thread(pk)
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request, pk):
        thread = get_thread(pk)
        serializer = ThreadSerializer(thread, data.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        thread = get_thread(pk)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def add_participant(request, thread_id):
    thread = get_thread(pk=thread_id)
    if not thread.participants.filter(pk=request.user.id).exists():
        raise exceptions.PermissionDenied(detail="Only participants can add new participants to the thread")
    participant_id = request.data['id']
    participant = CustomUser.objects.get(pk=participant_id)
    thread.participants.add(participant)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)

@api_view(['POST'])
def remove_participant(request, thread_id):
    thread = get_thread(pk=thread_id)
    if not request.user.is_admin():
        raise exceptions.PermissionDenied(detail="Only admin can remove participants from the thread")
    if not thread.is_member(request.user.id):
        raise exceptions.PermissionDenied(detail="Only participants can add new participants to the thread")
    participant_id = request.data['id']
    participant = CustomUser.objects.get(pk=participant_id)
    thread.participants.remove(participant)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)


class MessageView(APIView):
    def get(self, request, thread_id):
        thread = get_thread(thread_id)
        if not thread.is_member(request.user.id):
            raise exceptions.PermissionDenied(detail="Only member can view thread messages")
        messages = models.Message.objects.filter(thread__id=thread_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, thread_id):
        thread = get_thread(thread_id)
        if not thread.is_member(request.user.id):
            raise exceptions.PermissionDenied(detail="Only member can add thread messages")
        # TODO: serializer for Message create
        text = request.data["text"].strip()
        if text:
            message = models.Message(text=text, thread=thread, sender = request.user)
            message.save()
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        return Response(dict(text="Empty message body"), status=status.HTTP_400_BAD_REQUEST)