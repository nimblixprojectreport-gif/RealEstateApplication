from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .services import chatbot_reply


# =====================================
# CONVERSATION VIEWSET (User Messaging)
# =====================================

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    # Only buyer or owner can see conversations
    def get_queryset(self):
        return Conversation.objects.filter(
            Q(buyer=self.request.user) | Q(owner=self.request.user)
        )

    # Automatically set buyer as logged-in user
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    # ==========================
    # GET MESSAGES
    # ==========================
    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # ==========================
    # SEND MESSAGE
    # ==========================
    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        conversation = self.get_object()

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                conversation=conversation,
                sender=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ==========================
    # MARK AS READ
    # ==========================
    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        conversation = self.get_object()

        conversation.messages.filter(
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        return Response({"message": "Messages marked as read"})

    # ==========================
    # DELETE CONVERSATION
    # ==========================
    def destroy(self, request, *args, **kwargs):
        conversation = self.get_object()

        if request.user != conversation.buyer and request.user != conversation.owner:
            return Response(
                {"error": "You are not allowed to delete this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        conversation.delete()

        return Response(
            {"message": "Conversation deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# =====================================
# CHATBOT API
# =====================================

@api_view(["POST"])
@permission_classes([AllowAny])
def chatbot_api(request):

    if not request.data:
        return Response({"error": "No JSON data sent"}, status=400)

    message = request.data.get("message")

    if not message:
        return Response({"error": "Message field required"}, status=400)

    response = chatbot_reply(request.user, message)

    return Response(response)