from django.db import models


class Facility(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "facility"

	def __str__(self):
		return self.name
