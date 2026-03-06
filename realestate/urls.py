from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def home(request):
    return HttpResponse("Real Estate API Running")


urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),

    path('notification/', include('notifications.urls')),

    path('api/enquiries/', include('enquiries.urls')),

    path('api/', include('properties.urls')),
    path("api/chat/", include("chat.urls")),


    path("api/", include("properties.urls")),


    path('api/', include('accounts.urls')),


    # Payments
    path("api/v1/payments/", include("payments.urls")),

    # Subscriptions
    path("subscription/", include("subscriptions.urls")),

    # Notifications
    path("notification/", include("notifications.urls")),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]


