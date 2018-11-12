from rest_framework import status, exceptions, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from dialogs.serializers import ThreadSerializer, MessageSerializer
from dialogs import serializers as sr
from accounts.models import CustomUser
from dialogs import models

class AdminOnly(permissions.BasePermission):
    message = "You must be admin to perform this action"
    def has_permission(self, request, view):
        return request.user.is_admin()

class MemberOnly(permissions.BasePermission):
    message = "You must be member of thread to perform this action"
    def has_permission(self, request, view):
        thread_id = request.resolver_match.kwargs.get('thread_id')
        thread = models.Thread.objects.get(id=thread_id)
        return thread.is_member(request.user.id)


class ThreadList(APIView):
    def get(self, request):
        threads = models.Thread.objects.filter(participants__id=request.user.id)
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    @permission_classes([AdminOnly])
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


@api_view()
def get_thread_view(request, pk):
    thread = get_thread(pk)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([MemberOnly])
def add_participant(request, thread_id):
    thread = get_thread(pk=thread_id)
    #participant_id = request.data['id']
    serializer = sr.UserIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    participant = CustomUser.objects.get(pk=serializer.data['user_id'])
    if participant.is_admin():
        raise ValidationError(detail="Only one admin allowed for thread")
    thread.participants.add(participant)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([AdminOnly, MemberOnly])
def remove_participant(request, thread_id, user_id):
    thread = get_thread(pk=thread_id)
    if user_id == request.user.id:
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    participant = CustomUser.objects.get(pk=user_id)
    thread.participants.remove(participant)
    serializer = ThreadSerializer(thread)
    return Response(serializer.data)


class MessageView(APIView):
    permission_classes = [MemberOnly]

    def get(self, request, thread_id):
        thread = get_thread(thread_id)
        messages = models.Message.objects.filter(thread__id=thread_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, thread_id):
        thread = get_thread(thread_id)
        serializer = sr.MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            message = models.Message(text=serializer.data['text'], thread=thread, sender = request.user)
            message.save()
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
