from django.conf import settings
from django.db import models

# Create your models here.

class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_member(self, user_id):
        return self.participants.filter(id=user_id).exists()


class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)