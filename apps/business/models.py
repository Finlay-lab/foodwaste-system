import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class BusinessProfile(models.Model):
    """Matches class BusinessProfile and ERD entity BusinessProfile."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_profile",
        db_column="user_id",
    )
    business_name = models.CharField(max_length=155)
    business_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=32)
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "business_profiles"
        ordering = ["business_name"]

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse("business:manage")

    @classmethod
    def register_business(cls, owner, **fields):
        """Class operation from the class diagram: registerBusiness()."""
        return cls.objects.create(owner=owner, **fields)
