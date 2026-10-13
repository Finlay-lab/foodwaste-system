from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.accounts.decorators import system_administrator_required

from .forms import FoodCategoryForm
from .models import FoodCategory


@system_administrator_required
def category_list(request):
    categories = FoodCategory.objects.all()
    return render(
        request,
        "inventory/category_list.html",
        {"categories": categories, "title": "Food categories"},
    )


@system_administrator_required
@require_http_methods(["GET", "POST"])
def category_create(request):
    form = FoodCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category saved.")
        return redirect("inventory:category_list")
    return render(
        request,
        "inventory/category_form.html",
        {"form": form, "title": "Add category"},
    )


@system_administrator_required
@require_http_methods(["GET", "POST"])
def category_update(request, pk):
    category = get_object_or_404(FoodCategory, pk=pk)
    form = FoodCategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated.")
        return redirect("inventory:category_list")
    return render(
        request,
        "inventory/category_form.html",
        {"form": form, "title": "Edit category", "category": category},
    )


@system_administrator_required
@require_http_methods(["GET", "POST"])
def category_delete(request, pk):
    category = get_object_or_404(FoodCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted.")
        return redirect("inventory:category_list")
    return render(
        request,
        "inventory/category_confirm_delete.html",
        {"category": category, "title": "Delete category"},
    )
