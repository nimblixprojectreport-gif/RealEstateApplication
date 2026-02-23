import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
from properties.models import Property


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_conversations")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_conversations")
    created_at = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    message_type = models.CharField(max_length=20)
    content = models.TextField(blank=True)
    media_url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
