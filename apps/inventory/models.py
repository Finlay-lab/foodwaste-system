import uuid

from django.db import models
from django.urls import reverse


class FoodCategory(models.Model):
    """Matches class FoodCategory and ERD entity FoodCategory."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "food_categories"
        ordering = ["category_name"]
        verbose_name = "food category"
        verbose_name_plural = "food categories"

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("inventory:category_list")
