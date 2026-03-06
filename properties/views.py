import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Property


def _serialize_property(property_obj):
    return {
        "id": str(property_obj.id),
        "owner_id": str(property_obj.owner_id),
        "title": property_obj.title,
        "description": property_obj.description,
        "price": str(property_obj.price),
        "listing_type": property_obj.listing_type,
        "property_type": property_obj.property_type,
        "status": property_obj.status,
        "bedrooms": property_obj.bedrooms,
        "bathrooms": property_obj.bathrooms,
        "area_sqft": (
            str(property_obj.area_sqft) if property_obj.area_sqft is not None else None
        ),
        "city": property_obj.city,
        "state": property_obj.state,
        "country": property_obj.country,
        "pincode": property_obj.pincode,
        "latitude": (
            str(property_obj.latitude) if property_obj.latitude is not None else None
        ),
        "longitude": (
            str(property_obj.longitude) if property_obj.longitude is not None else None
        ),
        "is_featured": property_obj.is_featured,
        "created_at": property_obj.created_at.isoformat(),
        "updated_at": property_obj.updated_at.isoformat(),
    }


def _read_payload(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}

    if not payload:
        payload = request.POST.dict()

    return payload


@require_http_methods(["POST"])
def create_property(request):
    """Create a property via POST and return JSON confirmation."""
    payload = _read_payload(request)

    required_fields = [
        "title",
        "price",
        "listing_type",
        "property_type",
        "status",
    ]
    missing_fields = [field for field in required_fields if not payload.get(field)]
    if missing_fields:
        return JsonResponse(
            {
                "success": False,
                "message": "Missing required fields.",
                "missing_fields": missing_fields,
            },
            status=400,
        )

    user = (
        request.user
        if getattr(request, "user", None) and request.user.is_authenticated
        else None
    )
    if user is None:
        owner_id = payload.get("owner_id")
        if not owner_id:
            return JsonResponse(
                {
                    "success": False,
                    "message": "owner_id is required when request is unauthenticated.",
                },
                status=400,
            )

        User = get_user_model()
        try:
            user = User.objects.get(pk=owner_id)
        except User.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid owner_id.",
                },
                status=404,
            )

    property_obj = Property.objects.create(
        owner=user,
        title=payload["title"],
        description=payload.get("description", ""),
        price=payload["price"],
        listing_type=payload["listing_type"],
        property_type=payload["property_type"],
        status=payload["status"],
        bedrooms=payload.get("bedrooms"),
        bathrooms=payload.get("bathrooms"),
        area_sqft=payload.get("area_sqft"),
        city=payload.get("city", ""),
        state=payload.get("state", ""),
        country=payload.get("country", ""),
        pincode=payload.get("pincode", ""),
        latitude=payload.get("latitude"),
        longitude=payload.get("longitude"),
        is_featured=bool(payload.get("is_featured", False)),
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Property created successfully.",
            "property_id": str(property_obj.id),
        },
        status=201,
    )


@require_http_methods(["GET"])
def search_properties(request):
    queryset = Property.objects.all().order_by("-created_at")

    city = request.GET.get("city")
    status = request.GET.get("status")
    listing_type = request.GET.get("listing_type")

    if city:
        queryset = queryset.filter(city__icontains=city)
    if status:
        queryset = queryset.filter(status__iexact=status)
    if listing_type:
        queryset = queryset.filter(listing_type__iexact=listing_type)

    data = [_serialize_property(item) for item in queryset]
    return JsonResponse(
        {"success": True, "count": len(data), "results": data}, status=200
    )


@require_http_methods(["GET"])
def property_detail(request, id):
    try:
        property_obj = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Property not found."}, status=404
        )

    return JsonResponse(
        {"success": True, "property": _serialize_property(property_obj)}, status=200
    )


@require_http_methods(["PUT", "PATCH", "POST"])
def update_property(request, id):
    try:
        property_obj = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Property not found."}, status=404
        )

    payload = _read_payload(request)
    updatable_fields = [
        "title",
        "description",
        "price",
        "listing_type",
        "property_type",
        "status",
        "bedrooms",
        "bathrooms",
        "area_sqft",
        "city",
        "state",
        "country",
        "pincode",
        "latitude",
        "longitude",
        "is_featured",
    ]

    for field in updatable_fields:
        if field in payload:
            setattr(property_obj, field, payload[field])

    property_obj.save()
    return JsonResponse(
        {
            "success": True,
            "message": "Property updated successfully.",
            "property": _serialize_property(property_obj),
        },
        status=200,
    )


@require_http_methods(["DELETE", "POST"])
def delete_property(request, id):
    try:
        property_obj = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Property not found."}, status=404
        )

    property_obj.delete()
    return JsonResponse(
        {"success": True, "message": "Property deleted successfully."}, status=200
    )


@require_http_methods(["GET"])
def my_listings(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "Authentication required."}, status=401
        )

    queryset = Property.objects.filter(owner=request.user).order_by("-created_at")
    data = [_serialize_property(item) for item in queryset]
    return JsonResponse(
        {"success": True, "count": len(data), "results": data}, status=200
    )
