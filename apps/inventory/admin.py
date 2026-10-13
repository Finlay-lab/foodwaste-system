from django.contrib import admin

from .models import FoodCategory


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "description")
    search_fields = ("category_name", "description")
    readonly_fields = ("id",)
