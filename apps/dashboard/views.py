from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.decorators import role_required
from apps.accounts.models import User
from apps.business.models import BusinessProfile
from apps.inventory.models import FoodCategory


@login_required
def home(request):
    return redirect(request.user.get_dashboard_url())


@role_required(User.Role.RESTAURANT_MANAGER)
def restaurant_manager(request):
    return render(
        request,
        "dashboard/restaurant_manager.html",
        {"page_title": "Restaurant Manager Dashboard"},
    )


@role_required(User.Role.INVENTORY_STAFF)
def inventory_staff(request):
    return render(
        request,
        "dashboard/inventory_staff.html",
        {"page_title": "Inventory Staff Dashboard"},
    )


@role_required(User.Role.SYSTEM_ADMINISTRATOR)
def system_administrator(request):
    return render(
        request,
        "dashboard/system_administrator.html",
        {
            "page_title": "System Administrator Dashboard",
            "total_users": User.objects.count(),
            "total_businesses": BusinessProfile.objects.count(),
            "total_categories": FoodCategory.objects.count(),
        },
    )
