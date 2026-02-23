from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer



class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )



class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(
                id=pk,
                user=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True
        notification.save()

        return Response(
            {"message": "Notification marked as read"},
            status=status.HTTP_200_OK
        )
from django.http import HttpResponse

def notification_list(request):
    return HttpResponse("Notifications working!")
# Create your views here.
from django.http import JsonResponse
from .models import Notification


def notification_list(request):
    notifications = Notification.objects.all().values(
        "id", "title", "message", "is_read", "created_at"
    )

    return JsonResponse(list(notifications), safe=False)
