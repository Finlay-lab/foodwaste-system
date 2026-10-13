from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.accounts.decorators import restaurant_manager_required, system_administrator_required

from .forms import BusinessProfileForm
from .models import BusinessProfile


@restaurant_manager_required
@require_http_methods(["GET", "POST"])
def manage(request):
    try:
        profile = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        profile = None
    form = BusinessProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        if profile is None:
            BusinessProfile.register_business(request.user, **form.cleaned_data)
            messages.success(request, "Business profile saved.")
        else:
            form.save()
            messages.success(request, "Business profile updated.")
        return redirect("business:manage")
    return render(
        request,
        "business/manage.html",
        {
            "form": form,
            "profile": profile,
            "title": "Business profile" if profile else "Register business",
        },
    )


@system_administrator_required
def business_list(request):
    profiles = BusinessProfile.objects.select_related("owner")
    return render(
        request,
        "business/list.html",
        {"profiles": profiles, "title": "Businesses"},
    )
