from django.urls import path
from .views import (
    create_property,
    search_properties,
    property_detail,
    update_property,
    delete_property,
    my_listings
)

urlpatterns = [
    path("create/", create_property),
    path("", search_properties),
    path("<uuid:id>/", property_detail),
    path("<uuid:id>/update/", update_property),
    path("<uuid:id>/delete/", delete_property),
    path("my/", my_listings),
]
