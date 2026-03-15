
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, chatbot_api

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = router.urls + [
    path("chatbot/", chatbot_api, name="chatbot"),
]


"""DefaultRouter() automatically creates URLs.

register() connects:

conversations → ConversationViewSet

router.urls generates all CRUD URLs automatically.

This single line:

router.register(r'conversations', ConversationViewSet, basename='conversation')

Creates:

GET     /conversations/
POST    /conversations/
GET     /conversations/{id}/
PUT     /conversations/{id}/
PATCH   /conversations/{id}/
DELETE  /conversations/{id}/
GET     /conversations/{id}/messages/
POST    /conversations/{id}/send_message/
PATCH   /conversations/{id}/mark_read/

You don’t manually write them. Router does it."""


