from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


#def home(request):
#   return HttpResponse("Real Estate API Running")


urlpatterns = [

    path('admin/', admin.site.urls),
    ##JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ##Forgot and Reset password
    path("api/accounts/", include("accounts.urls")),
    path('api/enquiries/', include('enquiries.urls')),
    path('api/properties/', include('properties.urls')),
    path("api/chat/", include("chat.urls")),
    path("api/", include("properties.urls")),
    
    ##Payments
    #path("admin/", admin.site.urls),
    path("properties_owner/", include("properties_owner.urls")),
    path("api/properties/", include("properties.urls")),
    path("api/enquiries/", include("enquiries.urls")),
    path("facility/", include("facility.urls")),
    path("api/", include("properties_owner.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("subscription/", include("subscriptions.urls")),
    ##Reviews API
    path("api/", include("reviews.urls")),
    ##Notifications
    path("api/notification/", include("notifications.urls")),
    ##Chats
    path("api/chat/", include("chat.urls")),
]

