from django.urls import path

from .views import list_facilities

urlpatterns = [
    path("", list_facilities, name="list_facilities"),
]
