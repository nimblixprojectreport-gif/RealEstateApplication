import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User


class AdminLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    action = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=100)
    entity_id = models.UUIDField()
    metadata = models.JSONField()

    created_at = models.DateTimeField(default=timezone.now)
