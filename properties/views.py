from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer
from decimal import Decimal

# -------------------------------
# CREATE PROPERTY
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_property(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# SEARCH / LIST PROPERTIES
# -------------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def search_properties(request):
    queryset = Property.objects.all().order_by("-created_at")

    # Optional filters
    city = request.GET.get("city")
    status_ = request.GET.get("status")
    listing_type = request.GET.get("listing_type")

    if city:
        queryset = queryset.filter(city__icontains=city)
    if status_:
        queryset = queryset.filter(status__iexact=status_)
    if listing_type:
        queryset = queryset.filter(listing_type__iexact=listing_type)

    serializer = PropertySerializer(queryset, many=True)
    return Response({"success": True, "count": len(serializer.data), "results": serializer.data})


# -------------------------------
# PROPERTY DETAIL + RECOMMENDATIONS
# -------------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def property_detail(request, id):
    try:
        property_obj = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        return Response({"message": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    property_data = PropertySerializer(property_obj).data

    # Recommend similar properties within ±20% price range
    min_price = property_obj.price * Decimal("0.8")
    max_price = property_obj.price * Decimal("1.2")

    recommended = Property.objects.filter(
        city=property_obj.city,
        property_type=property_obj.property_type,
        price__gte=min_price,
        price__lte=max_price
    ).exclude(pk=property_obj.pk)[:5]

    recommended_data = PropertySerializer(recommended, many=True).data

    return Response({
        "property": property_data,
        "recommended_properties": recommended_data
    })


# -------------------------------
# UPDATE PROPERTY
# -------------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_property(request, id):
    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    # Only owner can update
    if property_obj.owner != request.user:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    serializer = PropertySerializer(property_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# DELETE PROPERTY
# -------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_property(request, id):
    try:
        property_obj = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

    # Only owner can delete
    if property_obj.owner != request.user:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    property_obj.delete()
    return Response({"message": "Property deleted successfully"}, status=status.HTTP_200_OK)


# -------------------------------
# MY LISTINGS (logged-in user)
# -------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_listings(request):
    queryset = Property.objects.filter(owner=request.user).order_by("-created_at")
    serializer = PropertySerializer(queryset, many=True)
    return Response({"success": True, "count": len(serializer.data), "results": serializer.data})