import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
from properties.models import Property


class Enquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_inquiries")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_inquiries")

    message = models.TextField()
    status = models.CharField(max_length=20)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
