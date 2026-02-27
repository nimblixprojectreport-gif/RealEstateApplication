from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),
    path("api/", include("properties.urls")),
    path("api/enquiries/", include("enquiries.urls")),
    path("facility", include("facility.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("subscription/", include("subscriptions.urls")),
    path("notification/", include("notifications.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
