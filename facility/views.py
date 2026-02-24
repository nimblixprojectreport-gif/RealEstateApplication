from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Facility


@require_GET
def list_facilities(request):
	facilities = Facility.objects.all().values(
		"id", "name", "description", "is_active", "created_at"
	)
	return JsonResponse(list(facilities), safe=False, status=200)
