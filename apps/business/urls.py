from django.urls import path

from . import views

app_name = "business"

urlpatterns = [
    path("profile/", views.manage, name="manage"),
    path("", views.business_list, name="list"),
]
