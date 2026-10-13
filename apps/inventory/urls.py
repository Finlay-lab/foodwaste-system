from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("categories/", views.category_list, name="category_list"),
    path("categories/new/", views.category_create, name="category_create"),
    path("categories/<uuid:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<uuid:pk>/delete/", views.category_delete, name="category_delete"),
]
