from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("manager/", views.restaurant_manager, name="restaurant_manager"),
    path("staff/", views.inventory_staff, name="inventory_staff"),
    path("admin/", views.system_administrator, name="system_administrator"),
]
