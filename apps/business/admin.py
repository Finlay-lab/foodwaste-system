from django.contrib import admin

from .models import BusinessProfile


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "business_type",
        "location",
        "contact_number",
        "registration_date",
        "owner",
    )
    search_fields = ("business_name", "location", "owner__email")
    readonly_fields = ("id", "registration_date")
