import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
from properties.models import Property


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
